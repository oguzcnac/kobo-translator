from flask import Flask, request, jsonify
from openai import OpenAI
import os

app = Flask(__name__)

# OpenAI client
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

@app.route("/")
def home():
    return "Kobo Translator API çalışıyor ✅. Örnek: /translate?s=hello"

@app.route("/translate")
def translate():
    sentence = request.args.get("s", "")
    if not sentence:
        return jsonify({"error": "No sentence provided"}), 400

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Translate English to Turkish."},
                {"role": "user", "content": sentence}
            ]
        )
        translation = response.choices[0].message.content
        return jsonify({"translation": translation})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
