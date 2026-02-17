import sqlite3
import os

DB_NAME = "inventario_ti.db"
SCHEMA_FILE = "schema.sql"


def main():

    # opcional: apagar o banco antigo para evitar conflitos
    if os.path.exists(DB_NAME):
        os.remove(DB_NAME)
        print("Banco antigo removido.")

    with open(SCHEMA_FILE, "r", encoding="utf-8") as f:
        schema = f.read()

    conn = sqlite3.connect(DB_NAME)

    try:
        conn.executescript(schema)
        conn.commit()
        print("Banco criado com sucesso.")
    finally:
        conn.close()


if __name__ == "__main__":
    main()