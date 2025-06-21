import os
from openai import OpenAI # pyright: ignore[reportMissingImports]
from dotenv import load_dotenv # pyright: ignore[reportMissingImports]

load_dotenv()

def generate_bible_stories(prompt, conversation_history):
    
    client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv('API_KEY')
    )

    conversation_history.append(
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": prompt
                }
            ]
        }
    )

    try:
        completion = client.chat.completions.create(
        model="deepseek/deepseek-chat-v3-0324:free",
        messages=conversation_history,
        temperature=0.7,
        )
        model_response = completion.choices[0].message.content

        conversation_history.append({"role": "assistant", "content": model_response})

        return model_response, conversation_history

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return "An unexpected error occurred. Please try again.", conversation_history
