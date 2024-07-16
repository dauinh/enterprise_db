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

    def remove_duplicates(self, new_file_path) -> None:
        """Asume that file only contains one column."""
        old_file = self.read()
        unique = set()
        results = []
        for row in old_file:
            url = row[0]
            if url not in unique:
                results.append(url)
                unique.add(url)

        new_save_file = CSVStorage(new_file_path)
        for row in results:
            new_save_file.save([row])
