# main.py
from flask import Flask, request
from chat import process_message

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        sender = request.form.get("From", "UnknownUser")
        incoming_msg = request.form.get("Body", "")

        if not incoming_msg:
            return "No message received", 400

        # Process message through chat.py
        reply_text = process_message(sender, incoming_msg)

        # Log for debugging
        print(f"From {sender}: {incoming_msg}")
        print(f"Reply: {reply_text}")

        return reply_text, 200

    except Exception as e:
        print("Webhook Error:", e)
        return "Sorry, something went wrong while processing your message.", 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
