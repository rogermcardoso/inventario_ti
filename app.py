from flask import Flask, render_template, request, redirect, url_for, g, abort
import sqlite3
from datetime import datetime

DATABASE = "inventario_ti.db"

app = Flask(__name__)


# -------------------------------
# Banco
# -------------------------------

def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(error):
    db = g.pop("db", None)
    if db is not None:
        db.close()


# -------------------------------
# Home
# -------------------------------

@app.route("/")
def index():
    return render_template("index.html")


# -------------------------------
# Equipamentos
# -------------------------------

@app.route("/equipamentos")
def equipamentos():
    db = get_db()

    dados = db.execute("""
        SELECT e.*,
               u.nome AS usuario_atual
        FROM equipamentos e
        LEFT JOIN usuarios u
           ON e.usuario_atual_id = u.id
        ORDER BY e.patrimonio
    """).fetchall()

    return render_template("equipamentos.html", dados=dados)


@app.route("/equipamentos/novo", methods=["GET", "POST"])
def novo_equipamento():
    db = get_db()

    if request.method == "POST":
        db.execute("""
            INSERT INTO equipamentos
            (patrimonio, tipo, marca, modelo, numero_serie,
             sistema_operacional, memoria, ano_compra,
             status_maquina, observacao)
            VALUES (?,?,?,?,?,?,?,?,?,?)
        """, (
            request.form["patrimonio"],
            request.form["tipo"],
            request.form["marca"],
            request.form["modelo"],
            request.form["numero_serie"],
            request.form["sistema_operacional"],
            request.form["memoria"],
            request.form["ano_compra"],
            request.form["status_maquina"],
            request.form["observacao"]
        ))

        db.commit()
        return redirect(url_for("equipamentos"))

    return render_template("equipamento_form.html")


@app.route("/equipamentos/<patrimonio>")
def detalhe_equipamento(patrimonio):
    db = get_db()

    eq = db.execute("""
        SELECT e.*,
               u.nome AS usuario_atual
        FROM equipamentos e
        LEFT JOIN usuarios u
            ON e.usuario_atual_id = u.id
        WHERE e.patrimonio = ?
    """, (patrimonio,)).fetchone()

    if not eq:
        abort(404)

    return render_template("equipamento_detalhe.html", e=eq)


# -------------------------------
# Usuários
# -------------------------------

@app.route("/usuarios")
def usuarios():
    db = get_db()
    dados = db.execute("SELECT * FROM usuarios ORDER BY nome").fetchall()
    return render_template("usuarios.html", dados=dados)


@app.route("/usuarios/novo", methods=["GET", "POST"])
def novo_usuario():
    db = get_db()

    if request.method == "POST":
        db.execute("""
            INSERT INTO usuarios
            (nome, cargo, centro_custo, departamento, termo_assinado)
            VALUES (?,?,?,?,?)
        """, (
            request.form["nome"],
            request.form["cargo"],
            request.form["centro_custo"],
            request.form["departamento"],
            request.form["termo_assinado"]
        ))

        db.commit()
        return redirect(url_for("usuarios"))

    return render_template("usuario_form.html")


# -------------------------------
# Movimentações
# -------------------------------

@app.route("/movimentacoes")
def movimentacoes():
    db = get_db()

    dados = db.execute("""
        SELECT m.*,
               u1.nome AS usuario_anterior,
               u2.nome AS usuario_novo
        FROM movimentacoes m
        LEFT JOIN usuarios u1 ON u1.id = m.usuario_anterior_id
        LEFT JOIN usuarios u2 ON u2.id = m.usuario_novo_id
        ORDER BY m.data_movimentacao DESC
    """).fetchall()

    return render_template("movimentacoes.html", dados=dados)


@app.route("/movimentacoes/nova", methods=["GET", "POST"])
def nova_movimentacao():
    db = get_db()

    patrimonio = request.args.get("patrimonio")

    usuarios = db.execute(
        "SELECT id, nome FROM usuarios ORDER BY nome"
    ).fetchall()

    equipamento = None
    if patrimonio:
        equipamento = db.execute("""
            SELECT *
            FROM equipamentos
            WHERE patrimonio = ?
        """, (patrimonio,)).fetchone()

    if request.method == "POST":

        patrimonio = request.form["patrimonio"]
        usuario_novo_id = request.form.get("usuario_novo_id") or None
        tipo = request.form["tipo_movimentacao"]
        obs = request.form["observacao"]

        eq = db.execute("""
            SELECT usuario_atual_id
            FROM equipamentos
            WHERE patrimonio = ?
        """, (patrimonio,)).fetchone()

        if not eq:
            abort(400)

        usuario_anterior_id = eq["usuario_atual_id"]

        db.execute("""
            INSERT INTO movimentacoes
            (patrimonio,
             usuario_anterior_id,
             usuario_novo_id,
             tipo_movimentacao,
             data_movimentacao,
             observacao)
            VALUES (?,?,?,?,?,?)
        """, (
            patrimonio,
            usuario_anterior_id,
            usuario_novo_id,
            tipo,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            obs
        ))

        # atualiza o equipamento
        db.execute("""
            UPDATE equipamentos
            SET usuario_atual_id = ?
            WHERE patrimonio = ?
        """, (usuario_novo_id, patrimonio))

        db.commit()

        return redirect(url_for("movimentacoes"))

    return render_template(
        "movimentacao_form.html",
        usuarios=usuarios,
        equipamento=equipamento,
        patrimonio=patrimonio
    )


# -------------------------------
# Histórico por patrimônio
# -------------------------------

@app.route("/historico/<patrimonio>")
def historico_patrimonio(patrimonio):
    db = get_db()

    equipamento = db.execute("""
        SELECT *
        FROM equipamentos
        WHERE patrimonio = ?
    """, (patrimonio,)).fetchone()

    if not equipamento:
        abort(404)

    historico = db.execute("""
        SELECT m.*,
               u1.nome AS usuario_anterior,
               u2.nome AS usuario_novo
        FROM movimentacoes m
        LEFT JOIN usuarios u1 ON u1.id = m.usuario_anterior_id
        LEFT JOIN usuarios u2 ON u2.id = m.usuario_novo_id
        WHERE m.patrimonio = ?
        ORDER BY m.data_movimentacao DESC
    """, (patrimonio,)).fetchall()

    return render_template(
        "historico_patrimonio.html",
        equipamento=equipamento,
        dados=historico
    )


# -------------------------------
# Main
# -------------------------------

if __name__ == "__main__":
    app.run(debug=True)