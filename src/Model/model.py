import hashlib
import sqlite3 as sqlite
import os

class StockManagementModel:
    def __init__(self):
        self.create_database()

    def create_database(self):
        os.makedirs('database', exist_ok=True)
        with sqlite.connect('database/Gestion_de_Stock.db') as conn:
            c = conn.cursor()
            c.execute('''CREATE TABLE IF NOT EXISTS Articles (
                            Name TEXT PRIMARY KEY,
                            Category TEXT,
                            UnitPriceForPurchase REAL,
                            UnitPriceForSell REAL,
                            Quantity INTEGER)''')
            c.execute('''CREATE TABLE IF NOT EXISTS Logs (
                            ID INTEGER PRIMARY KEY AUTOINCREMENT,
                            OperationName TEXT,
                            ItemName TEXT,
                            UnitPriceForSell_Or_Purchase REAL,
                            Quantity INTEGER,
                            TotalMoney REAL,
                            Date TEXT DEFAULT CURRENT_DATE)''')
            c.execute('''CREATE TABLE IF NOT EXISTS Users (
                            ID INTEGER PRIMARY KEY AUTOINCREMENT,
                            User_Name TEXT UNIQUE NOT NULL,
                            Password TEXT NOT NULL,
                            Role TEXT NOT NULL)''')
            c.execute("INSERT OR IGNORE INTO Users (User_Name, Password, Role) VALUES (?, ?, ?)", ("admin", self.hash_password("admin"), "admin"))

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def get_user(self, username):
        with sqlite.connect('database/Gestion_de_Stock.db') as conn:
            c = conn.cursor()
            c.execute("SELECT Password, Role FROM Users WHERE User_Name = ?", (username,))
            return c.fetchone()

    def add_article(self, name, category, price_for_purchase, unit_price):
        try:
            with sqlite.connect('database/Gestion_de_Stock.db') as conn:
                c = conn.cursor()
                c.execute("INSERT INTO Articles (Name, Category, UnitPriceForPurchase, UnitPriceForSell, Quantity) VALUES (?, ?, ?, ?, ?)",
                          (name, category, price_for_purchase, unit_price, 0))
        except sqlite.IntegrityError:
            return False
        return True

    def get_article(self, name):
        with sqlite.connect('database/Gestion_de_Stock.db') as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM Articles WHERE Name = ?", (name,))
            return c.fetchone()

    def update_article(self, name, category, price_for_purchase, unit_price):
        with sqlite.connect('database/Gestion_de_Stock.db') as conn:
            c = conn.cursor()
            c.execute("UPDATE Articles SET Category = ?, UnitPriceForPurchase = ?, UnitPriceForSell = ? WHERE Name = ?",
                      (category, price_for_purchase, unit_price, name))

    def delete_article(self, name):
        with sqlite.connect('database/Gestion_de_Stock.db') as conn:
            c = conn.cursor()
            c.execute("DELETE FROM Articles WHERE Name = ?", (name,))

    def update_stock(self, name, reason, quantity, price):
        with sqlite.connect('database/Gestion_de_Stock.db') as conn:
            c = conn.cursor()
            c.execute("SELECT Quantity FROM Articles WHERE Name = ?", (name,))
            current_quantity = c.fetchone()[0]
            if reason in ["Sale", "Damage"]:
                new_quantity = current_quantity - quantity
            else:
                new_quantity = current_quantity + quantity
            c.execute("UPDATE Articles SET Quantity = ? WHERE Name = ?", (new_quantity, name))
            c.execute("INSERT INTO Logs (OperationName, ItemName, UnitPriceForSell_Or_Purchase, Quantity, TotalMoney) VALUES (?, ?, ?, ?, ?)",
                      (reason, name, price, quantity, price * quantity))

    def search_articles(self, category, name, status):
        query = "SELECT * FROM Articles WHERE 1=1"
        params = []

        if category != "ALL":
            query += " AND Category = ?"
            params.append(category)
        if name != "ALL":
            query += " AND Name = ?"
            params.append(name)
        if status == "In stock":
            query += " AND Quantity > 0"
        elif status == "Out of stock":
            query += " AND Quantity = 0"

        with sqlite.connect('database/Gestion_de_Stock.db') as conn:
            c = conn.cursor()
            c.execute(query, params)
            return c.fetchall()

    def get_categories(self):
        with sqlite.connect('database/Gestion_de_Stock.db') as conn:
            c = conn.cursor()
            c.execute("SELECT DISTINCT Category FROM Articles")
            categories = [category[0] for category in c.fetchall()]
            if not categories:
                return 
            return categories

    def get_article_names(self):
        with sqlite.connect('database/Gestion_de_Stock.db') as conn:
            c = conn.cursor()
            c.execute("SELECT Name FROM Articles")
            names = [article[0] for article in c.fetchall()]
            if not names:
                return
            return names
    
    def get_from_articles(self):
        with sqlite.connect('database/Gestion_de_Stock.db') as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM Articles")
            return c.fetchall()
        
    def get_from_logs(self, start_date, end_date):
        with sqlite.connect('database/Gestion_de_Stock.db') as conn:
            c = conn.cursor()
            c.execute("SELECT OperationName, ItemName, SUM(Quantity), UnitPriceForSell_Or_Purchase, SUM(TotalMoney) FROM Logs WHERE Date BETWEEN ? AND ? GROUP BY OperationName, ItemName", (start_date, end_date))
            return c.fetchall()

    def check_low_stock(self, threshold):
        with sqlite.connect('database/Gestion_de_Stock.db') as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM Articles WHERE Quantity <= ?", (threshold,))
            return c.fetchall()

    def create_user(self, username, password, role):
        hashed_password = self.hash_password(password)
        try:
            with sqlite.connect('database/Gestion_de_Stock.db') as conn:
                c = conn.cursor()
                c.execute("INSERT INTO Users (User_Name, Password, Role) VALUES (?, ?, ?)", (username, hashed_password, role))
        except sqlite.IntegrityError:
            return False
        return True

    def delete_user(self, username):
        with sqlite.connect('database/Gestion_de_Stock.db') as conn:
            c = conn.cursor()
            c.execute("DELETE FROM Users WHERE User_Name = ?", (username,))

    def get_logs(self, start_date, end_date):
        with sqlite.connect('database/Gestion_de_Stock.db') as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM Logs WHERE Date BETWEEN ? AND ?", (start_date, end_date))
            return c.fetchall()
