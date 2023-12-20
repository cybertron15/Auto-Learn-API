import os
#import openai
from dotenv import load_dotenv
load_dotenv()
import openai
#
openai.api_key = os.getenv("OPENAI_API_KEY")
#os.environ['OPENAI_API_KEY'] = "OPENAI-API-KEY"


from langchain.llms import OpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI


# prompt = PromptTemplate(input_variables=["language"],
#                         template="""You are an Author. You are an subject matter expert in {language} language. 
#                         Your task is to develop a comprehensive course chapters for a course titled {language} programming Language.
#                         The structure of course should be topicwise.
#                         This course is aimed at Expert level. The learning objectives for this course are 
#                         Audience can read and understand deeply, User can Apply it in real world concept. 
#                         Using the principles of the ADDIE MODEL""")

prompt = PromptTemplate(input_variables=['subject_topic'],
                        template="""You are python subject matter expert. Generate content on chapter
                        {subject_topic}. Here are some key Headings this content should cover:
                        [Overview of Python, History and evolution of Python, Installing Python, 
                        Setting up the development environment,
                        Running Python programs, Python syntax and basic concepts].
                        Generate content by keeping Learning objectives in mind which are [Gain a deep understanding of the Python programming language,
                        Apply Python concepts and principles in real-world scenarios,
                        Develop expertise in Python programming for advanced level projects.""")


chatopenai = ChatOpenAI(
                model_name="gpt-3.5-turbo",
                openai_api_key=openai.api_key,
                temperature=0)
llmchain_chat = LLMChain(llm=chatopenai, prompt=prompt)
print(llmchain_chat.run("Introduction to Python"))

    
    
    
    # llm= OpenAI(temperature=0.1, model_name="gpt-3.5-turbo")
    
    # completion = llm.predict(question)
    # print(completion)
    
    
#chatpredict("IS python is compiled language?")