import tkinter as tk
from tkinter import messagebox
import sqlite3
from datetime import datetime
import matplotlib.pyplot as plt

# Create database

conn = sqlite3.connect("bmi_database.db")

cursor = conn.cursor()


cursor.execute("""
CREATE TABLE IF NOT EXISTS records(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    weight REAL,
    height REAL,
    bmi REAL,
    category TEXT,
    date TEXT
)
""")

conn.commit()

# Window

root = tk.Tk()

root.title("BMI Calculator")
root.geometry("400x400")

# Step 6: Input fields


# Name
tk.Label(
    root,
    text="Name"
).pack()

name_entry = tk.Entry(root)

name_entry.pack()



# Weight
tk.Label(
    root,
    text="Weight (kg)"
).pack()

weight_entry = tk.Entry(root)

weight_entry.pack()



# Height
tk.Label(
    root,
    text="Height (m)"
).pack()

height_entry = tk.Entry(root)

height_entry.pack()


# Step 8: Save data


def save_data(name, weight, height, bmi, category):

    cursor.execute(
        """
        INSERT INTO records
        (name, weight, height, bmi, category, date)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            name,
            weight,
            height,
            bmi,
            category,
            datetime.now()
        )
    )

    conn.commit()


# Step 9: Show BMI History Graph

def show_graph():

    cursor.execute(
        "SELECT date, bmi FROM records"
    )

    data = cursor.fetchall()


    if len(data) == 0:
        messagebox.showinfo(
            "No Data",
            "Calculate BMI first"
        )
        return


    dates = []
    values = []


    for row in data:

        dates.append(row[0])

        values.append(row[1])


    plt.figure(figsize=(8,4))


    plt.plot(
        dates,
        values,
        marker="o"
    )


    plt.title("BMI Trend")

    plt.xlabel("Date")

    plt.ylabel("BMI")


    plt.xticks(rotation=45)


    plt.tight_layout()


    plt.show()



# Step 7: BMI Calculation

def calculate_bmi():

    try:

        name = name_entry.get()

        weight = float(weight_entry.get())

        height = float(height_entry.get())


        if weight <= 0 or height <= 0:
            raise ValueError


        bmi = weight / (height * height)


        if bmi < 18.5:
            category = "Underweight"

        elif bmi < 25:
            category = "Normal"

        elif bmi < 30:
            category = "Overweight"

        else:
            category = "Obese"


        result.config(
            text=f"BMI: {bmi:.2f}\nCategory: {category}"
        )

        save_data(name, weight, height, bmi, category)

    except:

        messagebox.showerror(
            "Error",
            "Enter valid weight and height"
        )



# Calculate button

button = tk.Button(
    root,
    text="Calculate BMI",
    command=calculate_bmi
)

button.pack()



# Result display

result = tk.Label(
    root,
    text="BMI: \nCategory: ",
    font=("Arial",14)
)

result.pack()


# Graph Button

graph_btn = tk.Button(
    root,
    text="Show BMI Trend",
    command=show_graph
)

graph_btn.pack()



root.mainloop()