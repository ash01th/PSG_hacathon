import os
from groq import Groq
from dotenv import load_dotenv

# Loading environment variables from  .env file
load_dotenv(dotenv_path='api_key.env')
client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

#messages sent to LLM (sample input)
msg1=[
    {
        "role": "system",
        "content": "you are a helpful assistant."
    },
    {
        "role": "user",
        "content": "what is two plus two?",
    },
     {
        "role": "assistant",
        "content": "two plus two is four do you need help with anything else?",
    },
    {
        "role": "user",
        "content": "what is four plus four?",
    },

]

# initilize model and get response
def get_response_from_llama(msg):
    print(msg)
    chat_completion = client.chat.completions.create(
    messages=msg,
    model="llama3-8b-8192",
    )
    return chat_completion.choices[0].message.content

