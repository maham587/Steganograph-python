
import encode_decode_binary

import encode_decode_text
def Decode(src, key):
    nb_pixel_used, type_encoded = extract_key(key)
    if(type_encoded == "TEXT"):
        return encode_decode_text.Decode_text(src, nb_pixel_used)
    
    if(type_encoded == "PDF"):
        return encode_decode_binary.Decode_binary(src, nb_pixel_used)

def gen_key(nb_pixel_used, type_encoded):
    return str(nb_pixel_used) + '@' + type_encoded

def extract_key(key_string):
    components = key_string.split('@')
    if len(components) == 2:
        nb_pixel_used = int(components[0])
        type_encoded = components[1]
        return nb_pixel_used, type_encoded
    else:
        raise ValueError("Invalid key formaat")