from dotenv import load_dotenv
load_dotenv()
from langchain.tools import tool 

# Makes the function a tool and adds it to the Langchain tool class 
@tool 
def get_text_length(text:str)-> int:
    """Returns length of a string by characters"""
    text = text.strip("'\n").strip('"')
    # stripping non alphabetic charactes cause langchain might add unwanted characters
    return len(text)

if __name__ == "__main__":
    print("Inside main | ReAct")
    # Can't use the below method to invoke since it's a tool now
    # print(get_text_length("abcjd sdkc"))
    print(get_text_length.invoke(input={"text": "Dog"}))
