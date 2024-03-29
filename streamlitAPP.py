import os 
import json
import pandas as pd
import traceback
from dotenv import load_dotenv
from langchain_community.callbacks import get_openai_callback
from src.McqGenerator.utils import get_table_data,read_file
from src.McqGenerator.ee import generate_evaluate_chain
from src.McqGenerator.logger import logging
import streamlit as st

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
    uploaded_file=st.file_uploader("Upload a PDF or TXT File")
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
    with st.spinner("Loading....."):
        try:
            text=read_file(uploaded_file)
            ## count the tokens and cost api calls
            with get_openai_callback() as cb:
                response=generate_evaluate_chain(
                    {
                        "text": text,
                        "number": mcq_count,
                        "subject":subject,
                        "tone": tone,
                        "response_json": json.dumps(RESPONSE_JSON)
                    }
                    )
        except Exception as e:
            traceback.print_exception(type(e),e,e.__traceback__)
            st.error("error")     

        else:
            print(f"Total Tokens: {cb.total_tokens}")
            print(f"Prompt Tokens: {cb.prompt_tokens}")
            print(f"Completion Tokens: {cb.completion_tokens}")
            print(f"Total Cost:{cb.total_cost}")
            if isinstance(response, dict):
            #Extract the quiz data from the response
                quiz=response.get("quiz", None)
                print(quiz)
                if quiz is not None:
                    table_data=get_table_data(quiz)
                    
                    
                    if table_data is not None:
                        df=pd.DataFrame(table_data)
                        
                        df.index=df.index+1
                        st.table(df)
                        #Display the review in atext box as well
                        st.text_area(label="Review", value=response ["review"])
                    else:
                        st.error("Error in the table data")      
                else:
                    st.write(response)         

