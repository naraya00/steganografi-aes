from PIL import Image
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
import base64

def pad(text):
    return text + (16 - len(text) % 16) * chr(16 - len(text) % 16)

def unpad(text):
    return text[:-ord(text[-1])]

def encrypt_message(message, password):
    key = SHA256.new(password.encode()).digest()
    cipher = AES.new(key, AES.MODE_ECB)
    padded = pad(message)
    encrypted = cipher.encrypt(padded.encode())
    return base64.b64encode(encrypted).decode()

def decrypt_message(encrypted_message, password):
    key = SHA256.new(password.encode()).digest()
    cipher = AES.new(key, AES.MODE_ECB)
    decoded = base64.b64decode(encrypted_message)
    decrypted = cipher.decrypt(decoded).decode()
    return unpad(decrypted)

def encode_message(input_image_path, output_image_path, message, password):
    encrypted = encrypt_message(message, password)
    binary = ''.join(format(ord(c), '08b') for c in encrypted + '§')

    img = Image.open(input_image_path)
    if img.mode != 'RGB':
        img = img.convert('RGB')
    pixels = img.load()

    i = 0
    for y in range(img.height):
        for x in range(img.width):
            if i < len(binary):
                r, g, b = pixels[x, y]
                r = (r & ~1) | int(binary[i])
                pixels[x, y] = (r, g, b)
                i += 1
            else:
                img.save(output_image_path)
                return

def decode_message(image_path, password):
    img = Image.open(image_path)
    pixels = img.load()

    binary = ''
    for y in range(img.height):
        for x in range(img.width):
            r, g, b = pixels[x, y]
            binary += str(r & 1)

    chars = [binary[i:i+8] for i in range(0, len(binary), 8)]
    message = ''
    for c in chars:
        char = chr(int(c, 2))
        if char == '§':
            break
        message += char

    return decrypt_message(message, password)
