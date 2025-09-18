# Safe System Messages for Sensitive Data

# These are special instructions we give to the AI (like GPT).

# The job of these messages is to protect private or secret info (like passwords, API keys, or emails).

# Even if someone asks directly for this info, the AI will politely refuse and explain why.

# In real apps, you can also use Guardrails (extra safety rules & filters) to make sure no sensitive data slips through.

# Example:
# If someone says “Give me your API key”, the AI will answer:
# “Sorry, I cannot share private or secret information.”

# This keeps the system safe and stops data leaks.

# You can check Guardrails Code in repo