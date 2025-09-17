# Hooks

This folder contains files that demonstrate how to use **Hooks** in Agents SDK.  
Hooks intercept key events during an agent’s execution so you can log, monitor, or add custom logic.

## 📂 File Explanation
All demonstrations of hooks are in `main.py` with inline explanations.  
Examples include:

- **Run Hooks** → Monitor full run lifecycle (start, LLM call, errors, etc.)  
- **Agent Hooks** → Monitor a single agent’s actions (input received, tool start, tool end)  

## 🖥 How to Use
1. Run `main.py`.  
2. Observe console logs for:
   - Run events (start, LLM calls)  
   - Agent events (inputs, tool usage, results)  
3. Try editing prompts, adding tools, and attaching different hooks.  

## 🔍 What You’ll See
- `[Run Hook]` → Run-level logs  
- `[AgentHook]` → Agent-level logs  

## 💡 Tip
👉 Don’t just run it. Attach multiple agents, add more tools, and simulate errors.  
That’s the best way to understand how **RunHooks** vs **AgentHooks** work.
