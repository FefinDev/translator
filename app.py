from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from deep_translator import GoogleTranslator
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = FastAPI()

app.mount(
    "/static",
    StaticFiles(directory=os.path.join(BASE_DIR, "static")),
    name="static"
)

templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

LANGUAGES = GoogleTranslator().get_supported_languages(as_dict=True)


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "translated": "",
            "text": "",
            "source": "auto",
            "target": "es",
            "languages": LANGUAGES
        }
    )


@app.post("/", response_class=HTMLResponse)
async def translate(
    request: Request,
    text: str = Form(""),
    source: str = Form("auto"),
    target: str = Form("es")
):

    try:
        translated = GoogleTranslator(
            source=source,
            target=target
        ).translate(text)
    except Exception as e:
        translated = f"Error: {e}"

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "translated": translated,
            "text": text,
            "source": source,
            "target": target,
            "languages": LANGUAGES
        }
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7200)