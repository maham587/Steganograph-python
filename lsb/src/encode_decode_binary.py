import numpy as np
from PIL import Image

def Encode_binary(src, pdf, dest):
    img = Image.open(src, 'r')
    width, height = img.size
    if img.mode == 'RGB':
        n = 3
    elif img.mode == 'RGBA':
        n = 4
    array = np.array(list(img.getdata()))
    total_pixels = array.size // n

    with open(pdf, 'rb') as file:
        binary = file.read()
    
    # Convert binary data to binary string
    binary = ''.join(format(byte, '08b') for byte in binary)

    # Check if the image can contain the binary data
    
    req_pixels = len(binary)
    print(req_pixels, total_pixels)
    if req_pixels > 3 * total_pixels:
        print("ERROR: Need larger file size")
    else:
        index = 0
        for p in range(total_pixels):
            for q in range(n):
                if index < req_pixels:
                    array[p][q] = int(bin(array[p][q])[2:9] + binary[index], 2)
                    index += 1

        array = array.reshape(height, width, n)
        enc_img = Image.fromarray(array.astype('uint8'), img.mode)
        enc_img.save(dest)
        print("PDF Encoded Successfully")
        print(index)
        key = gen_key(index, "PDF")
        return key

def Decode_binary(src, index):
    img = Image.open(src, 'r')
    array = np.array(list(img.getdata()))

    if img.mode == 'RGB':
        n = 3
    elif img.mode == 'RGBA':
        n = 4
    total_pixels = array.size // n
    hidden_bits = ""
    k = 0
    p = 0
    while p < total_pixels and k < index:
        for q in range(n):
            k += 1
            hidden_bits += (bin(array[p][q])[2:][-1])
            if k == index:
                break
        p += 1

    hidden_bits = [hidden_bits[i:i+8] for i in range(0, len(hidden_bits), 8)]
     
    binary_data = ''.join(hidden_bits)
    byte_data = bytearray(int(binary_data[i:i+8], 2) for i in range(0, len(binary_data), 8))
    
    with open('../outputs/output.pdf', 'wb') as pdf_file:
        pdf_file.write(byte_data)

    print("PDF Decoded Successfully")
    print("done...100%")


def gen_key(nb_pixel_used, type_encoded):
    return str(nb_pixel_used) + '@' + type_encoded

def extract_key(key_string):
    components = key_string.split('@')
    if len(components) == 2:
        nb_pixel_used = int(components[0])
        type_encoded = components[1]
        return nb_pixel_used, type_encoded
    else:
        raise ValueError("Invalid key format")
    