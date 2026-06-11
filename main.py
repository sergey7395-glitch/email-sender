import os, smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

class EmailRequest(BaseModel):
    to: str
    subject: str
    html: str

@app.post("/send-email")
def send_email(req: EmailRequest):
    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = req.subject
        msg["From"] = f"{os.getenv('SENDER_NAME','Стальная защита')} <{os.getenv('YANDEX_EMAIL')}>"
        msg["To"] = req.to
        msg.attach(MIMEText(req.html, "html", "utf-8"))
        with smtplib.SMTP("smtp.yandex.ru", 587) as s:
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
