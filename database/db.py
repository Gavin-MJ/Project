import sqlite3


DATABASE_FILE:str = "database/database.db"
""" Database File Path """

ITEMS:list[dict] = [
    {'path': 'images/grape.png', 'stock': 37, 'name': 'grapes'},
    {'path': 'images/apple.png', 'stock': 15, 'name': 'apple'},
]
""" For initial Testing """

# Image grape.png Source: https://www.istockphoto.com/photo/grape-dark-grape-grapes-with-leaves-isolated-with-clipping-path-full-depth-of-field-gm803721418-139375583
# Image apple.png Source: https://www.istockphoto.com/photo/red-apple-gm495878092-78240015

class Database():
    def __init__(self):
        self.connection:sqlite3.Connection = sqlite3.connect(DATABASE_FILE)
        self.cursor:sqlite3.Cursor = self.connection.cursor()
        self.check_contents()
    
    def commit(self):
        """ Commits Database """

        self.connection.commit()

    def parseItem(self, item) -> dict:
        """ Parses Database Entry into Dict """

        return {"path": item[0], "name": item[1], "stock": item[2]} if item else None

    def items_to_list(self) -> list[dict]:
        """ Fetches All Database products and converts to dict """

        self.cursor.execute("SELECT * FROM items")

        items = self.cursor.fetchall()
        
        return [self.parseItem(item) for item in items]

    def find_item_by_name(self, name:str):
        """ Finds a product by product name """

        self.cursor.execute(f"SELECT * FROM items WHERE name COLLATE NOCASE = '{name}'")

        return self.parseItem(self.cursor.fetchone())

    def update_stock_by_name(self, name:str, stock:int):
        """ Updates products stock by product name """

        if not str(stock).isnumeric():
            return

        self.cursor.execute( f"UPDATE items SET stock = {stock} WHERE name COLLATE NOCASE = '{name}'")
        self.connection.commit()

        return self.find_item_by_name(name)

    def check_contents(self):
        """ Creates Database Table and fills items for testing. only adds items on initial setup/run """

        try:
            self.cursor.execute("""
                CREATE TABLE "items" (
                    "path"	TEXT,
                    "name"	TEXT UNIQUE,
                    "stock"	INTEGER,
                    PRIMARY KEY("name")
                );
            """)

            for item in ITEMS:
                try:
                    self.cursor.execute("""
                        INSERT INTO items (path, name, stock) VALUES (?, ?, ?)
                    """, (item["path"], item["name"], item["stock"]))
                except sqlite3.IntegrityError:
                    pass # skips if the value name already exists (duplicate products)
            
            self.commit()
        except sqlite3.OperationalError:
            pass # skips if the table already exists
        
db:Database = Database()
""" Database Object used throughout the program """
