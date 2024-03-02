import json
import numpy as np
import torch
from sklearn.preprocessing import LabelEncoder
from transformers import BertTokenizerFast, BertForSequenceClassification, Trainer, TrainingArguments
from sklearn.utils import shuffle
import nltk

class GenericAssistant:
    def __init__(self, intents_file, intent_methods={}, name="Eco", model_name='bert-base-uncased'):
        self.name = name
        self.tokenizer = BertTokenizerFast.from_pretrained(model_name)
        self.intent_methods = intent_methods

        with open(intents_file, 'r') as file:
            self.intents = json.load(file)['intents']

        self.label_encoder = LabelEncoder()
        self._prepare_data()

    def _prepare_data(self):
        patterns = []
        tags = []
        for intent in self.intents:
            for pattern in intent['patterns']:
                patterns.append(pattern)
                tags.append(intent['tag'])

        self.X = patterns
        self.y = self.label_encoder.fit_transform(tags)
        self.labels = self.label_encoder.classes_

    def train_model(self, model_name='bert-base-uncased', training_args=None):
        train_encodings = self.tokenizer(self.X, truncation=True, padding=True)
        train_dataset = IntentClassificationDataset(train_encodings, self.y)

        model = BertForSequenceClassification.from_pretrained(model_name, num_labels=len(self.labels))

        if training_args is None:
            training_args = TrainingArguments(
                output_dir='./results',
                num_train_epochs=100,
                per_device_train_batch_size=16,
                per_device_eval_batch_size=64,
                warmup_steps=500,
                weight_decay=0.01,
                logging_dir='./logs',
            )

        trainer = Trainer(
            model=model,
            args=training_args,
            train_dataset=train_dataset,
        )

        trainer.train()

        trainer.save_model()  # This will save the model in the output_dir specified in TrainingArguments

        self.model = model

    def load_model(self, model_dir='./results'):
        self.model = BertForSequenceClassification.from_pretrained(model_dir)


    def predict_intent_tag(self, message):
        inputs = self.tokenizer.encode_plus(message, return_tensors='pt')
        outputs = self.model(**inputs)
        prediction = torch.argmax(outputs.logits).item()
        predicted_tag = self.labels[prediction]
        return predicted_tag

    def get_response(self, message):
        tag = self.predict_intent_tag(message)
        if tag in self.intent_methods:
            return self.intent_methods[tag]()
        else:
            responses = [intent['responses'] for intent in self.intents if intent['tag'] == tag]
            if responses:
                return np.random.choice(responses[0])
            else:
                return "Sorry, I didn't understand that. Can you rephrase?"

    def chat(self):
        print(f"Hello! I'm {self.name}. How can I assist you today?")

        while True:
            message = input("You: ")
            if message == "quit":
                break
            response = self.get_response(message)
            print(f"{self.name}: {response}")

class IntentClassificationDataset(torch.utils.data.Dataset):
    def __init__(self, encodings, labels):
        self.encodings = encodings
        self.labels = labels

    def __getitem__(self, idx):
        item = {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}
        item['labels'] = torch.tensor(self.labels[idx])
        return item

    def __len__(self):
        return len(self.labels)

