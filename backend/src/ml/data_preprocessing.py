import os
import json
from typing import List, Dict, Tuple
from transformers import MBart50TokenizerFast
from datasets import Dataset
import pandas as pd

class DialoguePreprocessor:
    def __init__(self, model_name: str = "facebook/mbart-large-50-many-to-many-mmt"):
        self.tokenizer = MBart50TokenizerFast.from_pretrained(model_name)
        self.supported_languages = {
            'hi': 'hi_IN',  # Hindi
            'te': 'te_IN',  # Telugu
            # Add more languages as needed
        }
    
    def load_raw_data(self, data_path: str) -> List[Dict]:
        """Load raw dialogue data from JSON files."""
        dialogues = []
        for lang in self.supported_languages:
            file_path = os.path.join(data_path, f"dialogues_{lang}.json")
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    lang_dialogues = json.load(f)
                    for dialogue in lang_dialogues:
                        dialogue['language'] = lang
                        dialogues.append(dialogue)
        return dialogues

    def preprocess_dialogue(self, dialogue: Dict) -> Tuple[str, str]:
        """Preprocess a single dialogue pair."""
        input_text = dialogue['input']
        response = dialogue['response']
        lang = dialogue['language']
        
        # Add language tokens
        lang_token = self.supported_languages[lang]
        input_text = f"{input_text}"
        response = f"{response}"
        
        return input_text, response

    def create_dataset(self, dialogues: List[Dict]) -> Dataset:
        """Create a HuggingFace dataset from dialogues."""
        processed_data = []
        
        for dialogue in dialogues:
            input_text, response = self.preprocess_dialogue(dialogue)
            
            # Tokenize inputs and responses
            inputs = self.tokenizer(
                input_text,
                padding='max_length',
                truncation=True,
                max_length=128,
                return_tensors='pt'
            )
            
            with self.tokenizer.as_target_tokenizer():
                labels = self.tokenizer(
                    response,
                    padding='max_length',
                    truncation=True,
                    max_length=128,
                    return_tensors='pt'
                )
            
            processed_data.append({
                'input_ids': inputs['input_ids'].squeeze(),
                'attention_mask': inputs['attention_mask'].squeeze(),
                'labels': labels['input_ids'].squeeze(),
                'language': dialogue['language']
            })
        
        return Dataset.from_pandas(pd.DataFrame(processed_data))

    def process_and_save(self, raw_data_path: str, output_path: str):
        """Process all dialogues and save the dataset."""
        dialogues = self.load_raw_data(raw_data_path)
        dataset = self.create_dataset(dialogues)
        dataset.save_to_disk(output_path)

if __name__ == "__main__":
    processor = DialoguePreprocessor()
    processor.process_and_save(
        raw_data_path="../../data/raw",
        output_path="../../data/processed"
    ) 