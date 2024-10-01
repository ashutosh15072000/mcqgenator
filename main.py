import langchain
from langchain_community.llms import OpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.chains import SequentialChain
from langchain_community.callbacks import get_openai_callback
from langchain_groq import ChatGroq
import os 
import json
import pandas as pd
import traceback
import PyPDF2
import streamlit as st
from dotenv import load_dotenv
import os 
import json
import pandas as pd
import traceback
from dotenv import load_dotenv
from langchain_community.callbacks import get_openai_callback
from src.McqGenerator.utils import get_table_data
from src.McqGenerator.ee import generate_evaluate_chain
from src.McqGenerator.logger import logging
import streamlit as st
## Load environment from .env
load_dotenv()

key=os.getenv("GROQ_API_KEY")

from langchain_community.chat_models import ChatOpenAI

llm=ChatGroq(groq_api_key=key,model_name='llama-3.1-70b-versatile',temperature=0.7)


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


##loading jason file
with open("A:\mcqgenator\Response.json",'r') as files:
        try:
            RESPONSE_JSON = json.load(files)
        except json.JSONDecodeError:
            print("Empty response")    
  

 ## creating title for the app
st.title("Mcq Generator")

## Create a form using st.form
with st.form("user_input"):
    ##File upload
    uploaded_file=st.text_area("Upload a PDF or TXT File")
    ## input field
    mcq_count=st.number_input("No of Mcq",min_value=3,max_value=50)
    ## input subject
    subject=st.text_input("Insert Subject",max_chars=20)
    ## Quiz Tone
    tone=st.text_input("Complexity Level of Questions",max_chars=20,placeholder="Simple")
    ## Add Button
    button=st.form_submit_button("Create MCQs")

## check if button is clicked and all field have input


if button and uploaded_file is not None and mcq_count and subject and tone:
            text=uploaded_file
            ## count the tokens and cost api calls
            response=generate_evaluate_chain(
                    {
                        "text": text,
                        "number": mcq_count,
                        "subject":subject,
                        "tone": tone,
                        "response_json": json.dumps(RESPONSE_JSON)
                    })
            st.session_state['response']=response
     
            st.session_state['mcq_count']=mcq_count
    
            st.switch_page("pages/MCQ.py")
