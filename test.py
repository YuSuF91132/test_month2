import sqlite3

class DataBaseManager:
    def __init__(self, db_name):
        self.db_name = db_name
    def o_connect(self):
        try:
            connection = sqlite3.connect(self.db_name)
            print(f"Соединение с базой данных {self.db_name} открыто") 
            return connection
        except sqlite3.Error as error:
            print(f"Ошибка при открытии соединения: {error}")
            return None      

    def c_connection(self, connection):
        try:
            if connection:
                connection.close()
                print(f"Соединение с базой данных {self.db_name} закрыто")
            else:
                print("Соединение не было открыто или уже закрыто.") 
        except sqlite3.Error as error:
            print(f"Ошибка при закрытии соединения: {error}")
            
    def perform_transaction(self, operations):
        with self._connect() as conn:
            cursor = conn.cursor()
            try:
                for operation in operations:
                    cursor.execute(operation['query'], operation.get('params', []))
                conn.commit()
            except Exception as e:
                conn.rollback()
                print(f"Transaction failed: {e}")
                return False
            return True        



import sqlite3

class User:
    def __init__(self, db_name):
        self.db_name = db_name
        self._create_table()

    def _connect(self):
        return sqlite3.connect(self.db_name)

    def _create_table(self):
        with self._connect() as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    age INTEGER NOT NULL
                )
            ''')
            conn.execute('''
                CREATE TABLE IF NOT EXISTS admins (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    role TEXT NOT NULL,
                    FOREIGN KEY(user_id) REFERENCES users(id)
                )
            ''')
            conn.execute('''
                CREATE TABLE IF NOT EXISTS customers (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    address TEXT NOT NULL,
                    FOREIGN KEY(user_id) REFERENCES users(id)
                )
            ''')
    def add_user(self, name, age):
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO users (name, age) VALUES (?, ?)', (name, age))
            conn.commit()
            return cursor.lastrowid

    def get_user_by_id(self, user_id):
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
            return cursor.fetchone()

    def delete_user(self, user_id):
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM users WHERE id = ?', (user_id,))
            conn.commit()


# user_manager = User("my_database.db")
# user_id = user_manager.add_user("yt", 1)
# print(f"User added with ID: {user_id}")
# user = user_manager.get_user_by_id(user_id)
# print(f"User fetched by ID: {user}")
# user_manager.delete_user(user_id)
# print(f"User with ID {user_id} deleted.")

class Admin(User):
    def __init__(self, db_name):
        super().__init__(db_name)

    def add_admin(self, user_id, role):
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO admins (user_id, role) VALUES (?, ?)', (user_id, role))
            conn.commit()
            return cursor.lastrowid

    def get_admin_by_user_id(self, user_id):
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM admins WHERE user_id = ?', (user_id,))
            return cursor.fetchone()

    def delete_admin(self, user_id):
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM admins WHERE user_id = ?', (user_id,))
            conn.commit()


class Customer(User):
    def __init__(self, db_name):
        super().__init__(db_name)

    def add_customer(self, user_id, address):
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO customers (user_id, address) VALUES (?, ?)', (user_id, address))
            conn.commit()
            return cursor.lastrowid

    def get_customer_by_user_id(self, user_id):
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM customers WHERE user_id = ?', (user_id,))
            return cursor.fetchone()

    def delete_customer(self, user_id):
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM customers WHERE user_id = ?', (user_id,))
            conn.commit()


user_manager = User("my_database.db")
admin_manager = Admin("my_database.db")
customer_manager = Customer("my_database.db")


user_id = user_manager.add_user("John Doe", 30)
print(f"User added with ID: {user_id}")

admin_id = admin_manager.add_admin(user_id, "SuperAdmin")
print(f"Admin added with ID: {admin_id}")


customer_id = customer_manager.add_customer(user_id, "123 Main St")
print(f"Customer added with ID: {customer_id}")


admin = admin_manager.get_admin_by_user_id(user_id)
print(f"Admin fetched by user ID: {admin}")


customer = customer_manager.get_customer_by_user_id(user_id)
print(f"Customer fetched by user ID: {customer}")


admin_manager.delete_admin(user_id)
print(f"Admin with user ID {user_id} deleted.")


customer_manager.delete_customer(user_id)
print(f"Customer with user ID {user_id} deleted.")

user_manager.delete_user(user_id)
print(f"User with ID {user_id} deleted.")
