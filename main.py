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
    now = datetime.datetime.now()
    return f"{now.year} оны {now.month} сарын {now.day} өдөр {now.hour:02d}:{now.minute:02d}"


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
    "ℹ️ 'гарах' гэж бичвэл програм дуусна."
)


class Message(BaseModel):
    text: str


@app.post("/chat")
def chat(message: Message):
    user_input = message.text
   
    response = my_chatbot(user_input)
    return {"reply": response}


# def my_chatbot(text: str):
#     if "hello" in text.lower():
#         return "Hi! How can I help you?"
#     return "I didn’t understand that."
def normalize(text: str) -> str:
    return " ".join(text.strip().lower().split())

def my_chatbot(user_input: str) -> str:
    ui = normalize(user_input)

    if ui in ("тусламж", "help", "tuslamj"):
        return HELP_TEXT
    if ui in ("цаг", "tsag", "time"):
        return f"Одоо цаг: {now_time()}"

    # if ui in ("цаг агаар", "tsag agaar", "weather"):
    #     lat = input("latitude: ")
    #     lon = input("longitude: ")

    #     url = f"{Base_url}?lat={lat}&lon={lon}&appid={Api_key}&units=metric"

    #     response = requests.get(url)
    #     data = response.json()

    #     if response.status_code == 200:
    #         city = data.get("name", "Unknown location")
    #         temp = data["main"]["temp"]
    #         weather = data["weather"][0]["description"].title()
    #         humidity = data["main"]["humidity"]
    #         wind = data["wind"]["speed"]

    #         return (
    #             f"\n Location: {city} ({lat}, {lon})"
    #             f"\n Wind speed: {wind} m/s"
    #             f"\n Temperature: {temp}°C"
    #             f"\n Humidity: {humidity}%"
    #             f"\n Weather: {weather}"
    #         )
    #     else:
    #         return "Цаг агаарын мэдээллийг авахад алдаа гарлаа."

    for intent in INTENTS:
        for kw in intent["keywords"]:
            if normalize(kw) == ui:
                ans = intent["answer"]
                return ans(ui) if callable(ans) else ans

    return "Уучлаарай, ойлгосонгүй. 'тусламж' гэж бичээд боломжит асуултуудыг үзээрэй."


# while True:
#     user_input = input("Таны асуулт : ")
#     if normalize(user_input) == "гарах":
#         print("Баяртай")
#         break
#     print(chatbot_response(user_input))
