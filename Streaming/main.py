#Streaming: is like when an Agent run, that progress/ response will generate partially means in chunks instead of waiting full repsonse. It is mainly improve UX, a person can feel ttyping progress.

#Types of Streaming:

#Raw Response Events: It genereate token by token response means word by word answer just like Chatgpt typing effect

#Run Items Events and Agents Events: It is a higher level updates means it only show step by step progress like a tool call, tool give output, when handoff run and so on.

# Use Case: 
# If you want the typing effect means word by word answer use Raw Response Events but,
# If you want to see the step by step progress so use Run Items Events and Agents Events

from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, function_tool, ItemHelpers
#importing classes from agents module like,
# Agent: to create AI agent
# Runner: to run agent task 
# AsyncOpenAI: to connect with external openai comaptible API
# OpenAIChatCompletionsModel: to define which LLM model the agent will use

from openai.types.responses import ResponseTextDeltaEvent
import asyncio
import random


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

# Raw Response Events:

async def main():
     agent = Agent(
         name="Poetry Agent",
         instructions="You are helpful assistant",
         model=model
     )
     result = Runner.run_streamed(agent, "please give five different poetry of Allama Iqbal in Roman Urdu") #run_streamed will give output in streaming mode

     #events: each update from the agent(token,tool call, message)
     async for event in result.stream_events(): #result.stream_events:give events one by one

                            #raw_response_event: LLM send small chunk texts
        if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent): #ResponseTextDeltaEvent: represnt one small text piece(token) from LLM

            print(event.data.delta, end= "", flush=True) #.delta: newly generated texts

     # whole logic: 
     # Loop listens for streaming events
     # if response comes in chunks 
     # it prints each chunk immediately.
     # this repeat the same process untill full response complete, 
     # so that it look like the answer is being generated word by word    

if __name__ == "__main__":
    asyncio.run(main())

#-------------------------------------------------------------------------------------#


# Run Items Events and Agents events

@function_tool
def how_many_poetry()-> int:
    return random.randint(1, 10)

async def main():
    agent = Agent(
        name="Poet",
        instructions="First call the `how_many_poetry` tool, then write poetry of Allama Iqbal.",
        model= model,
        tools=[how_many_poetry]
    )

    result = Runner.run_streamed(agent, "Greetings")

    async for event in result.stream_events():
        if event.type == "raw_response_event": 
            continue 
        # chunks will ignore here


        #if agent updated
        elif event.type == "agent_updated_stream_event": #when agent changes to new agent
            print(f"Agent updated stream event: {event.new_agent.name}")

        elif event.type == "run_item_stream_event":  #steps updated 

            if event.item.type == "tool_call_item": #agent decide to call tool
                print("Tool Called")

            elif event.item.type == "tool_call_output_item": #tool finish running and return output
                print(f"Tool Output: {event.item.output}")  

            elif event.item.type == "message_output_item":
                print(f"Message Output: {ItemHelpers.text_message_output(event.item)}")  #final output

            else:
                pass

# Whole Logic:
# Agent runs in streaming mode
# Chunks will ignore(low level text)
# Big steps happens: Tool called, tool give output, agent change
# This way you do not see word by word response but you will see whole steps of how agent update

if __name__ == "__main__":
    asyncio.run(main())