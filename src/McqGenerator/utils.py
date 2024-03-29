import os 
import json
import pandas as pd
import traceback
import PyPDF2


def read_file(file):
    if file.name.endswith(".pdf"):
        try:
            pdf_reader=PyPDF2.PdfFileReader()
            text=""
            for page in pdf_reader.pages:
                text+=page.extract_text()
            return text
        except Exception as e:
            raise Exception ("error reading the file Pdf File")
    elif file.name.endswith(".txt"):
        return file.read().decode("utf-8")
    else:
        raise Exception("Unsupported file format only Pdf and txt file supported")


def get_table_data(quiz_str):
    try:
    #convert the quiz from a strto dict
        quiz_dict=json.loads(quiz_str)
        quiz_table_data=[]
        #iterate over the quiz dictionary and extract the required information
        for key, value in quiz_dict.items():
            mcq=value["mcq"]
            option="||".join(
            [
            f"{options} {option_value}" for options,option_value in value["options"].items()
            ]
            )
            correct=value["correct"]
            quiz_table_data.append({"MCQ": mcq, "Choices": option, "Correct": correct})
        return quiz_table_data
    except Exception as e:
        traceback.print_exception(type (e), e, e. traceback)
        return False


    
                               