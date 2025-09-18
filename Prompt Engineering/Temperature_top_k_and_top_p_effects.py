# Prompt Engineering:

# Prompt Engineering means giving clear instructions to an AI (like GPT-4) so it gives you the answer you want. It’s like telling the AI exactly what to do, so it doesn’t give vague or wrong answers.
#Example:

#If you say, “Tell me a story,” the AI might give something random.
#But if you say, “Write a 100-word story for kids about a lion in a jungle,” you get a clear, useful story.

#Why It’s Important:

#Helps AI give the right answer (facts, fun, or steps).
#Stops wrong or unsafe answers.
#Keeps sensitive info (like names or passwords) safe.

# Some techniques of Prompt Engineering are below:



#Temperature, Top_k, and Top_p Effects
#These settings control how the AI answers—serious or creative.

#-----------------------------------------------------------------------------#



from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, ModelSettings

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

#Temperature: Controls how random the answer is.

#Low (0.2-0.5): Serious, exact answers.
#High (0.8-1.0): Fun, creative answers.

agentTemperature = Agent(
    name="Temperature",
    instructions="You are helpful math tutor",
    model=model,
    model_settings=ModelSettings(
        temperature=0.9, # focused or precise answer bcx Low temperature makes the AI give simple, correct answers
    )
)

#---------------------------------------#

#Top_k: Decides how many word choices the AI picks from.

# Small (10): Simple, focused answers.
# Big (50): More varied answers.
#High top_k lets the AI use more words, so answers are more fun.

agentTopK = Agent(
    name="Top K",
    instructions="You are helpful assistant.",
    model=model,
    model_settings=ModelSettings(
        top_k= 40, 
    )
)

#-------------------------------------------# 

#Top_p: Picks from a small set of likely words.

# Low (0.1): Predictable answers.
# High (0.9): More varied answers.

agentTopP = Agent(
    name="Top P",
    instructions="You are helpful assistant",
    model=model,
    model_settings=ModelSettings(
        top_p=0.7, #top_p must be in the range [0.0, 1.0]
    )
)
result1 = Runner.run_sync(agentTemperature, "Solve 5 + 2 * 3 + 8")
print("Temperature Effect Answer:",result1.final_output)

result2 = Runner.run_sync(agentTopP, "Solve 5 + 2 * 3 + 8")
print("Top P Effect Answer:",result2.final_output)

result3 = Runner.run_sync(agentTopK, "Write a short sentence about the moon")
print("Top K Effect Answer:",result3.final_output)