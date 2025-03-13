import csv
import os

def parse_csv_file(filepath, preview_only=False, max_rows=5):
    """
    Parse a CSV file and return headers or full data
    
    Args:
        filepath (str): Path to the CSV file
        preview_only (bool): If True, only return headers
        max_rows (int): Maximum number of rows to return for preview
        
    Returns:
        list or dict: Headers list if preview_only=True, otherwise all data
    """
    # Check if file exists
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")
        
    # Read the CSV file
    with open(filepath, 'r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        
        try:
            # Get headers from the first row
            headers = next(csv_reader)
            
            if preview_only:
                # Return only the headers
                return headers
                
            # Read all rows
            rows = []
            for i, row in enumerate(csv_reader):
                if max_rows and i >= max_rows:
                    break
                rows.append(row)
                
            return {
                'headers': headers,
                'rows': rows
            }
            
        except StopIteration:
            # File is empty
            raise ValueError("CSV file is empty")
        except Exception as e:
            # Other parsing errors
            raise Exception(f"Error parsing CSV file: {str(e)}")

def get_column_index(column_letter):
    """
    Convert column letter to index (A=0, B=1, etc.)
    
    Args:
        column_letter (str): Column letter (A-Z)
        
    Returns:
        int: Column index
    """
    if not column_letter or len(column_letter) != 1 or not ('A' <= column_letter <= 'Z'):
        raise ValueError(f"Invalid column letter: {column_letter}. Must be a single letter A-Z.")
        
    return ord(column_letter) - ord('A')

def get_column_values(filepath, column_letter):
    """
    Get all values from a specific column in a CSV file
    
    Args:
        filepath (str): Path to the CSV file
        column_letter (str): Column letter (A-Z)
        
    Returns:
        list: All values from the specified column
    """
    # Get column index
    column_index = get_column_index(column_letter)
    
    # Read the CSV file
    with open(filepath, 'r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        
        try:
            # Skip headers
            next(csv_reader)
            
            # Get all values from the specified column
            values = []
            for row in csv_reader:
                if len(row) > column_index:
                    values.append(row[column_index].strip())
                else:
                    values.append("")  # Empty value for rows that don't have this column
                    
            return values
            
        except StopIteration:
            # File is empty or only has headers
            return []
        except Exception as e:
            # Other errors
            raise Exception(f"Error reading column {column_letter}: {str(e)}")
