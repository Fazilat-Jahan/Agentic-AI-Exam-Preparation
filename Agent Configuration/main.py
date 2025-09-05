#Think like you are creating a digital Helper Agent who will help you in your daily tasks
#so you decide that 

# What its name will be
# What it will do for you (instructions / behavior)
# Which LLM model it will use
# What will be the format of its response
# Which tools it can use

# (Advanced) How it handles context or dependencies
# (Advanced) Whether outputs should be structured (JSON, list, etc.)
# (Advanced) How instructions can change at runtime
# (Advanced) Whether it collaborates with other agents (handoffs, manager patterns)
# (Advanced) How to observe lifecycle events (hooks)
# (Advanced) How to validate input/output (guardrails)
# (Advanced) How to clone/copy an agent
# (Advanced) Rules for tool usage (forcing tool use, tool use behavior)

# This whole setup is called Agent Configuration
# which means the Agent’s Profile, Abilities, and Rules.

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
    #basic Configuration of the agent
    name= "Math Helper",  # Name of the agent
    instructions= "You are a friendly math helper who give answer in easy way with lilbit description.",  #Behavior of the agent
    model=model, #which model the agent will use
    tools=[], #tools that the agent can use (right now it's empty)
)

# Given task to agent
result = Runner.run_sync(agent, "What is the sum of 2 + 2.5.")  # Running the agent with a task
# run_sync: for synchronous execution, means the agent waits until the LLM generates the full response

print(result.final_output) #printing the agents final response


#Advance Configuration of the agent 

#This outline will be expanded later, with each topic explained in detail and implemented with examples.


#Context = inject state or dependencies
#Output-type = get structured output instead of plain text (list, json, etc)
#Dynamic instructions = change instructions on runtime
#Multi agent patterns (Handsoff, manager(agents as tool))
#hooks =observe lifecycle events
#Guardrails = validation for input/output
#Clone = copy of an agent
#Forcing tool use = control whether tools must be used or not 
#Tool use behavior = define how tools are used
