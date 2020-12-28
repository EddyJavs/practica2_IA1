#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import time

#CONSTANTES DEL ALGORITMO
maximo_generaciones = 2000 #Número máximo de generaciones que va a tener el algoritmo
suma_anterior = 1 #Para guardar la suma de la población anterior

"""
*   Función que crea la población
"""
def inicializarPoblacion(NoIndividuos,archivo):
    poblacion = []

    for i in range(NoIndividuos):
        #La población inicial ya la definió el ingeniero en la tabla
        #Individuo 1
        arregloRandom=[random.uniform(-2, 2),random.uniform(-2, 2),random.uniform(-2, 2),random.uniform(-2, 2)]
        solucion = Nodo(arregloRandom ,  evaluarFitness(arregloRandom,archivo))
        poblacion.append(solucion)
    return poblacion #Retorno la población ya creada






"""
*   Función que verifica si el algoritmo ya llegó a su fin
"""
def verificarCriterio(poblacion, generacion,criterio,archivo):
    #maximo numero de generaciones
    if criterio == 1:
        #Si ya llegó al máximo de generaciones lo detengo
        if generacion >= maximo_generaciones:
            return True
    #porcentaje de la poblacion con valor fitness aceptable        
    elif criterio ==2:
        #si almenos el 50% de los individuos tienen un valor fitness menor a 2
        aceptables=0
        for individuo in poblacion:
            individuo.fitness = evaluarFitness(individuo.solucion,archivo)    
            if individuo.fitness <= 2:
                aceptables+=1
        if aceptables > len(poblacion)/2:
            return True
    #Valor fitness de un individuo dentro de la poblacion
    elif criterio ==3:
        #si hay un individuo con fitness menor a 0.4
        sumaFitness=0
        for individuo in poblacion:
            if individuo.fitness < 0.4:
                return True    
    return


"""
*   Función que evalúa qué tan buena es una solución, devuelve el valor fitness de la solución
*   @solucion = el número viene en un arreglo como este [0, 1, 1, 1]
"""
def evaluarFitness(solucion,archivo):
    valorFitness=0
    N = len(archivo)
    i = 0
    ValSumatoria = 0
    for Nota in archivo:
        NC = solucion[0]*float(Nota[0])+solucion[1]*float(Nota[1])+solucion[2]*float(Nota[2])+solucion[3]*float(Nota[3])
        NR =float(Nota[4])
        Dif_NR_NC = NR - NC
        Dif_Cuadrada=Dif_NR_NC*Dif_NR_NC
        ValSumatoria = ValSumatoria + Dif_Cuadrada
    valorFitness=ValSumatoria/N
    return valorFitness


"""
*   Función que toma a los mejores padres para luego crear una nueva generación
"""
def seleccionarPadres(poblacion,criterio):
    #Se seleccionan los 5 mejores padres
    padres = []
    #seleccion aleatoria
    if criterio == 1:
        # se seleccionan individuos aleatoriamente
        poblacion=random.sample(poblacion,len(poblacion))
        for i in range(int(len(poblacion)/2)):
            padres.append(poblacion[i])
    #selecccion con los mejores padres    
    elif criterio == 2:
        # se seleccionan los mejores individuos
        poblacion = sorted(poblacion, key=lambda item: item.fitness, reverse=False)[:len(poblacion)] #Los ordena de menor a mayor
        for i in range(int(len(poblacion)/2)):
            padres.append(poblacion[i])
    #seleccion por torneo
    elif criterio == 3:
        impar = False
        for i in range(int(len(poblacion)/2)):
            if i+1==len(poblacion):
                print("valor de I: " + i)
                break
            if poblacion[i].fitness < poblacion[i+1].fitness:
                padres.append(poblacion[i])
            else:
                padres.append(poblacion[i+1])
    print(len(padres))
    if len(poblacion)/2 == len(padres):
        return padres
    else:
        print("Ocurrio un error al seleccionar padres")
        return "Ocurrio un error al seleccionar padres"
    


"""
*   Función que toma dos soluciones padres y las une para formar una nueva solución hijo
*   Se va a alternar los bits de ambos padres
*   Se va a tomar un bit del padre 1, un bit del padre 2 y así sucesivamente
"""
def cruzar(padre1, padre2):
    #Cada posicion:
    #60% de ser del primer padre
    #40% de ser del segundo padre
    hijo = [0,0,0,0]
    for i in range(4):
        valRandom =random.randrange(100)
        
        if valRandom < 60:
            hijo[i] = padre1[i]
        else:
            hijo[i] = padre2[i]
    return hijo #Retorno al hijo ya cruzado


"""
*   Función que toma una solución y realiza la mutación
*   
"""
def mutar(solucion):
    #Se tiene un 50% de posibilidad de mutar
    valRandom =random.randrange(100)
    if valRandom > 50:
        #si va a mutar
        #verrifico si cada posicion muta o no.
        for i in range(4):
            valRandom =random.randrange(100)
            if valRandom > 50:
                #si muta esa posicion:
                solucion[i] = random.uniform(-2, 2)
                
        return solucion #Retorno la misma solución, solo que ahora mutó
    else:
        #No va a mutar, retorno el mismo valor
        return solucion
            

"""
*   Función que toma a los mejores padres y genera nuevos hijos
"""
def emparejar(padres,archivo):
    nuevaPoblacion = []
    for padre in padres:
        nuevaPoblacion.append(padre) 
    #Genero a los hijos que hagan falta,
    # genero tantos hijos como padres hayan
    for i in range(len(padres)):
        hijo = Nodo()
        if i+1 < len(padres):
            hijo.solucion = cruzar(padres[i].solucion, padres[i+1].solucion)
            hijo.solucion = mutar(hijo.solucion) 
        else:
            hijo.solucion = cruzar(padres[0].solucion, padres[i].solucion)
            hijo.solucion = mutar(hijo.solucion)
        
        hijo.fitness= evaluarFitness(hijo.solucion,archivo)
        nuevaPoblacion.append(hijo)
    return nuevaPoblacion


"""
*   Método para imprimir los datos de una población
"""
def imprimirPoblacion(poblacion):
    for individuo in poblacion:
        print('Individuo: ', individuo.solucion, ' Fitness: ', individuo.fitness)


"""
*   Método que ejecutará el algoritmo genético para obtener
*   los coeficientes del filtro
"""
def ejecutar(datos_archivo,criterio_fin,criterio_selecPadres,archivoNAME):
    #np.seterr(over='raise')
    print("Algoritmo corriendo")
    criterio_fin_INT=0
    if criterio_fin == "Maximo numero de generaciones":
        criterio_fin_INT = 1
    elif criterio_fin == "Un porcentaje de la poblacion que tenga un valor fitness aceptable":
        criterio_fin_INT = 2
    elif criterio_fin == "Un individuo dentro de la poblacion con buen valor fitness":
        criterio_fin_INT = 3

    criterio_selecPadres_INT=0
    if criterio_selecPadres == "Seleccion aleatoria":
        criterio_selecPadres_INT = 1
    elif criterio_selecPadres == "Seleccion mejores padres":
        criterio_selecPadres_INT = 2
    elif criterio_selecPadres == "Seleccion por torneo":
        criterio_selecPadres_INT = 3

    generacion = 0
    poblacion = inicializarPoblacion(30,datos_archivo)
    fin = verificarCriterio(poblacion, generacion,criterio_fin_INT,datos_archivo)

    #Imprimo la población
    print('*************** GENERACION ', generacion, " ***************")
    imprimirPoblacion(poblacion)

    while(fin == None):
        padres = seleccionarPadres(poblacion,criterio_selecPadres_INT)
        poblacion = emparejar(padres,datos_archivo)
        generacion += 1 #Lo pongo aquí porque en teoría ya se creó una nueva generación
        fin = verificarCriterio(poblacion, generacion,criterio_fin_INT,datos_archivo)
        #generacion += 1

        #Imprimo la población
        #print('*************** GENERACION ', generacion, " ***************")
        #imprimirPoblacion(poblacion)

    #print('Cantidad de generaciones:', generacion)
    #imprimirPoblacion(poblacion) #Población final

    #Obtengo la mejor solución y la muestro
    arregloMejorIndividuo = sorted(poblacion, key=lambda item: item.fitness, reverse=False)[:len(poblacion)] #Los ordena de menor a mayor
    mejorIndividuo = arregloMejorIndividuo[0]

    print('\n\n*************** MEJOR SOLUCION***************')
    print('Individuo: ', mejorIndividuo.solucion,  ' Fitness: ', mejorIndividuo.fitness,    'Generacion: ', generacion)
    Escribir_en_bitacora(archivoNAME,criterio_fin,criterio_selecPadres,generacion,mejorIndividuo.solucion)
    return mejorIndividuo.solucion

def Escribir_en_bitacora(archivo,CF,CP,NG,MS):
    ar =  "C:\\Users\\eddja\\Desktop\\Vacas Diciembre 2020\\IA\\LAB\\Practica1\\Bitacora.bca"
    f = open(ar,'a')
    localtime = time.asctime( time.localtime(time.time()) )
    f.write("-*-*-*-*-*-*-*-*-*-*-*--*-*-*-*-*-*-*-*-*-*-*-*-*--*-*-*-*-*-*-*-*-*-*-*-*-*\n")
    f.write("Fecha y hora de ejecucion: "+localtime+"\n")
    f.write("Nombre del documento CSV utilizado: "+archivo+"\n" )
    f.write("Criterio de finalización utilizado: "+ CF+"\n")
    f.write("Criterio de selección de padres utilizado: "+CP+"\n")
    f.write("Número de generaciones generadas: "+str(NG)+"\n")
    f.write("Mejor solución encontrada por el algoritmo: "+ str(MS)+"\n")

class Nodo:
    #solucion = []
    #fitness = 0 #Valor fitness
    #x = 0 #Para la tarea se guarda el valor de x

    #Le defino parámetros al constructor y le pongo valores por defecto por si no se envían
    def __init__(self, solucion = [], fitness = 0, x = 0):
        self.solucion = solucion
        self.fitness = fitness
        self.x = x



