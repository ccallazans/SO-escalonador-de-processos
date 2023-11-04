from memories.FifoMemory import janelaFifo
from memories.LRUMemory import janelaLRU
from tkinter import messagebox
from tkinter import *

def menuMemoria():
    window = Tk()
    window.geometry("400x400+500+150")
    window.resizable(height=False, width=False)
    window.configure(bg="#cf9416")

    lbl1 = Label(window, text="Quantidade de páginas", anchor="center")
    lbl1.place(x=70, y=120)
    ent1 = Entry(justify="center")
    ent1.place(x=200, y=120)
    lbl1.configure(bg="#cf9416")

    def chamarEscal():
        if ent1.get() != "":
            if processo.get() == "FIFO":
                janelaFifo(ent1.get())
            elif processo.get() == "LRU":
                janelaLRU()                           
        else:
            messagebox.showinfo(message="Preencha todos os campos!")

    lbl2 = Label(window, text="Processo de escalonamento", anchor="center")
    lbl2.place(x=40, y=250)
    lbl2.configure(bg="#cf9416")

    processo = StringVar()
    processo.set("FIFO")
    proc_menu = OptionMenu(window, processo, "FIFO", "LRU")
    proc_menu.place(x=200, y=250)

    botao_avancar = Button(window, text="Avançar", command=chamarEscal)
    botao_avancar.place(x=200, y=150)

    window.mainloop()
