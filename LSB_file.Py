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
    total_pixels = array.size//n

    hidden_bits = ""
    k = 0 
    p = 0
    while p < total_pixels and k < index:
        for q in range(0, 3):
            hidden_bits += (bin(array[p][q])[2:][-1])
            k = k + 1
            if(k == index):
                break
        p = p + 1

    from PIL import Image
 

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


     
#********************** def Encode_binary(src, pdf, dest) **************************#
 
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
    
    with open('target.pdf', 'wb') as pdf_file:
        pdf_file.write(byte_data)

    print("PDF Decoded Successfully")
    print("done...100%")

def Decode(src, key):
    nb_pixel_used, type_encoded = extract_key(key)
    if(type_encoded == "TEXT"):
        return Decode_text(src, nb_pixel_used)
    
    if(type_encoded == "PDF"):
        return Decode_binary(src, nb_pixel_used)

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
    

#_________________________________________________main___________________________________________#
        
key = Encode_binary("src.png", "test.pdf", "dest.png")
Decode("dest.png", key)
#Encode("test.png", "Hello world", "output.png")
#Decode("output.png")