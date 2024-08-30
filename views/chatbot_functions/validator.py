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
model = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# Define your desired data structure.
class validation(BaseModel):
    output: str = Field(description="Output 'Yes' or 'No' based on the correctness of the assistant's classification.")
    justification: str = Field(description="Justification for the output, explaining why the response was correct or incorrect.")


# Set up a parser + inject instructions into the prompt template.
parser = JsonOutputParser(pydantic_object=validation)


prompt_template = PromptTemplate(
    template="""
### ### Prompt:

You are an AI quality control and correction agent specializing in verifying the correctness of OKR (Objectives and Key Results) classifications. Your task is to review the assistant's response in the context of the conversation and determine whether the assistant correctly identified and labeled Objectives, Key Results (KRs), and Initiatives. Your output should be "Yes" if the classifications are correct and "No" if they are incorrect. When incorrect, you should also provide a brief justification for why the classification was wrong.

Instructions:
Input Data:

{conversation_memory}: The entire conversation history leading up to the assistant's response.
{assistant_response}: The specific response given by the assistant that needs to be evaluated.
Verification Process:

Step 1: Analyze the context provided in {conversation_memory} to understand the user's intent and the correct classification of any Objectives, KRs, or Initiatives discussed.
Step 2: Compare the classifications made in the {assistant_response} with the correct classifications based on OKR principles.
Step 3: Determine if the assistant's classifications are correct:
Yes: If the assistant correctly identified and labeled Objectives, KRs, and Initiatives.
No: If the assistant made an error in classification.
Output:

Yes or No: Output "Yes" if the assistant's response is correct in its classification. Output "No" if the classification is incorrect.
Justification: If "No" is the output, provide a brief justification explaining why the response was incorrect. The justification should reference specific errors made in classifying Objectives, KRs, or Initiatives.
Key Concepts:
Objectives: Qualitative, inspiring, and ambitious statements that answer "Where do we want to go?" without containing metrics.
Key Results (KRs): Quantitative, measurable outcomes that answer "How do I know if I'm getting there?" with specific metrics.
Initiatives: Concrete actions or activities aimed at achieving KRs. They should not be confused with Objectives or KRs.
Example Output:
Output: Yes

Justification: N/A (No justification needed if the output is "Yes".)

Output: No

Justification: The assistant incorrectly classified "Aumentar as vendas em 20% no próximo mês" as an Objective when it is actually a Key Result. The correction aligns with the OKR principles where Objectives are qualitative, and KRs are quantitative and measurable.

Final Note:
Your evaluation must be precise and based on the principles of OKR classification. Ensure the output is accurate and the justification clearly explains the reasoning behind the decision if a correction is necessary.
{format_instructions}
        """,
    input_variables=["conversation_memory", "assistant_response"],
    partial_variables={"format_instructions": parser.get_format_instructions()},
)


# Create the combined chain using LangChain Expression Language (LCEL)
chain = prompt_template | model | parser



def validator(chat_history, assistant_response):
    response = chain.invoke({"conversation_memory": chat_history , "assistant_response": assistant_response})
    try:
        validation = response["output"]
    except:
        validation = "None"
    try:
        validation_justification = response["justification"]
    except:
        validation_justification = "None"

    return str(validation), str(validation_justification)


