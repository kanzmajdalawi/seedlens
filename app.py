import os
from flask import Flask, render_template, request, jsonify, session
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.urandom(24)

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def load_prompt():
    with open("prompt.txt", "r") as f:
        return f.read()

@app.route("/")
def index():
    session.clear()
    return render_template("index.html")

@app.route("/results")
def results():
    return render_template("results.html")

@app.route("/evaluate", methods=["POST"])
def evaluate():
    data = request.get_json()
    description = data.get("description", "")

    if not description.strip():
        return jsonify({"error": "No description provided"}), 400

    system_prompt = load_prompt()

    conversation_history = [
        {
            "role": "user",
            "content": f"Please evaluate this startup:\n\n{description}"
        }
    ]

    response = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=2000,
        system=system_prompt,
        messages=conversation_history
    )

    assistant_message = response.content[0].text

    conversation_history.append({
        "role": "assistant",
        "content": assistant_message
    })

    session["history"] = conversation_history
    session["description"] = description

    return jsonify({
        "response": assistant_message,
        "history": conversation_history
    })

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")

    if not user_message.strip():
        return jsonify({"error": "No message provided"}), 400

    system_prompt = load_prompt()

    history = session.get("history", [])

    history.append({
        "role": "user",
        "content": user_message
    })

    response = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=2000,
        system=system_prompt,
        messages=history
    )

    assistant_message = response.content[0].text

    history.append({
        "role": "assistant",
        "content": assistant_message
    })

    session["history"] = history

    return jsonify({
        "response": assistant_message,
        "history": history
    })

@app.route("/save", methods=["POST"])
def save():
    history = session.get("history", [])
    description = session.get("description", "")

    if not history:
        return jsonify({"error": "No session to save"}), 400

    report_lines = []
    report_lines.append("=" * 50)
    report_lines.append("VERDIKT SESSION REPORT")
    report_lines.append("=" * 50)
    report_lines.append("")
    report_lines.append(f"STARTUP:\n{description}")
    report_lines.append("")

    for msg in history:
        role = "FOUNDER" if msg["role"] == "user" else "VERDIKT"
        report_lines.append(f"{role}:\n{msg['content']}")
        report_lines.append("")

    report_text = "\n".join(report_lines)

    return jsonify({"report": report_text})

@app.route("/reset", methods=["POST"])
def reset():
    session.clear()
    return jsonify({"status": "reset"})

if __name__ == "__main__":
    app.run(debug=True, port=5001)
    