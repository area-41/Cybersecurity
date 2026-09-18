import pyaes

# Chave de 256 bits (32 bytes)
key = b'minha-chave-secreta-com-32-bytes'  # Conte os caracteres: precisa ter exatamente 32

# Mensagem para criptografar
plaintext = b'Ola, este e um teste de criptografia AES!'

# Inicializa o AES no modo CTR
aes = pyaes.AESModeOfOperationCTR(key)
ciphertext = aes.encrypt(plaintext)

ciphertext2 = aes.encrypt(ciphertext)  # Criptografa novamente para mostrar que o CTR gera diferentes resultados
print('Mensagem original:', plaintext.decode('utf-8'))
print('Cifrado:', ciphertext)
print('Cifrado 2:', ciphertext2)

# Descriptografia
aes_decrypter = pyaes.AESModeOfOperationCTR(key)
decrypted2 = aes_decrypter.decrypt(ciphertext2)
print('Decriptado:', decrypted2)


decrypted = aes_decrypter.decrypt(decrypted2)
print('Decriptado de novo:', decrypted.decode('utf-8'))


