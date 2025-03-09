import tkinter as tk
from tkinter import messagebox
import requests

BASE_URL = "http://127.0.0.1:5000"  # Backend URL

def generate_plan():
    user_id = user_id_entry.get()
    goals = goals_entry.get("1.0", tk.END).strip()

    if not user_id or not goals:
        messagebox.showerror("Input Error", "Please enter both User ID and Goals.")
        return

    response = requests.post(f"{BASE_URL}/generate_study_plan", json={"user_id": user_id, "goals": goals})
    if response.status_code == 200:
        plan = response.json()["study_plan"]
        plan_text.config(state=tk.NORMAL)
        plan_text.delete("1.0", tk.END)
        plan_text.insert(tk.END, plan)
        plan_text.config(state=tk.DISABLED)
    else:
        messagebox.showerror("Error", "Failed to generate study plan.")

def view_plans():
    response = requests.get(f"{BASE_URL}/get_study_plans")
    if response.status_code == 200:
        plans = response.json()
        plan_text.config(state=tk.NORMAL)
        plan_text.delete("1.0", tk.END)
        for p in plans:
            plan_text.insert(tk.END, f"📌 ID: {p['id']}, User: {p['user_id']}\n")
            plan_text.insert(tk.END, f"🎯 Goals: {p['goals']}\n")
            plan_text.insert(tk.END, f"📝 Plan: {p['plan']}\n")
            plan_text.insert(tk.END, "-"*50 + "\n")
        plan_text.config(state=tk.DISABLED)
    else:
        messagebox.showerror("Error", "Failed to fetch study plans.")

# GUI Setup
root = tk.Tk()
root.title("Studbud - AI Study Planner")

tk.Label(root, text="User ID:", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=10)
user_id_entry = tk.Entry(root, font=("Arial", 12))
user_id_entry.grid(row=0, column=1, padx=10, pady=10)

tk.Label(root, text="Enter Your Study Goals:", font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=10)
goals_entry = tk.Text(root, height=3, width=40, font=("Arial", 12))
goals_entry.grid(row=1, column=1, padx=10, pady=10)

generate_btn = tk.Button(root, text="Generate Plan", font=("Arial", 12), command=generate_plan)
generate_btn.grid(row=2, column=0, columnspan=2, pady=10)

view_btn = tk.Button(root, text="View Plans", font=("Arial", 12), command=view_plans)
view_btn.grid(row=3, column=0, columnspan=2, pady=10)

plan_text = tk.Text(root, height=10, width=60, font=("Arial", 12), state=tk.DISABLED)
plan_text.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

root.mainloop()
