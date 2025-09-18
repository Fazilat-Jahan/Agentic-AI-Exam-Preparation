# Tree of Thoughts 

# Tree of Thoughts means the AI doesn’t just think one way.
# It tries many small ideas (like branches of a tree).
# Then it checks which idea is good or bad.
# At the end, it chooses the best idea and gives the answer.


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

agentTree = Agent(
    name="Tree of Thoughts",
    instructions=(
        "You are a smart helper. "
        "When solving problems, do not give only one thought. "
        "Think like a tree: make many small ideas, check which ones are good, "
        "then choose the best path and give the final answer."
    ),
    model=model,
)

# Run it
result = Runner.run_sync(agentTree, "I want to plan my weekend. I can read, watch a movie, or go for a walk. What should I do?")
print("Tree of Thoughts Answer:", result.final_output)