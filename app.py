# =============================================================
#  app.py — Ponto de entrada da aplicação Flask
#  Aqui registramos os blueprints e inicializamos o servidor.
# =============================================================

from flask import Flask
from database import init_db
from routes.tarefas import tarefas_bp
from routes.cep import cep_bp

def create_app():
    """Cria e configura a aplicação Flask."""
    app = Flask(__name__)

    # Inicializa o banco de dados (cria a tabela se não existir)
    init_db()

    # Registra os blueprints (grupos de rotas)
    app.register_blueprint(tarefas_bp)
    app.register_blueprint(cep_bp)

    return app


if __name__ == "__main__":
    app = create_app()
    # debug=True reinicia o servidor automaticamente ao salvar o arquivo
    app.run(debug=True)
