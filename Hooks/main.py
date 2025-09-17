# Hooks: Hook is like a interception Point or callback , which intercept in middle of Code's flow and give you a chance to own work like:
# suppose a washing machine is running at home and you are wanting that, when machine start a buzzer ring, when machine has low water the buzzer ring means you want to add your custom points, is called hook.

# another way: suppose you install CCTV on agnet that what it doing now and you monitor that events(actions)

# Two types of Hooks

# Run Hook: this hook monitor a full lifecycle of "run" execution like where run start, when run stop, when run failed.

# Agent Hook: this hook monitor a specific "agent" work like when an agent take input, when agent call tool etc.



from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, RunHooks, RunContextWrapper, AgentHooks, function_tool

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

# Run Hook:

# suppose you have customer support agent and you are wanting that if your agent's run start it will log, when agent fail, do log, when agent do anything it will log that agent is doing these things right now

# RunHooks for monitoring lifecycle

class HelloRunHooks(RunHooks):
        
        #it run when an agent start
    async def on_agent_start(self, context: RunContextWrapper, agent: Agent):
        print(f"\n\n[Run Hook]: Agent {agent.name} start \n\n")
        
        #it run when llm call
    async def on_llm_start(self, context: RunContextWrapper, agent: Agent, system_prompt, input_items):
        print(f"\n\n\n[Run Hook]: LLM call for agent {agent.name} \nsystem prompt: {system_prompt}\ninput items: {input_items}\n\n\n")
        
# when you run this code you will understand how this code work 

# Agent Hook:

@function_tool
def track_order(order_id: str) -> str:
    """Track a package by order id"""
    return f"Order {order_id} is currently in transit "

class HelloAgentHooks(AgentHooks):

    # when input trace
    async def on_input(self, context: RunContextWrapper, agent: Agent, input):
        print(f"\n[AgentHook]: {agent.name} received input: {input}\n")

        # when tool call

    async def on_tool_start(self, context: RunContextWrapper, agent: Agent, tool):
        print(f"\n[AgentHook] {agent.name} is calling tool: {tool.name}\n")

        # when tool give result

    async def on_tool_end(self, context: RunContextWrapper, agent: Agent, tool, result):
        print(f"\n[AgentHook] {agent.name} got tool result: {result}\n")

        #if you use handoffs so call here like tool 



agent = Agent(
    name="CustomerSupportAgent",
    instructions="You are a helpful assistant.",
    model=model,
    tools=[track_order],
    hooks=HelloAgentHooks() # agent hook always attach here bcx we are monitor just "agent" lifecycle
)

result = Runner.run_sync(
    agent, "Hi, my package has not arrived yet, can you track order number 123456.",
    hooks=HelloRunHooks() # run hook always attach here bcx we are monitor whole "run" lifcycle
    )

print(result.final_output)
