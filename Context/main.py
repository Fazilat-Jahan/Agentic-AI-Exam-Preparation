# Context: means give extra information to your agent so that tools and hooks take extra data and llm /agent runs do consistency, and in every run attach specific data.

#There are two types of context

# Local context: it is just for code not sent to LLM like 
# name, id, dependencies, helper function, it will run through RunContextWrapper to the tools

# LLM Context: it is which show to the LLM when generates response, it is just in conversation history. it will add in 
#agent instructions, in input message, in retrivel/web search, when tool exposes

# Suppose you have coustomer support bot
# the user id, plan text and logger object for backend work it all use in local context
# the username is Jahan and she is on premium plan use for generate respose from LLM


from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, function_tool, RunContextWrapper
#importing classes from agents module like,
# Agent: to create AI agent
# Runner: to run agent task 
# AsyncOpenAI: to connect with external openai comaptible API
# OpenAIChatCompletionsModel: to define which LLM model the agent will use
# function_tool: to convert a normal Python function into a tool that agents can call

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

# making context object: which is just for python backend not for sending to LLM
@dataclass
class UserInfo:
    name: str
    id: int

# a tool which use context
@function_tool
def fetch_username(
    #in this tool use wrapper which always pass Run Context Wrapper which have context
    wrapper: RunContextWrapper[UserInfo]) -> str:
    """Fetch the name of the user"""
    #through wrapper.context we access UserInfo object

    return f"The user {wrapper.context.name}'s id is {wrapper.context.id}"


#create context object
async def main():
    user_info = UserInfo(name="Jahan", id=123)

    agent = Agent[UserInfo](
        name= "User Information",
        tools=[fetch_username],
        model=model
    )

    result = await Runner.run(starting_agent=agent, input="What is the name of user name", context= user_info) #this is local context

    print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())