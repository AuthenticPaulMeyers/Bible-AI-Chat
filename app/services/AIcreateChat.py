import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

def get_response_from_character(character_description, question):
    
    client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("API_KEY")
    )

    completion = client.chat.completions.create(
    model="deepseek/deepseek-r1-0528:free",
    messages=[
        {
            "role": "system",
            "content": f"""{character_description}. You help and answer bible questions in simple, kind, and gentle language suitable for children aged 8-20. Refer to Bible teachings where relevant.
            """
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": question
                }
            ]
        },
    ],
    )
    return completion.choices[0].message.content