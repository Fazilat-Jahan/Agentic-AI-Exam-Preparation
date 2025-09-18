# Model setting: is a analogy of controlling Agent brain like behavior means you will adjust/customize the llm response
# it is a class which hold configuration
#like
# Temperature : How much Agent creative and focused
# Tool Choice: Can agent use extra tools(auto, required,none)
# Max Token: Response Length limit


from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, function_tool, ModelSettings

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
agent = Agent(
    name="Math Tutor",
    instructions="You are helpful math tutor, who willl solve math problem with details like how this answer solve",
    model=model,
    tools=[math],
    model_settings=ModelSettings(
        temperature=1.9, # focused or precise answer (can increase)
        max_tokens=1000, # response max limit (increase how much you want response)
        tool_choice="auto", #agent will decide to call tool or not, if it is required so llm go with tool, if none so no tool call

    )
)

result = Runner.run_sync(agent, "Solve 5 + 2 * 3 + 8")
print(result.final_output)

