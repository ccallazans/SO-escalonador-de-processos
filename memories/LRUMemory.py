# from windows.memory import *
from tkinter import *
from tkinter import messagebox

def janelaLRU(janela_anterior):
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

    return canvas, quadrados, canvas2, quadrados2, mem_fisica, mem_virtual, pegarValores

def armazenar_valores(entrada):
    if entrada.get() != "":
        adicionar_valor_fis_lru(entrada.get())
        entrada.delete(0, "end")
    else:
        messagebox.showinfo("VALOR INVÁLIDO!", "Insira um dado não vazio!")

#Adiciona valor na memoria fisica
def adicionar_valor_fis_lru(windown, num, mem_fisica, pegarValores, canvas, quadrados, num_paginas): 
    valor = num

    if valor not in mem_fisica:
        pegarValores.append(valor)

        if len(mem_fisica) >= 50:
            mem_fisica.pop(0)

        for janela in range(num_paginas):
            mem_fisica.append(valor)
            atualizar_pilha(windown, mem_fisica, canvas, quadrados, pegarValores)
    else:
        mem_fisica.remove(valor)
        mem_fisica.append(valor)
        pegarValores.remove(valor)
        pegarValores.append(valor)
        atualizar_pilha(windown, mem_fisica, canvas, quadrados, pegarValores)

def atualizar_pilha(windown, mem_fisica, canvas, quadrados, pegarValores):
    for i in range(50):
        if i < len(mem_fisica):
            canvas.itemconfigure(quadrados[i], text=mem_fisica[i])
        else:
            canvas.itemconfigure(quadrados[i], text="")

    candidato_a_sair(windown, mem_fisica, pegarValores)

def candidato_a_sair(windown, mem_fisica, pegarValores):
    titCandidato = Label(windown, text="Valor candidato a sair", anchor='center', fg='black', font=('Arial', 16))
    titCandidato.place(x=100, y=680)

    txtCandidato = Label(windown, text=mem_fisica[0], anchor='center', fg='red', font=('Arial', 16))
    txtCandidato.place(x=100, y=720)

    if len(pegarValores) > len(mem_fisica):
        tam = len(pegarValores) - len(mem_fisica)
        textoForaMem = Label(windown, text="Valores retirados da memória: ", anchor='center', fg='red', font=('Arial', 13))
        textoForaMem.place(x=200, y=840)
        x=10
        for i in range(tam):              
            textoForaMem2 = Label(windown, text=pegarValores[i], anchor='center', font=('Arial', 13))
            textoForaMem2.place(x=x+500, y=900)
            x+=25