import pandas as pd
import numpy as np
import json
import chardet
class DataCleaner:
    def __init__(self, schema_file):
        self.schema_file = schema_file
        self.df = None
        self.schema = None
        self.type_map = {
            "INTEGER": np.int64,
            "FLOAT": np.float64,
            "STRING": str,
            "TIMESTAMP": "datetime64[ns]"
        }

    def load_schema(self):
        with open(self.schema_file, 'r') as file:
            self.schema = json.load(file)
    

    def detect_encoding(self, csv_file):
     with open(csv_file, 'rb') as file:
        result = chardet.detect(file.read(10000))  # Read the first 10,000 bytes
        return result['encoding']

    def load_csv(self, csv_file):
        encoding = self.detect_encoding(csv_file)
        print(f"Detected encoding: {encoding}")
        self.df = pd.read_csv(csv_file, encoding=encoding)

    def clean_data(self):
        if self.df is None or self.schema is None:
            raise ValueError("CSV file or schema not loaded.")

        for column in self.schema:
            column_name = column['name']
            column_type = column['type']

            if column_name in self.df.columns:
                if column_type in self.type_map:
                    if column_type in ["INTEGER", "FLOAT"]:
                        # Replace None with 0
                        self.df[column_name] = self.df[column_name].replace({None: 0})
                        # Convert to numeric, handle errors by converting them to NaN, then fill NaN with 0
                        self.df[column_name] = pd.to_numeric(self.df[column_name], errors='coerce').fillna(0).astype(self.type_map[column_type])
                    elif column_type == "TIMESTAMP":
                        self.df[column_name] = pd.to_datetime(self.df[column_name], errors='coerce')
                    else:
                        self.df[column_name] = self.df[column_name].astype(self.type_map[column_type])

        
        for column in self.schema:
            column_name = column['name']
            if column_name not in self.df.columns:
                if column['type'] == 'STRING':
                    self.df[column_name] = ""
                elif column['type'] == 'INTEGER':
                    self.df[column_name] = 0
                elif column['type'] == 'FLOAT':
                    self.df[column_name] = 0.0
                elif column['type'] == 'TIMESTAMP':
                    self.df[column_name] = pd.NaT

    def save_cleaned_csv(self, output_csv):
        if self.df is None:
            raise ValueError("No data to save. Please clean data first.")

        self.df.to_csv(output_csv, index=False, sep='\t')
        print(f"Cleaned data has been saved to {output_csv}")

def clean_csv_using_schema(schema_file, csv_file, output_csv):
    cleaner = DataCleaner(schema_file)
    cleaner.load_schema()
    cleaner.load_csv(csv_file)
    cleaner.clean_data()
    cleaner.save_cleaned_csv(output_csv)


if __name__ == "__main__":
    schema_file = '/root/workspace/schemas/schema_bakingo_swiggy_rating_feedback.json'
    csv_file = '/root/workspace/swiggy_rating_feedbacks.csv'
    output_csv = '/root/workspace/cleaned_bakingo_swiggy_rating_feedback.csv'

    clean_csv_using_schema(schema_file, csv_file, output_csv)
