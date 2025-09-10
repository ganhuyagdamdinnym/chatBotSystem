import requests
Api_key="8b862482f201393a9cfecaa69c0dc094"
Base_url="https://api.openweathermap.org/data/2.5/weather"

while True:
    lat=input("latitude:")    
    lon=input("longitude:")



    url= f"{Base_url}?lat={lat}&lon={lon}&appid={Api_key}&units=metric"
  
    response=requests.get(url)
    data=response.json()
    if response.status_code == 200:  
     city = data.get("name", "Unknown location")
     temp = data["main"]["temp"]
     weather = data["weather"][0]["description"].title()
     humidity=data["main"]["humidity"]
     wind=data["wind"]["speed"]

    #  print("data",data)
    print(f"\n Location: {city} ({lat}, {lon})")    
    print(f"\n Wind speed: {wind} m/s")
    print(f"\n temperature: {temp}°C")
    print(f"\n Humidity:{humidity}% ")
    print(f"\n Wather: {weather}")