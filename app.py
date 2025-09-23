from flask import Flask, request
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
        return "No sentence provided", 400

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Translate English to Turkish. Sadece çeviriyi yaz, başka bir şey ekleme."},
                {"role": "user", "content": sentence}
            ]
        )
        translation = response.choices[0].message.content.strip()
        translation = translation.replace("_", " ")  # alt çizgileri boşluğa çevir

        return translation  # JSON değil, düz metin
    except Exception as e:
        return f"Error: {str(e)}", 500
