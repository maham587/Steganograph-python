import encode_decode_binary
import encode_decode_text
import decode
import encode_image
import decode_image
 
def test_pdf():
    #**** testing lsb by pdf encoding
    key = encode_decode_binary.Encode_binary("../inputs/src.png", "../inputs/input.pdf", "../outputs/output.png")
    decode.Decode("../outputs/output.png", key)


def test_text():
    #***** testing lsb by hidding text 
    key = encode_decode_text.Encode_text("../inputs/src.png", "Hello world !", "../outputs/output.png")
    decode.Decode("../outputs/output.png", key)


def test_code_img():
    encoded_image = encode_image.encode_image ("../inputs/input.png", "../inputs/image_to_hide.png")
    encoded_image.save("../outputs/output.png")
def test_decode_img():
    decoded_image = decode_image.decode_image("../outputs/output.png")
    decoded_image.save("../outputs/output.png")

if __name__ == '__main__':
    test_text()


    
