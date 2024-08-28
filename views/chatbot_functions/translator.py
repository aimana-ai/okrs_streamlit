from dotenv import load_dotenv
from langchain.prompts import ChatPromptTemplate
from langchain_core.prompts import PromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field

# Load environment variables from .env
load_dotenv()

# Create a ChatOpenAI model
model = ChatOpenAI(model="gpt-4o")

# Define your desired data structure.
class translated_answer(BaseModel):
    translated_answer: str = Field(description="The content of the variable {response} translated to Portuguese-br")


# Set up a parser + inject instructions into the prompt template.
parser = JsonOutputParser(pydantic_object=translated_answer)


prompt_template = PromptTemplate(
    template="""
### **Prompt:**

You are a professional translator. Your task is to accurately translate the content provided in the variable `{response}` from English to Portuguese. Ensure that the translation maintains the original meaning, tone, and context of the text.

Translate the following: {response} 
        
{format_instructions}
        """,
    input_variables=["response"],
    partial_variables={"format_instructions": parser.get_format_instructions()},
)


# Create the combined chain using LangChain Expression Language (LCEL)
chain = prompt_template | model | parser



def translate_answer(response):
    response = chain.invoke({"response": response})
    translated_answer = response["translated_answer"]
    return str(translated_answer)