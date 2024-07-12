# webscrape/storage.py
import csv


class CSVStorage:
    def __init__(self, file_path) -> None:
        self.file_path = file_path

    def clear(self) -> None:
        # Clear existing file
        with open(self.file_path, mode="w") as empty:
            pass
    
    def save(self, data) -> None:
        with open(self.file_path, mode="a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(data)

    def read(self) -> list:
        data = []
        with open(self.file_path, mode="r") as file:
            reader = csv.reader(file)
            for row in reader:
                data.append(row)
        return data
