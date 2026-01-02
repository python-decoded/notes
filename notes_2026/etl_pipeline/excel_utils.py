from typing import Iterable
import pandas as pd


def save_to_excel_file(data: Iterable[dict], file_path):
    df = pd.DataFrame(data)
    df.to_excel(file_path, index=False)


if __name__ == "__main__":
    data = [
        {"id": 1, "name": "Alice", "age": 30},
        {"id": 2, "name": "Bob", "age": 25},
        {"id": 3, "name": "Charlie", "age": 35},
    ]
    save_to_excel_file((r for r in data), file_path="output.xlsx")
