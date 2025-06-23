from PIL import Image

def _int_to_bin(rgb):
    return tuple(format(c, '08b') for c in rgb)

def _bin_to_int(rgb_bin):
    return tuple(int(c, 2) for c in rgb_bin)

def encode_image(image_path, data, output_path):
    img = Image.open(image_path)
    if img.mode != 'RGB':
        img = img.convert('RGB')
    pixels = img.load()

    data += "====="
    data_bin = ''.join(format(ord(i), '08b') for i in data)

    data_len = len(data_bin)
    idx = 0

    for y in range(img.height):
        for x in range(img.width):
            if idx >= data_len:
                break
            r, g, b = _int_to_bin(pixels[x, y])
            if idx < data_len:
                r = r[:-1] + data_bin[idx]
                idx += 1
            if idx < data_len:
                g = g[:-1] + data_bin[idx]
                idx += 1
            if idx < data_len:
                b = b[:-1] + data_bin[idx]
                idx += 1
            pixels[x, y] = _bin_to_int((r, g, b))
        if idx >= data_len:
            break

    img.save(output_path)

def decode_image(image_path):
    img = Image.open(image_path)
    pixels = img.load()
    data_bin = ""

    for y in range(img.height):
        for x in range(img.width):
            r, g, b = _int_to_bin(pixels[x, y])
            data_bin += r[-1] + g[-1] + b[-1]

    all_bytes = [data_bin[i:i+8] for i in range(0, len(data_bin), 8)]
    message = ""
    for byte in all_bytes:
        char = chr(int(byte, 2))
        message += char
        if message[-5:] == "=====":
            break
    return message[:-5]
