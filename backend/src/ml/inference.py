from transformers import MBartForConditionalGeneration, MBart50TokenizerFast
import torch
from typing import Optional
import logging
from utils import setup_logging

class MultilingualChatbot:
    def __init__(
        self,
        model_path: str = "../../models/pretrained/finetuned_mbart",
        device: Optional[str] = None
    ):
        # Setup logging
        setup_logging()
        self.logger = logging.getLogger(__name__)
        
        # Set device
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        self.logger.info(f"Using device: {self.device}")
        
        # Load model and tokenizer
        self.model = MBartForConditionalGeneration.from_pretrained(model_path).to(self.device)
        self.tokenizer = MBart50TokenizerFast.from_pretrained(model_path)
        
        # Language mapping
        self.language_codes = {
            'hi': 'hi_IN',  # Hindi
            'te': 'te_IN',  # Telugu
            # Add more languages as needed
        }

    def generate_response(
        self,
        input_text: str,
        language: str,
        max_length: int = 100,
        num_beams: int = 5,
        temperature: float = 0.7
    ) -> str:
        """Generate a response for the given input text in the specified language."""
        try:
            # Set the language token
            lang_code = self.language_codes.get(language)
            if not lang_code:
                raise ValueError(f"Unsupported language: {language}")

            # Tokenize input
            inputs = self.tokenizer(
                input_text,
                return_tensors="pt",
                padding=True,
                truncation=True,
                max_length=512
            ).to(self.device)

            # Generate response
            outputs = self.model.generate(
                **inputs,
                max_length=max_length,
                num_beams=num_beams,
                temperature=temperature,
                forced_bos_token_id=self.tokenizer.lang_code_to_id[lang_code],
                no_repeat_ngram_size=2,
                early_stopping=True
            )

            # Decode response
            response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            return response

        except Exception as e:
            self.logger.error(f"Error generating response: {str(e)}")
            return f"Error: {str(e)}"

    def get_supported_languages(self) -> list:
        """Return list of supported languages."""
        return list(self.language_codes.keys())

if __name__ == "__main__":
    # Example usage
    chatbot = MultilingualChatbot()
    
    # Test Hindi
    hindi_response = chatbot.generate_response(
        "नमस्ते, कैसे हो आप?",
        language="hi"
    )
    print(f"Hindi response: {hindi_response}")
    
    # Test Telugu
    telugu_response = chatbot.generate_response(
        "నమస్కారం, ఎలా ఉన్నారు?",
        language="te"
    )
    print(f"Telugu response: {telugu_response}") 