import tkinter as tk
from tkinter import ttk
from tkinter import PhotoImage
from datetime import datetime, timedelta
from PIL import Image, ImageTk
from tkinter import simpledialog


root = tk.Tk()
root.title("Utilisation tracker")
root.geometry("800x300")
root.iconbitmap("app-icon.ico")

# Load the image
original_image = Image.open("new_ticket.jpg")
new_size = (30, 30)
resized_image = original_image.resize(new_size, Image.ANTIALIAS)
tk_image = ImageTk.PhotoImage(resized_image)

new_size1 = (30, 30)
resized_image1 = original_image.resize(new_size1, Image.ANTIALIAS)
tk_image1 = ImageTk.PhotoImage(resized_image1)

original_image2 = Image.open("dell.jpg")
new_size2 = (30, 30)
resized_image2 = original_image2.resize(new_size2, Image.ANTIALIAS)
tk_image2 = ImageTk.PhotoImage(resized_image2)

original_image3 = Image.open("stat.png")
new_size = (30, 30)
resized_image3 = original_image3.resize(new_size, Image.ANTIALIAS)
tk_image3 = ImageTk.PhotoImage(resized_image3)

row = [1]  # Store row as a mutable list
number_of_cases = [0]

zero_datetime = datetime(1970, 1, 1, 0, 0, 0)

cases = {}  # Store case start and end times here (as a dictionary of lists)
print(cases)

time_to_send = ""

# Create the "Total Accumulated Time" label
accumulated_time_label = tk.Label(root, text="Total Accumulated Time: 00:00:00")
accumulated_time_label.grid(row=row[0] + 2, column=0, padx=10, pady=10, columnspan=10, sticky="nsew")

delete_button_disabled = False


def create_case(case_number):
    row[0] += 1  # Increment the row value

    def delete_case():
        # Extract case_number from case_frame's text
        case_number = case_frame["text"]
        case_frame.destroy()
        if case_number in cases:
            cases.pop(case_number)  # Remove the case from the dictionary
            calculate_accumulated_time()  # Recalculate and update the accumulated time
            row[0] -= 1  # Update the row count
            reposition_accumulated_time_label()  # Move the accumulated time label
            number_of_cases[0] -= 1

    def update_time_difference(event):
        start_time_str = start_time_combobox.get()
        end_time_str = end_time_combobox.get()

        if start_time_str and end_time_str:
            start_time = datetime.strptime(start_time_str, "%I:%M %p")
            end_time = datetime.strptime(end_time_str, "%I:%M %p")
            time_difference = end_time - start_time
            result_label.config(text=f"Difference:   {time_difference}")
            cases[case_number] = time_difference
            calculate_accumulated_time()  # Recalculate and update the accumulated time

    # Create a label frame for each case
    case_frame = tk.LabelFrame(root, text=case_number)
    case_frame.grid(row=row[0], column=0, padx=10, pady=5, sticky="nsew")

    time_values = []
    current_time = datetime.strptime("08:00 AM", "%I:%M %p")
    end_time = datetime.strptime("06:00 PM", "%I:%M %p")

    while current_time <= end_time:
        time_values.append(current_time.strftime("%I:%M %p"))
        current_time += timedelta(minutes=15)

    if not time_values:
        time_values = ["08:00 AM"]  # Provide a default value if time_values is empty

    start_time_label = tk.Label(case_frame, text="Start Time:")
    start_time_label.grid(row=0, column=2)

    start_time_combobox = ttk.Combobox(case_frame, values=time_values, width=8)
    start_time_combobox.grid(row=0, column=3, padx=(5, 5))
    start_time_combobox.bind("<<ComboboxSelected>>", update_time_difference)

    end_time_label = tk.Label(case_frame, text="End Time:")
    end_time_label.grid(row=0, column=4)

    end_time_combobox = ttk.Combobox(case_frame, values=time_values, width=8)
    end_time_combobox.grid(row=0, column=5, padx=(5, 5))
    end_time_combobox.bind("<<ComboboxSelected>>", update_time_difference)

    result_label = tk.Label(case_frame, text="The calculated time")
    result_label.grid(row=0, column=7, padx=(5, 5))

    list_inst = ["NGS", "PCR", "qPCR", "BigFoot", "CE", "RandW", "Marray"]
    label = tk.Label(case_frame)
    label1 = tk.Label(label, bg="white", text=case_number)

    combobox = ttk.Combobox(label, values=list_inst, width=5)

    label.grid(row=0, column=0, padx=(5, 5))
    label1.grid(row=0, column=0, padx=(5, 5))
    combobox.grid(row=0, column=2, padx=(5, 5))

    button_start = tk.Button(case_frame, image=tk_image1, command=new_case)
    button_start.grid(row=0, column=8)

    button_delete = tk.Button(case_frame, image=tk_image2, command=delete_case)
    button_delete.grid(row=0, column=9, padx=(5, 5))

    # Initialize time_difference based on the initial combobox values
    update_time_difference(None)


def reposition_accumulated_time_label():
    if hasattr(accumulated_time_label, "grid_info"):
        accumulated_time_label.grid_forget()  # Remove the label from the grid
    accumulated_time_label.grid(row=row[0] + 2, column=0, padx=10, pady=10, columnspan=10, sticky="nsew")


def calculate_accumulated_time():
    global total_time
    total_time = sum(cases.values(), timedelta())
    total_time_str = str(total_time)
    if hasattr(accumulated_time_label, "grid_info"):
        accumulated_time_label.grid_forget()  # Remove the label from the grid
    accumulated_time_label.config(text=f"Total Accumulated Time: {total_time_str}")
    accumulated_time_label.grid(row=row[0] + 2, column=0, padx=10, pady=10, columnspan=10, sticky="nsew")
    print("The total time is: {} with a type of {}".format(total_time, type(total_time)))
def start():
    global user_input
    user_input = simpledialog.askstring("case number", "Please enter case number:")
    if user_input is not None:
        print("The case ID is:", user_input)
        create_case(user_input)


def new_case():
    global user_input
    global number_of_cases
    user_input = simpledialog.askstring("case number", "Please enter case number:")
    if user_input in cases.keys():
        tk.messagebox.showerror("Error", f"Case ID '{user_input}' already exists, modify the time in the existing case")
        user_input = None
    if user_input is not None:
        print("The case ID is: ", user_input)
        create_case(user_input)
        number_of_cases[0] += 1
        print("The number of cases is {}".format(number_of_cases))


# Create the "Start" button
button_start = tk.Button(root, image=tk_image1, command=start)
button_start.grid(row=0, column=0, padx=10, pady=10)

# Create the "Stat" button
button_stat = tk.Button(root, image=tk_image3, command=start)
button_stat.grid(row=0, column=1, padx=10, pady=10)

root.mainloop()

