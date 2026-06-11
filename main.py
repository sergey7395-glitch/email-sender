import os, smtplib, requests
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

class ImageRequest(BaseModel):
    image_base64: str

class EmailRequest(BaseModel):
    to: str
    subject: str
    html: str

@app.post("/upload-image")
def upload_image(req: ImageRequest):
    try:
        response = requests.post(
            "https://api.imgbb.com/1/upload",
            data={"key": "0ef83fe08f2a45469fd210b8d071c3e2", "image": req.image_base64}
        )
        data = response.json()
        if data.get("success"):
            return {"success": True, "url": data["data"]["url"]}
        raise Exception(str(data))
    except Exception as e:
        return {"success": False, "error": str(e)}

@app.post("/send-email")
def send_email(req: EmailRequest):
    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = req.subject
        msg["From"] = f"{os.getenv('SENDER_NAME','Стальная защита')} <{os.getenv('YANDEX_EMAIL')}>"
        msg["To"] = req.to
        msg.attach(MIMEText(req.html, "html", "utf-8"))
        with smtplib.SMTP("smtp.yandex.ru", 25) as s:
            s.ehlo()
            s.starttls()
            s.login(os.getenv("YANDEX_EMAIL"), os.getenv("YANDEX_PASSWORD"))
            s.sendmail(os.getenv("YANDEX_EMAIL"), req.to, msg.as_string())
        return {"success": True}
    except Exception as e:
        return {"success": False, "error": str(e)}

@app.get("/")
def root():
    return {"status": "ok"}
