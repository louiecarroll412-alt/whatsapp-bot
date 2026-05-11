import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

ACCESS_TOKEN = "YOUR_ACCESS_TOKEN"
PHONE_NUMBER_ID = "YOUR_PHONE_NUMBER_ID"
VERIFY_TOKEN = "YOUR_VERIFY_TOKEN"

@app.route("/webhook", methods=["GET", "POST"])
def webhook():

    if request.method == "GET":
        mode = request.args.get("hub.mode")
        token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")

        if mode == "subscribe" and token == VERIFY_TOKEN:
            return challenge, 200
        return "Verification failed", 403

    data = request.get_json()

    if data.get("object") == "whatsapp_business_account":
        for entry in data.get("entry", []):
            for change in entry.get("changes", []):
                value = change.get("value")

                if "messages" in value:
                    message = value["messages"][0]
                    sender_id = message["from"]

                    if message.get("type") == "text":
                        text = message["text"]["body"]
                        send_text(sender_id, f"You said: {text}")

    return jsonify({"status": "ok"}), 200


def send_text(to_number, text):
    url = f"https://graph.facebook.com/v18.0/{PHONE_NUMBER_ID}/messages"

    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "messaging_product": "whatsapp",
        "to": to_number,
        "type": "text",
        "text": {"body": text}
    }

    response = requests.post(url, json=payload, headers=headers)
    return response.json()


if __name__ == "__main__":
    app.run(port=5000)