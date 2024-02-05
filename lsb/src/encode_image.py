import os
from PIL import Image
from utils import rgb_to_binary, add_leading_zeros



def get_binary_pixel_values(image, width, height):
    """
    Retrieves a string of concatenated binary representations of RGB channel values of all pixels in an image.

    Args:
        image:  An RGB image
        width:  Width of the image
        height: Height of the image

    Returns:
        A string with concatenated binary numbers representing the RGB channel values of all pixels in the image
        where each binary number representing one channel value is 8 bits long, padded with leading zeros 
        when necessary. Therefore, each pixel in the image is represented by a 24-bit long binary sequence.
    """
    hidden_image_pixels = ''
    for col in range(width):
        for row in range(height):
            pixel = image[col, row]
            red, green, blue = pixel[0], pixel[1], pixel[2]
            r_binary, g_binary, b_binary = rgb_to_binary(red, green, blue)
            hidden_image_pixels += r_binary + g_binary + b_binary
    return hidden_image_pixels

def change_binary_values(visible_image, hidden_image_pixels, width_visible, height_visible, width_hidden, height_hidden):
    """
    Replaces the 4 least significant bits of a subset of pixels in an image with bits representing a sequence of binary
    values of RGB channels of all pixels of the image to be concealed.

    The first pixel in the top left corner is used to store the width and height of the image to be hidden, which is
    necessary for recovery of the hidden image.

    Args:
        visible_image:        An RGB image to be used for hiding another image
        hidden_image_pixels:  Binary string representing all pixel values of the image to be hidden
        width_visible:        Width of the image to be used for hiding another image
        height_visible:       Height of the image to be used for hiding another image
        width_hidden:         Width of the image to be hidden
        height_hidden:        Height of the image to be hidden

    Returns:
        An RGB image which is a copy of visible_image where the 4 least significant bits of a subset of pixels
        are replaced with bits representing the hidden image.
    """
    idx = 0
    for col in range(width_visible):
        for row in range(height_visible):
            if row == 0 and col == 0:
                # Add zeros to have 12 bits 
                width_hidden_binary = add_leading_zeros(bin(width_hidden)[2:], 12)
                height_hidden_binary = add_leading_zeros(bin(height_hidden)[2:], 12)
                w_h_binary = width_hidden_binary + height_hidden_binary
                # Replace the first pixel with the width and height of the hidden image
                visible_image[col, row] = (
                    int(w_h_binary[0:8], 2),
                    int(w_h_binary[8:16], 2),
                    int(w_h_binary[16:24], 2)
                )
                continue

            # We are just interested in the 3 first bytes r, g, and b
            r, g, b, _ = visible_image[col, row]
            r_binary, g_binary, b_binary = rgb_to_binary(r, g, b)
            # Extract the first four bits from the binary string starting from the MSB
            # Then concatenate with four bits of the image to hide
            r_binary = r_binary[0:4] + hidden_image_pixels[idx:idx+4]
            g_binary = g_binary[0:4] + hidden_image_pixels[idx+4:idx+8]
            b_binary = b_binary[0:4] + hidden_image_pixels[idx+8:idx+12]
            
            idx += 12
            # Convert binary values to integers so that each pixel is a tuple of integers (a, b, c)
            visible_image[col, row] = (
                int(r_binary, 2),
                int(g_binary, 2),
                int(b_binary, 2)
            )
            if idx >= len(hidden_image_pixels):
                return visible_image
    # Can never be reached, but let's return the image anyway
    return visible_image

def encode_image(visible_image_path, hidden_image_path):
    """
    Loads the image to be hidden and the image used for hiding and conceals the pixel information from one image
    in the other one.

    Args:
        visible_image_path:    An RGB image used for hiding another image
        hidden_image_path:     An RGB image to be concealed

    Returns:
        An RGB image which is supposed to be not very different visually from the visible image, but contains all the information
        necessary to recover an identical copy of the image we want to hide.
    """
    visible_image = Image.open(visible_image_path)
    hidden_image = Image.open(hidden_image_path)
    encoded_image = visible_image.load()
    hidden_image_copy = hidden_image.load()
    width_visible, height_visible = visible_image.size
    width_hidden, height_hidden = hidden_image.size

    # Check if the number of pixels in the hidden image is 2 times fewer than the visible image
    if width_hidden * height_hidden * 2 >= width_visible * height_visible:
        print("Error: The number of pixels in the hidden image should be 2 times fewer than the visible image.")
        exit

    hidden_image_pixels = get_binary_pixel_values(hidden_image_copy, width_hidden, height_hidden)
    encoded_image = change_binary_values(encoded_image, hidden_image_pixels, width_visible, height_visible, width_hidden, height_hidden)
    return visible_image
 
