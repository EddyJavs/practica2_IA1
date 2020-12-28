from django.shortcuts import render, redirect, reverse
from .forms import *
from .AlgoritmoGenetico import *
from Clasificacion import Example1
#from Clasificacion import Example2

from django.http import HttpResponseRedirect
# Create your views here.
import csv
Solucion = [0.0,0.0,0.0,0.0]
Modelos = []

def ParametrosAlgoritmo(request,id=0):
    
    if request.method == 'POST':
        if id == 1:
            data=request.POST
            #print(data['archivo'])
            ##print(data['finalizacion'])
            #print(data['padres'])
            
            archivo = "C:\\Users\\eddja\\Desktop\\Vacas Diciembre 2020\\IA\\LAB\\Practica1\\"+data['archivo']
            print(archivo)
            notas=[]
            with open(archivo) as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    notas.append([row['PROYECTO 1'], row['PROYECTO 2'],row['PROYECTO 3'],row['PROYECTO 4'],row['NOTA FINAL']])
                    #print(row['PROYECTO 1'], row['PROYECTO 2'],row['PROYECTO 3'],row['PROYECTO 4'])
            #print(notas)
            sol = ejecutar(notas,data['finalizacion'],data['padres'],data['archivo'])
            print(sol)
            setSolucion(sol)
        if id == 2:
            data=request.POST
            print(data['p1'])
            print(data['p2'])
            print(data['p3'])
            print(data['p4'])
            print(Solucion)
            NC1 = float(data['p1']) * Solucion[0]
            NC2 = float(data['p2']) * Solucion[1]
            NC3 = float(data['p3']) * Solucion[2]
            NC4 = float(data['p4']) * Solucion[3]
            NF = NC1 + NC2 + NC3 + NC4
            print("Nota final predicha: ", str(NF))
            return render(request,'home.html',{'message':NF})
        return HttpResponseRedirect('/ParametrosAlgoritmo/')
    else:
        form = UploadFileForm()

    return render(request,'home.html',{'form':form})

def setSolucion(solu):
    global Solucion
    Solucion = solu
    print(Solucion)

def Clasificacion(request,id=0):
    global ModelUsac
    if request.method == 'POST':
        
        if id == 1:
            form = UploadFileForm()
            ModelUsac=Example1.Entrenar("USAC")
            Modelos.append(ModelUsac)
            ModelMarroquin=Example1.Entrenar("Marroquin")
            Modelos.append(ModelMarroquin)
            ModelMariano=Example1.Entrenar("Mariano")
            Modelos.append(ModelMariano)
            ModelLandivar=Example1.Entrenar("Landivar")
            Modelos.append(ModelLandivar)
        if id == 2:
            form = UploadFileForm(request.POST, request.FILES)
            if form.is_valid():
                files = request.FILES.getlist('file')
                predicciones=Example1.Predecir(files,Modelos)
                print(predicciones)
                Flag = False
                if len(predicciones) > 5:
                    Flag = True
                porcentajeUSAC,porcentajeLandivar,porcentajeMarroquin,porcentajeMariano=getPorcentajes(predicciones)
                dic = {
                    'flag':Flag,
                    'predicciones':predicciones,
                    'pUsac':porcentajeUSAC,
                    'pLandivar':porcentajeLandivar,
                    'pMarroquin':porcentajeMarroquin,
                    'pMariano':porcentajeMariano,
                    'form':form
                }
                return render(request,'clasificacion.html',dic)
            else:
                print("FORMULARIO INVALIDO")
            
    else:
        form = UploadFileForm()
        
    return render(request,'clasificacion.html',{'form':form})
        
def getPorcentajes(Predicciones):
    AciertosLandivar=0
    TotalLandivar=0
    AciertosUSAC=0
    TotalUSAC=0
    AciertosMarroquin=0
    TotalMarroquin=0
    AciertosMariano=0
    TotalMariano=0
    for prediccion in Predicciones:
        if prediccion[0] == "Landivar":
            TotalLandivar+=1
            if prediccion[2]=="Landivar":
                AciertosLandivar+=1
        elif prediccion[0] == "USAC":
            TotalUSAC+=1
            if prediccion[2]=="USAC":
                AciertosUSAC+=1
        elif prediccion[0] == "Marroquin":
            TotalMarroquin+=1
            if prediccion[2]=="Marroquin":
                AciertosMarroquin+=1
        elif prediccion[0] == "Mariano":
            TotalMariano+=1
            if prediccion[2]=="Mariano":
                AciertosMariano+=1
    porcentajeLandivar=0 if TotalLandivar == 0 else ( AciertosLandivar*100)/TotalLandivar
    porcentajeUSAC=0 if TotalUSAC == 0 else (AciertosUSAC*100)/TotalUSAC
    porcentajeMarroquin=0 if TotalMarroquin==0 else(AciertosMarroquin*100)/TotalMarroquin
    porcentajeMariano=0 if TotalMariano==0 else(AciertosMariano*100)/TotalMariano
    return porcentajeUSAC,porcentajeLandivar,porcentajeMarroquin,porcentajeMariano

