# Chain-of-Thought Prompting:

#(CoT) prompting makes the AI show its reasoning step by step before giving the final answer.
# It’s very useful for math, logic, and multi-step problems, because instead of only giving the result, the model explains how it solved the problem.

from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel

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

agent = Agent(
    name="CoT Math Tutor",
    instructions="You are a math tutor. Solve each problem step by step in detail. At the end, write 'Final:' with the answer.",
    model=model,
)

result = Runner.run_sync(agent, "If a pen costs 7 and I buy 5 pens, how much total?")
print(result.final_output)