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
class route(BaseModel):
    conversation_phase: str = Field(description="Indicate the current phase of the conversation.")
    description: str = Field(description="Briefly describe the identified phase.")
    suggested_action: str = Field(description="Recommend the next step or guide the user back to an incomplete prior step, with clear instructions on what needs to be addressed.")

# Set up a parser + inject instructions into the prompt template.
parser = JsonOutputParser(pydantic_object=route)


prompt_template = PromptTemplate(
    template="""
### **ROLE:**

You are an AI assistant specialized in conversation routing, tasked with analyzing dialogue summaries to pinpoint the exact phase in the OKR (Objectives and Key Results) creation process. Your role is crucial in guiding users through a logical sequence, ensuring maximum efficiency and quality in their OKR development.

### **TASK:**

Read the variables `{main_topics}`, `{last_utterance}`, and `{context}`, which contain a detailed summary of the conversation so far, and accurately identify the current phase of the OKR process. Ensure that each phase is validated before moving on to the next step. If any prior steps have not been completed, the user should be guided to complete those first.

### **Conversation Phases:**

1. **Identify the Focus Area:**
   - The user specifies the area or domain for OKRs, such as Finance, Marketing, HR, IT, Sales, Customer Service, or Operations.
   
2. **Understand Challenges and Opportunities:**
   - Discuss the challenges or areas for improvement within the selected focus area.
   
3. **Suggest Objectives:**
   - Suggest and validate specific objectives based on identified challenges (no Key Results at this stage).
   
4. **Define Key Results (KRs):**
   - Propose and refine 2 to 4 KRs for each validated objective, ensuring they are specific and measurable.
   
5. **Review and Finalize:**
   - Review and finalize the OKRs, providing a complete and structured summary.

### **Instructions:**

1. **Analyze the Summary:**
   - Carefully read `{main_topics}`, `{last_utterance}`, and `{context}`.
   - **Step 1:** Look for mentions of specific areas (e.g., Finance, Marketing).
   - **Step 2:** Identify discussions about challenges or opportunities.
   - **Step 3:** Check for suggestions or validations of objectives.
   - **Step 4:** Look for discussions about KRs.
   - **Step 5:** Identify reviews or finalizations of OKRs.

2. **Ensure Sequential Validation:**
   - **Step 1:** Ensure that the focus area has been clearly identified. If not, guide the user to complete this step.
   - **Step 2:** Ensure challenges and opportunities have been fully discussed and understood. If not, guide the user back to this phase.
   - **Step 3:** Ensure that objectives have been suggested and validated. If not, direct the user to finalize objectives before proceeding.
   - **Step 4:** Ensure that key results (KRs) are defined for each objective. If not, guide the user to complete this step before moving forward.
   - **Step 5:** Only review and finalize if all previous steps are completed and validated.

### **Final Considerations:**

Before executing these instructions, take a deep breath and carefully consider the entire context of the conversation. Ensure that you have fully understood the user’s intent, and that all prior steps have been thoroughly validated. Be critical but supportive, guiding the user with clarity and precision. Always keep in mind the overall goal of helping the user develop effective OKRs that are aligned with their strategic objectives.

**Important:** The `Conversation Phase` should ALWAYS be one of the steps in the OKR creation process (Identify the Focus Area, Understand Challenges and Opportunities, Suggest Objectives, Define Key Results, Review and Finalize). If the conversation is not aligned with any of these phases, direct the user to the appropriate step.
        
{format_instructions}
        """,
    input_variables=["main_topics", "last_utterance","context"],
    partial_variables={"format_instructions": parser.get_format_instructions()},
)


# Create the combined chain using LangChain Expression Language (LCEL)
chain = prompt_template | model | parser



def router(query, main_topics, context):
    response = chain.invoke({"main_topics": main_topics , "last_utterance": query, "context": context})
    conversation_phase = response["conversation_phase"]
    description = response["description"]
    suggested_action = response["suggested_action"]
    return str(conversation_phase), str(description), str(suggested_action)