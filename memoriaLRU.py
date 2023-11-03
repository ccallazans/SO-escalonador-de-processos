import tkinter as tk
from screen import *
from menuMemoria import *
from tkinter import *
from tkinter import messagebox

def janelaLRU():

    def page_fault(pf):
            
        if pf == "yes":
            texto = "Page Fault"
            textoPF = Label(memoriaFifo, text=texto, anchor='center', fg='blue', font=('Arial', 13))
            textoPF.place(x=485, y=185)

        if pf == "no":
            textoPF = Label(memoriaFifo, anchor='center', fg='blue', font=('Arial', 13), text="                  ")
            textoPF.place(x=485, y=185)
            textoPF.grid_remove()

    def candidato_a_sair():
        titCandidato = Label(memoriaFifo, text="Valor candidato a sair", anchor='center', fg='black', font=('Arial', 16))
        titCandidato.place(x=70, y=130)

        txtCandidato = Label(memoriaFifo, text=mem_fisica[0], anchor='center', fg='red', font=('Arial', 16))
        txtCandidato.place(x=150, y=160)

        if len(pegarValores) > len(mem_fisica):
            tam = len(pegarValores) - len(mem_fisica)
            textoForaMem = Label(memoriaFifo, text="Valores retirados da memória: ", anchor='center', fg='red', font=('Arial', 13))
            textoForaMem.place(x=335, y=385)
            x=10
            for i in range(tam):              
                textoForaMem2 = Label(memoriaFifo, text=pegarValores[i], anchor='center', font=('Arial', 13))
                textoForaMem2.place(x=x+335, y=405)
                x+=25
    
    def armazenar_valores():
        if entrada.get() != "":
            adicionar_valor_fis(entrada.get())
            entrada.delete(0, 'end')
        else:
            messagebox.showinfo("VALOR INVÁLIDO!", "Insira um dado não vazio!")

    #Adiciona valor na memoria fisica
    def adicionar_valor_fis(num): 
        valor = num

        if valor not in mem_fisica:
            pegarValores.append(valor)

            if len(mem_fisica) >= 8:
                mem_fisica.pop(0)

            mem_fisica.append(valor)
            atualizar_pilha()
            page_fault("yes")
        else:
            mem_fisica.remove(valor)
            mem_fisica.append(valor)
            pegarValores.remove(valor)
            pegarValores.append(valor)
            atualizar_pilha()
            page_fault("no") 

    def atualizar_pilha():
        for i in range(8):
            if i < len(mem_fisica):
                canvas.itemconfigure(quadrados[i], text=mem_fisica[i])
            else:
                canvas.itemconfigure(quadrados[i], text="")

        candidato_a_sair()
    # --------------------------------------------------------------------------

    # Criar a janela
    memoriaFifo = tk.Tk()
    memoriaFifo.title("Simulação de LRU")
    memoriaFifo.geometry("650x450+500+150")
    #memoriaFifo.resizable(height=False, width=False)

    # Criar o canvas para exibir os quadrados de memoria fisica
    canvas = tk.Canvas(memoriaFifo, width=100, height=205)
    canvas.place(x=340, y=160)
    
    titulo = Label(memoriaFifo, text='Memoria Fisica', anchor='center')
    titulo.place(x=340, y=130)

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
        textoIndice.place(x=335, y= y+135)

    # Criar os widgets
    entrada = tk.Entry(memoriaFifo)
    entrada.place(x=40, y=45)    

    botao_adicionar = tk.Button(memoriaFifo, text="Adicionar", command=armazenar_valores)
    botao_adicionar.place(x=40, y=15)

    mem_fisica   = []
    pegarValores = []

    # Iniciar o loop principal
    memoriaFifo.mainloop()
