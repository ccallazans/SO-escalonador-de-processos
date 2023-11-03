import tkinter as tk
from tkinter import *
from memoriaFifo import janelaFifo
from memoriaLRU import janelaLRU
from tkinter import messagebox

def menuMemoria():

    # Criar a janela
    janela = tk.Tk()
    janela.geometry("400x400+500+150")
    janela.resizable(height=False, width=False)
    janela.configure(bg='#cf9416')

    #Criação dos labels e campos
    lbl1 = Label(janela, text='Quantidade de páginas', anchor='center')
    lbl1.place(x=70, y=120)
    ent1 = Entry(justify='center')
    ent1.place(x=200, y=120)
    lbl1.configure(bg='#cf9416')

    def chamarEscal():
        if ent1.get() != '':
            if processo.get() == "FIFO":
                janelaFifo(ent1.get())
            elif processo.get() == "LRU":
                janelaLRU()                           
        else:
            messagebox.showinfo(message="Preencha todos os campos!")

    lbl2 = Label(janela, text='Processo de escalonamento', anchor='center')
    lbl2.place(x=40, y=250)
    lbl2.configure(bg='#cf9416')

    processo = StringVar()
    processo.set( "FIFO" )
    proc_menu = OptionMenu(janela, processo, "FIFO", "LRU")
    proc_menu.place(x=200, y=250)

    botao_avancar = tk.Button(janela, text="Avançar", command=chamarEscal)
    botao_avancar.place(x=200, y=150)


    # Iniciar o loop principal
    janela.mainloop()
