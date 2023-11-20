#from langchain.llms import OpenAI
import os
import openai
from dotenv import load_dotenv
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

from langchain.llms import OpenAI

def chatpredict(question):
    llm= OpenAI(temperature=0.1, model_name="gpt-3.5-turbo")
    
    completion = llm(question)
    print(completion)
    
    
print(chatpredict("IS python is compiled language?"))