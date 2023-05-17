import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import pandas as pd
import xlsxwriter

# Define global variables
df = pd.DataFrame()
columns_label = None
rows_label = None

def browse_file():
    global df
    global columns_label
    global rows_label
    
    file_path = filedialog.askopenfilename()
    if file_path:
        df = pd.read_csv(file_path)
        column_names = df.columns.tolist()
        column_variable.set('')
        column_dropdown['menu'].delete(0, 'end')
        for column in column_names:
            column_dropdown['menu'].add_command(label=column, command=tk._setit(column_variable, column))
        update_number_of_columns_rows_label()
        update_sample_data_label()  # Call the function to update the sample data

def update_number_of_columns_rows_label():
    global df
    global columns_label
    global rows_label
    
    if df is not None:
        columns = df.shape[1]
        rows = df.shape[0]
        columns_label.config(text="Number of Columns: {}".format(columns))
        rows_label.config(text="Number of Rows: {}".format(rows))
    else:
        columns_label.config(text="Number of Columns: ")
        rows_label.config(text="Number of Rows: ")

def convert_data_type():
    selected_column = column_variable.get()
    selected_data_type = data_type_variable.get()
    if selected_column and selected_data_type:
        # Perform data type conversion
        if selected_data_type == "String":
            df[selected_column] = df[selected_column].astype(str)
        elif selected_data_type == "Integer":
            df[selected_column] = pd.to_numeric(df[selected_column], errors='coerce').astype(pd.Int64Dtype())
        elif selected_data_type == "Float":
            df[selected_column] = pd.to_numeric(df[selected_column], errors='coerce').astype(float)

        print("Converting column '{}' to data type: {}".format(selected_column, selected_data_type))
        update_current_data_type_label()

def update_current_data_type_label(*args):
    selected_column = column_variable.get()
    if selected_column:
        current_data_type = df[selected_column].dtype
        current_data_type_label.config(text="Current Data Type: {}".format(current_data_type))
    else:
        current_data_type_label.config(text="Current Data Type: ")


def update_sample_data_label():
    sample_data_text.configure(state="normal")
    sample_data_text.delete("1.0", tk.END)
    sample_data_text.insert(tk.END, "Sample Data:\n\n")
    if not df.empty:
        max_display_length = 10000  # Specify the maximum number of characters to display
        sample_data = df.head(10).to_string(index=False)
        if len(sample_data) > max_display_length:
            sample_data = sample_data[:max_display_length] + "..."  # Truncate the text
        sample_data_text.insert(tk.END, sample_data)
    sample_data_text.configure(state="disabled")

    
def save_csv_file():
    file_path = filedialog.asksaveasfilename(defaultextension='.csv')
    if file_path:
        df.to_csv(file_path, index=False)
        print("CSV file saved successfully!")

def save_xlsx_file():
    global df
    file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel Files", "*.xlsx")])
    if file_path:
        with pd.ExcelWriter(file_path, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False)
            writer.book.use_zip64()
            worksheet = writer.sheets['Sheet1']
            for column in df.columns:
                max_len = df[column].astype(str).map(len).max()
                if column is not None:
                    worksheet.set_column(column + ':' + column, max_len + 2)
        print("Excel file saved successfully!")

def clear_fields():
    global sample_data_text

    # Rest of the code to clear the fields
    column_variable.set('')
    data_type_variable.set("Select Data Type")
    current_data_type_label.config(text="Current Data Type: ")
    columns_label.config(text="Number of Columns: ")
    rows_label.config(text="Number of Rows: ")
    
    
    # Clear sample data
    if sample_data_text:
        sample_data_text.configure(state="normal")
        sample_data_text.delete("1.0", tk.END)
        sample_data_text.insert(tk.END, "Sample Data:\n\n")
        sample_data_text.configure(state="disabled")

# Create Tkinter window
window = tk.Tk()
window.title("Column Destroyer")
window.geometry("800x600")
window.resizable(800, 600)

# Create a style for labels with purple lettering
style = ttk.Style()
style.configure("DarkLabel.TLabel",
                foreground="#b64fcf",  # Set foreground color to purple
                #background="#1f1f1f",  # Set background color to dark gray
                font=("Helvetica", 12))

# Create a style for buttons with purple lettering
style.configure("DarkButton.TButton",
                foreground="#b64fcf",  # Set foreground color to purple
                #background="#1f1f1f",  # Set background color to dark gray
                font=("Helvetica", 12))

# Create a style for dropdowns with purple lettering
style.configure("Dark.TCombobox",
                foreground="#b64fcf",  # Set foreground color to purple
                #background="#1f1f1f",  # Set background color to dark gray
                font=("Helvetica", 12))
# Browse button
browse_button = tk.Button(window, text="Upload CSV Files", command=browse_file)
browse_button.grid(row=0, column=0, padx=10, pady=10)

# Convert button
convert_button = tk.Button(window, text="Convert Data Type", command=convert_data_type)
convert_button.grid(row=1, column=1, padx=10, pady=10)


# Column dropdown
column_variable = tk.StringVar(window)
column_dropdown = ttk.OptionMenu(window, column_variable, "", style="Dark.TCombobox")
column_dropdown.grid(row=1, column=0, padx=10, pady=10)
# Add the trace() method after creating the column_dropdown widget
column_variable.trace("w", update_current_data_type_label)

# Data type dropdown
data_type_variable = tk.StringVar(window)
data_type_variable.set("Target Data Type")
data_type_dropdown = tk.OptionMenu(window, data_type_variable, "String", "Integer", "Float")
data_type_dropdown.grid(row=0, column=1, padx=10, pady=10)

# Current data type label
current_data_type_label = tk.Label(window, text="Current Data Type: ")
current_data_type_label.grid(row=2, column=0, columnspan=2, padx=10, pady=10)


# Initialize labels for number of columns and rows
columns_label_text = tk.StringVar()
columns_label_text.set("Number of Columns: ")
columns_label = ttk.Label(window, text="Number of Columns: ", style="DarkLabel.TLabel")
columns_label.grid(row=3, column=0, sticky=tk.W)

rows_label_text = tk.StringVar()
rows_label_text.set("Number of Rows: ")
rows_label = ttk.Label(window, text="Number of Rows: ", style="DarkLabel.TLabel")
rows_label.grid(row=3, column=1, sticky=tk.W)

# Sample data label
sample_data_frame = tk.Frame(window)
sample_data_frame.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

sample_data_scrollbar = tk.Scrollbar(sample_data_frame)
sample_data_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

sample_data_text = tk.Text(sample_data_frame, height=10, width=50)
sample_data_text.pack(side=tk.LEFT, fill=tk.Y)

sample_data_scrollbar.config(command=sample_data_text.yview)
sample_data_text.config(yscrollcommand=sample_data_scrollbar.set)

sample_data_text.insert(tk.END, "Sample Data:\n\n")
sample_data_text.config(state=tk.DISABLED)


# Save as CSV button
save_csv_button = tk.Button(window, text="Save as CSV", command=save_csv_file)
save_csv_button.grid(row=5, column=0, padx=10, pady=10)

# Save as Excel button
save_xlsx_button = tk.Button(window, text="Save as Excel", command=save_xlsx_file)
save_xlsx_button.grid(row=5, column=1, padx=10, pady=10)

# Clear button
clear_button = tk.Button(window, text="Clear", command=clear_fields)
clear_button.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

# Start the Tkinter event loop
window.mainloop()

