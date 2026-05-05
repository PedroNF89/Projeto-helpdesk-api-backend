# =============================================================
#  routes/tarefas.py — Rotas CRUD para o recurso "tarefas"
#
#  Blueprint é uma forma de agrupar rotas relacionadas.
#  Assim mantemos o código organizado em arquivos separados.
# =============================================================

from flask import Blueprint, request, jsonify
from database import get_connection

# Cria o blueprint com o prefixo /tarefas para todas as rotas aqui
tarefas_bp = Blueprint("tarefas", __name__, url_prefix="/tarefas")

# ── Valores permitidos para o campo status ──────────────────
STATUS_VALIDOS = {"pendente", "concluido"}


# ─────────────────────────────────────────────────────────────
#  POST /tarefas  →  Criar uma nova tarefa
# ─────────────────────────────────────────────────────────────
@tarefas_bp.route("", methods=["POST"])
def criar_tarefa():
    """
    Recebe JSON com 'titulo' (obrigatório) e 'status' (opcional).
    Insere no banco e devolve a tarefa criada com código 201.
    """
    dados = request.get_json()

    # Validação: titulo é obrigatório
    if not dados or not dados.get("titulo"):
        return jsonify({"erro": "O campo 'titulo' é obrigatório."}), 400

    titulo = dados["titulo"].strip()
    status = dados.get("status", "pendente").lower()

    # Validação: status deve ser um dos valores permitidos
    if status not in STATUS_VALIDOS:
        return jsonify({"erro": f"Status inválido. Use: {STATUS_VALIDOS}"}), 400

    conn = get_connection()
    cursor = conn.execute(
        "INSERT INTO tarefas (titulo, status) VALUES (?, ?)",
        (titulo, status),
    )
    conn.commit()

    # Busca a tarefa recém-criada para devolvê-la ao cliente
    tarefa = conn.execute(
        "SELECT * FROM tarefas WHERE id = ?", (cursor.lastrowid,)
    ).fetchone()
    conn.close()

    return jsonify(dict(tarefa)), 201


# ─────────────────────────────────────────────────────────────
#  GET /tarefas  →  Listar todas as tarefas
# ─────────────────────────────────────────────────────────────
@tarefas_bp.route("", methods=["GET"])
def listar_tarefas():
    """
    Retorna todas as tarefas do banco.
    Suporte a filtro por status via query string:
      GET /tarefas?status=pendente
    """
    status_filtro = request.args.get("status")

    conn = get_connection()

    if status_filtro:
        tarefas = conn.execute(
            "SELECT * FROM tarefas WHERE status = ?", (status_filtro,)
        ).fetchall()
    else:
        tarefas = conn.execute("SELECT * FROM tarefas").fetchall()

    conn.close()

    # Converte cada linha SQLite em dicionário Python
    return jsonify([dict(t) for t in tarefas]), 200


# ─────────────────────────────────────────────────────────────
#  PUT /tarefas/<id>  →  Atualizar uma tarefa
# ─────────────────────────────────────────────────────────────
@tarefas_bp.route("/<int:tarefa_id>", methods=["PUT"])
def atualizar_tarefa(tarefa_id):
    """
    Atualiza 'titulo' e/ou 'status' de uma tarefa existente.
    Retorna 404 se o id não existir.
    """
    dados = request.get_json()

    if not dados:
        return jsonify({"erro": "Envie um JSON com os campos a atualizar."}), 400

    conn = get_connection()

    # Verifica se a tarefa existe
    tarefa = conn.execute(
        "SELECT * FROM tarefas WHERE id = ?", (tarefa_id,)
    ).fetchone()

    if not tarefa:
        conn.close()
        return jsonify({"erro": f"Tarefa {tarefa_id} não encontrada."}), 404

    # Usa os valores recebidos ou mantém os atuais
    novo_titulo = dados.get("titulo", tarefa["titulo"]).strip()
    novo_status = dados.get("status", tarefa["status"]).lower()

    if novo_status not in STATUS_VALIDOS:
        conn.close()
        return jsonify({"erro": f"Status inválido. Use: {STATUS_VALIDOS}"}), 400

    conn.execute(
        "UPDATE tarefas SET titulo = ?, status = ? WHERE id = ?",
        (novo_titulo, novo_status, tarefa_id),
    )
    conn.commit()

    tarefa_atualizada = conn.execute(
        "SELECT * FROM tarefas WHERE id = ?", (tarefa_id,)
    ).fetchone()
    conn.close()

    return jsonify(dict(tarefa_atualizada)), 200


# ─────────────────────────────────────────────────────────────
#  DELETE /tarefas/<id>  →  Deletar uma tarefa
# ─────────────────────────────────────────────────────────────
@tarefas_bp.route("/<int:tarefa_id>", methods=["DELETE"])
def deletar_tarefa(tarefa_id):
    """
    Remove uma tarefa do banco pelo id.
    Retorna 404 se o id não existir.
    """
    conn = get_connection()

    tarefa = conn.execute(
        "SELECT * FROM tarefas WHERE id = ?", (tarefa_id,)
    ).fetchone()

    if not tarefa:
        conn.close()
        return jsonify({"erro": f"Tarefa {tarefa_id} não encontrada."}), 404

    conn.execute("DELETE FROM tarefas WHERE id = ?", (tarefa_id,))
    conn.commit()
    conn.close()

    return jsonify({"mensagem": f"Tarefa {tarefa_id} deletada com sucesso."}), 200
