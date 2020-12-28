#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import numpy as np
import h5py
import os
import scipy.misc
import random

#from scipy import ndimage,misc
import matplotlib.pyplot as plt
from matplotlib import image
from numpy import asarray

source = None

def read_file(path):
    data = []
    with open(path) as file:
        reader = csv.reader(file)
        for row in reader:
            data.append(row)
    result = np.array(data)
    np.random.shuffle(result)
    result = result.astype(float).T
    # Se separa el conjunto de pruebas del de entrenamiento
    slice_point = int(result.shape[1] * 0.7)
    train_set = result[:, 0: slice_point]
    test_set = result[:, slice_point:]

    # Se separan las entradas de las salidas
    train_set_x_orig = train_set[0: 3, :]
    train_set_y_orig = np.array([train_set[3, :]])

    test_set_x_orig = test_set[0: 3, :]
    test_set_y_orig = np.array([test_set[3, :]])

    return train_set_x_orig, train_set_y_orig, test_set_x_orig, test_set_y_orig, ['Perdera', 'Ganara']


def load_dataset():
    train_dataset = h5py.File('\\Users\eddja\Desktop\Vacas Diciembre 2020\IA\LAB\Practica2\ModeloGenetico\Clasificacion\Datasets/train_catvnoncat.h5', "r")
    print(train_dataset)
    #train_set_x_orig = arreglo de imágenes
    #train_set_y_orig = arreglo de imágenes

    train_set_x_orig = np.array(train_dataset["train_set_x"][:])  # entradas de entrenamiento
    train_set_y_orig = np.array(train_dataset["train_set_y"][:])  # salidas de entrenamiento

    print('************** train_set_x_orig **************')
    print(train_set_x_orig)
    #print(type(train_set_x_orig))
    #print('************** train_set_y_orig **************')
    #print(train_set_y_orig.shape)
    #print(len(train_set_y_orig))



    test_dataset = h5py.File('\\Users\eddja\Desktop\Vacas Diciembre 2020\IA\LAB\Practica2\ModeloGenetico\Clasificacion\Datasets/test_catvnoncat.h5', "r")
    test_set_x_orig = np.array(test_dataset["test_set_x"][:])  # entradas de prueba
    test_set_y_orig = np.array(test_dataset["test_set_y"][:])  # salidas de prueba

    #print('************** test_set_x_orig **************')
    #print(test_set_x_orig)
    #print(len(test_set_x_orig))
    #print('************** test_set_y_orig **************')
    #print(test_set_y_orig) #Arreglo con las respuestas correctas, donde 0 = NO es un gato, 1 = SÍ es un gato
    #print(len(test_set_y_orig))



    #Les aplica reshape, convierte al arreglo en un arreglo de areglos
    train_set_y_orig = train_set_y_orig.reshape((1, train_set_y_orig.shape[0]))
    test_set_y_orig = test_set_y_orig.reshape((1, test_set_y_orig.shape[0]))

    #print('************** train_set_y_orig con reshape**************')
    #print(train_set_y_orig)
    #print(len(train_set_y_orig))
    #print('************** test_set_y_orig con reshape**************')
    #print(test_set_y_orig)
    #print(len(test_set_y_orig))

    #print(type(train_set_x_orig))
    #print(type(train_set_y_orig))
    #print(type(test_set_x_orig))
    #print(type(test_set_y_orig))

    #print(len(train_set_x_orig))
    #print(train_set_x_orig.shape)

    return train_set_x_orig, train_set_y_orig, test_set_x_orig, test_set_y_orig, ['No Gato', 'Gato']




#Lee las imagenes dentro de un directorio, crea el dataset y lo retorna
#recibe como parametro la direccion a partir de la cual se obtendran las imagenes,
#busca en todas las carpetas dentro de esta y la universidad de la cual hara el modelo
def read_images(path,Universidad):
    data = []
    Directorio = os.listdir(path)
    
    #print(Directorio)
    #En esta matriz coloca el par ordenado [MatrizIMGEN, Universidad] para poder 
    #darle un nuevo orden aleatorio y que no se pierda su resultado 
    matrizAux = []
    #Para cada carpeta dentro del directorio voy obteniendo las imagenes
    CountImages=0
    for carpeta in Directorio:
        #ingreso dentro de la carpeta para obtener las imagenes
        #print(carpeta)
        Imagenes = os.listdir(path +"\\"+ carpeta)
        #print(Imagenes)
        for imagen in Imagenes:
            RutaImagen = path +"\\"+ carpeta +"\\"+ imagen
            #print(RutaImagen)
            #obtengo un numpy array de la imagen
            logo = image.imread(RutaImagen)
            if logo.shape[0] != 128 & logo.shape[1] != 128:
                print("ERROOOOOOOOOOOORRRR!")
                return
            UniversidadCorrecta = 1 if carpeta == Universidad else 0            
            matrizAux.append([logo,UniversidadCorrecta])
            #print(logo.shape)
            CountImages+=1
    
    random.shuffle(matrizAux)
    columnaImagen=[fila[0] for fila in matrizAux]
    columnaValor=[fila[1] for fila in matrizAux]
    
    #convierto el array a un numpy array de las imagenes y de los valores
    result = np.array(columnaImagen)
    result2 = np.array(columnaValor)
    #print(result2.shape)
    # Se separa el conjunto de imagenes pruebas del de entrenamiento 
    slice_point = int(result.shape[0] * 0.7)
    train_set_x_orig = result[ 0: slice_point,:]
    test_set_x_orig = result[ slice_point:,:]
    #print(train_set_x_orig.shape)
    #print(test_set_x_orig.shape)
    # Se separa el conjunto de valores de pruebas del de entrenamiento 
    train_set_y_orig = result2[ 0: slice_point]
    test_set_y_orig = result2[ slice_point:]
    #print(train_set_y_orig.shape)
    #print(test_set_y_orig.shape)

    return train_set_x_orig, train_set_y_orig, test_set_x_orig, test_set_y_orig, ['Si es', 'No es']
    
def get_Image(path):
    print(path)
    logo = image.imread(path)
    if logo.shape[0] != 128 & logo.shape[1] != 128:
        print("ERROOOOOOOOOOOORRRR!")
        return "Error imagen de tamanio incorrecto"
    print(logo.shape)
    logo.reshape(logo.shape[0]*logo.shape[1]*logo.shape[2])
    arr = np.array([1])
    arr = np.append(arr,logo)
    return arr