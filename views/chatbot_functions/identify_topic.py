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
class identificator(BaseModel):
    classification: str = Field(description="Classify the last message sent by the user into Objective, Key Result, Iniciative or None")
    justification: str = Field(description="Briefly describe why the statement was classified into its category")

# Set up a parser + inject instructions into the prompt template.
parser = JsonOutputParser(pydantic_object=identificator)


prompt_template = PromptTemplate(
    template="""
## **ROLE:**
You are an OKR expert with deep expertise in distinguishing between Objectives, Key Results (KRs), Initiatives, and unrelated statements.

## **TASK:**
Your task is to analyze the user’s statement provided in the variable `
{last_utterance}
` and classify it as one of the following: an Objective, a Key Result (KR), an Initiative, or None. Use the criteria and examples provided to make an accurate determination.

## **SPECIFICS:**
1. **Analyze the Statement:**  
   - **Objective:** Determine if the statement answers "Where do we want to go?" It should be qualitative, inspiring, and devoid of metrics. Look for statements that are ambitious, achievable, and typically use verbs, often accompanied by a timeframe.
   - **Key Result (KR):** Check if the statement answers "How do I know if I am getting there?" It should be quantitative, measurable, and contain clear metrics indicating progress.
   - **Initiative:** Identify if the statement answers "What will I do to get there?" These are actionable steps or tasks aimed at achieving a KR.
   - **None:** If the statement does not match any of the above categories, classify it as "None."

## **CONTEXT:**
The statement is stored in the variable `
{last_utterance}
` and may describe an OKR-related concept or something else entirely.

## **EXAMPLE OUTPUT:**
- **Classification:** Objective  
  **Justification:** The statement "Be a well-known and desired brand by large companies" is qualitative, inspiring, and lacks metrics, which qualifies it as an Objective.

- **Classification:** Key Result (KR)  
  **Justification:** The statement "Train 80% of the team in agile methodologies" is quantitative and measurable, with a clear metric, categorizing it as a Key Result (KR).

- **Classification:** Initiative  
  **Justification:** The statement "Conduct a three-day workshop on agile methodologies" describes a specific task intended to achieve a KR, hence it is classified as an Initiative.

- **Classification:** None  
  **Justification:** The statement "Improve internal communication" is vague and does not clearly fit as an Objective, Key Result (KR), or Initiative.

## **NOTES:**
- **Clarity:** Ensure your classification is precise and based on the provided criteria.
- **Justification:** Provide a concise explanation for your classification, referencing the defining characteristics of the statement.
- **Brevity:** Keep your output succinct yet informative.

## **FINAL INSTRUCTION:**
Carefully analyze the statement step by step, classify it accurately, and justify your reasoning clearly.

{format_instructions}
        """,
    input_variables=["last_utterance"],
    partial_variables={"format_instructions": parser.get_format_instructions()},
)


# Create the combined chain using LangChain Expression Language (LCEL)
chain = prompt_template | model | parser



def identify_topic(query):
    response = chain.invoke({ "last_utterance": query})
    classification = response["classification"]
    justification = response["justification"]
    return str(classification), str(justification)