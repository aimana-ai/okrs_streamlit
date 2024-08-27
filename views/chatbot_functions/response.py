import streamlit as st
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain_openai import ChatOpenAI
# Load dotenv
from dotenv import load_dotenv
load_dotenv()

# Create a ChatOpenAI model
model = ChatOpenAI(model="gpt-4o")#, api_key=st.secrets.openai.OPENAI_API_KEY)


# Define prompt templates (no need for separate Runnable chains)
prompt_template = ChatPromptTemplate.from_messages(
    [
        ("system", """You are a helpful and nice bot that answers the users question in the best manner possible
         Here is the question: {user_query}. Do not say anything that is not related to the question and if you 
         do not know the answer, just say you do not know. Use the following chat history to generate the response:
         {chat_history}"""),
    ]
)

# Create the combined chain using LangChain Expression Language (LCEL)
chain = prompt_template | model | StrOutputParser()


def response_generator(prompt, messages):
    response = prompt
    messages = messages
    response = chain.invoke({"user_query": prompt, "chat_history": messages})
    return str(response)



