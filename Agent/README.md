# Build First Agent 🤖

This explains how to create and run an AI Agent using the **OpenAI Agents SDK** with Gemini LLM.  

---

## 🚀 Setup Steps

### 1. Initialize the project
```bash
uv init
````

### 2. Create a virtual environment

```bash
uv venv
```

### 3. Activate the virtual environment

```bash
# Windows
.venv\Scripts\activate

# macOS/Linux
source .venv/bin/activate
```

### 4. Install dependencies

```bash
# Install OpenAI Agents SDK
uv add openai-agents

# Install dotenv to load environment variables
pip install python-dotenv
```

### 5. Set environment variables

Create a `.env` file in the root directory and add the Gemini API key:

```
GEMINI_API_KEY=api_key_here
```

### 6. Run the agent

```bash
uv run main.py
```

---


## 🌐 Free vs Paid Usage

### Using Gemini (Free API Key)

* Works with the **Gemini API endpoint**
* Requires setting `GEMINI_API_KEY` in `.env`
* Example:

  ```python
  MODEL_NAME = "gemini-2.0-flash"
  GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
  base_url = "https://generativelanguage.googleapis.com/v1beta/openai/"
  ```

### Using OpenAI (Paid API Key)

* Works with the **OpenAI API endpoint**
* Requires setting `OPENAI_API_KEY` in `.env`
* Example:

  ```python
  MODEL_NAME = "gpt-4o"
  OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
  # No custom base_url needed (uses OpenAI directly)
  ```

👉 To switch between Gemini (free) and OpenAI (paid), update:

1. **API key reference** in `.env` (`GEMINI_API_KEY` → `OPENAI_API_KEY`)
2. **Model name** (`gemini-2.0-flash` → `gpt-4o` or other OpenAI model)
3. **base\_url** (use Gemini endpoint for free key, default OpenAI endpoint for paid key)

---

## ✅ Example Output

```
Why do programmers prefer dark mode?
Because light attracts bugs. 🐛
```

