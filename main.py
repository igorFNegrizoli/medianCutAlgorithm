import cv2
from funcs import medianCut, constructImage
import numpy as np

def write_png(buf, width, height):
    """ buf: must be bytes or a bytearray in Python3.x,
        a regular string in Python2.x.
    """
    import zlib, struct

    # reverse the vertical line order and add null bytes at the start
    width_byte_4 = width * 4
    raw_data = b''.join(
        b'\x00' + bytes(buf[span:span + width_byte_4])
        for span in range((height - 1) * width_byte_4, -1, - width_byte_4)
    )

    def png_pack(png_tag, data):
        chunk_head = png_tag + data
        return (struct.pack("!I", len(data)) +
                chunk_head +
                struct.pack("!I", 0xFFFFFFFF & zlib.crc32(chunk_head)))

    return b''.join([
        b'\x89PNG\r\n\x1a\n',
        png_pack(b'IHDR', struct.pack("!2I5B", width, height, 8, 6, 0, 0, 0)),
        png_pack(b'IDAT', zlib.compress(raw_data, 9)),
        png_pack(b'IEND', b'')])

def saveAsPNG(array, filename):
    import struct
    if any([len(row) != len(array[0]) for row in array]):
        raise ValueError("Array should have elements of equal size")

                                #First row becomes top row of image.
    flat = []; map(flat.extend, reversed(array))
                                 #Big-endian, unsigned 32-byte integer.
    buf = b''.join([struct.pack('>I', ((0xffFFff & i32)<<8)|(i32>>24) )
                    for i32 in flat])   #Rotate from ARGB to RGBA.

    data = write_png(buf, len(array[0]), len(array))
    f = open(filename, 'wb')
    f.write(data)
    f.close()

def color2Hex2Num(color):
    #transformaçoes: [B,G,R] -> [A, R,G,B] -> 0xARGB -> int(0xARGB)
    #A = 255
    color.append(255)

    hex_str = hex(color[3])
    hex_int = int(hex_str, 16)
    a = hex_int + 0x00
    
    hex_str = hex(color[2])
    hex_int = int(hex_str, 16)
    b = hex_int + 0x00

    hexArr = hex( (a<<8) | b )
    #0 a esquerda fica um só
    hexArr = hexArr + hex(color[1])[2:]
    hexArr = hexArr + hex(color[0])[2:]

    print(hexArr)


def append_hex(a, b):
    sizeof_b = 0

    # get size of b in bits
    while((b >> sizeof_b) > 0):
        sizeof_b += 1

    # align answer to nearest 4 bits (hex digit)
    sizeof_b += sizeof_b % 4

    return hex((a << sizeof_b) | b)

#imagem BGR (RGB pra que)
image = cv2.imread('testPics/birds.jpeg')
grupos = medianCut(image, 255)
novaImagem = constructImage(grupos, image)
#novaImagem = [[[136, 0, 21], [136, 0, 21], [255, 174, 200], [255, 174, 200]],
#    [[255, 174, 200], [185, 122, 87], [185, 122, 87], [140, 255, 251]],
#    [[239, 228, 176], [239, 228, 176], [200, 191, 231], [196, 255, 14]],
#    [[255, 127, 39], [34, 177, 76], [195, 195, 195], [195, 195, 195]]]
#print(color2Hex2Num([136, 0, 21]))
finalImage = []
width = len(novaImagem[0])
height = len(novaImagem)
for i in novaImagem:
    for j in i:
        for k in j:
            finalImage.append(k)
        finalImage.append(255)


#buf = [0, 0, 0, 255, 0, 0, 0, 255, 255, 0, 0, 255, 0, 0, 0, 255]
data = write_png(finalImage, width, height)
with open("imgTeste.png", 'wb') as fh:
    fh.write(data)

#image = cv2.imread('imgTeste.jpg')
#print(image)
#novaImagem = np.array(novaImagem)


#data = write_png(rgbByteArray, width, height)
#with open("imgTeste.png", 'wb') as fh:
#    fh.write(data)

#cv2.imshow("imagem", novaImagem)
#important, do not remove
#cv2.waitKey(0)
#cv2.destroyAllWindows()
