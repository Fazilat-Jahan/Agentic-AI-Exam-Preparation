# Streaming 

This folder contains examples that demonstrate **how streaming works** in the Agents 

---

## 📂 Files Overview

### 1. Raw Response Streaming (word-by-word)
- Shows how to stream responses **token-by-token** (like ChatGPT typing).
- Uses `raw_response_event` with `ResponseTextDeltaEvent`.
- Inline explanations included.
- Use case: when you want the **typing effect** (word-by-word output).

### 2. Run-Item & Agent Events Streaming (step-by-step)
- Shows higher-level updates instead of raw tokens.
- Includes:
  - Agent updated (`agent_updated_stream_event`)
  - Tool called (`tool_call_item`)
  - Tool output (`tool_call_output_item`)
  - Message output (`message_output_item`)
- Inline explanations included.
- Use case: when you want to track **agent progress step-by-step** (tool calls, outputs, handoffs, etc.).

---

## ⚙️ How It Works
- **Streaming**: Agent output comes in parts (chunks or events) instead of waiting for the full response.
- **Two main styles:**
  1. **Raw Response Events** → word-by-word response.
  2. **Run-Item/Agent Events** → structured step updates.

---

## 🛠 How to Learn from These Files
1. Read the inline explanations in `main.py` file.
2. Run the scripts and observe:
   - Raw token stream → looks like continuous typing.
   - Run-item events → shows tool usage & step updates.
3. Play with the code:
   - Change model or prompt.
   - Add your own tools.
   - Watch how the streaming updates change.

👉 The goal is to experiment, break things, and understand how streaming really works.
