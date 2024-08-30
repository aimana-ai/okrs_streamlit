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
model = ChatOpenAI(model="gpt-4o", temperature=0)

# Define your desired data structure.
class identificator(BaseModel):
    objectives: str = Field(description="List of critically identified objectives or leave empty if none identified")
    krs: str = Field(description="List of critically identified key results or leave empty if none identified")
    iniciatives: str = Field(description="List of critically identified initiatives or leave empty if none identified")

# Set up a parser + inject instructions into the prompt template.
parser = JsonOutputParser(pydantic_object=identificator)


prompt_template = PromptTemplate(
    template="""
**ROLE:**
You are an AI assistant with a sharp focus on critically analyzing conversations about OKRs to accurately extract and classify Objectives, Key Results (KRs), and Initiatives.

# **TASK:**
Carefully analyze the conversation to identify and extract the Objectives, Key Results (KRs), and Initiatives. Your task is to critically assess and correctly classify these elements into three distinct variables: `Objectives`, `KRs`, and `Initiatives`. If no relevant content is found for any of these categories, the corresponding variable should remain empty.

# **SPECIFICS:**
1. **Critically Identify Objectives:**
   - **Criteria:** Look for statements that answer "Where do we want to go?" They should be qualitative, inspiring, ambitious, and devoid of metrics. Objectives typically use action-oriented verbs and may be tied to a specific timeframe. Be critical of any statement that may seem quantitative or task-oriented, as it does not belong in this category.
   - **Variable:** `Objectives`

2. **Critically Identify Key Results (KRs):**
   - **Criteria:** Identify statements that answer "How do I know if I am getting there?" They must be quantitative, measurable, and tied to specific metrics that indicate progress. KRs should represent outcomes, not tasks or actions. Ensure that the KR is ambitious yet attainable and clearly measurable.
   - **Variable:** `KRs`

3. **Critically Identify Initiatives:**
   - **Criteria:** Look for statements that answer "What will I do to get there?" These should be concrete, actionable steps or tasks aimed at achieving a KR. Initiatives are specific activities or efforts, not outcomes. Critically differentiate between strategic outcomes (KRs) and tactical actions (Initiatives).
   - **Variable:** `Initiatives`

4. **Classification:**
   - Be meticulous in ensuring that each element is correctly classified. If a statement contains mixed elements (e.g., an objective combined with a KR), separate and classify them accordingly. Avoid any misclassification, particularly confusing KRs with tasks or confusing objectives with initiatives. If no content matches a category, leave the respective variable empty.

# **CONTEXT:**
Given the conversation stored in `{chat_history}`, perform a thorough analysis to extract and critically classify any identified Objectives, Key Results (KRs), and Initiatives. Populate the following variables with the most accurate and concise content. If a category does not apply, the corresponding variable should remain empty:

- `Objectives: [List of critically identified objectives or leave empty if none identified]`
- `KRs: [List of critically identified key results or leave empty if none identified]`
- `Initiatives: [List of critically identified initiatives or leave empty if none identified]`

# **EXAMPLE OUTPUT:**
- **Objectives:** "Expand our market presence in Europe," "Enhance customer satisfaction through superior service."
- **KRs:** "Achieve 20% market share in Europe," "Increase NPS to 85."
- **Initiatives:** "Launch targeted marketing campaigns in key European cities," "Implement new customer service training programs."

# **NOTES:**
- **Critical Accuracy:** Be exacting in your classification, ensuring that each element is properly and strictly identified. Misclassifications should be avoided at all costs.
- **Clarity:** The extracted variables must be clear and unambiguous, reflecting the true intent of the conversation.
- **Precision:** Focus on extracting only the most relevant and precise statements for each category. If no relevant statements are identified, leave the respective variable empty.
--**Not found:** If no content is found for a specific category, leave the corresponding variable empty.
{format_instructions}
        """,
    input_variables=["chat_history"],
    partial_variables={"format_instructions": parser.get_format_instructions()},
)


# Create the combined chain using LangChain Expression Language (LCEL)
chain = prompt_template | model | parser



def list_variables(chat_history):
    response = chain.invoke({ "chat_history": chat_history})
    try:
        objectives = response["objectives"]
    except KeyError:
        objectives = ["No objectives were identified in the conversation."]

    try:
        krs = response["krs"]
    except KeyError:
        krs = ["No key results were identified in the conversation."]

    try:
        initiatives = response["initiatives"]
    except KeyError:
        initiatives = ["No initiatives were identified in the conversation."]

    return str(objectives), str(krs), str(initiatives)

