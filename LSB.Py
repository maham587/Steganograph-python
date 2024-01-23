from PIL import Image
import numpy as np  


# def Encode(src, message, dest):
   
#     img = Image.open(src, 'r')
#     width, height = img.size

#     #list conversion is used to obtain the image pixel values in the form of an iterative sequence
#     array = np.array(list(img.getdata()))

#     if img.mode == 'RGB':
#         n = 3
#     elif img.mode == 'RGBA':
#         n = 4
#     total_pixels = array.size//n

#     message += "$t3g0"
#     b_message = ''.join([format(ord(i), "08b") for i in message])
#     req_pixels = len(b_message)

#     if req_pixels > total_pixels:
#         print("ERROR: Need larger file size")

#     else:
#         index=0
#         for p in range(total_pixels):
#             for q in range(0, 3):
#                 if index < req_pixels:
#                     array[p][q] = int(bin(array[p][q])[2:9] + b_message[index], 2)
#                     index += 1

#         array=array.reshape(height, width, n)
#         enc_img = Image.fromarray(array.astype('uint8'), img.mode)
#         enc_img.save(dest)
#         print("Image Encoded Successfully")


# def Decode(src):

#     img = Image.open(src, 'r')
#     array = np.array(list(img.getdata()))

#     if img.mode == 'RGB':
#         n = 3
#     elif img.mode == 'RGBA':
#         n = 4
#     total_pixels = array.size//n

#     hidden_bits = ""
#     for p in range(total_pixels):
#         for q in range(0, 3):
#             hidden_bits += (bin(array[p][q])[2:][-1])

#     hidden_bits = [hidden_bits[i:i+8] for i in range(0, len(hidden_bits), 8)]

#     message = ""
#     for i in range(len(hidden_bits)):
#         if message[-5:] == "$t3g0":
#             break
#         else:
#             message += chr(int(hidden_bits[i], 2))
#     if "$t3g0" in message:
#         print("Hidden Message:", message[:-5])
#     else:
#         print("No Hidden Message Found")


# # Examples of encoding and decoding
# Encode(r'C:\Users\sambh\OneDrive\Images\Pellicule\HD-wallpaper-california-sunset.png', 'Sunset in California is wonderful ', r'C:\Users\sambh\OneDrive\Images\Pellicule\california_sunset_encoded.png')
# Decode(r'C:\Users\sambh\OneDrive\Images\Pellicule\encoded_image.png')



def encode_image(src, secret_image, dest):
    cover_img = Image.open(src, 'r')
    secret_img = Image.open(secret_image, 'r')

    cover_array = np.array(list(cover_img.getdata()))
    secret_array = np.array(list(secret_img.getdata()))

    if cover_img.mode == 'RGB':
        n = 3
    elif cover_img.mode == 'RGBA':
        n = 4
    total_pixels = cover_array.size // n

    secret_data = []
    for pixel in secret_array:
        for color in pixel[:3]:  # Using only RGB components
            secret_data.append(format(color, '08b'))  # Convert each color component to 8-bit binary

    if len(secret_data) > total_pixels * n:
        print("ERROR: Secret image too large for cover image")
        return

    secret_data += ['0' * 8] * (total_pixels * n - len(secret_data))  # Padding with zeros if necessary

    index = 0
    for p in range(total_pixels):
        for q in range(0, n):
            cover_array[p][q] = int(bin(cover_array[p][q])[2:9] + secret_data[index], 2)
            index += 1

    cover_array = cover_array.reshape(cover_img.height, cover_img.width, n)
    encoded_img = Image.fromarray(cover_array.astype('uint8'), cover_img.mode)
    encoded_img.save(dest)
    print("Image Encoded Successfully")


def decode_image(src):
    img = Image.open(src, 'r')
    array = np.array(list(img.getdata()))

    if img.mode == 'RGB':
        n = 3
    elif img.mode == 'RGBA':
        n = 4
    total_pixels = array.size // n

    hidden_data = ""
    for p in range(total_pixels):
        for q in range(0, 3):
            hidden_data += (bin(array[p][q])[2:][-1])  # Extracting the least significant bit from each color channel

    hidden_data = [hidden_data[i:i + 8] for i in range(0, len(hidden_data), 8)]

    recovered_data = []
    for binary in hidden_data:
        recovered_data.append(int(binary, 2))

    recovered_data = np.array(recovered_data).reshape((img.height, img.width, n))

    recovered_img = Image.fromarray(recovered_data.astype('uint8'), img.mode)
    recovered_img.show()


# Utilisation de ces fonctions pour cacher et extraire une image
encode_image(r'C:\Users\sambh\OneDrive\Images\Pellicule\cover_image.png', r'C:\Users\sambh\OneDrive\Images\Pellicule\secret_image_200x200.png', r'C:\Users\sambh\OneDrive\Images\Pellicule\image_in_image.png')
#decode_image(r'C:\Users\sambh\OneDrive\Images\Pellicule\image_in_image.png')
