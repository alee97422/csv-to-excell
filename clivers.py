import argparse
import pandas as pd

def convert_data_type(file_path, column_name, data_type):
    df = pd.read_csv(file_path)
    if column_name in df.columns:
        if data_type == "string":
            df[column_name] = df[column_name].astype(str)
        elif data_type == "integer":
            df[column_name] = pd.to_numeric(df[column_name], errors='coerce').astype(pd.Int64Dtype())
        elif data_type == "float":
            df[column_name] = pd.to_numeric(df[column_name], errors='coerce').astype(float)
        
        return df
    else:
        print("Column '{}' does not exist in the CSV file.".format(column_name))
        return None

def save_csv(df, file_path):
    df.to_csv(file_path, index=False)
    print("CSV file saved successfully!")

def save_xlsx(df, file_path):
    with pd.ExcelWriter(file_path, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False)
        writer.book.use_zip64()
        for column in df.columns:
            max_len = df[column].astype(str).map(len).max()
            writer.sheets['Sheet1'].set_column(column + ':' + column, max_len + 2)
    print("Excel file saved successfully!")

def main():
    parser = argparse.ArgumentParser(description="CSV Data Type Conversion")
    parser.add_argument("file_path", help="Path to the CSV file")
    parser.add_argument("column_name", help="Name of the column to convert")
    parser.add_argument("data_type", help="Data type to convert to (string, integer, or float)")
    parser.add_argument("--save-csv", help="Path to save the modified DataFrame as a CSV file")
    parser.add_argument("--save-xlsx", help="Path to save the modified DataFrame as an Excel file")
    args = parser.parse_args()

    df = convert_data_type(args.file_path, args.column_name, args.data_type)
    if df is not None:
        if args.save_csv:
            save_csv(df, args.save_csv)
        if args.save_xlsx:
            save_xlsx(df, args.save_xlsx)

if __name__ == "__main__":
    main()
