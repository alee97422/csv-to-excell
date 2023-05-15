import tkinter as tk
from tkinter import filedialog
import pandas as pd

def browse_file():
    global df
    file_path = filedialog.askopenfilename()
    if file_path:
        df = pd.read_csv(file_path)
        column_names = df.columns.tolist()
        column_variable.set('')
        column_dropdown['menu'].delete(0, 'end')
        for column in column_names:
            column_dropdown['menu'].add_command(label=column, command=tk._setit(column_variable, column))
        update_current_data_type_label()

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

def update_current_data_type_label():
    selected_column = column_variable.get()
    if selected_column:
        current_data_type = df[selected_column].dtype
        current_data_type_label.config(text="Current Data Type: {}".format(current_data_type))
    else:
        current_data_type_label.config(text="Current Data Type: ")

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
    column_variable.set('')
    data_type_variable.set("Select Data Type")
    current_data_type_label.config(text="Current Data Type: ")

# Create Tkinter window
window = tk.Tk()
window.title("Column Destroyer")
window.geometry("800x600")

# Add a Browse button to upload the CSV file
browse_button = tk.Button(window, text="Browse", command=browse_file)
browse_button.pack()

# Add a button to convert data type
convert_button = tk.Button(window, text="Convert Data Type", command=convert_data_type)
convert_button.pack()

# Create a dropdown to select the column
column_variable = tk.StringVar(window)
column_dropdown = tk.OptionMenu(window, column_variable, "")
column_dropdown.pack()

# Create a dropdown to select the data type
data_type_variable = tk.StringVar(window)
data_type_variable.set("Select Data Type")
data_type_dropdown = tk.OptionMenu(window, data_type_variable, "String", "Integer", "Float")
data_type_dropdown.pack()

# Add a label to display the current data type
current_data_type_label = tk.Label(window, text="Current Data Type: ")
current_data_type_label.pack()

# Add a button to save the modified DataFrame as a CSV file
save_csv_button = tk.Button(window, text="Save as CSV", command=save_csv_file)
save_csv_button.pack()

# Add a button to save the modified DataFrame as an Excel file
save_xlsx_button = tk.Button(window, text="Save as Excel", command=save_xlsx_file)
save_xlsx_button.pack()

# Add a button to clear all fields
clear_button = tk.Button(window, text="Clear", command=clear_fields)
clear_button.pack()

# Start the Tkinter event loop
window.mainloop()