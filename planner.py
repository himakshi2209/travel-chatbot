'''
import tkinter as tk
from tkinter import messagebox
import json

# Load data from tourism.json file
with open('tourism.json', 'r') as jsonfile:
    data = json.load(jsonfile)

# Create a list to store the chat conversation
chat_conversation = []

# Create a dictionary to map cities to their respective data
city_data = {}
for region, cities in data.items():
    for city_info in cities:
        city_name = city_info["City"]
        city_data[city_name] = city_info

# Create variables to store user choices
selected_region = None
selected_city = None

def start_chat():
    chat_conversation.clear()
    chat_conversation.append("Chatbot: Welcome! Let's plan your trip.")
    chat_conversation.append("Chatbot: Are you planning to travel to North or South India?")
    update_chat_display()

def update_chat_display():
    chat_output.config(state=tk.NORMAL)
    chat_output.delete(1.0, tk.END)
    chat_output.insert(tk.END, '\n'.join(chat_conversation))
    chat_output.config(state=tk.DISABLED)

def on_region_selected(region):
    global selected_region
    selected_region = region
    chat_conversation.append(f"User: I want to travel to {region} India.")
    chat_conversation.append("Chatbot: Great! Now, please choose a city from the list.")
    city_buttons_frame.pack_forget()
    display_city_buttons()

def display_city_buttons():
    city_buttons_frame.pack(pady=10)
    for city in city_data.keys():
        city_button = tk.Button(city_buttons_frame, text=city, command=lambda c=city: on_city_selected(c))
        city_button.pack(side=tk.LEFT, padx=5, pady=5)

def on_city_selected(city):
    global selected_city
    selected_city = city
    chat_conversation.append(f"User: I choose {city}.")
    chat_conversation.append("Chatbot: How many days are you planning to travel?")
    city_buttons_frame.pack_forget()
    city_info = city_data[city]
    display_places(city_info)

def display_places(city_info):
    chat_conversation.append("Chatbot: Please enter the number of days for travel:")
    days_entry.pack(padx=10, pady=5)
    budget_label.pack(pady=5)
    budget_entry.pack(padx=10, pady=5)
    submit_button.config(command=lambda: calculate_budget(city_info))

def calculate_budget(city_info):
    try:
        days = int(days_entry.get())
        budget_per_person = int(budget_entry.get())
        locations = city_info["Locations"]

        recommended_destinations = []

        for location in locations:
            travel_time = float(location['Travel Time (hours)'])
            per_person_budget = int(location['Budget Per Person(INR)'])

            total_cost = days * per_person_budget

            if total_cost <= budget_per_person and travel_time <= days:
                destination = f"Place: {location['Place Name']}, Budget: {per_person_budget} INR"
                recommended_destinations.append(destination)

        if recommended_destinations:
            chat_conversation.append("Chatbot: Recommended Destinations:")
            chat_conversation.extend(recommended_destinations)
        else:
            chat_conversation.append("Chatbot: Sorry, no destinations match your criteria.")

        update_chat_display()

    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter valid numbers for days and budget.")

# Create a Tkinter window
root = tk.Tk()
root.title("Travel Planner Chatbot")

# Create a Chatbot-style interface using a Text widget
chat_output = tk.Text(root, width=50, height=20, state=tk.DISABLED, wrap=tk.WORD)
chat_output.pack(padx=10, pady=10)

# Create a "Start" button to begin the chat
start_button = tk.Button(root, text="Start", command=start_chat)
start_button.pack(pady=10)

# Frame to hold city buttons
city_buttons_frame = tk.Frame(root)

# Create labels and entry fields
days_label = tk.Label(root, text="Number of days for travel:")
days_entry = tk.Entry(root)
budget_label = tk.Label(root, text="Budget per person (INR):")
budget_entry = tk.Entry(root)

# Create a "Submit" button
submit_button = tk.Button(root, text="Submit", command=lambda: calculate_budget(city_data[selected_city]))

root.mainloop()

import tkinter as tk
from tkinter import messagebox
import json

# Load data from tourism.json file
with open('tourism.json', 'r') as jsonfile:
    data = json.load(jsonfile)

# Create a list to store the chat conversation
chat_conversation = []

# Create a dictionary to map cities to their respective data
city_data = {}
for region, cities in data.items():
    for city_info in cities:
        city_name = city_info["City"]
        city_data[city_name] = city_info
        city_info["Region"]=region

# Create variables to store user choices
selected_region = None
selected_city = None

def start_chat():
    chat_conversation.clear()
    chat_conversation.append("Chatbot: Welcome! Let's plan your trip.")
    chat_conversation.append("Chatbot: Are you planning to travel to North or South India?")
    update_chat_display()
    display_region_buttons()
    start_button.pack_forget()  # Hide the "Start" button

def update_chat_display():
    chat_output.config(state=tk.NORMAL)
    chat_output.delete(1.0, tk.END)
    chat_output.insert(tk.END, '\n'.join(chat_conversation))
    chat_output.config(state=tk.DISABLED)

def display_region_buttons():
    region_buttons_frame.pack(pady=10)
    for region in data.keys():
        region_button = tk.Button(region_buttons_frame, text=region, command=lambda r=region: on_region_selected(r))
        region_button.pack(side=tk.LEFT, padx=5, pady=5)

def on_region_selected(region):
    global selected_region
    selected_region = region
    chat_conversation.append(f"User: I want to travel to {region} India.")
    chat_conversation.append("Chatbot: Great! Now, please choose a city from the list.")
    region_buttons_frame.pack_forget()
    display_city_buttons(region)

def display_city_buttons(region):
    city_buttons_frame.pack(pady=10)
    for city, city_info in city_data.items():
        if city_info["Region"] == region:
            city_button = tk.Button(city_buttons_frame, text=city, command=lambda c=city: on_city_selected(c))
            city_button.pack(side=tk.LEFT, padx=5, pady=5)

def on_city_selected(city):
    global selected_city
    selected_city = city
    chat_conversation.append(f"User: I choose {city}.")
    chat_conversation.append("Chatbot: How many days are you planning to travel?")
    city_buttons_frame.pack_forget()
    city_info = city_data[city]
    display_places(city_info)

def display_places(city_info):
    chat_conversation.append("Chatbot: Please enter the number of days for travel:")
    days_entry.pack(padx=10, pady=5)
    budget_label.pack(pady=5)
    budget_entry.pack(padx=10, pady=5)
    submit_button.config(command=lambda: calculate_budget(city_info))

def calculate_budget(city_info):
    try:
        days = int(days_entry.get())
        budget_per_person = int(budget_entry.get())
        locations = city_info["Locations"]

        recommended_destinations = []

        for location in locations:
            travel_time = float(location['Travel Time (hours)'])
            per_person_budget = int(location['Budget Per Person (INR)'])

            total_cost = days * per_person_budget

            if total_cost <= budget_per_person and travel_time <= days:
                destination = f"Place: {location['Place Name']}, Budget: {per_person_budget} INR"
                recommended_destinations.append(destination)

        if recommended_destinations:
            chat_conversation.append("Chatbot: Recommended Destinations:")
            chat_conversation.extend(recommended_destinations)
        else:
            chat_conversation.append("Chatbot: Sorry, no destinations match your criteria.")

        update_chat_display()

    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter valid numbers for days and budget.")

# Create a Tkinter window
root = tk.Tk()
root.title("Travel Planner Chatbot")

# Create a Chatbot-style interface using a Text widget
chat_output = tk.Text(root, width=50, height=20, state=tk.DISABLED, wrap=tk.WORD)
chat_output.pack(padx=10, pady=10)

# Create a "Start" button to begin the chat
start_button = tk.Button(root, text="Start", command=start_chat)
start_button.pack(pady=10)

# Frame to hold region buttons
region_buttons_frame = tk.Frame(root)

# Frame to hold city buttons
city_buttons_frame = tk.Frame(root)

# Create labels and entry fields
days_label = tk.Label(root, text="Number of days for travel:")
days_entry = tk.Entry(root)
budget_label = tk.Label(root, text="Budget per person (INR):")
budget_entry = tk.Entry(root)

# Create a "Submit" button
submit_button = tk.Button(root, text="Submit")

root.mainloop()
'''
import tkinter as tk
from tkinter import messagebox
import json

# Load data from tourism.json file
with open('tourism.json', 'r') as jsonfile:
    data = json.load(jsonfile)

# Create a list to store the chat conversation
chat_conversation = []

# Create a dictionary to map cities to their respective data
city_data = {}
for region, cities in data.items():
    for city_info in cities:
        city_name = city_info["City"]
        city_data[city_name] = city_info
        city_info["Region"] = region

# Create variables to store user choices
selected_region = None
selected_city = None

def start_chat():
    chat_conversation.clear()
    chat_conversation.append("Chatbot: Welcome! Let's plan your trip.")
    chat_conversation.append("Chatbot: Are you planning to travel to North or South India?")
    update_chat_display()
    display_region_buttons()
    start_button.pack_forget()  # Hide the "Start" button

def update_chat_display():
    chat_output.config(state=tk.NORMAL)
    chat_output.delete(1.0, tk.END)
    chat_output.insert(tk.END, '\n'.join(chat_conversation))
    chat_output.config(state=tk.DISABLED)

def display_region_buttons():
    region_buttons_frame.pack(pady=10)
    for region in data.keys():
        region_button = tk.Button(region_buttons_frame, text=region, command=lambda r=region: on_region_selected(r))
        region_button.pack(side=tk.LEFT, padx=5, pady=5)

def on_region_selected(region):
    global selected_region
    selected_region = region
    chat_conversation.append(f"User: I want to travel to {region} India.")
    chat_conversation.append("Chatbot: Great! Now, please choose a city from the list.")
    region_buttons_frame.pack_forget()
    display_city_buttons(region)

def display_city_buttons(region):
    city_buttons_frame.pack(pady=10)
    for city, city_info in city_data.items():
        if city_info["Region"] == region:
            city_button = tk.Button(city_buttons_frame, text=city, command=lambda c=city: on_city_selected(c))
            city_button.pack(side=tk.LEFT, padx=5, pady=5)

def on_city_selected(city):
    global selected_city
    selected_city = city
    chat_conversation.append(f"User: I choose {city}.")
    chat_conversation.append("\n")
    chat_conversation.append("Chatbot: How many days are you planning to travel? ")
    chat_conversation.append("Chatbot: How much budget do you have per person? ")
    chat_conversation.append("\n")
    city_buttons_frame.pack_forget()
    city_info = city_data[city]
    display_input_fields(city_info)

def display_input_fields(city_info):
    chat_conversation.append("Chatbot: Please enter the number of days for travel along with the per person budget:")
    days_var = tk.StringVar()
    days_label_frame.pack(pady=5)
    '''
    days_label = tk.Label(days_label_frame, text="Number of days for travel:")
    days_label.pack()'''
    days_entry = tk.Entry(days_label_frame, textvariable=days_var)
    days_entry.pack(pady=5)

    budget_var = tk.StringVar()
    budget_label_frame.pack(pady=5)
    '''
    budget_label = tk.Label(budget_label_frame, text="Budget per person (INR):")
    budget_label.pack()'''
    budget_entry = tk.Entry(budget_label_frame, textvariable=budget_var)
    budget_entry.pack(pady=5)

    submit_button.config(command=lambda: calculate_budget(city_info, days_var, budget_var))
    submit_button.pack(pady=10)

def calculate_budget(city_info, days_var, budget_var):
    try:
        days = int(days_var.get())
        budget_per_person = int(budget_var.get())
        locations = city_info["Locations"]

        recommended_destinations = []

        for location in locations:
            travel_time = float(location['Travel Time (hours)'])
            per_person_budget = int(location['Budget Per Person (INR)'])

            total_cost = days * per_person_budget

            if total_cost <= budget_per_person and travel_time <= days:
                destination = f"Place: {location['Place Name']}, Budget: {per_person_budget} INR"
                recommended_destinations.append(destination)

        if recommended_destinations:
            
            chat_conversation.append("\n")
            chat_conversation.append("Chatbot: Recommended Destinations:")
            chat_conversation.extend(recommended_destinations)
        else:
            chat_conversation.append("Chatbot: Sorry, no destinations match your criteria.")

        update_chat_display()

    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter valid numbers for days and budget.")

# Create a Tkinter window
root = tk.Tk()
root.title("Travel Planner Chatbot")

# Create a Chatbot-style interface using a Text widget
chat_output = tk.Text(root, width=50, height=20, state=tk.DISABLED, wrap=tk.WORD)
chat_output.pack(padx=10, pady=10)

# Create a "Start" button to begin the chat
start_button = tk.Button(root, text="Start", command=start_chat)
start_button.pack(pady=10)

# Frame to hold region buttons
region_buttons_frame = tk.Frame(root)

# Frame to hold city buttons
city_buttons_frame = tk.Frame(root)

# Frame to hold days and budget labels
days_label_frame = tk.LabelFrame(root, text="Number of days for travel:")
budget_label_frame = tk.LabelFrame(root, text="Budget per person (INR):")

# Create a "Submit" button
submit_button = tk.Button(root, text="Submit")

root.mainloop()
