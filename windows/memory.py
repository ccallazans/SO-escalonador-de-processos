from memories.FifoMemory import janelaFifo
from memories.LRUMemory import janelaLRU
from tkinter import messagebox
from tkinter import *

def menuMemoria():
    window = Tk()
    window.geometry("700x700")
    window.resizable(True, True)
    window.configure(bg="#bcbcbc")

    lbl1 = Label(window, text="Quantidade de páginas", anchor="center")
    lbl1.place(x=70, y=120)
    ent1 = Entry(justify="center")
    ent1.place(x=250, y=120)
    window.configure(bg="#bcbcbc")

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
    window.configure(bg="#bcbcbc")

    processo = StringVar()
    processo.set("FIFO")
    proc_menu = OptionMenu(window, processo, "FIFO", "LRU")
    proc_menu.place(x=250, y=250)

    botao_avancar = Button(window, text="Avançar", command=chamarEscal)
    botao_avancar.place(x=250, y=150)

    window.mainloop()
