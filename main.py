import tkinter as tk
from tkinter import messagebox
import sqlite3

# ---------- Database Setup ----------
conn = sqlite3.connect("users.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    username TEXT PRIMARY KEY,
    password TEXT
)
""")
conn.commit()

# ---------- Main Window ----------
root = tk.Tk()
root.title("Account System")
root.geometry("500x400")

def show_frame(frame):
    frame.tkraise()

container = tk.Frame(root)
container.pack(fill="both", expand=True)

container.grid_rowconfigure(0, weight=1)
container.grid_columnconfigure(0, weight=1)

# ---------- Start Screen ----------
start_screen = tk.Frame(container, bg="#4f0054")
start_screen.grid(row=0, column=0, sticky="nsew")

tk.Label(
    start_screen,
    text="FitFinder",
    font=("Arial", 32, "bold"),
    bg="#4f0054",
    fg="white"
).pack(pady=40)

tk.Button(start_screen, text="Login",
          command=lambda: show_frame(login_screen)).pack(pady=10)

tk.Button(start_screen, text="Create Account",
          command=lambda: show_frame(register_screen)).pack(pady=10)

# ---------- Login Screen ----------
login_screen = tk.Frame(container, bg="#4f0054")
login_screen.grid(row=0, column=0, sticky="nsew")

tk.Label(
    login_screen,
    text="Login",
    font=("Arial", 28, "bold"),
    bg="#4f0054",
    fg="white"
).pack(pady=20)

login_user = tk.Entry(login_screen)
login_user.pack(pady=5)
login_user.insert(0, "Username")

login_pass = tk.Entry(login_screen, show="*")
login_pass.pack(pady=5)
login_pass.insert(0, "Password")

def login():
    username = login_user.get()
    password = login_pass.get()

    cursor.execute("SELECT * FROM users WHERE username=? AND password=?",
                   (username, password))
    result = cursor.fetchone()

    if result:
        messagebox.showinfo("Success", "Login Successful!")
        show_frame(ai_screen)
    else:
        messagebox.showerror("Error", "Invalid login")

tk.Button(login_screen, text="Login", command=login).pack(pady=10)
tk.Button(login_screen, text="Back",
          command=lambda: show_frame(start_screen)).pack()

# ---------- Register Screen ----------
register_screen = tk.Frame(container, bg="#4f0054")
register_screen.grid(row=0, column=0, sticky="nsew")

tk.Label(
    register_screen,
    text="Create Account",
    font=("Arial", 28, "bold"),
    bg="#4f0054",
    fg="white"
).pack(pady=20)

reg_user = tk.Entry(register_screen)
reg_user.pack(pady=5)
reg_user.insert(0, "Username")

reg_pass = tk.Entry(register_screen, show="*")
reg_pass.pack(pady=5)
reg_pass.insert(0, "Password")

def register():
    username = reg_user.get()
    password = reg_pass.get()

    if username == "" or password == "":
        messagebox.showerror("Error", "Fields cannot be empty")
        return

    try:
        cursor.execute("INSERT INTO users VALUES (?, ?)", (username, password))
        conn.commit()
        messagebox.showinfo("Success", "Account Created!")
        show_frame(login_screen)
    except:
        messagebox.showerror("Error", "Username already exists")

tk.Button(register_screen, text="Register", command=register).pack(pady=10)
tk.Button(register_screen, text="Back",
          command=lambda: show_frame(start_screen)).pack()

# ---------- AI Fashion Screen ----------
ai_screen = tk.Frame(container, bg="#4f0054")
ai_screen.grid(row=0, column=0, sticky="nsew")

tk.Label(
    ai_screen,
    text="FitFinder AI",
    font=("Arial", 28, "bold"),
    bg="#4f0054",
    fg="white"
).pack(pady=20)

question_entry = tk.Entry(ai_screen, width=40)
question_entry.pack(pady=10)

response_label = tk.Label(
    ai_screen,
    text="",
    wraplength=400,
    bg="#4f0054",
    fg="white"
)
response_label.pack(pady=20)

def fake_ai(question):
    question = question.lower()

    if "date" in question:
        return "Try a smart casual look: fitted jeans, clean sneakers, and a stylish jacket."
    elif "summer" in question:
        return "Light fabrics like linen, pastel colors, and comfy sneakers work great."
    elif "winter" in question:
        return "Layer up with a coat, sweater, and boots."
    else:
        return "Try neutral colors with one bold statement piece!"

def get_response():
    question = question_entry.get()
    answer = fake_ai(question)
    response_label.config(text=answer)

tk.Button(
    ai_screen,
    text="Ask AI",
    command=get_response
).pack(pady=10)

tk.Button(
    ai_screen,
    text="Logout",
    command=lambda: show_frame(start_screen)
).pack(pady=10)

# ---------- Start on Start Screen ----------
show_frame(start_screen)

root.mainloop()

#-----------------------------------------------

import openai

openai.api_key = "YOUR_API_KEY"

def ask_ai(question):
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a fashion stylist AI. Give trendy, helpful outfit advice."},
            {"role": "user", "content": question}
        ]
    )
    return response.choices[0].message["content"]

#-------------------------------------------------------

ai_screen = tk.Frame(container, bg="#4f0054")
ai_screen.grid(row=0, column=0, sticky="nsew")

tk.Label(
    ai_screen,
    text="Fashion AI Assistant",
    font=("Arial", 24, "bold"),
    bg="#4f0054",
    fg="white"
).pack(pady=20)

question_entry = tk.Entry(ai_screen, width=40)
question_entry.pack(pady=10)

response_label = tk.Label(
    ai_screen,
    text="",
    wraplength=400,
    bg="#4f0054",
    fg="white"
)
response_label.pack(pady=20)

def get_response():
    question = question_entry.get()
    answer = ask_ai(question)
    response_label.config(text=answer)

tk.Button(ai_screen, text="Ask AI", command=get_response).pack()