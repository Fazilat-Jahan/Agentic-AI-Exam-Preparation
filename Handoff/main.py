# Handoff: A main agent transfers a task to a specialist agent for better handling and better results.
  
#Just like not every doctor can treat every disease, they transfer you to a specialist doctor according to your condition for better treatment. 
 
#Similarly, in AI agents, one agent cannot handle every task perfectly. So it hands off the task to a specialist agent to get better results and reduce hallucinations.


# In code, it literally switches control from one agent to another.
# In conversation, it feels like being transferred to the right person.

# Airport Check-in Handoff Example
# Goal: See how one agent (Check-in Agent) can hand off the conversation to a more specialized agent (like Baggage or Immigration etc).


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

#step1: Define Specialist Agents

# Specialist Agent for Baggage Issues
baggage_agent = Agent(
    name="BaggageAgent",
    instructions="You are a specialist in handling baggage issues. Assist the passenger with their issues like extra luggage, lost bags, etc.",
    model=model
)

# Specialist Agent for Immigration Issues

immigration_agent = Agent(
    name="ImmigrationAgent",
    instructions="You are a specialist in handling immigration issues. Assist the passenger with their visa, passport, and immigration-related questions.",
    model=model
)

# Specialist Agent for customer service queries
customer_service_agent = Agent(
    name="Customer Service Agent",
    instructions="You are a specialist in handling customer service issues. Assist the passenger with their upgrades, seat changes, and general customer support, etc.",
    model=model
)

#step2: Define Main Agent (Check-in Agent) that will handoff to specialist agents

checkin_agent = Agent(
    name="CheckInAgent",
    instructions="""
    You are a check-in agent at an airport. Your job is to assist passengers with their check-in process.
    If the passenger has baggage issues, hand off the conversation to the BaggageAgent.
    If the passenger has immigration issues, hand off the conversation to the ImmigrationAgent.
    For other issues, you can handle them yourself or hand off to the CustomerServiceAgent.
    """,
    model=model,
    #add specialist agents in handoffs parameter
    handoffs=[baggage_agent, immigration_agent, customer_service_agent]
)




# Given task to agent
result = Runner.run_sync(checkin_agent, "I have extra luggage, what should I do?")  # Running the agent with a task
# run_sync: for synchronous execution, means the agent waits until the LLM generates the full response

#result = Runner.run_sync(checkin_agent, 
#                        """"I have extra luggage, what should I do?,
#  My visa got expired, can I still board?,
# Can I upgrade my seat to business class?""") 

#try these different inputs to see how handoff works

print(result.final_output) #printing the agents final response

print("Last Agent", result.last_agent.name) #printing the last agent who actually answered

