# 📋 API de Tarefas com Flask

API REST completa construída com Python e Flask para gerenciamento de tarefas, com integração à API externa ViaCEP. Projeto criado para demonstrar boas práticas de desenvolvimento backend em eventos de tecnologia e entrevistas.

---

## 🚀 Tecnologias utilizadas

| Tecnologia | Função |
|---|---|
| **Python 3.10+** | Linguagem principal |
| **Flask 3.1** | Framework web para criar a API |
| **SQLite** | Banco de dados (arquivo local, sem instalação) |
| **ViaCEP** | API externa para consulta de CEPs |

---

## 📁 Estrutura do projeto

```
flask_tarefas/
├── app.py              # Ponto de entrada: inicializa o Flask
├── database.py         # Conexão e criação do banco de dados
├── requirements.txt    # Dependências do projeto
├── routes/
│   ├── __init__.py     # Marca a pasta como pacote Python
│   ├── tarefas.py      # Rotas CRUD das tarefas
│   └── cep.py          # Rota de consulta de CEP
└── README.md
```

---

## ⚙️ Como rodar o projeto

### 1. Clone ou baixe o projeto

```bash
git clone <url-do-repositorio>
cd flask_tarefas
```

### 2. Crie e ative um ambiente virtual

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Rode o servidor

```bash
python app.py
```

O servidor estará disponível em: **http://127.0.0.1:5000**

---

## 📡 Rotas da API

### Tarefas

| Método | Rota | Descrição |
|--------|------|-----------|
| `POST` | `/tarefas` | Criar uma nova tarefa |
| `GET` | `/tarefas` | Listar todas as tarefas |
| `GET` | `/tarefas?status=pendente` | Filtrar tarefas por status |
| `PUT` | `/tarefas/{id}` | Atualizar uma tarefa |
| `DELETE` | `/tarefas/{id}` | Deletar uma tarefa |

### CEP

| Método | Rota | Descrição |
|--------|------|-----------|
| `GET` | `/cep/{cep}` | Consultar cidade e estado pelo CEP |

---

## 🧪 Exemplos de uso

### Criar tarefa
```bash
curl -X POST http://localhost:5000/tarefas \
  -H "Content-Type: application/json" \
  -d '{"titulo": "Estudar Flask"}'
```

**Resposta:**
```json
{"id": 1, "titulo": "Estudar Flask", "status": "pendente"}
```

### Listar tarefas
```bash
curl http://localhost:5000/tarefas
```

### Atualizar tarefa
```bash
curl -X PUT http://localhost:5000/tarefas/1 \
  -H "Content-Type: application/json" \
  -d '{"status": "concluido"}'
```

### Deletar tarefa
```bash
curl -X DELETE http://localhost:5000/tarefas/1
```

### Consultar CEP
```bash
curl http://localhost:5000/cep/01310100
```

**Resposta:**
```json
{
  "cep": "01310-100",
  "cidade": "São Paulo",
  "estado": "SP",
  "bairro": "Bela Vista",
  "logradouro": "Avenida Paulista"
}
```

---

## 👤 Autor

Projeto desenvolvido para fins de aprendizado e demonstração técnica.
