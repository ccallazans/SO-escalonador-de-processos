from tkinter import *
from windows.processScheduler import process_window

def window():
    window = Tk()
    window.title("Escalonador: Processos e Memória")
    window.geometry("700x700")
    window.resizable(True, True)
    window.configure(bg="#bcbcbc")

    process_label = Label(window, text="Qtd de processos:", anchor="center")
    process_label.place(x=70, y=120)
    process_input = Entry(justify="center")
    process_input.place(x=200, y=120)

    def next_window():
        num_process = int(process_input.get())
        window.destroy()
        process_window(num_process)

    conffirm_button = Button(window, text ="Confirmar", command = next_window)
    conffirm_button.place(x=260, y=260)

    window.mainloop()
