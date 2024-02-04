import numpy as np
from PIL import Image

def Encode_text(src, message, dest):
    img = Image.open(src, 'r')
    width, height = img.size
    array = np.array(list(img.getdata()))
    if img.mode == 'RGB':
        n = 3
    elif img.mode == 'RGBA':
        n = 4
    total_pixels = array.size//n

     
    b_message = ''.join([format(ord(i), "08b") for i in message])
    req_pixels = len(b_message)

    if req_pixels > total_pixels:
        print("ERROR: Need larger file size")

    else:
        index=0
        for p in range(total_pixels):
            for q in range(0, 3):
                if index < req_pixels:
                    array[p][q] = int(bin(array[p][q])[2:9] + b_message[index], 2)
                    index += 1

        array=array.reshape(height, width, n)
        enc_img = Image.fromarray(array.astype('uint8'), img.mode)
        enc_img.save(dest)
        print("Image Encoded Successfully")
        key = gen_key(index, "TEXT")
        return key

def Decode_text(src, index):

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
        for q in range(0, 3):
            hidden_bits += (bin(array[p][q])[2:][-1])
            k += 1
            if k == index:
                break
        p += 1

    hidden_bits = [hidden_bits[i:i + 8] for i in range(0, len(hidden_bits), 8)]

    # Convert binary to text
    hidden_text = ''.join([chr(int(b, 2)) for b in hidden_bits])
    print(hidden_text)
    return hidden_text


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
    