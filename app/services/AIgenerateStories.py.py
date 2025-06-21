import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

def generate_bible_stories(prompt):
    
    client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv('API_KEY')
    )

    completion = client.chat.completions.create(
    model="deepseek/deepseek-r1-0528:free",
    messages=[
        {
            "role": "system",
            "content": """You are a friendly devoted christian, child-safe Holy Bible assistant named Biblia. You help and answer bible questions in simple, kind, and gentle language suitable for children aged 8-20. Refer to Bible teachings where relevant. You are also a good Bible story-teller who is able to narrate Bible stories based on what the user is feeling. You do not respond to any questions outside of Biblical context.
            """
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": prompt
                }
            ]
        },
    ],
    )
    return completion.choices[0].message.content
