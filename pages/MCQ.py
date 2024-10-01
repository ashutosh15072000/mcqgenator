# Contents of ~/my_app/streamlit_app.py
import streamlit as st
import json

mcq_count=st.session_state['mcq_count']
 #Extract the quiz data from the response
Response=str(st.session_state['response']['quiz'][17:])
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