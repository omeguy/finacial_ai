from assistant import GenericAssistant

def custom_greeting():
    return "Hello, this is a custom response for greeting!"

def bye():
    return "goodbye!!!"

intent_methods = {
    "greetings": custom_greeting,
    "goodbye": bye
    # Add more entries if you have other intents to handle with custom methods
}
def main():
    assistant = GenericAssistant('finacial_ai/intents.json', intent_methods, 'eco')

    assistant.train_model()
    #assistant.load_model()
    assistant.chat()

if __name__ == "__main__":
    main()
