import os
from openai import OpenAI # pyright: ignore[reportMissingImports]
from dotenv import load_dotenv # pyright: ignore[reportMissingImports]

load_dotenv()

def generate_bible_stories(prompt, conversation_history):
    
    client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv('API_KEY')
    )

    # Add user response to the conversation history
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
            model="deepseek/deepseek-r1-0528:free",
            messages=conversation_history,
            temperature=0.7,
            stream=True
        )
        # Chunk ai responses
        full_response = ""
        for chunk in completion:
            if chunk.choices[0].delta.content:
                full_response += chunk.choices[0].delta.content

        # Add AI response to the conversation history
        conversation_history.append({"role": "assistant", "content": full_response})

        return full_response, conversation_history

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return "An unexpected error occurred. Please try again.", conversation_history
