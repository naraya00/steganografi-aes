from PIL import Image

def encode_LSB(image_path, data, output_path):
    img = Image.open(image_path).convert("RGB")

    encoded = img.copy()
    binary_data = ''.join(format(ord(c), '08b') for c in data) + '1111111111111110'  # EOF marker
    data_index = 0

    for y in range(img.height):
        for x in range(img.width):
            if data_index >= len(binary_data):
                break
            pixel = list(img.getpixel((x, y)))
            for n in range(3):  # RGB
                if data_index < len(binary_data):
                    pixel[n] = pixel[n] & ~1 | int(binary_data[data_index])
                    data_index += 1
            encoded.putpixel((x, y), tuple(pixel))
        if data_index >= len(binary_data):
            break

    encoded.save(output_path)

def decode_LSB(image_path):
    img = Image.open(image_path).convert("RGB")

    binary_data = ""
    for y in range(img.height):
        for x in range(img.width):
            pixel = img.getpixel((x, y))
            for n in range(3):
                binary_data += str(pixel[n] & 1)

    all_bytes = [binary_data[i:i+8] for i in range(0, len(binary_data), 8)]
    decoded = ""
    for byte in all_bytes:
        if byte == '11111110':  # EOF marker
            break
        decoded += chr(int(byte, 2))
    return decoded
