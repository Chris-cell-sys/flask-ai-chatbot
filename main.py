from flask import Flask, render_template, request, jsonify, session
from flask_session import Session
from openai import OpenAI
import os

app = Flask(__name__)
app.secret_key = "titkoskulcs"
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

@app.route("/")
def home():
    if "messages" not in session:
        session["messages"] = [
            {"role": "system", "content": "Te egy barátságos magyar AI chatbot vagy."}
        ]
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_msg = request.json["message"]
    session["messages"].append({"role": "user", "content": user_msg})
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=session["messages"]
    )
    ai_reply = response.choices[0].message.content.strip()
    session["messages"].append({"role": "assistant", "content": ai_reply})
    session.modified = True
    return jsonify({"reply": ai_reply})

@app.route("/reset", methods=["POST"])
def reset():
    session["messages"] = [
        {"role": "system", "content": "Te egy barátságos magyar AI chatbot vagy."}
    ]
    return jsonify({"reply": "A beszélgetést töröltem. Kezdhetjük újra!"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT",8080)
    app.run(host="0.0.0.0", port=port)
