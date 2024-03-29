import langchain
from langchain_community.llms import OpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.chains import SequentialChain
from langchain_community.callbacks import get_openai_callback
import os 
import json
import pandas as pd
import traceback
import PyPDF2
from dotenv import load_dotenv
## Load environment from .env
load_dotenv()

key=os.getenv("OPENAI_API_KEY")

from langchain_community.chat_models import ChatOpenAI

llm=ChatOpenAI(openai_api_key=key,model_name='gpt-3.5-turbo',temperature=0.7)


TEMPLATE="""
TEXT:{text}
You are an Expert Mcq Maker.Given the above the text, it is your job to \
create a quiz of {number} multiple choice question for {subject} student in {tone} tone.
Make sure the Questions are not repeated and check all the questions to be conforming the text as well,
Ensure to make {number} MCQ
### RESPONSE_JSON
{response_json}"""



Quiz_generation_prompt=PromptTemplate(
    input_variables=['text','number','subject','tone','response_json'],
    template=TEMPLATE
    )

quiz_chain=LLMChain(llm=llm,prompt=Quiz_generation_prompt,output_key='quiz',verbose=True)


TEMPLATE2="""
You are an expert english grammarian and writer. Given a Multiple Choice Quiz for {subject} students.\
You need to evaluate the complexity of the question and give a complete analysis of the quiz. Only use at max 50 words for complexity analysis. 
if the quiz is not at per with the cognitive and analytical abilities of the students,\
update the quiz questions which needs to be changed and change the tone such that it perfectly fits the student abilities
Quiz_MCQs:
{quiz}

Check from an expert English Writer of the above quiz:
"""



Quiz_evaluation_prompt=PromptTemplate(
    input_variables=['subject','quiz'],
    template=TEMPLATE2
)

review_chain=LLMChain(llm=llm,prompt=Quiz_evaluation_prompt,verbose=True,output_key='review')



generate_evaluate_chain=SequentialChain(chains=[quiz_chain, review_chain], input_variables=['text','number','subject','tone','response_json'],
                                        output_variables=["quiz", "review"], verbose=True)


