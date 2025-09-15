import requests
import json
import datetime

Api_key = "8b862482f201393a9cfecaa69c0dc094"
Base_url = "https://api.openweathermap.org/data/2.5/weather"

with open("./data.json", "r", encoding="utf-8") as f:
    INTENTS = json.load(f)


def now_time():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M")


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


def normalize(text: str) -> str:
    return " ".join(text.strip().lower().split())


def chatbot_response(user_input: str) -> str:
    ui = normalize(user_input)

    if ui in ("тусламж", "help", "tuslamj"):
        return HELP_TEXT
    if ui in ("цаг", "tsag", "time"):
        return f"Одоо цаг: {now_time()}"

    if ui in ("цаг агаар", "tsag agaar", "weather"):
        lat = input("latitude: ")
        lon = input("longitude: ")

        url = f"{Base_url}?lat={lat}&lon={lon}&appid={Api_key}&units=metric"

        response = requests.get(url)
        data = response.json()

        if response.status_code == 200:
            city = data.get("name", "Unknown location")
            temp = data["main"]["temp"]
            weather = data["weather"][0]["description"].title()
            humidity = data["main"]["humidity"]
            wind = data["wind"]["speed"]

            return (
                f"\n Location: {city} ({lat}, {lon})"
                f"\n Wind speed: {wind} m/s"
                f"\n Temperature: {temp}°C"
                f"\n Humidity: {humidity}%"
                f"\n Weather: {weather}"
            )
        else:
            return "Цаг агаарын мэдээллийг авахад алдаа гарлаа."

    for intent in INTENTS:
        for kw in intent["keywords"]:
            if normalize(kw) == ui:
                ans = intent["answer"]
                return ans(ui) if callable(ans) else ans

    return "Уучлаарай, ойлгосонгүй. 'тусламж' гэж бичээд боломжит асуултуудыг үзээрэй."


while True:
    user_input = input("Таны асуулт : ")
    if normalize(user_input) == "гарах":
        print("Баяртай")
        break
    print(chatbot_response(user_input))
