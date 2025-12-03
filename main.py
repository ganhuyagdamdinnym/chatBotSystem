from fastapi import FastAPI
from pydantic import BaseModel
import requests
import json
import datetime
from fastapi.middleware.cors import CORSMiddleware

Api_key = "8b862482f201393a9cfecaa69c0dc094"
Base_url = "https://api.openweathermap.org/data/2.5/weather"

with open("./data.json", "r", encoding="utf-8") as f:
    INTENTS = json.load(f)

def now_time():
    months = [
        "нэгдүгээр", "хоёрдугаар", "гуравдугаар", "дөрөвдүгээр",
        "тавдугаар", "зургаадугаар", "долоодугаар", "наймдугаар",
        "есдүгээр", "аравдугаар", "арван нэгдүгээр", "арван хоёрдугаар"
    ]
    now = datetime.datetime.now()
    month_name = months[now.month - 1]
    return f"{now.year} оны {month_name} сарын {now.day}-ны өдөр, {if(now.hour=>16){24-now.hour}else{now.hour}} цаг {now.minute} минут"

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

HELP_TEXT = (
    "🧭 Жишээ асуултууд:\n"
    " - 'элсэлт ямар шаардлагатай вэ'\n"
    " - 'хичээлийн хуваарь'\n"
    " - 'төлбөрийн хуваарь'\n"
    " - 'тэтгэлэг'\n"
    " - 'дотуур байр'\n"
    " - 'номын сан хэд хүртэл ажилладаг'\n"
    " - 'дахин шалгалт'\n"
    " - 'интерншип/дадлага'\n"
    " - 'wifi асуудал'\n"
    " - 'төгсөх шаардлага'\n"
    " - 'гомдол, санал'\n"
    " - 'цаг'\n"
    " - 'цаг агаар'\n"
   
)

class Message(BaseModel):
    text: str

@app.post("/chat")
def chat(message: Message):
    user_input = message.text
    response = my_chatbot(user_input)
    return {"reply": response}

def normalize(text: str) -> str:
    return " ".join(text.strip().lower().split())

def my_chatbot(user_input: str) -> str:
    ui = normalize(user_input)

    if ui in ("тусламж", "help", "tuslamj"):
        return HELP_TEXT
    if ui in ("цаг", "tsag", "time"):
        return f"Одоо цаг: {now_time()}"

    for intent in INTENTS:
        for kw in intent["keywords"]:
            if normalize(kw) == ui:
                ans = intent["answer"]
                return ans(ui) if callable(ans) else ans

    return "Уучлаарай, ойлгосонгүй. 'тусламж' гэж бичээд боломжит асуултуудыг үзээрэй."
