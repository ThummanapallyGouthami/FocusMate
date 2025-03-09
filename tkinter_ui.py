import tkinter as tk
from tkinter import messagebox
import requests

BASE_URL = "http://127.0.0.1:5001"  # Ensure backend is running on this port

def generate_plan():
    user_id = user_id_entry.get().strip()
    goals = goals_entry.get("1.0", tk.END).strip()

    if not user_id or not goals:
        messagebox.showerror("Input Error", "Please enter both User ID and Goals.")
        return

    try:
        response = requests.post(f"{BASE_URL}/generate_plan/", json={"user_id": user_id, "goals": goals})
        if response.status_code == 200:
            plan = response.json().get("plan", "No plan generated.")
            plan_text.config(state=tk.NORMAL)
            plan_text.delete("1.0", tk.END)
            plan_text.insert(tk.END, plan)
            plan_text.config(state=tk.DISABLED)
        else:
            messagebox.showerror("Error", f"Failed to generate study plan.\n{response.text}")
    except requests.exceptions.ConnectionError:
        messagebox.showerror("Connection Error", "Failed to connect to the backend server. Make sure it is running.")

def view_plans():
    try:
        response = requests.get(f"{BASE_URL}/get_plans/")
        if response.status_code == 200:
            plans = response.json()
            plan_text.config(state=tk.NORMAL)
            plan_text.delete("1.0", tk.END)
            for p in plans:
                plan_text.insert(tk.END, f"📌 ID: {p.get('user_id', 'N/A')}, Goals: {p.get('goals', 'N/A')}\n📝 Plan: {p.get('plan', 'N/A')}\n")
                plan_text.insert(tk.END, "-"*50 + "\n")
            plan_text.config(state=tk.DISABLED)
        else:
            messagebox.showerror("Error", f"Failed to fetch study plans.\n{response.text}")
    except requests.exceptions.ConnectionError:
        messagebox.showerror("Connection Error", "Failed to connect to the backend server. Make sure it is running.")

# Create the main window
root = tk.Tk()
root.title("Studbud - AI Study Planner")

# User ID Input
tk.Label(root, text="User ID:", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=10)
user_id_entry = tk.Entry(root, font=("Arial", 12))
user_id_entry.grid(row=0, column=1, padx=10, pady=10)

# Goals Input
tk.Label(root, text="Enter Your Study Goals:", font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=10)
goals_entry = tk.Text(root, height=3, width=40, font=("Arial", 12))
goals_entry.grid(row=1, column=1, padx=10, pady=10)

# Buttons
generate_btn = tk.Button(root, text="Generate Plan", font=("Arial", 12), command=generate_plan)
generate_btn.grid(row=2, column=0, columnspan=2, pady=10)

view_btn = tk.Button(root, text="View Plans", font=("Arial", 12), command=view_plans)
view_btn.grid(row=3, column=0, columnspan=2, pady=10)

# Plan Display
plan_text = tk.Text(root, height=10, width=60, font=("Arial", 12), state=tk.DISABLED)
plan_text.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

# Run the Tkinter GUI
root.mainloop()
