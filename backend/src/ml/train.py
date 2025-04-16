import os
from transformers import (
    MBartForConditionalGeneration,
    MBart50TokenizerFast,
    Seq2SeqTrainingArguments,
    Seq2SeqTrainer,
    DataCollatorForSeq2Seq
)
from datasets import load_from_disk
import torch
from utils import setup_logging
import logging

class MultilingualTrainer:
    def __init__(
        self,
        model_name: str = "facebook/mbart-large-50-many-to-many-mmt",
        output_dir: str = "../../models/pretrained/finetuned_mbart"
    ):
        self.model = MBartForConditionalGeneration.from_pretrained(model_name)
        self.tokenizer = MBart50TokenizerFast.from_pretrained(model_name)
        self.output_dir = output_dir
        
        # Setup logging
        setup_logging()
        self.logger = logging.getLogger(__name__)

    def load_dataset(self, data_path: str):
        """Load preprocessed dataset."""
        return load_from_disk(data_path)

    def train(
        self,
        train_dataset,
        eval_dataset,
        batch_size: int = 8,
        num_epochs: int = 3,
        learning_rate: float = 2e-5,
    ):
        """Fine-tune the model on the dialogue dataset."""
        training_args = Seq2SeqTrainingArguments(
            output_dir=self.output_dir,
            num_train_epochs=num_epochs,
            per_device_train_batch_size=batch_size,
            per_device_eval_batch_size=batch_size,
            warmup_steps=500,
            weight_decay=0.01,
            logging_dir="./logs",
            logging_steps=100,
            evaluation_strategy="steps",
            eval_steps=500,
            save_steps=1000,
            save_total_limit=2,
            learning_rate=learning_rate,
            fp16=torch.cuda.is_available(),
            gradient_accumulation_steps=4,
        )

        # Create data collator
        data_collator = DataCollatorForSeq2Seq(
            tokenizer=self.tokenizer,
            model=self.model,
            padding=True
        )

        # Initialize trainer
        trainer = Seq2SeqTrainer(
            model=self.model,
            args=training_args,
            train_dataset=train_dataset,
            eval_dataset=eval_dataset,
            data_collator=data_collator,
            tokenizer=self.tokenizer,
        )

        # Start training
        self.logger.info("Starting training...")
        trainer.train()
        
        # Save the final model
        trainer.save_model()
        self.tokenizer.save_pretrained(self.output_dir)
        self.logger.info(f"Model saved to {self.output_dir}")

if __name__ == "__main__":
    trainer = MultilingualTrainer()
    
    # Load datasets
    train_dataset = trainer.load_dataset("../../data/processed/train")
    eval_dataset = trainer.load_dataset("../../data/processed/eval")
    
    # Start training
    trainer.train(train_dataset, eval_dataset) 