from dotenv import load_dotenv
load_dotenv()

def get_text_length(text:str)-> int:
    """Returns length of a string by characters"""
    return len(text)

if __name__ == "__main__":
    print("Inside main | ReAct")
    print(get_text_length("abcjd sdkc"))
    