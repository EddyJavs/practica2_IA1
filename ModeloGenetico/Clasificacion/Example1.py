from .File import *
from .Data import Data
from .Model import Model
from .Plotter import *
import numpy as np
import os

# Se obtienen los datos
ejemplo_dir = "\\Users\eddja\Desktop\Vacas Diciembre 2020\IA\LAB\Practica2\ImagenesP2"

#la siguiente linea obtengo el dataset de las imagenes

#train_set_x, train_set_y, test_set_x, test_set_y, classes = read_file("Datasets/MC2A.csv")


'''

# Definir los conjuntos de datos
train_set = Data(train_set_x, train_set_y, 100)
test_set = Data(test_set_x, test_set_y, 100)

# Se entrenan los modelos
model1 = Model(train_set, test_set, reg=False, alpha=0.5, lam=0.5)
model1.training()

model2 = Model(train_set, test_set, reg=False, alpha=0.05, lam=150)
model2.training()

# Se grafican los entrenamientos
Plotter.show_Model([model1, model2])

# Prueba de prediccion
exams = ['primer', 'segundo', 'tercer']
#p = [1]
p = [1]
for exam in exams:
    grade = input('Ingrese la nota del '+exam+' parcial: ')
    p.append(int(grade) / 100)

print('p: ', p)
grades = np.array(p)
print('grades: ', grades)
result = model1.predict(grades)
print('--', classes[result[0]], '--')
'''
def Entrenar(Universidad):
    print("*-*-*-*-*--*-* Entrenando modelo "+Universidad+"*-*-*-*-*-*-*-*-*-*")
    train_set_x_orig, train_set_y, test_set_x_orig, test_set_y, classes = read_images("\\Users\eddja\Desktop\Vacas Diciembre 2020\IA\LAB\Practica2\ImagenesP2",Universidad)
    # Convertir imagenes a un solo arreglo
    train_set_x = train_set_x_orig.reshape(train_set_x_orig.shape[0], -1).T
    test_set_x = test_set_x_orig.reshape(test_set_x_orig.shape[0], -1).T
    # Definir los conjuntos de datos
    train_set = Data(train_set_x, train_set_y, 100)
    test_set = Data(test_set_x, test_set_y, 100)
    # Se entrenan los modelos
    model1 = Model(train_set, test_set,  reg=False, alpha=0.001, lam=150, universidad = Universidad)
    model1.training()
    model2 = Model(train_set, test_set,  reg=False, alpha=0.0000001, lam=100, universidad = Universidad)
    model2.training()
    model3 = Model(train_set, test_set,  reg=False, alpha=0.000001, lam=200, universidad = Universidad)
    model3.training()
    model4 = Model(train_set, test_set,  reg=False, alpha=0.0001, lam=50, universidad = Universidad)
    model4.training()
    model5 = Model(train_set, test_set,  reg=True, alpha=0.00001, lam=150, universidad = Universidad)
    model5.training()
    show_Model([model1,model2,model3,model4,model5])
    return model1


def Predecir(Imagenes,Modelos):
    rutaCarpeta="\\Users\eddja\Desktop\Vacas Diciembre 2020\IA\LAB\Practica2\ModeloGenetico\ModeloGenetico\static\img"
    predicciones=[]
    for img in Imagenes:
        imagen = rutaCarpeta + "\\" + str(img)
        npImg=get_Image(imagen)
        #print(npImg.shape)
        #La comparo con todos los modelos
        resultados = []
        for model in Modelos:
            result = model.predict(npImg)
            resultados.append(result)
            print(result)
        maxPorcentaje= max(resultados)
        indice = resultados.index(maxPorcentaje)
        #arreglo donde almaceno elnombre de la imagen y prediccion
        prediccion = []
        prediccion.append(str(img).split("_")[0])
        prediccion.append("img/"+str(img))
        if indice == 0:
            prediccion.append("USAC")
        elif indice ==1:
            prediccion.append("Marroquin")
        elif indice ==2:
            prediccion.append("Mariano")
        elif indice ==3:
            prediccion.append("Landivar")
        predicciones.append(prediccion)
    return predicciones