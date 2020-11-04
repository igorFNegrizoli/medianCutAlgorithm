#meuNumero.to_bytes(4, 'little') retorna uma cadeia de bytes em little endian, meuNumero pode ser int ou hex

def num2LittleEndian(num, n):
    #n é a quantidade de bytes da palavra
    #retorna array de bytes
    retorno = []
    for i in num.to_bytes(n, 'little'):
        retorno.append(i)
    return bytearray(retorno)

def bgr2bgrr(color):
    retorno = color.append(0)
    return retorno

def createTable(image):
    table = []
    for i in image:
        for j in i:
            if j not in table:
                table.append(j)
    #print(table)
    returnTable = []
    #print(table)
    if len(table) > 256:
        raise ValueError("Array should have elements of equal size")
    for i in table:
        returnTable.append(bytearray(i))
    #retorna um array de bytearray, na hora de escrever no arquivo lembrar de fazer um "for i in returnTable" 
    # e dar um "f.write(i)" ffs não escrever a returnTable
    return returnTable

def getTableIndex(table, color):
    colorInBarr = bytearray(color)
    for i in range(len(table)):
        if table[i] == colorInBarr:
            return num2LittleEndian(i, 1)
    print("LASCOU MANE")
    return False

def buildBMP(image, fileAdd):
    f = open(fileAdd, "w+b")

    w = len(image[0])
    h = len(image)
    table = createTable(image)
    fSize = 54 + (len(table)*4) + (w*h)

    f.write(bytearray([0x42, 0x4d])) #head - fixo em todo .bmp
    f.write(num2LittleEndian(fSize, 4)) #fileSize - tamanho total que o arquivo ocupa em disco (54 + len(tabela)*4 + len(byteArray))
    f.write(num2LittleEndian(0, 4)) #reserved 4b - inuteis, todos setados em 0
    f.write(num2LittleEndian(54, 4)) #startingAdd - em que endereço(byte) começa o mapa de bits 

    #BITMAPINFOHEADER

    f.write(num2LittleEndian(40,4)) #biSize - tamanho do BITMAPINFOHEADER
    f.write(num2LittleEndian(w, 4)) #biWidth - largura da imagem
    f.write(num2LittleEndian(h, 4)) #biHeight - altura da imagem
    f.write(num2LittleEndian(1, 2)) #biPlanes - quantas imagens tem no arquivo = 1
    f.write(num2LittleEndian(8, 2)) #biBitCount - quantos bytes tem a cor, no nosso caso 8 pois temos 256 cores
    f.write(num2LittleEndian(0, 4)) #biCompression - qual alg de compressao usado = nenhum = 0
    f.write(num2LittleEndian((w*h), 4)) #biSizeImage - tamanho da imagem
    f.write(num2LittleEndian(0, 4)) #biXPelsPerMeter, biYPelsPerMeter - densidade de pixels, nao vamos usar o de x nem de y
    f.write(num2LittleEndian(0, 4))
    f.write(num2LittleEndian(0, 4)) #biClrUsed - numero de cores usadas, nem precisa enquantar com isso, seta em 0
    f.write(num2LittleEndian(0, 4)) #biClrImportant - as n cores mais importantes da tabela, todas = 0

    #gravar tabela no arquivo
    for i in table:
        f.write(i)
        f.write(num2LittleEndian(0,1))

    #gravar indices das cores no arquivo
    byteList = []
    for i in image:
        for j in i:
            byteList.append(getTableIndex(table, j))

    for i in byteList[::-1]:
        f.write(i)
    f.close()