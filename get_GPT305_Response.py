import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=openai_api_key)

def get_GPT305_Response(prompt):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        messages=[
            {
                "role" : "user",
                "content" : prompt,
            }
        ],
        response_format={"type" : "text"},
        max_tokens=100
    )
    return response.choices[0].message.content.strip()

if __name__ == '__main__':
    while True:
        user_input = input("You: ")
        if(user_input.lower() in ["quit" , "exit" , "bye"]):
            break;
        response = get_GPT305_Response(user_input)
        print("GPT 3.5 Turbo : " + response)