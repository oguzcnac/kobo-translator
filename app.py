from flask import Flask, request
import os
from openai import OpenAI

app = Flask(__name__)

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

@app.route("/translate")
def translate():
    sentence = request.args.get("s")
    if not sentence:
        return "Eksik parametre: s", 400

    prompt = f'Translate this English sentence into Turkish. Output only the translation:\n\n"{sentence}"'

    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role":"user","content":prompt}],
        max_tokens=200
    )

    return resp.choices[0].message.content.strip()
