import tkinter as tk
from tkinter import messagebox
import requests
from PIL import Image, ImageTk
from io import BytesIO
from config import API_KEY


unit = "metric"

def toggle_unit():
    global unit

    if unit == "metric":
        unit = "imperial"
        unit_button.config(text="Switch to °C")
    else:
        unit = "metric"
        unit_button.config(text="Switch to °F")


def get_weather():
    city = city_entry.get()

    if city == "":
        messagebox.showerror("Error", "Please enter a city name!")
        return

    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units={unit}"

    try:
        response = requests.get(url)
        data = response.json()
        print(data)

        if data["cod"] != 200:
            messagebox.showerror("Error", "City not found!")
            return

        temp = data["main"]["temp"]
        hum = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]
        weather = data["weather"][0]["description"]

        icon = data["weather"][0]["icon"]
        print(icon)

        icon_url = f"https://openweathermap.org/img/wn/{icon}@2x.png"
        print(icon_url)

        icon_response = requests.get(icon_url)

        img = Image.open(BytesIO(icon_response.content))
        img = img.resize((100, 100))

        weather_icon = ImageTk.PhotoImage(img)

        icon_label.config(image=weather_icon)
        icon_label.image = weather_icon

        symbol = "°C" if unit == "metric" else "°F"
        temperature.config(text=f"Temperature: {temp} {symbol}")
        humidity.config(text=f"Humidity: {hum}%")
        wind.config(text=f"Wind Speed: {wind_speed} m/s")
        condition.config(text=f"Condition: {weather.title()}")

    except Exception:
        messagebox.showerror("Error", "Check your internet connection!")

# Create window
root = tk.Tk()
root.configure(bg="#87CEEB")
root.title("Weather App")
root.geometry("400x700")
root.resizable(False, False)

title = tk.Label(
    root,
    text="🌤 Weather App",
    font=("Arial", 22, "bold"),
    bg="#87CEEB",
    fg="navy"
)
title.pack(pady=15)

city_label = tk.Label(root, text="Enter City:", font=("Arial", 12))
city_label.pack()

city_entry = tk.Entry(
    root,
    font=("Arial", 14),
    width=22,
    justify="center"
)
city_entry.pack(pady=10)

search_button = tk.Button(
    root,
    text="Get Weather",
    font=("Arial", 13, "bold"),
    bg="green",
    fg="white",
    padx=15,
    pady=5,
    command=get_weather
)
search_button.pack(pady=10)

unit_button = tk.Button(
    root,
    text="Switch to °F",
    font=("Arial", 11),
    command=toggle_unit
)
unit_button.pack(pady=5)

icon_label = tk.Label(root, bg="#87CEEB")
icon_label.pack(pady=10)

temperature = tk.Label(root, text="Temperature: --", font=("Arial", 12), bg="#87CEEB")
temperature.pack(pady=5)

humidity = tk.Label(root, text="Humidity: --", font=("Arial", 12), bg="#87CEEB")
humidity.pack(pady=5)

wind = tk.Label(root, text="Wind Speed: --", font=("Arial", 12), bg="#87CEEB")
wind.pack(pady=5)

condition = tk.Label(root, text="Condition: --", font=("Arial", 12), bg="#87CEEB")
condition.pack(pady=5)

root.mainloop()