import numpy as np
import imageio
import random, sys

def string_extensor(text, key):
    size = len(key) - (len(text) % len(key))
    if (int((len(text)/len(key)))%2 == 0):
        size += len(key)
    if isinstance((len(text)/len(key)), float):
        for i in range(size):
            text = ''.join([text, chr(random.randint(1, 26) + 96)])
    return text

def string_to_matrix(text, key):
    ncols = len(key)
    nlins = int(len(text)/len(key))
    matrix = np.chararray((nlins, ncols))
    for i in range(nlins):
        for j in range(ncols):
            matrix[i, j] = text[i*ncols + j]
    return matrix
def save_matrix_to_image(matrix, name):
    nlins = matrix.shape[0]
    ncols = matrix.shape[1]
#    print(matrix.shape)
    res = np.ndarray((int(nlins/2), int(ncols/2),4), dtype=np.uint8)
#    print(res.shape)
    for i in range(int(nlins/2)):
        for j in range(int(ncols/2)):
#            print(i, j)
            res[i, j, 0] = ord(matrix[2 * i, 2 * j])
#            print(chr(res[i,j,0]))
            res[i, j, 1] = ord(matrix[(i * 2)+1, 2 * j])
#            print(chr(res[i,j,1]))
            res[i, j, 2] = ord(matrix[2 * i, (j * 2)+1])
#            print(chr(res[i,j,2]))
            res[i, j, 3] = ord(matrix[(i * 2) +1, (j * 2) +1])
#            print(chr(res[i,j,3]))
    imageio.imwrite(name, res)
def read_data_from_image(name):
    img = imageio.imread(name)
    res = np.chararray((img.shape[0]*2, img.shape[1]*2))
#    print(res)
#    print('resultado:')
#    print(img.shape)
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
#            print(i, j)
            res[i*2,j*2] = chr(img[i,j,0])
            res[i*2+1,j*2] = chr(img[i,j,1])
            res[i*2,j*2+1] = chr(img[i,j,2])
            res[i*2+1 ,j*2+1] = chr(img[i,j,3])
    return res

def cypher(text_mtx, key):
    aux_key = list(key)
    key_ord = np.zeros(len(key))
    res = np.chararray(text_mtx.shape)
    for i in range(len(key)):
        idx = np.argmin(aux_key)
        res[:, i] = text_mtx[:, idx]
        aux_key[idx] = 'z'
    return res

def decypher(text_mtx, key):
    aux_key = list(key)
    key_ord = np.zeros(len(key))
    res = np.chararray(text_mtx.shape)
    for i in range(len(key)):
        idx = np.argmin(aux_key)
        text_mtx[:, i] = res[:, idx]
        aux_key[idx] = 'z'
    return res

with open (sys.argv[1], "r") as myfile:
    t=myfile.readlines()

with open (sys.argv[2], "r") as myfile:
    k=myfile.readlines()
t = str(t).rstrip()
k = str(k).rstrip()
output = str(sys.argv[3]).rstrip()
t = string_extensor(t, k)
res = string_to_matrix(t, k)
save_matrix_to_image(res, output)
res = read_data_from_image(output)
res = cypher(res, k)
res = decypher(res, k)
