from flask import Flask, render_template, request, jsonify
from openai import OpenAI
from dotenv import load_dotenv
import os
import requests
load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)
MAKE_WEBHOOK = "https://hook.eu1.make.com/lx5cyj1vave3t6ggi04dec4e39hcywg8"
app = Flask(__name__)


# ---------------- HOME ----------------
@app.route("/")
def home():
     return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)

# ---------------- SUMMARY (DIFFICULTY) ----------------
@app.route("/summary", methods=["POST"])
def summary():

    data = request.get_json()
    notes = data["notes"]
    level = data.get("level", "medium")

    response = client.chat.completions.create(
        model="meta-llama/llama-3.1-8b-instruct",
        messages=[
            {
                "role": "user",
                "content": f"""
Summarize these notes in {level} difficulty:

- easy = simple language
- medium = exam level
- hard = deep technical explanation

Notes:
{notes}
"""
            }
        ]
    )

    summary = response.choices[0].message.content
    requests.post(
    MAKE_WEBHOOK,
    json={
        "feature": "Summary",
        "difficulty": level,
        "notes": notes,
        "output": summary,
        "question": ""
    }
)
    return jsonify({"summary": summary})


# ---------------- QUESTIONS ----------------
@app.route("/questions", methods=["POST"])
def questions():

    data = request.get_json()
    notes = data["notes"]

    response = client.chat.completions.create(
        model="meta-llama/llama-3.1-8b-instruct",
        messages=[
            {
                "role": "user",
                "content": f"Create 5 exam questions with answers from these notes:\n\n{notes}"
            }
        ]
    )

    result = response.choices[0].message.content
    requests.post(
    MAKE_WEBHOOK,
    json={
        "feature": "Questions",
        "difficulty": "",
        "notes": notes,
        "output": result,
        "question": ""
    }
)
    return jsonify({"questions": result})


# ---------------- FLASHCARDS ----------------
@app.route("/flashcards", methods=["POST"])
def flashcards():

    data = request.get_json()
    notes = data["notes"]

    response = client.chat.completions.create(
        model="meta-llama/llama-3.1-8b-instruct",
        messages=[
            {
                "role": "user",
                "content": f"""
Create flashcards from these notes.

Format:
Q: question
A: answer

Notes:
{notes}
"""
            }
        ]
    )

    result = response.choices[0].message.content
    requests.post(
    MAKE_WEBHOOK,
    json={
        "feature": "Flashcards",
        "difficulty": "",
        "notes": notes,
        "output": result,
        "question": ""
    }
)
    return jsonify({"flashcards": result})


# ---------------- CHAT ----------------
@app.route("/ask", methods=["POST"])
def ask():

    data = request.get_json()
    notes = data["notes"]
    question = data["question"]

    response = client.chat.completions.create(
        model="meta-llama/llama-3.1-8b-instruct",
        messages=[
            {
                "role": "user",
                "content": f"""
You are a study assistant.

Notes:
{notes}

Question:
{question}
"""
            }
        ]
    )

    answer = response.choices[0].message.content
    requests.post(
    MAKE_WEBHOOK,
    json={
        "feature": "Chat",
        "difficulty": "",
        "notes": notes,
        "output": answer,
        "question": question
    }
)
    return jsonify({"answer": answer})


# ---------------- RUN ----------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)