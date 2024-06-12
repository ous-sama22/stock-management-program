
# Stock Management App

A simple stock management application built with Python, Tkinter, and OpenPyXL.

## Features

1. Authentication:
   -Login interface for users.
2. Article Management:
   -Add an item (name, category, purchase price, sale price).
   -Update article information.
   -Delete an article (reserved for administrators).
3. Stock management:
   -Stock update (sale, damage, return, purchase).
   -Checking low stocks (items whose quantity is below a defined threshold).
4. Search and Consultation of Articles:
   -Search for items by category, name, or status (in stock, out of stock).
5. Display:
   -View stock (full list of items with their details).
   -Display statistics (detailing sales, purchases, returns, and damage operations over a specified period).
   -An option to export data in Excel format.
6. User Management (reserved for administrators):
   -Adding new users with defined roles (administrator, standard user).
   -Deleting users.

## Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/ous-sama22/stock-management-program.git
   cd stock-management-program
   ```

2. Create and activate a virtual environment:
   ```sh
   python -m venv venv
   source venv/bin/activate   # On Windows, use `venv\Scripts\activate`
   ```

3. Install the dependencies:
   ```sh
   pip install -r requirements.txt
   ```

## Usage

Run the application:
```sh
python main.py
```

## Requirements

- Python 3.7+
- Tkinter
- tkcalendar
- openpyxl
- customtkinter

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
