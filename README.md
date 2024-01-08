## SB Image Steganograph (Least-Significant Bit)

### Description

Steganography it is to embeded data inside multimedia with a very geniune manner so that no one can access this data such us photo, video, gif

LSB stands for Least-Significant-Bit is a type of Steganography where we insert our data into non significant bits in the multimedia.

![image](LSB.png "Titre de l'image")

##### encode text

You provide a string and the program hides it
We will implement decoding version

##### encode image

You provide an OpenCV image and the method iterates for every pixel in order to hide them. A good practice is to have a carrier 8 times bigger than the image to hide (so that each pixel will be put only in the first bit).
We will implement decoding version

##### encode binary

You provide a binary file to hide; This method can obfuscate any kind of file.
We will implement decoding version

### implementation in Python

With an image + (text/image/binary). We must generate a key + signature.
A key + signature will be sent to destination in order to perform decoding tasks.

### Bibliography

https://medium.com/swlh/lsb-image-steganography-using-python-2bbbee2c69a2
