"""
This module contains the FileProcessor class, which is used to process files.
"""
import os
import tempfile
from pathlib import Path
from typing import BinaryIO
import pandas as pd


class FileProcessor:
    """
    This class is used to process files.
    """

    def __init__(self, file_content: BinaryIO, file_type: str, file_name: str):
        self.file_content = file_content
        self.file_type = file_type
        self.file_name = file_name

    def save_file_to_tmp(self) -> str:
        """
        Save file content to a temporary file with appropriate extension based on file type.

        Args:
            file_content (bytes): The file content as bytes
            file_type (str): MIME type of the file (e.g., 'text/csv', 
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            original_filename (str, optional): Original filename for reference

        Returns:
            str: Path to the saved temporary file
        """
        # Create tmp directory in current directory if it doesn't exist
        tmp_dir = Path.cwd() / 'tmp'
        tmp_dir.mkdir(exist_ok=True)

        # Map MIME types to file extensions
        mime_to_extension = {
            'text/csv': '.csv',
            'application/vnd.ms-excel': '.xls',
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': '.xlsx'
        }

        # Get extension from MIME type, fallback to original filename extension
        extension = mime_to_extension.get(self.file_type.lower())

        if not extension and self.file_name:
            # Fallback: extract extension from original filename
            original_path = Path(self.file_name)
            extension = original_path.suffix

        if not extension:
            # Final fallback: default to .csv
            extension = '.csv'

        # Create temporary file with appropriate extension
        temp_file = tempfile.NamedTemporaryFile(
            mode='wb',
            suffix=extension,
            prefix='upload_',
            dir=tmp_dir,
            delete=False
        )

        try:
            # Write content to file
            temp_file.write(self.file_content.read())
            temp_file.flush()

            print(f"File saved to: {temp_file.name}")
            return temp_file.name

        except Exception as e:
            print(f"Error saving file: {e}")
            # Clean up on error
            temp_file.close()
            if os.path.exists(temp_file.name):
                os.unlink(temp_file.name)
            raise
        finally:
            temp_file.close()

    def format_for_nicegui_table(self, file_path: str):
        """
        Format DataFrame data for NiceGUI table display.

        Args:
            file_path (str): Path to the file
            head_rows (int): Number of rows to include (default: 5)

        Returns:
            tuple: (columns_list, rows_list) formatted for NiceGUI table
        """
        if file_path.endswith('.csv'):
            df = pd.read_csv(file_path)
        elif file_path.endswith('.xlsx') or file_path.endswith('.xls'):
            df = pd.read_excel(file_path)
        else:
            raise ValueError(f"Unsupported file type: {file_path}")

        # Get the csv columns

        df_columns = df.columns.tolist()

        # Get the csv rows
        rows = df.to_dict(orient='records')

        # Format columns for NiceGUI table
        columns = []
        for col_name in df_columns:
            column_config = {
                'name': col_name,
                'label': col_name,
                'field': col_name,
                'required': True,
                'align': 'left',
                'sortable': True
            }
            columns.append(column_config)

        # Format rows for NiceGUI table
        rows = []
        for _, row in df.iterrows():
            row_dict = {}
            for col_name in df_columns:
                # Convert numpy/pandas types to Python native types
                value = row[col_name]
                if pd.isna(value):
                    row_dict[col_name] = None
                elif isinstance(value, (int, float)):
                    row_dict[col_name] = value
                else:
                    row_dict[col_name] = str(value)
            rows.append(row_dict)

        return columns, rows

    def process_csv(self, file_path: str):
        """
        Process the CSV file.

        Read CSV file and return head and body separately

        Args:
            head_rows (int): Number of rows to include in the head (default: 5)

        Returns:
            tuple: (head_dataframe, body_dataframe)
        """
        # Read the entire CSV file
        df = pd.read_csv(file_path)

        # Get the head (first few rows)
        columns = df.columns.tolist()

        # Get the body (all data)
        body = df

        return columns, body

    def process_excel(self, file_path: str):
        """
        Read Excel file and return head and body separately

        Args:
            head_rows (int): Number of rows to include in the head (default: 5)

        Returns:
            tuple: (head_dataframe, body_dataframe)
        """
        # Read the entire Excel file
        df = pd.read_excel(file_path)

        # Get the head (first few rows)
        columns = df.columns.tolist()

        # Get the body (all data)
        body = df

        return columns, body
        