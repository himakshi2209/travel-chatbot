'''
import tkinter as tk
from tkinter import messagebox
import json
import time
from PIL import Image, ImageTk  # Import necessary libraries

# Load data from tourism.json file
with open('tourism.json', 'r') as jsonfile:
    data = json.load(jsonfile)
with open('flights.json', 'r') as jsonfilee:
    flight_data = json.load(jsonfilee)
with open('trains.json', 'r') as jsonfileee:
    train_data = json.load(jsonfileee)

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
    city_buttons_frame.pack_forget()
    display_input_fields(city_data[city])

def display_input_fields(city_info):
    chat_conversation.append("\n")
    chat_conversation.append("Chatbot: Please provide the following details:")
    
    days_var = tk.StringVar()
    budget_var = tk.StringVar()
    transportation_var = tk.StringVar()
    current_destination_var = tk.StringVar()

    input_frame.pack(pady=10)
    
    days_label = tk.Label(input_frame, text="Number of days for travel:")
    days_label.pack()
    days_entry = tk.Entry(input_frame, textvariable=days_var)
    days_entry.pack(pady=5)

    budget_label = tk.Label(input_frame, text="Budget per person (INR):")
    budget_label.pack()
    budget_entry = tk.Entry(input_frame, textvariable=budget_var)
    budget_entry.pack(pady=5)

    transportation_label = tk.Label(input_frame, text="Transportation Type (Flight/Train):")
    transportation_label.pack()
    transportation_entry = tk.Entry(input_frame, textvariable=transportation_var)
    transportation_entry.pack(pady=5)

    current_destination_label = tk.Label(input_frame, text="Current Destination:")
    current_destination_label.pack()
    current_destination_entry = tk.Entry(input_frame, textvariable=current_destination_var)
    current_destination_entry.pack(pady=5)

    next_button.config(command=lambda: calculate_transportation(city_info, days_var, budget_var, transportation_var, current_destination_var))
    next_button.pack(pady=10)

def calculate_transportation(city_info, days_var, budget_var, transportation_var, current_destination_var):
    try:
        days = int(days_var.get())
        budget_per_person = int(budget_var.get())
        transportation_type = transportation_var.get()
        #destination_to_be_visited = current_destination_var.get()  # Renamed this variable
        current_destination=current_destination_var.get()
        destination_to_be_visited=city_info["City"]
        if transportation_type.lower() == "flight":
            transportation_data = flight_data
        elif transportation_type.lower() == "train":
            transportation_data = train_data
        else:
            messagebox.showerror("Invalid Transportation Type", "Please enter 'Flight' or 'Train' for transportation type.")
            return

        if transportation_data:
            recommended_transportation = []

            if current_destination in transportation_data:  # Use the current city as the key
                for transport_info in transportation_data[current_destination]:
                    price = transport_info.get("price", 0)
                    if transport_info["to"].lower() == destination_to_be_visited.lower() and price <= budget_per_person:
                        recommended_transportation.append(transport_info)

            if recommended_transportation:
                chat_conversation.append("\n")
                chat_conversation.append("Chatbot: Recommended Transportation Options:")
                for transport_info in recommended_transportation:
                    if transportation_type.lower()=="flight":
                        chat_conversation.append(f"{transport_info['airline']} to {destination_to_be_visited} - Price: {transport_info['price']} INR")
                    if  transportation_type.lower()=="train":
                        chat_conversation.append(f"{transport_info['train_name']} to {destination_to_be_visited} - Price: {transport_info['price']} INR")
                  
                remaining_budget = budget_per_person - recommended_transportation[0]["price"]
                chat_conversation.append(f"Remaining Budget: {remaining_budget} INR")

                display_places_to_visit(city_info, remaining_budget)
            else:
                chat_conversation.append("Chatbot: No transportation available for this route.")
        else:
            chat_conversation.append("Chatbot: Transportation data not found. Please check your JSON files.")

        update_chat_display()
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter valid numbers for days and budget.")


def display_places_to_visit(city_info, remaining_budget):
    chat_conversation.append("\n")
    chat_conversation.append("Chatbot: Recommended Places to Visit:")

    locations = city_info["Locations"]
    recommended_places = []

    for location in locations:
        if int(location["Budget Per Person (INR)"]) <= remaining_budget:
            recommended_places.append(location)

    if recommended_places:
        for place in recommended_places:
            chat_conversation.append(f"Place: {place['Place Name']}, Budget: {place['Budget Per Person (INR)']} INR")
    else:
        chat_conversation.append("Chatbot: No places match your remaining budget.")

    update_chat_display()

# Create a Tkinter window
roo = tk.Tk()
roo.title("Travel Planner Chatbot")

root=tk.Frame(roo)
root.place(x=0,y=0,width=2400,height=1000)

# Load the background image
background_image = Image.open("img1.jpg")  # Change the path to your image file
background_image = ImageTk.PhotoImage(background_image)
# Create a Label widget to display the background image
background_label = tk.Label(root, image=background_image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)  # Make the label cover the entire window


# Create a Chatbot-style interface using a Text widget
chat_output = tk.Text(root, width=50, height=20, state=tk.DISABLED, wrap=tk.WORD)
#chat_output.pack(padx=10, pady=10)

# List of background images
background_images = [
    "im1.jpg",
    "im2.jpg",
    "im3.jpg"
]

frame = tk.Frame(roo,width=800, height=900)
frame.place(x=0,y=0)
#frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

# Create a Canvas to display the background image
canvas = tk.Canvas(frame, width=800, height=900)
#canvas.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
canvas.place(x=0,y=0)

# Function to change the background
def change_background(index):
    if index < len(background_images):
        image = Image.open(background_images[index])
        photo = ImageTk.PhotoImage(image)
        
        # Store a reference to the PhotoImage to prevent it from being garbage collected
        canvas.photo = photo

        canvas.create_image(0, 0, anchor=tk.NW, image=photo)

        # Schedule the next background change after 5 seconds
        root.after(5000, change_background, index + 1)
    else:
        # Restart from the first image
        change_background(0)

# Start changing the background
change_background(0)

# Create a "Start" button to begin the chat
start_button = tk.Button(root, text="Start", command=start_chat)
start_button.pack(pady=10)

# Frame to hold region buttons
region_buttons_frame = tk.Frame(root)

# Frame to hold city buttons
city_buttons_frame = tk.Frame(root)

# Frame to hold input fields
input_frame = tk.Frame(root)

# Create a "Next" button for input fields
next_button = tk.Button(root, text="Next")

root.mainloop()
'''
import tkinter as tk
from tkinter import messagebox
import json
from PIL import Image, ImageTk

# Load data from tourism.json file
with open('tourism.json', 'r') as jsonfile:
    data = json.load(jsonfile)
with open('flights.json', 'r') as jsonfilee:
    flight_data = json.load(jsonfilee)
with open('trains.json', 'r') as jsonfileee:
    train_data = json.load(jsonfileee)

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
    city_buttons_frame.pack_forget()
    display_input_fields(city_data[city])

def display_input_fields(city_info):
    chat_conversation.append("\n")
    chat_conversation.append("Chatbot: Please provide the following details:")
    
    days_var = tk.StringVar()
    budget_var = tk.StringVar()
    transportation_var = tk.StringVar()
    current_destination_var = tk.StringVar()

    input_frame.pack(pady=10)
    
    days_label = tk.Label(input_frame, text="Number of days for travel:")
    days_label.pack()
    days_entry = tk.Entry(input_frame, textvariable=days_var)
    days_entry.pack(pady=5)

    budget_label = tk.Label(input_frame, text="Budget per person (INR):")
    budget_label.pack()
    budget_entry = tk.Entry(input_frame, textvariable=budget_var)
    budget_entry.pack(pady=5)

    transportation_label = tk.Label(input_frame, text="Transportation Type (Flight/Train):")
    transportation_label.pack()
    transportation_entry = tk.Entry(input_frame, textvariable=transportation_var)
    transportation_entry.pack(pady=5)

    current_destination_label = tk.Label(input_frame, text="Current Destination:")
    current_destination_label.pack()
    current_destination_entry = tk.Entry(input_frame, textvariable=current_destination_var)
    current_destination_entry.pack(pady=5)

    next_button.config(command=lambda: calculate_transportation(city_info, days_var, budget_var, transportation_var, current_destination_var))
    next_button.pack(pady=10)

def calculate_transportation(city_info, days_var, budget_var, transportation_var, current_destination_var):
    try:
        days = int(days_var.get())
        budget_per_person = int(budget_var.get())
        transportation_type = transportation_var.get()
        current_destination = current_destination_var.get()
        destination_to_be_visited = city_info["City"]
        if transportation_type.lower() == "flight":
            transportation_data = flight_data
        elif transportation_type.lower() == "train":
            transportation_data = train_data
        else:
            messagebox.showerror("Invalid Transportation Type", "Please enter 'Flight' or 'Train' for transportation type.")
            return

        if transportation_data:
            recommended_transportation = []

            if current_destination in transportation_data:
                for transport_info in transportation_data[current_destination]:
                    price = transport_info.get("price", 0)
                    if transport_info["to"].lower() == destination_to_be_visited.lower() and price <= budget_per_person:
                        recommended_transportation.append(transport_info)

            if recommended_transportation:
                chat_conversation.append("\n")
                chat_conversation.append("Chatbot: Recommended Transportation Options:")
                for transport_info in recommended_transportation:
                    if transportation_type.lower() == "flight":
                        chat_conversation.append(f"{transport_info['airline']} to {destination_to_be_visited} - Price: {transport_info['price']} INR")
                    if transportation_type.lower() == "train":
                        chat_conversation.append(f"{transport_info['train_name']} to {destination_to_be_visited} - Price: {transport_info['price']} INR")

                remaining_budget = budget_per_person - recommended_transportation[0]["price"]
                chat_conversation.append(f"Remaining Budget: {remaining_budget} INR")

                display_places_to_visit(city_info, remaining_budget)
            else:
                chat_conversation.append("Chatbot: No transportation available for this route.")
        else:
            chat_conversation.append("Chatbot: Transportation data not found. Please check your JSON files.")

        update_chat_display()
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter valid numbers for days and budget.")

def display_places_to_visit(city_info, remaining_budget):
    chat_conversation.append("\n")
    chat_conversation.append("Chatbot: Recommended Places to Visit:")

    locations = city_info["Locations"]
    recommended_places = []

    for location in locations:
        if int(location["Budget Per Person (INR)"]) <= remaining_budget:
            recommended_places.append(location)

    if recommended_places:
        for place in recommended_places:
            chat_conversation.append(f"Place: {place['Place Name']}, Budget: {place['Budget Per Person (INR)']} INR")
    else:
        chat_conversation.append("Chatbot: No places match your remaining budget.")

    update_chat_display()

# Create a Tkinter window
root = tk.Tk()
root.title("Travel Planner Chatbot")

# Create a Frame to hold chat output
chat_output_frame = tk.Frame(root, bg="white")
chat_output_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Load the background image
background_image = Image.open("background_image.jpg")
background_image = ImageTk.PhotoImage(background_image)

background_label = tk.Label(chat_output_frame, image=background_image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)  # Fill the entire window

# Create a Chatbot-style interface using a Text widget
chat_output = tk.Text(chat_output_frame, width=60, height=30, state=tk.DISABLED, wrap=tk.WORD)
chat_output.pack(padx=10, pady=10)

# List of background images
background_images = [
    "im1.jpg",
    "im2.jpg",
    "im3.jpg",
    "im4.jpg",
    "im5.jpg",
    "im6.jpg",
    "im7.jpg",
    "im8.jpg",
    "im9.jpg",
    "im10.jpg",
    "im11.jpg"
]

# Create a Frame to hold the canvas
canvas_frame = tk.Frame(root, bg="white")
canvas_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

# Create a Canvas to display the background image
canvas = tk.Canvas(canvas_frame, width=500, height=600)
canvas.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

# Function to change the background
def change_background(index):
    if index < len(background_images):
        image = Image.open(background_images[index])
        photo = ImageTk.PhotoImage(image)
        
        # Store a reference to the PhotoImage to prevent it from being garbage collected
        canvas.photo = photo

        canvas.create_image(0, 0, anchor=tk.NW, image=photo)

        # Schedule the next background change after 5 seconds
        root.after(15000, change_background, index + 1)
    else:
        # Restart from the first image
        change_background(0)

# Start changing the background
change_background(0)

# Create a "Start" button to begin the chat
start_button = tk.Button(chat_output_frame, text="Start", command=start_chat)
start_button.pack(pady=10)

# Frame to hold region buttons
region_buttons_frame = tk.Frame(chat_output_frame, bg="white")


background_label = tk.Label(region_buttons_frame, image=background_image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)  # Fill the entire window


# Frame to hold city buttons
city_buttons_frame = tk.Frame(chat_output_frame, bg="white")


background_label = tk.Label(city_buttons_frame, image=background_image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)  # Fill the entire window


# Frame to hold input fields
input_frame = tk.Frame(chat_output_frame, bg="white")

background_label = tk.Label(input_frame, image=background_image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)  # Fill the entire window

# Create a "Next" button for input fields
next_button = tk.Button(chat_output_frame, text="Next")

# Run the Tkinter main loop
root.mainloop()
