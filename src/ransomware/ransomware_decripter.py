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

        # 1. Ler o arquivo criptografado completo
        with open(file_name, "rb") as f:
            full_data = f.read()

        # 2. SEPARAR os primeiros 16 bytes (IV) do conteúdo cifrado
        iv = full_data[:16]  # Pega os primeiros 16 bytes
        crypto_data = full_data[16:]  # Pega do byte 16 até o final

        # 3. Remover o arquivo criptografado
        os.remove(file_name)

        # 4. Derivar a mesma chave da senha do usuário
        senha_usuario = "minha_senha_curta"
        key = hashlib.sha256(senha_usuario.encode("utf-8")).digest()

        # 5. Criar o contador usando o IV extraído do próprio arquivo
        counter = pyaes.Counter(initial_value=int.from_bytes(iv, byteorder="big"))
        aes = pyaes.AESModeOfOperationCTR(key, counter=counter)

        # 6. Descriptografar APENAS o crypto_data (sem o IV)
        decrypted_data = aes.decrypt(crypto_data)

        # 7. Salvar o arquivo restaurado
        original_file = Path(file_name)  # Convert to Path object for consistency
        original_file = file_name.with_suffix('')  # Remove the extension to restore original name
        
        with open(original_file, "wb") as f:
            f.write(decrypted_data)