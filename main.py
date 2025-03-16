from dotenv import load_dotenv
load_dotenv()
from langchain.tools import tool
from langchain.tools.render import render_text_description
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents.structured_chat.output_parser import StructuredChatOutputParser
from langchain.agents.output_parsers.react_single_input import ReActSingleInputOutputParser

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
    # print(get_text_length.invoke(input={"text": "Dog"}))
    tools = [get_text_length]

    template = """
        Answer the following questions as best you can. You have access to the following tools:

        {tools}

        Use the following format:

        Question: the input question you must answer
        Thought: you should always think about what to do
        Action: the action to take, should be one of [{tool_names}]
        Action Input: the input to the action
        Observation: the result of the action
        ... (this Thought/Action/Action Input/Observation can repeat N times)
        Thought: I now know the final answer
        Final Answer: ONLY output this after an Observation

        Begin!

        Question: {input}
        Thought:
    """

    prompt = PromptTemplate.from_template(template=template).partial(
        tools=render_text_description(tools), tool_names=", ".join([t.name for t in tools])
    )
    
    llm = ChatGoogleGenerativeAI(
        temperature=0, 
        model="gemini-2.0-flash", 
        stop_sequences=["\nObservation", "\nFinal Answer"]
    )

    agent = {"input": lambda x: x["input"]} | prompt | llm | StructuredChatOutputParser()

    # agent = {"input": lambda x: x["input"]} | prompt | llm | ReActSingleInputOutputParser()

    res = agent.invoke({"input": "What is the length in characters of the text DOG ?"})
    print(res)