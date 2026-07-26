import tkinter as tk


# Function to update expression
def click(value):
    current = entry.get()
    entry.delete(0, tk.END)
    entry.insert(0, current + str(value))


# Function to clear display
def clear():
    entry.delete(0, tk.END)


# Function to calculate result
def calculate():
    try:
        expression = entry.get()
        result = eval(expression)
        entry.delete(0, tk.END)
        entry.insert(0, result)
    except Exception:
        entry.delete(0, tk.END)
        entry.insert(0, "Error")


# Main window
root = tk.Tk()
root.title("Calculator")
root.geometry("350x500")
root.resizable(False, False)

# Entry box
entry = tk.Entry(root, font=("Arial", 22), bd=8,
                 relief=tk.RIDGE, justify="right")
entry.grid(row=0, column=0, columnspan=4, padx=10, pady=15,
           sticky="nsew")

# Buttons
buttons = [
    ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3),
    ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3),
    ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3),
    ('0', 4, 0), ('.', 4, 1), ('=', 4, 2), ('+', 4, 3),
    ('C', 5, 0)
]

for (text, row, col) in buttons:
    if text == "=":
        button = tk.Button(root, text=text, font=("Arial", 18),
                           command=calculate, bg="lightgreen")
    elif text == "C":
        button = tk.Button(root, text=text, font=("Arial", 18),
                           command=clear, bg="tomato")
    else:
        button = tk.Button(root, text=text, font=("Arial", 18),
                           command=lambda t=text: click(t))

    button.grid(row=row, column=col, sticky="nsew",
                padx=5, pady=5, ipadx=10, ipady=15)

# Make grid responsive
for i in range(6):
    root.grid_rowconfigure(i, weight=1)

for i in range(4):
    root.grid_columnconfigure(i, weight=1)

root.mainloop()
