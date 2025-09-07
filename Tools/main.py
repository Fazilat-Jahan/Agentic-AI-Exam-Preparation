#Tool: LLm can think and talk but for extra real task or live data, it needs to call tools. 
# Let's suppose you ask to agent about Dubai weather, an agent(LLM) may reply it's probably sunny or hot (hallucination), but for real accurate weather, agent needs to call a Weather tool which reply with live weather conditions of Dubai.

#There are several types of tools

#1. Function Tools -
#   These are simple Python functions that you define yourself.
#   Example: A calculator function, a CSV reader, etc.

#2. API Based Tools -
#   These tools call an external API to get fresh data.
#   Example: Weather API, News API, Stock Price API etc.

#3. Hosted Tools -
#   These tools are already hosted on a server (by OpenAI).
#   They are used for searching, browsing, or analyzing.
#   Example: file_search, code_interpreter, web_browser etc.

#4. Agent as Tool -
#   This allows you to use an agent as a tool, so one agent can call another agent
#   without handing off control. The main agent stays in charge.
#   Example: A "Customer Service Agent" using a "Booking Agent" as a tool,
#   but still keeping control of the conversation.



from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, function_tool
#importing classes from agents module like,
# Agent: to create AI agent
# Runner: to run agent task 
# AsyncOpenAI: to connect with external openai comaptible API
# OpenAIChatCompletionsModel: to define which LLM model the agent will use
# function_tool: to convert a normal Python function into a tool that agents can call


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

#1. Function Tools -
#   These are simple Python functions that you define yourself.
#   Example: A calculator function, a CSV reader, etc.


# Define a simple calculator tool
@function_tool #it is a decorator that registers Python function as a tool for the agent.
#simple python function to add two numbers
def calculator(a:int, b:int) -> int: 
    """A simple calculator that adds two numbers."""
    return a + b

agent = Agent(
    name="Calculator Agent",
    instructions="You are a helpful calculator agent. You can add two numbers using the calculator tool.",
    model=model,
    tools= [calculator], #adding function tool 
)

result = Runner.run_sync(agent, "What is 6 + 4")
print("Function Tool Answer: ",result.final_output)  

# 👉 Try the CSV Reader tool also to get more info about how function tools work.
#  Rest of the tool types will be discussed soon in detail.