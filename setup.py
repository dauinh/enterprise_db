from setuptools import setup, find_packages

setup(
    name="muji_db",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "mysql-connector-python==8.4.0",
        "python-dotenv==1.0.1",
        "selenium==4.22.0",
        "pytest==8.2.2" "setuptools==70.3.0",
    ],
    entry_points={
        "console_scripts": [
            # Define any console scripts here if needed
        ],
    },
    author="dauinh",
    description="A project containing a web scraper and other modules",
    url="https://github.com/dauinh/muji_db",
)
