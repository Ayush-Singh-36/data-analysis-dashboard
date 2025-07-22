import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

df = None

def load_file():
    global df
    file_path = filedialog.askopenfilename(
        title="Select a CSV file",
        filetypes=[("CSV files", "*.csv"), ("All Files", "*.*")]
    )
    if file_path:
        df = pd.read_csv(file_path)
        messagebox.showinfo("Success", "CSV file loaded successfully!")
        update_column_dropdown()

def show_summary():
    if df is None:
        messagebox.showwarning("Warning", "Please load the csv file first!")
        return
    summary_text.delete(1.0, tk.END)
    summary_text.insert(tk.END, f"shape: {df.shape}\n\n")
    summary_text.insert(tk.END, f"Columns:\n{list(df.columns)}\n\n")
    summary_text.insert(tk.END, f"Missing values:\n{df.isnull().sum()}\n\n")
    summary_text.insert(tk.END, f"Data Summary (describe):\n{df.describe()}\n")

def update_column_dropdown():
    column_menu['menu'].delete(0, 'end')
    if df is not None:
        for col in df.columns:
            column_menu['menu'].add_command(label=col, command=lambda c=col: selected_column.set(c))
        if len(df.columns) > 0:
            selected_column.set(df.columns[0])

def plot_chart(chart_type):
    if df is None or selected_column.get() == "":
        messagebox.showwarning("Warning", "Please select a column first!")
        return

    column = selected_column.get()

    for widget in graph_frame.winfo_children():
        widget.destroy()

    fig, ax = plt.subplots(figsize=(4, 4))

    if chart_type == "Histogram":
        ax.hist(df[column].dropna(), bins=20, color="skyblue", edgecolor="black")
        ax.set_title(f"Histogram of {column}")
    elif chart_type == "Boxplot":
        ax.boxplot(df[column].dropna())
        ax.set_title(f"Boxplot of {column}")

    canvas = FigureCanvasTkAgg(fig, master=graph_frame)
    canvas.draw()
    canvas.get_tk_widget().pack()

root = tk.Tk()
root.title("Data Analysis Dashboard")

tk.Button(root, text="Load CSV file", command=load_file).pack(pady=5)
tk.Button(root, text="Show Data Summary", command=show_summary).pack(pady=5)

summary_text = tk.Text(root, height=15, width=80)
summary_text.pack()

tk.Label(root, text="Select column for visualisation:").pack()
selected_column = tk.StringVar()
column_menu = tk.OptionMenu(root, selected_column, "")
column_menu.pack()

tk.Button(root, text="Show Histogram", command=lambda: plot_chart("Histogram")).pack()
tk.Button(root, text="Show Boxplot", command=lambda: plot_chart("Boxplot")).pack()

graph_frame = tk.Frame(root)
graph_frame.pack()

root.mainloop()
