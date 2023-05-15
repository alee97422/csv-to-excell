
# CSV Data Type Conversion

This program allows you to convert the data type of a column in a CSV file. It provides two interfaces: GUI (Graphical User Interface) and CLI (Command-Line Interface).

## GUI Version

### Prerequisites
- Python 3.x installed
- Required Python packages: tkinter, pandas, xlsxwriter

### Usage
1. Run the script `guivers.py` using the following command:
   ```bash
   python guivers.py

The GUI window will open.

Click the "Browse" button to select a CSV file from your local machine.

Select the column from the dropdown list that you want to convert.

Select the desired data type from the dropdown list (String, Integer, or Float).

Click the "Convert Data Type" button to perform the conversion.

The current data type of the selected column will be displayed below the dropdowns.

To save the modified DataFrame as a CSV file, click the "Save as CSV" button.

To save the modified DataFrame as an Excel file, click the "Save as Excel" button.

To clear all fields and start a new conversion, click the "Clear" button.

## CLI Version

### Prerequisites
Python 3.x installed
Required Python packages: pandas, xlsxwriter

### Usage
Run the script cli vers.py using the following command:

python clivers.py file_path column_name data_type [--save-csv SAVE_CSV] [--save-xlsx SAVE_XLSX]
Replace file_path with the path to the CSV file you want to convert.

Replace column_name with the name of the column you want to convert.

Replace data_type with the desired data type to convert to (string, integer, or float).

Optional: Specify the --save-csv flag followed by the desired path to save the modified DataFrame as a CSV file.

Optional: Specify the --save-xlsx flag followed by the desired path to save the modified DataFrame as an Excel file.

Execute the command to perform the conversion and save the modified DataFrame (if specified).

The program will print messages indicating the progress and success of the conversion and file saving.

