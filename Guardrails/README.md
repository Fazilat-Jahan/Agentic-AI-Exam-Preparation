# 🚦 Guardrail – Input & Output

This contains two files that demonstrate how to use guardrails with agents:

- **`input_guardrail.py`** → Example where guardrail checks **before sending query to agent**  
- **`output_guardrail.py`** → Example where guardrail checks **after agent generates output**

---

## 📂 File Explanations

### 1. `input_guardrail.py`
- Shows how to block or allow queries **before** they reach the main agent.  
- Code has **inline explanations** for each line.  
- Useful when you want to **filter bad/irrelevant inputs** (e.g., math question when only customer-support queries are allowed).  

---

### 2. `output_guardrail.py`
- Shows how to validate agent’s **response** before sending it back to the user.  
- Code has **inline comments** explaining each step.  
- Useful when you want to **double-check agent answers** for correctness, safety, or policy compliance.  

---

## 🛠 How to Learn from These Files

1. **First, read the code with inline explanations** — don’t just run it.  
2. Understand the flow:  
   - Where the guardrail agent is defined  
   - How `GuardrailFunctionOutput` is returned  
   - Why exceptions (`TripwireTriggered`) are raised  
3. **Play with code**:  
   - Change queries in code (try math, support, random jokes).  
   - Adjust guardrail instructions and see how behavior changes.  

---

👉 **Note:** The goal is to **experiment, break, and fix it**. That’s how you’ll really understand how guardrails work.
