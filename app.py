from flask import Flask, render_template, request
from deep_translator import GoogleTranslator

app = Flask(__name__)

LANGUAGES = GoogleTranslator().get_supported_languages(as_dict=True)

@app.route("/", methods=["GET", "POST"])
def home():

    translated = ""
    text = ""
    source = "auto"
    target = "es"

    if request.method == "POST":

        text = request.form.get("text", "")
        source = request.form.get("source", "auto")
        target = request.form.get("target", "es")

        try:
            translated = GoogleTranslator(
                source=source,
                target=target
            ).translate(text)

        except Exception as e:
            translated = f"Error: {e}"

    return render_template(
        "index.html",
        translated=translated,
        text=text,
        source=source,
        target=target,
        languages=LANGUAGES
    )


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=7200,
        debug=True
    )