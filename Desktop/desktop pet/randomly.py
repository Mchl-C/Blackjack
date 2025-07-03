import tkinter as tk
import random

# Function to randomly select an option
def choose_random():
    if options:
        selected_option = random.choice(options)
        result_label.config(text=f"Selected: {selected_option}")
    else:
        result_label.config(text="No options available.")

# Function to add an option to the list
def add_option():
    new_option = entry.get().strip()
    if new_option:
        options.append(new_option)
        update_options_label()
        entry.delete(0, tk.END)

# Function to remove an option from the list
def remove_option():
    option_to_remove = entry.get().strip()
    if option_to_remove in options:
        options.remove(option_to_remove)
        update_options_label()
        entry.delete(0, tk.END)

# Function to update the options label
def update_options_label():
    options_label.config(text="Options: " + ", ".join(options))

def main():
    # Create the main window
    root = tk.Tk()
    root.title("Random Option Selector")

    # Set the window size
    root.geometry("200x300")  # Width x Height

    # Create an empty list of options
    global options
    options = []

    # Add a label to show the list of options
    global options_label
    options_label = tk.Label(root, text="Options: " + ", ".join(options))
    options_label.pack(pady=10)

    # Add an entry widget for adding/removing options
    global entry
    entry = tk.Entry(root)
    entry.pack(pady=5)

    # Add buttons to add or remove options
    add_button = tk.Button(root, text="Add Option", command=add_option)
    add_button.pack(pady=5)

    remove_button = tk.Button(root, text="Remove Option", command=remove_option)
    remove_button.pack(pady=5)

    # Add a button to trigger the random selection
    global result_label
    choose_button = tk.Button(root, text="Choose Randomly", command=choose_random)
    choose_button.pack(pady=10)

    # Add a label to display the selected option
    result_label = tk.Label(root, text="Selected: ")
    result_label.pack(pady=10)

    # Run the main loop
    root.mainloop()

if __name__ == "__main__":
    main()
