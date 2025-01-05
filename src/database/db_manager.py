import sqlite3

class DBManager:
    def __init__(self, db_name="finance.db"):
        self.conn = sqlite3.connect(db_name)
        self.create_table()
        self.update_table()

    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY,
            descricao TEXT,
            valor REAL,
            data TEXT,
            categoria TEXT
        )
        """
        self.conn.execute(query)
        self.conn.commit()

    def add_transaction(self, descricao, valor, data, categoria):
        query = "INSERT INTO transactions (descricao, valor, data, categoria) VALUES (?, ?, ?, ?)"
        self.conn.execute(query, (descricao, valor, data, categoria))
        self.conn.commit()

    def get_transaction_by_id(self, transacao_id):
        query = "SELECT * FROM transactions WHERE id = ?"
        cursor = self.conn.execute(query, (transacao_id,))
        return cursor.fetchone()

    def get_transactions(self):
        query = "SELECT * FROM transactions"
        cursor = self.conn.execute(query)
        return cursor.fetchall()

    def delete_transaction_by_id(self, transacao_id):
        query = "DELETE FROM transactions WHERE id = ?"
        self.conn.execute(query, (transacao_id,))
        self.conn.commit()

    def update_transaction(self, transacao_id, descricao, valor, categoria):
        query = """
        UPDATE transactions
        SET descricao = ?, valor = ?, categoria = ?
        WHERE id = ?
        """
        self.conn.execute(query, (descricao, valor, categoria, transacao_id))
        self.conn.commit()

    def update_table(self):
        try:
            self.conn.execute("ALTER TABLE transactions ADD COLUMN categoria TEXT")
            self.conn.commit()
        except sqlite3.OperationalError:
            pass  # A coluna já existe