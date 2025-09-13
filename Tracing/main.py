#Tracing: It is abuilt-in feature in openai agent sdk, who record important events, when agent run,it shown workflow, like LLM Generations, Function Tool call, handsoff , guardrails, custom events.

#By default , tracing is on. You can see the whole workflow on openai dashboard.
#if you want to disable tracing, write
#config=RunConfig(tracing_disabled=True) 

#Traces Vs Span:

#Traces: a one trace is a full workflow record like:
#workflow_name: by deafult it name is Agent_Workflow
#trace_id: auto generated unique id
#group_id: multiple traces from the same conversation
#metadata: custom info for debugging (optional)

#Spans: is a parts of traces means a small record of a operation
#Inside traces, a multiple spans are there.
#Every span captured a specific action like:

#agent-span (start-at, end-at timestamps): when agent run
#generation-span: when llm generate repsonse
#function-span: when tool calling
#guardrail-span: when guardrail run
#handoff-span: when a agent give control to another agent
#transcription-span: use to audio inputs(speech to text)
#speech-span:  use for audio outputs(text to speech)


#every span has a parent id, so it make in hierarchy.
#Runner.run always make trace

#Multi run traces(Highr level traces): when two run in one agent

#Note: You can control your traces because sometimes sensitive data can captured
#RunConfig.trace_include_sensitive_data = False


from agents import set_tracing_export_api_key, Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, trace

#importing classes from agents module like,
# Agent: to create AI agent
# Runner: to run agent task 
# AsyncOpenAI: to connect with external openai comaptible API
# OpenAIChatCompletionsModel: to define which LLM model the agent will use
# Trace: to trace workflow
# custom-Span: to create custom span
# set_tracing_export_api_key: to explicity show cutom span on dashboard



import os # importing os to access environment variables
from dotenv import load_dotenv

load_dotenv()
# load_dotenv()  # Load environment variables from a .env file

tracing_api_key = os.environ["OPENAI_API_KEY"]
set_tracing_export_api_key(tracing_api_key)

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

faq_agent= Agent(
    name= "FAQ Agent",
    instructions="Answer only product-related frequently asked questions.",
    model=model
)

support_agent = Agent(
    name = "Support Agent",
    instructions="Politely tell the user that only product-related queries are allowed.",
    model=model
)

# Trace Example:

#Trace 1 - Simple Trace (Single run)
#single querey will handle 
with trace("Single Trace workflow"):
    faq_result = Runner.run_sync(faq_agent, "What is Refund policy")
    print("FAQ Response: ",faq_result.final_output)
    #this will create agent span and generation span

# Trace 2- Multi Tracing (Higher Level Traces)

with trace("Multi Trace Workflow"):
    #first span
    faq_result = Runner.run_sync(faq_agent, "Tell me the joke")
    print("FAQ Response: ",faq_result.final_output)
    #second span
    support_result = Runner.run_sync(support_agent, f" User Asked {faq_result.final_output}")
    print("Support Response: ",support_result.final_output)    
    #it will create two individual agent span and generation in one trace


