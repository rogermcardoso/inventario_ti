import mysql.connector
import sqlite3
from datetime import datetime

# ----------------------------
# Configurações
# ----------------------------

OCS_CONFIG = {
    "host": "SEU_IP_OU_HOST_OCS",
    "user": "SEU_USUARIO",
    "password": "SUA_SENHA",
    "database": "ocsweb"
}

SQLITE_DB = "inventario_ti.db"


# ----------------------------
# Conexões
# ----------------------------

def conectar_ocs():
    return mysql.connector.connect(**OCS_CONFIG)


def conectar_sqlite():
    conn = sqlite3.connect(SQLITE_DB)
    conn.row_factory = sqlite3.Row
    return conn


# ----------------------------
# Sincronização
# ----------------------------

def main():

    print("Iniciando sincronização com OCS...")

    ocs = conectar_ocs()
    local = conectar_sqlite()

    ocs_cur = ocs.cursor(dictionary=True)
    local_cur = local.cursor()

    # Consulta mínima e segura no OCS
    # (nomes padrões do OCS Inventory NG)
    ocs_cur.execute("""
        SELECT
            h.SERIALNUMBER,
            h.OSNAME,
            h.MEMORY
        FROM hardware h
        WHERE h.SERIALNUMBER IS NOT NULL
          AND h.SERIALNUMBER <> ''
    """)

    registros = ocs_cur.fetchall()

    atualizados = 0
    ignorados = 0

    for r in registros:

        numero_serie = r["SERIALNUMBER"]
        sistema = r["OSNAME"]
        memoria = r["MEMORY"]

        # verifica se existe no seu inventário
        local_cur.execute("""
            SELECT patrimonio
            FROM equipamentos
            WHERE numero_serie = ?
        """, (numero_serie,))

        eq = local_cur.fetchone()

        if not eq:
            ignorados += 1
            continue

        local_cur.execute("""
            UPDATE equipamentos
               SET sistema_operacional = ?,
                   memoria = ?
             WHERE numero_serie = ?
        """, (
            sistema,
            str(memoria) if memoria is not None else None,
            numero_serie
        ))

        atualizados += 1

    local.commit()

    print("----------------------------------")
    print(f"Registros encontrados no OCS : {len(registros)}")
    print(f"Equipamentos atualizados     : {atualizados}")
    print(f"Equipamentos não encontrados : {ignorados}")
    print("Sincronização finalizada em :", datetime.now())

    ocs_cur.close()
    local_cur.close()
    ocs.close()
    local.close()


if __name__ == "__main__":
    main()