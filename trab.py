import numpy as np
import imageio
import random, sys
from unicodedata import normalize

def string_corrector(text):
	text = normalize('NFKD', text).encode("ASCII", "ignore").decode("ASCII")
	text = text.replace("\\n","")
	text = text.replace("']","")
	text = text.replace("['","")
	return text

def string_extensor(text, key):
    size = 0
    if ((len(text) % len(key)) != 0):
    	size = len(key) - (len(text) % len(key))
    if (((len(text)+size)/len(key))%2 != 0):
        size += len(key)
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
    res = np.ndarray((int(nlins/2), int(ncols/2),4), dtype=np.uint8)
    for i in range(int(nlins/2)):
        for j in range(int(ncols/2)):
            res[i, j, 0] = ord(matrix[2 * i, 2 * j])
            res[i, j, 1] = ord(matrix[(i * 2)+1, 2 * j])
            res[i, j, 2] = ord(matrix[2 * i, (j * 2)+1])
            res[i, j, 3] = ord(matrix[(i * 2) +1, (j * 2) +1])
    imageio.imwrite(name, res)
def read_data_from_image(name):
    img = imageio.imread(name)
    res = np.chararray((img.shape[0]*2, img.shape[1]*2))
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
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
    print(res)
    return res

def decypher(text_mtx, key):
    aux_key = list(key)
    key_ord = np.zeros(len(key))
    res = np.chararray(text_mtx.shape)
    for i in range(len(key)):
        idx = np.argmin(aux_key)
        res[:, idx] = text_mtx[:, i]
        aux_key[idx] = 'z'
    return res

def save_string_decyphered(text_mtx, name):
	string = text_mtx.tostring().decode("utf-8")
	file = open(name, "w")
	file.write(string)
	file.close()

"""
    arg[1] = Cypher / decypher
    arg[2] = input filename
    arg[3] = key filename
    arg[4] = output filename
"""
input_file = sys.argv[2]
output = str(sys.argv[4]).rstrip()

with open (sys.argv[3], "r") as myfile:
    k=myfile.readlines()
k = str(k).rstrip()
k = string_corrector(k)
op = str(sys.argv[1]).rstrip()
if op == 'C':
    with open (input_file, "r") as myfile:
        t=myfile.readlines()
    t = str(t).rstrip()
    print(t)
    t = string_corrector(t)
    print(t)
    t = string_extensor(t, k)
    res = string_to_matrix(t, k)
    res = cypher(res, k)
    save_matrix_to_image(res, output)
elif op == 'D':
    res = read_data_from_image(input_file)
    res = decypher(res, k)
    save_string_decyphered(res, output)
