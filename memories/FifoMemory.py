from windows.memory import *
from tkinter import *
from tkinter import messagebox
import pandas as pd
import numpy as np

def janelaFifo(num_pag, janela_anterior):
    numPag = num_pag
    # --------------------------------------------------------------------------

    # Criar a janela
    window = janela_anterior


    # Criar o canvas para exibir os quadrados de ram
    canvas = Canvas(window, width=1300, height=60)
    canvas.place(x=400, y=430)
    
    titulo = Label(window, text="RAM", anchor="center")
    titulo.place(x=400, y=400)

    # Criar os quadrados dentro do canvas de ram
    quadrados = []
    x, y = 10, 10
    for i in range(50):
        quadrado = canvas.create_rectangle(x, y, x+50, y+20, outline="black")
        texto = canvas.create_text(x+40, y+10, text="")
        quadrados.append(texto)
        x += 25

    # Criar o canvas para exibir os quadrados de disco
    canvas2 = Canvas(window, width=1300, height=60)
    canvas2.place(x=400, y=580)
    
    titulo2 = Label(window, text="DISCO", anchor="center")
    titulo2.place(x=400, y=550)

    # Criar os quadrados dentro do canvas de memoria Virtual
    quadrados2 = []
    x, y = 10, 10
    for i in range(50):
        quadrado2 = canvas2.create_rectangle(x, y, x+50, y+20, outline="black")
        texto2 = canvas2.create_text(x+40, y+10, text="")
        quadrados2.append(texto2)
        x += 25

    mem_fisica   = []
    mem_virtual  = []
    pegarValores = []

    # Iniciar o loop principal
    return canvas, quadrados, canvas2, quadrados2, mem_fisica, mem_virtual, pegarValores


# def page_fault(window, pf):
#     if pf == "yes":
#         texto = "Page Fault"
#         textoPF = Label(window, text=texto, anchor="center", fg="blue", font=("Arial", 13))
#         textoPF.place(x=485, y=185)

#     if pf == "no":
#         textoPF = Label(window, anchor="center", fg="blue", font=("Arial", 13), text="                  ")
#         textoPF.place(x=485, y=185)
#         textoPF.grid_remove()

#Adiciona valor na memoria virtual
def adicionar_valor_vir(window, mem_virtual, canvas2, quadrados2, num_processo):
    y = 10
    atualizar_pilha_vir(mem_virtual, canvas2, quadrados2, num_processo)

def atualizar_pilha_vir(mem_virtual, canvas2, quadrados2, num_processo):
    cont = -1
    for i in range(len(mem_virtual)):
        if i < len(mem_virtual) and i < 50:
            canvas2.itemconfigure(quadrados2[i], text=mem_virtual[i])
        elif i >= 50:
            cont += 1
            canvas2.itemconfigure(quadrados2[i], text=cont)     
        else:
            canvas2.itemconfigure(quadrados2[i], text="")
    
#Adiciona valor na memoria fisica
def adicionar_valor_fis(window, num, mem_fisica, mem_virtual, pegarValores, canvas, quadrados, num_paginas, canvas2, quadrados2): 
    valor = num
    tam = 50
    x = 10

    if valor not in mem_fisica:
        for janela in range(num_paginas):
            indice = len(mem_fisica) - tam
            pegarValores.append(valor)

            if len(mem_fisica) >= 50:
                #exibe os valores que sairam da memoria fisica
                textoForaMem = Label(window, text="Valores retirados da memória: ", anchor="center", fg="red", font=("Arial", 13))
                textoForaMem.place(x=335, y=385)

                textoForaMem2 = Label(window, text=pegarValores[(indice)], anchor="center", font=("Arial", 13))
                textoForaMem2.place(x=x+335, y=405)
                mem_virtual.append(pegarValores[(indice)])
                x+=25
                adicionar_valor_vir(window, mem_virtual, canvas2, quadrados2, valor)
                
                mem_fisica.pop(indice)
                mem_fisica.insert(indice, valor)
                
                
            mem_fisica.append(valor)
            atualizar_fila(mem_fisica, canvas, quadrados, num)

def atualizar_fila(mem_fisica, canvas, quadrados, num):
    for i in range(50):
        if i < len(mem_fisica):
            canvas.itemconfigure(quadrados[i], text=mem_fisica[i])
        else:
            canvas.itemconfigure(quadrados[i], text="")