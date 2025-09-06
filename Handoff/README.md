# 🤝 Handoff

This shows how **handoff works** using the OpenAI Agents SDK.

Just open **main.py** where every line already has **inline explanation** in a very easy way.  

---

## How to Run

1. Run the script:

```bash
python main.py
````

2. Check the output:

   * You’ll see the **final reply** (what the agent answered).
   * You’ll also see the **last agent** (which specialist actually answered).

---

## 🎮 Play With the Code

Change the input in `main.py` and run again, then observe:

* Sometimes the **BaggageAgent** will take over.
* Sometimes the **ImmigrationAgent** will take over.
* Sometimes the **CustomerServiceAgent** will take over.

👉 This way you’ll *see with your own eyes* how **handoff switches control between agents**.

---

## Why Play?

Because that’s the easiest way to understand:

* How the **main agent** decides who to hand off to
* How **specialist agents** respond
* How the `last_agent` output tells you *who actually solved the query*

---

👀 So go check out `main.py`, run it, and play with different passenger queries.
That’s the best way to “feel” how handoff works.
