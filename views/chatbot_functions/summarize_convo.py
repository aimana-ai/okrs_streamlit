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
class convo_summary(BaseModel):
    main_topics: str = Field(description="Brief summary of the key points of the conversation so far")
    last_message: str = Field(description="Last message sent by the user")
    context: str = Field(description="How the last message connects to the rest of the conversation")

# Set up a parser + inject instructions into the prompt template.
parser = JsonOutputParser(pydantic_object=convo_summary)


prompt_template = PromptTemplate(
    template="""
        # **ROLE:**
You are an AI assistant specializing in crafting clear and concise conversation summaries.

# **TASK:**
Analyze dialogue histories to create summaries that emphasize the user's final message. The summary should be no longer than 500 characters and follow a specific structure.

# **SPECIFICS:**
1. **Summarize Key Points:** Identify and distill the main topics, questions, and answers discussed.
2. **Emphasize Last Message:** Highlight the significance of `{last_utterance}` in relation to the overall conversation.
3. **Compose Summary:** Generate a summary in the following format:
   - **Main Topics:** [Brief summary of key points]
   - **Last Message:** [Summary of the last message and its importance]
   - **Context:** [How the last message connects with the conversation]

# **CONTEXT:**
Given the conversation stored in `{chat_history}` and the user’s last message in `{last_utterance}`, extract and synthesize information to create a summary that reflects the entire conversation with a focus on the final user input.

# **EXAMPLE:**
"Main Topics: Discussed [Topics]. Last Message: User mentioned [Last Message]. Context: This highlights [Significance and relevance to the discussion]."

# **NOTES:**
- **Brevity and Focus:** Keep the summary within 500 characters.
- **Clarity:** Ensure the summary is easily understandable and captures the essence of the conversation.
- **Structure:** Maintain a consistent and clear format for the summary.
- **Emphasis:** The user’s last message is critical and should be the focal point of the summary.
        
        
{format_instructions}
        """,
    input_variables=["last_utterance","chat_history"],
    partial_variables={"format_instructions": parser.get_format_instructions()},
)


# Create the combined chain using LangChain Expression Language (LCEL)
chain = prompt_template | model | parser



def summarize_convo(query, messages):
    messages = messages
    response = chain.invoke({"last_utterance": query, "chat_history": messages})
    main_topics = response["main_topics"]
    last_message = response["last_message"]
    context = response["context"]
    return str(main_topics), str(last_message), str(context)

