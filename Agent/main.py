# What is OpenAI Agents SDK ?
# Think like you want to build an AI app that works like a smart assistant, by using easy and lightweight coding/tools/framework.
# That's SDK (agents) basically gives you ready-made tools so that you can easily build your agentic AI app.
# Means you do not need to understand complex coding or deep technical stuff.
# OpenAI Agents SDK, helps you to create AI applications that can perform tasks on their own, like a personal assistant.


# Just What you need to understand core concepts of Agents SDK to build your own AI Agent are as follows:
# Agents: This is actually a AI brain which have LLM, Tools, Instructions
# Handsoff: An agent delegate tasks to other agents
# Guardrails: This is like a watchman who keep eyes on inputs/outputs for safety
# Sessions: This is like a memory bank which keeps track of conversations/history


# why we using this?
# 1. It has fewer features but works very powerful 
# 2. It has ability to directly turn Python functions into tools
# 3. It runs in looping like automatically call tools, send respond to LLM, until task is done
# 4. it has builtin Tracing to trace and visualize the flow of agent's actions on OpenAI dashboard.


# Installation: check in readme.md file


from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel
#importing classes from agents module like,
# Agent: to create AI agent
# Runner: to run agent task 
# AsyncOpenAI: to connect with external openai comaptible API
# OpenAIChatCompletionsModel: to define which LLM model the agent will use

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
# Define an Agent
agent     = Agent(
    name= "SimpleAgent",  # Name of the agent
    instructions= "You are a helpful assistant.",  # Instructions for the agent
    model=model
)

# Given task to agent
result = Runner.run_sync(agent, "Write a joke about programmers.")  # Running the agent with a task
# run_sync: for synchronous execution, means the agent waits until the LLM generates the full response

print(result.final_output) #printing the agents final response

