# chat.py
import os
import openai

# Hardcode or use env variable for testing
openai.api_key = os.getenv("OPENAI_API_KEY") or "YOUR_OPENAI_KEY_HERE"

# Keep a simple in-memory session store per user
user_sessions = {}

SYSTEM_PROMPT = """
You are 'GlamCut AI', a friendly and professional salon booking assistant.
Your only job is to help clients book, confirm, or reschedule haircut appointments.

Rules:
- Always greet warmly if it’s the first message.
- If the user says 'yes please', treat it as confirmation of booking.
- Understand relative dates like 'tomorrow', 'next Friday', or 'this weekend'.
- If the user says 'thank you', respond politely but do not rebook.
- Never talk about topics outside salon services.
- Keep replies short, friendly, and professional.
"""

def process_message(sender, incoming_msg):
    # Initialize session history if first message
    if sender not in user_sessions:
        user_sessions[sender] = []

    # Build conversation for GPT
    conversation = [
        {"role": "system", "content": SYSTEM_PROMPT},
        *user_sessions[sender],
        {"role": "user", "content": incoming_msg}
    ]

    try:
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=conversation,
            temperature=0.7,
            max_tokens=300
        )

        assistant_reply = response.choices[0].message.content.strip()

        # Save conversation history
        user_sessions[sender].append({"role": "user", "content": incoming_msg})
        user_sessions[sender].append({"role": "assistant", "content": assistant_reply})

        return assistant_reply

    except Exception as e:
        print("OpenAI Error:", e)
        return "Sorry, something went wrong while processing your message."


# For testing without Flask
if __name__ == "__main__":
    sender = "TestUser"
    while True:
        msg = input("You: ")
        if msg.lower() in ["exit", "quit"]:
            break
        reply = process_message(sender, msg)
        print("GlamCut AI:", reply)
