import json 
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.models import load_model
from nltk.stem import WordNetLemmatizer
from sklearn.utils import shuffle
import nltk

lemmatizer = WordNetLemmatizer()

class GenericAssistant:
    def __init__(self, intents_file, intent_methods={}, name="Assistant"):
        self.name = name

        with open(intents_file, 'r') as file:
            self.intents = json.load(file)['intents']

        self.vectorizer = CountVectorizer()
        self.label_encoder = LabelEncoder()
        self.model = load_model("neuralintents.h5")

        self.intent_methods = intent_methods
        self._prepare_data()

    def _prepare_data(self):
        patterns = []
        tags = []
        for intent in self.intents:
            for pattern in intent['patterns']:
                pattern = " ".join([lemmatizer.lemmatize(word.lower()) for word in nltk.word_tokenize(pattern)])
                patterns.append(pattern)
                tags.append(intent['tag'])

        self.X = self.vectorizer.fit_transform(patterns).toarray()
        self.y = self.label_encoder.fit_transform(tags)

    def train_model(self):
        model = Sequential()
        model.add(Dense(128, input_shape=(self.X.shape[1],), activation='relu'))
        model.add(Dropout(0.5))
        model.add(Dense(64, activation='relu'))
        model.add(Dropout(0.5))
        model.add(Dense(len(set(self.y)), activation='softmax'))

        model.compile(loss='sparse_categorical_crossentropy',
                      optimizer='adam', 
                      metrics=['accuracy'])

        self.X, self.y = shuffle(self.X, self.y)
        history = model.fit(self.X, self.y, epochs=200, verbose=1)

        model.save('neuralintents.h5')
        self.model = model

    def load_model(self):
        self.model = load_model("neuralintents.h5")

    def predict_intent_tag(self, message):
        message = " ".join([lemmatizer.lemmatize(word.lower()) for word in nltk.word_tokenize(message)])
        X = self.vectorizer.transform([message]).toarray()
        prediction = self.model.predict(X).argmax(axis=-1)
        predicted_tag = self.label_encoder.inverse_transform(prediction)[0]
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
