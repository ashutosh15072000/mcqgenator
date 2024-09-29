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
radio_messages={}

if button and uploaded_file is not None and mcq_count and subject and tone:
    with st.spinner("Loading....."):
        try:
            text=uploaded_file
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
                
                #Extract the quiz data from the response
                Response=str(response["quiz"][17:])
                Response=json.loads(Response)
                    # Convert dictionary to list
                questions_list = list(Response.values())
                radio_groups={}

                for no in range(1,mcq_count+1):
                    no=str(no)
                    a=Response[no]['options']['a']
                    b=Response[no]['options']['b']
                    c=Response[no]['options']['c']
                    d=Response[no]['options']['d']
                    radio_groups[Response[no]['mcq']]=[a,b,c,d]

                

                # Loop through the dictionary and create a radio button for each group
                for group_name, options in radio_groups.items():
                    selected_option = st.radio(f"{group_name}:", options,index=None)
                    for lists in questions_list:
                        if lists['mcq']==group_name:
                            correct_answer=lists['options'][lists['correct']]
                            if selected_option==correct_answer:
                                st.success("Correct")
                            elif selected_option==None:
                                pass    
                            else:
                                st.warning("Incorrect Answer")
                
        except Exception as e:
            traceback.print_exception(type(e),e,e.__traceback__)
            st.error("error")     

        else:
            print(f"Total Tokens: {cb.total_tokens}")
            print(f"Prompt Tokens: {cb.prompt_tokens}")
            print(f"Completion Tokens: {cb.completion_tokens}")
            print(f"Total Cost:{cb.total_cost}")
        
    

