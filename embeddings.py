import openai
from finacial_ai.database_manager.db_manager import DatabaseManager

db_manager = DatabaseManager('financial_ai.db')
openai = "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"

def create_embedding(event):
    # convert event dictionary to text
    text = ', '.join([f"{k}: {v}" for k, v in event.items()])
    
    # Create a prompt that asks the model to give an understanding of the event
    prompt = f"Give a brief understanding of the economic event: {text}"

    response = openai.ChatCompletion.create(
      model="text-davinci-002",
      prompt=prompt,
      max_tokens=60
    )

    return response.choices[0].text.strip()

# for each event in the database
events = db_manager.get_items('economic_events')

for event in events:
    # event is a tuple, so convert it to a dict
    event_dict = {
        'Date': event[1],
        'Time': event[2],
        'Currency': event[3],
        'Impact': event[4],
        'Event': event[5],
        'Actual': event[6],
        'Forecast': event[7],
        'Previous': event[8]
    }
    embedding = create_embedding(event_dict)
    print(embedding)
