# Context: means give extra information to your agent so that tools and hooks take extra data and llm /agent runs do consistency, and in every run attach specific data.

#There are two classes of context

# Local context: explanation in LocalContext.py

# LLM Context: it is which show to the LLM when generates response, it is just in conversation history. it will add in,
#agent instructions, input message, retrivel/web search, when tool exposes

#Suppose you create customer agent which remember user name and id or whole conversation, so you will use LLm Context so that response will be personalized e.g:
# Hey Fazilat! last time you asked about your subscription plan so .....




from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, RunContextWrapper
#importing classes from agents module like,
# Agent: to create AI agent
# Runner: to run agent task 
# AsyncOpenAI: to connect with external openai comaptible API
# OpenAIChatCompletionsModel: to define which LLM model the agent will use
# RunContextWrapper: To carry context object

from dataclasses import dataclass
import asyncio
import os # importing os to access environment variables
from dotenv import load_dotenv

load_dotenv()
# load_dotenv()  # Load environment variables from a .env file



MODEL_NAME = "gemini-2.0-flash" # which LLM model will agent use
GEMINI_API_KEY= os.getenv("GEMINI_API_KEY")



# external_client is the connection that allows us to talk with Gemini API
external_client = AsyncOpenAI(
        api_key = GEMINI_API_KEY,
        base_url = "https://generativelanguage.googleapis.com/v1beta/openai/" #it is Gemini api endpoint bcx we are using Gemini LLM in OpenAI Agents framework
    )

model = OpenAIChatCompletionsModel(
        model = MODEL_NAME,
        openai_client=external_client, #connect external cient with OpenAI client
    )

# making context object: which will be shown to LLM as apart of instructions (LLM Context)
@dataclass
class UserInfo:
    name: str
    id: int


#Function to dynamically create personalized LLM instructtions 

def dynamic_instruction(run_context:RunContextWrapper[UserInfo], agent:Agent) -> str:
    user_info: UserInfo = run_context.context

    #llm see this return instructions and personalized answer acordinglly
    return f"You are assisting {user_info.name}. Always personalized answers for user {user_info.name} ({user_info.id})"

#create context object
async def main():
    user_info = UserInfo(name="Jahan", id=123)

    agent = Agent[UserInfo](
        name= "User Information",
        instructions=dynamic_instruction,
        model=model,
        )

    result = await Runner.run(starting_agent=agent, input="recommend a book in Historical Fiction", context= user_info) 

    print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())