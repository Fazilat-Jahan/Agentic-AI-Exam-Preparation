# Tracing

This folder contains files that demonstrate how to use **Tracing** in Agents SDK.  
Tracing records important events (**LLM calls, tool usage, handoffs, etc.**) and shows the workflow on the **OpenAI dashboard**.  

---

## 📂 File Explanation

- All demonstrations of tracing scenarios are in **`main.py`** with inline explanations.  
- Examples include:  
  - Single trace
  - Multi trace
  - Spans  
  - Disabling tracing for sensitive runs  

---

## 🖥 How to Use

1. Run `main.py`.  
2. Open the [OpenAI Dashboard](https://platform.openai.com) → check traces.  
3. Observe how different **spans** appear:  
   - Agent spans  
   - Generation spans  
   - Custom spans  

---

## 💡 Tip

👉 Don’t just run it. Change queries, add more spans, and break/rebuild.
That’s the best way to deeply understand how tracing works.