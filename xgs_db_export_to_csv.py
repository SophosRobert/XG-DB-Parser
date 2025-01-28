import os
import sqlite3
import json
import csv
import argparse

def export_data_to_csv(directory_path):
    """
    Exports data from multiple SQLite database files in a directory to separate CSV files.

    Args:
        directory_path (str): The path to the directory containing the SQLite database files.
    """
    for filename in os.listdir(directory_path):
        if filename.endswith(".db"):
            db_path = os.path.join(directory_path, filename)
            csv_filename = os.path.splitext(filename)[0] + ".csv"
            csv_path = os.path.join(directory_path, csv_filename)

            conn = sqlite3.connect(db_path)
            c = conn.cursor()

            # Fetch data from the 'tbllog' table
            c.execute("SELECT * FROM tbllog")
            data = c.fetchall()

            # Extract the column names from the first row of data
            if data:
                column_names = []
                for row in data:
                    json_data = json.loads(row[0])
                    column_names.extend(json_data.keys())
                column_names = list(set(column_names))
                csv_data = [column_names]

                # Convert JSON data to rows
                for row in data:
                    json_data = json.loads(row[0])
                    csv_row = [json_data.get(key, "") for key in column_names]
                    csv_data.append(csv_row)

                # Write the CSV data to a file
                with open(csv_path, "w", newline="") as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerows(csv_data)

                print(f"Data exported to {csv_filename}")

            conn.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Export data from SQLite database files to CSV files.")
    parser.add_argument("directory_path", help="The path to the directory containing the SQLite database files.")
    args = parser.parse_args()

    export_data_to_csv(args.directory_path)