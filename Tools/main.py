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
#   Example: FileSearchTool , CodeInterpreterTool, WebSearchTool etc

#4. Agent as Tool -
#   This allows you to use an agent as a tool, so one agent can call another agent
#   without handing off control. The main agent stays in charge.
#   Example: A "Customer Service Agent" using a "Booking Agent" as a tool,
#   but still keeping control of the conversation.



from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, function_tool, WebSearchTool
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

#--------------------------------------------------------------------------------#

#2. API Based Tools -
#   These tools call an external API to get fresh data.
#   Example: Weather API, News API, Stock Price API etc.

import requests  # to make API calls
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY") #loading from .env file
# WeatherAPI.com tool
@function_tool
def getWeather(city: str) -> str:
    """Fetch the weather for a given location.

    Args:
        location: The location to fetch the weather for.
    """
    
    url = f"http://api.weatherapi.com/v1/current.json?key={WEATHER_API_KEY}&q={city}&aqi=no"
    response = requests.get(url)

    if response.status_code != 200:
        return f"❌ Could not fetch weather for {city}."

    data = response.json()
    temp = data["current"]["temp_c"]  
    desc = data["current"]["condition"]["text"]  
    return f"🌦️ Weather in {city}: {temp}°C, {desc}."


agent = Agent(
    name="WeatherAgent",
    instructions="You are a helpful weather agent. You can provide current weather information for any city using the weather tool.",
    tools= [getWeather], #adding API based tool
    model=model,
)


result = Runner.run_sync(agent, "What is the current weather in Karachi?")
print("API Based Tool Answer: ",result.final_output)

#--------------------------------------------------------------------------------#

#3. Hosted Tools -
#   These tools are already hosted on a server (by OpenAI).
#   They are used for searching, browsing, or analyzing.
#   Example: FileSearchTool , CodeInterpreterTool, WebSearchTool etc.

#👉 Hosted tools are not available with Gemini as of now.
#because it is builtin tool provided by OpenAI, and Gemini is developed by Google.

#Note: The biggest advantage of using Hosted Tools that you do not create a function or API call for the tool. You just import the tool from agents module and add it to your agent.
agent = Agent(
    name="HostedToolAgent",
    instructions="You are a helpful agent that can get someone details from LinkedIn using the web search tool.",
    tools=[WebSearchTool()], #add hosted tool
    model=model,
)

result = Runner.run_sync(agent, "Find the details about Fazilat Jahan Web Developer from LinkedIn.")
print("Hosted Tool Answer: ", result.final_output)

#--------------------------------------------------------------------------------#

#4. Agent as Tool -
#   This allows you to use an agent as a tool, so one agent can call another agent
#   without handing off control. The main agent stays in charge.
#   Example: A "Doctor Agent" using a "Specialist Agent" as a tool,
#   but still keeping control of the conversation.

# Define a Specialist Agent (e.g., Dermatologist)
dermatologist_agent = Agent(
    name="DermatologistAgent",
    instructions="You are a dermatologist. You give advice about skin issues like acne, rashes, or sunburn.",
    model=model,
)

# Define a General Doctor Agent that can use the Dermatologist as a tool
doctor_agent = Agent(
    name="DoctorAgent",
    instructions="You are a general doctor. You can answer common health questions, "
                 "and if the problem is skin-related, you can use the Dermatologist Agent as a tool.",
    model=model,
    tools=[dermatologist_agent.as_tool(
        tool_name="Dermatologist",
        tool_description="Use this tool to get expert advice on skin-related issues."
    )],  # Agent as Tool
)

result = Runner.run_sync(doctor_agent, "I have red itchy spots on my skin. What should I do?")
print("Agent as Tool Answer: ", result.final_output)

#Note: Handoffs and Agent as tool seams similar but they are totally different.
#In handoffs, the DermatologistAgent would take full control, and the DoctorAgent would step back completely.
# In Agent as Tool: The DoctorAgent always stays in charge, calls the DermatologistAgent like a helper function, and then gives the final response back to the user.

#In short:

#Handoff → the specialist talks directly to the user.

#Agent as Tool → the main agent talks, using the specialist behind the scenes.