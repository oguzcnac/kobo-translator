from flask import Flask, request, render_template_string
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.orm import sessionmaker, declarative_base
import openai
import os

app = Flask(__name__)

# 🔹 OpenAI ayarı
openai.api_key = os.environ.get("OPENAI_API_KEY")

# 🔹 Database ayarı (Render'ın verdiği URL environment variable olarak eklenecek)
DATABASE_URL = os.environ.get("DATABASE_URL")
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
Base = declarative_base()

class Word(Base):
    __tablename__ = "words"
    id = Column(Integer, primary_key=True, autoincrement=True)
    book = Column(String(255))
    word = Column(String(255))
    sentence = Column(Text)
    translation = Column(Text)

Base.metadata.create_all(engine)

# 🔹 Çeviri yapan fonksiyon
def do_translation(sentence):
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Sen profesyonel bir çevirmen ve dil öğretmenisin."},
            {"role": "user", "content": f"Bu cümleyi Türkçeye çevir ve gerekiyorsa deyimleri veya özel anlamları açıklayarak yaz:\n\n{sentence}"}
        ]
    )
    return response.choices[0].message["content"]

# 🔹 books.txt’den kitapları oku
with open("books.txt", "r", encoding="utf-8") as f:
    books = [line.strip() for line in f if line.strip()]

# 🔹 Translate endpoint
@app.route("/translate", methods=["GET"])
def translate():
    sentence = request.args.get("s", "")
    translation = do_translation(sentence)
    words = sentence.split()

    form_template = """
    <h3>Çeviri & Açıklama:</h3>
    <p>{{ translation }}</p>
    <hr>
    <h4>Cümle: {{ sentence }}</h4>
    <form method="post" action="/save_word">
      <label>Kelime seç:</label>
      <select name="word">
        {% for w in words %}
          <option value="{{ w }}">{{ w }}</option>
        {% endfor %}
      </select><br><br>
      <label>Senin çevirin:</label>
      <input type="text" name="my_translation" required><br><br>
      <label>Kitap:</label>
      <select name="book">
        {% for b in books %}
          <option value="{{ b }}">{{ b }}</option>
        {% endfor %}
      </select><br><br>
      <input type="hidden" name="sentence" value="{{ sentence }}">
      <button type="submit">Kaydet</button>
    </form>
    """
    return render_template_string(form_template, translation=translation, sentence=sentence, words=words, books=books)

# 🔹 Save endpoint
@app.route("/save_word", methods=["POST"])
def save_word():
    book = request.form["book"]
    word = request.form["word"]
    sentence = request.form["sentence"]
    translation = request.form["my_translation"]

    session = Session()
    new_word = Word(book=book, word=word, sentence=sentence, translation=translation)
    session.add(new_word)
    session.commit()
    session.close()

    return "✅ Kelime kaydedildi!"

@app.route("/")
def index():
    return "Kobo Translator + Word Collector çalışıyor!"
