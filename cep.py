# =============================================================
#  routes/cep.py — Rota de integração com a API externa ViaCEP
#
#  ViaCEP é uma API pública e gratuita que recebe um CEP
#  e devolve informações sobre o endereço.
#  Documentação: https://viacep.com.br
# =============================================================

from flask import Blueprint, jsonify
import urllib.request
import json

cep_bp = Blueprint("cep", __name__, url_prefix="/cep")


def buscar_cep(cep: str) -> dict | None:
    """
    Consulta a API ViaCEP e retorna os dados do endereço.
    Retorna None se o CEP não for encontrado ou der erro.

    Usamos urllib (biblioteca nativa do Python) para não precisar
    instalar nenhuma dependência extra para esta função.
    """
    # Remove traços e espaços que o usuário possa ter digitado
    cep_limpo = cep.replace("-", "").replace(" ", "")

    url = f"https://viacep.com.br/ws/{cep_limpo}/json/"

    try:
        with urllib.request.urlopen(url, timeout=5) as resposta:
            dados = json.loads(resposta.read().decode())

        # ViaCEP retorna {"erro": true} quando o CEP não existe
        if dados.get("erro"):
            return None

        return dados

    except Exception:
        return None


# ─────────────────────────────────────────────────────────────
#  GET /cep/<cep>  →  Consultar endereço pelo CEP
# ─────────────────────────────────────────────────────────────
@cep_bp.route("/<cep>", methods=["GET"])
def consultar_cep(cep):
    """
    Recebe um CEP na URL e devolve cidade e estado.
    Exemplo: GET /cep/01310100
    """
    # Validação básica: CEP deve ter apenas dígitos e ter 8 caracteres
    cep_limpo = cep.replace("-", "").replace(" ", "")

    if not cep_limpo.isdigit() or len(cep_limpo) != 8:
        return jsonify({"erro": "CEP inválido. Informe 8 dígitos numéricos."}), 400

    dados = buscar_cep(cep_limpo)

    if dados is None:
        return jsonify({"erro": "CEP não encontrado."}), 404

    # Retorna apenas os campos relevantes
    return jsonify({
        "cep":      dados.get("cep"),
        "cidade":   dados.get("localidade"),
        "estado":   dados.get("uf"),
        "bairro":   dados.get("bairro"),
        "logradouro": dados.get("logradouro"),
    }), 200
