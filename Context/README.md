# Context 

This folder contains two files that demonstrate how to use **context** with agents:

- **LocalContext.py** → where context is only used locally (backend-only, hidden from LLM).  
- **LLMContext.py** → where context is shared with the LLM (instructions/system prompt, visible to LLM).  

---

## 📂 File Explanations  

### 1. LocalContext.py  
- Shows how to pass extra data (like user info, IDs, or dependencies) to tools and hooks.  
- Code has inline explanations for each step.  
- Useful when you want to **keep sensitive data safe** (not visible to LLM).  
- Example: A customer-support bot can fetch the user’s email or ID from a database but only show the **plan name** to the LLM.  

### 2. LLMContext.py  
- Demonstrates how to expose context directly to the LLM.  
- Achieved through **dynamic instructions** (system prompts) or conversation history.  
- Useful for **personalization** (e.g., greeting user by name, remembering past queries).  
- Example: “Hey Jahan! Last time you asked about your subscription…”  

---

## 🛠 How to Learn from These Files  

1. Read the code with inline explanations — don’t just run it.  
2. Understand the flow:  
   - Where the context object is defined  
   - How local context is passed with `RunContextWrapper`  
   - How LLM context is injected with dynamic instructions  
3. Play with code:  
   - Change values in `UserInfo` (name, id, email).  
   - Add more instructions for LLM context.  
   - Test what data stays hidden vs what the LLM actually sees.  

---

## 🔑 Key Difference  

- **Local Context** → stays hidden from LLM (backend-only, safe).  
- **LLM Context** → becomes part of the conversation history (LLM can see it, so personalization/instructions work).  
