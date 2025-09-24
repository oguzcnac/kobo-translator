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
                {
                    "role": "system",
                    "content": (
                        "You are a translation assistant. "
                        "Translate the English sentence into natural Turkish. "
                        "If the sentence contains idioms, cultural references, or figurative speech, "
                        "explain their meaning in Turkish after the translation. "
                        "Output format:\n\n"
                        "Çeviri: <Türkçe çeviri>\n"
                        "Açıklama: <Kısa açıklama (gerekirse)>"
                    )
                },
                {"role": "user", "content": sentence}
            ]
        )
        result = response.choices[0].message.content.strip()
        return result
    except Exception as e:
        return f"Error: {str(e)}", 500
