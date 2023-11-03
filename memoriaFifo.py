import tkinter as tk
from screen import *
from menuMemoria import *
from tkinter import *
from tkinter import messagebox
import time

def janelaFifo(num_pag):
    numPag = num_pag

    def page_fault(pf):
        
        if pf == "yes":
            texto = "Page Fault"
            textoPF = Label(memoriaFifo, text=texto, anchor='center', fg='blue', font=('Arial', 13))
            textoPF.place(x=485, y=185)

        if pf == "no":
            textoPF = Label(memoriaFifo, anchor='center', fg='blue', font=('Arial', 13), text="                  ")
            textoPF.place(x=485, y=185)
            textoPF.grid_remove()
  
    #Adiciona valor na memoria virtual
    def adicionar_valor_vir():
        y = 10
        for i in range(len(mem_virtual)):
            textoIndice2 = Label(memoriaFifo, text=mem_virtual[i], anchor='center')
            textoIndice2.place(x=85, y= y+130)
            y+=25

        if len(mem_virtual) == int(numPag):
            entrada.configure(state='disabled')

        atualizar_pilha_vir()

    def atualizar_pilha_vir():
        cont = -1
        for i in range(len(mem_virtual)):
            if i < len(mem_virtual) and i < 8:
                canvas2.itemconfigure(quadrados2[i], text=i)
            elif i >= 8:
                cont += 1
                canvas2.itemconfigure(quadrados2[i], text=cont)     
            else:
                canvas2.itemconfigure(quadrados2[i], text="")
        
    def armazenar_valores():
    
        if entrada.get() != '':
            valor = entrada.get()
            adicionar_valor_fis(valor)
            adicionar_valor_vir()
            entrada.delete(0, 'end')
        else:
            messagebox.showinfo("VALOR INVÁLIDO!", "Insira um dado não vazio!")
        
    #Adiciona valor na memoria fisica
    def adicionar_valor_fis(num): 
        valor = num
        tam = 8
        indice = len(mem_fisica) - tam
        x = 10

        if valor not in mem_fisica:
            pegarValores.append(valor)

            if len(mem_fisica) >= 8:
                #exibe os valores que sairam da memoria fisica
                textoForaMem = Label(memoriaFifo, text="Valores retirados da memória: ", anchor='center', fg='red', font=('Arial', 13))
                textoForaMem.place(x=335, y=385)

                for i in range(8, len(mem_fisica)+1):              
                    textoForaMem2 = Label(memoriaFifo, text=pegarValores[(len(mem_fisica) - i)], anchor='center', font=('Arial', 13))
                    textoForaMem2.place(x=x+335, y=405)
                    x+=25

                mem_fisica.pop(indice)
                mem_fisica.insert(indice, valor)

            mem_fisica.append(valor)
            mem_virtual.append(valor)
            atualizar_fila()
            page_fault("yes")   
        else:
            page_fault("no") 
            messagebox.showinfo("VALOR INVÁLIDO!", "O valor informado já se encontra na memória")   

    def atualizar_fila():
        for i in range(8):
            if i < len(mem_fisica):
                canvas.itemconfigure(quadrados[i], text=mem_fisica[i])
            else:
                canvas.itemconfigure(quadrados[i], text="")
    # --------------------------------------------------------------------------

    # Criar a janela
    memoriaFifo = tk.Tk()
    memoriaFifo.title("Simulação de FIFO")
    memoriaFifo.geometry("750x650+500+150")
    #memoriaFifo.resizable(height=False, width=False)

    # Criar o canvas para exibir os quadrados de memoria fisica
    canvas = tk.Canvas(memoriaFifo, width=100, height=205)
    canvas.place(x=340, y=130)
    
    titulo = Label(memoriaFifo, text='Memoria Fisica', anchor='center')
    titulo.place(x=340, y=100)

    # Criar os quadrados dentro do canvas de memoria fisica
    quadrados = []
    x, y = 10, 10
    for i in range(8):
        quadrado = canvas.create_rectangle(x, y, x+80, y+20, outline="black")
        texto = canvas.create_text(x+40, y+10, text="")
        quadrados.append(texto)
        y += 25
        
        #imprime o valor de indice ao lado da tabela
        textoIndice = Label(memoriaFifo, text=i, anchor='center')
        textoIndice.place(x=335, y= y+105)

    # Criar o canvas para exibir os quadrados de memoria Virtual
    canvas2 = tk.Canvas(memoriaFifo, width=100, height=420)
    canvas2.place(x=100, y=130)
    
    titulo2 = Label(memoriaFifo, text='Memoria Virtual', anchor='center')
    titulo2.place(x=100, y=100)

    # Criar os quadrados dentro do canvas de memoria Virtual
    quadrados2 = []
    x, y = 10, 10
    for i in range(int(numPag)):
        quadrado2 = canvas2.create_rectangle(x, y, x+80, y+20, outline="black")
        texto2 = canvas2.create_text(x+40, y+10, text="")
        quadrados2.append(texto2)
        y += 25

    # Criar os widgets
    entrada = tk.Entry(memoriaFifo)
    entrada.place(x=40, y=45)    

    botao_adicionar = tk.Button(memoriaFifo, text="Adicionar", command=armazenar_valores)
    botao_adicionar.place(x=40, y=15)

    mem_fisica   = []
    mem_virtual  = []
    pegarValores = []

    # Iniciar o loop principal
    memoriaFifo.mainloop()
