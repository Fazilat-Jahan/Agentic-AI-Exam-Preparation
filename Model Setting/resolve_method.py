
# Resolve Method:

# We use Model Settings & resolve() to control agent behavior, save cost, manage token usage,
# and dynamically adjust responses for different tasks.

# Use case: When using multiple agents or the same agent for different scenarios,
# sometimes we want short, precise responses, and sometimes long, detailed ones.
# Using the resolve() method allows us to merge settings dynamically, so we don't need
# to explicitly define model settings each time.
# For short responses, the base settings are used; for long responses, the merged settings are applied.

from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, RunHooks, RunContextWrapper, AgentHooks, function_tool, ModelSettings

#importing classes from agents module like,
# Agent: to create AI agent
# Runner: to run agent task 
# AsyncOpenAI: to connect with external openai comaptible API
# OpenAIChatCompletionsModel: to define which LLM model the agent will use



import os # importing os to access environment variables
from dotenv import load_dotenv
import asyncio

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

@function_tool
def math(operations: str) -> str:
    """
    Simple math calculator tool.
    operation: String jaise '2 + 3' or '5 * 4'
    """
    result = eval(operations)
    return f"result:  {result}"


base_Settings = ModelSettings(
    temperature= 0.1,
    max_tokens=50,
    tool_choice="auto",
) 

override_Settings= ModelSettings(
    temperature=0.7,
    max_tokens=100,
    tool_choice="required",
)

# merge both setting by using resolve() method
final_settings = base_Settings.resolve(override_Settings)


agent = Agent(
    name="Math Tutor",
    instructions="You are helpful math tutor, who willl solve math problem with details like how this answer solve",
    model=model,
    tools=[math],
    model_settings = final_settings
)

result = Runner.run_sync(agent, "Solve 5 + 2 * 3 + 8")
print(result.final_output)