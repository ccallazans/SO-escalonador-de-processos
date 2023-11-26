from algorithms.Process import Process
from algorithms.Fifo import Fifo
from algorithms.Sjf import Sjf
from algorithms.RoundRobin import RoundRobin
from algorithms.Edf import Edf
from windows.memory import janelaFifo
from tkinter import *
import pandas as pd
import numpy as np

processesData = []
quantum = -1
overload = -1
pagina = -1

def process_window(numProcess):
    window = Tk()
    window.geometry("800x800")
    window.resizable(True, True)
    window.configure(bg="#bcbcbc")

    quantum_label = Label(window, text="Quantum", anchor="center")
    quantum_label.place(x=70, y=70)
    quantum_input = Entry(justify="center")
    quantum_input.place(x=70, y=120)

    if quantum >= 0:
        quantum_input.insert(0, quantum)

    overload_label = Label(window, text="Sobrecarga", anchor="center")
    overload_label.place(x=70, y=180)
    overload_input = Entry(justify="center")
    overload_input.place(x=70, y=220)

    if overload >= 0:
        overload_input.insert(0, overload)

    pagina_label = Label(window, text="Qtd Páginas", anchor="center")
    pagina_label.place(x=70, y=260)
    pagina_input = Entry(justify="center")
    pagina_input.place(x=70, y=280)

    if pagina >= 0:
        pagina_input.insert(0, pagina)

    select_memory = StringVar()
    select_memory.set("FIFO")
    select_memoryMenu = OptionMenu(window, select_memory, "FIFO", "LRU")
    select_memoryMenu.place(x=70, y=310)

    y_position = 30
    x_position = 250

    processes = []
    for actual_process in range(numProcess):
        y_position += 150

        label_process = Label(window, text=f"Id Processo: {actual_process}")
        label_process.place(x=x_position, y=y_position)

        label_t0 = Label(window, text="Tempo Início:")
        label_t0.place(x=x_position, y=y_position + 25)
        init_entry = Entry(window, justify="center")
        init_entry.place(x=x_position + 150, y=y_position + 25)

        label_t_exec = Label(window, text="Tempo de execução:")
        label_t_exec.place(x=x_position, y=y_position + 50)
        exec_entry = Entry(window, justify="center")
        exec_entry.place(x=x_position + 150, y=y_position + 50)

        label_deadline = Label(window, text="Deadline:")
        label_deadline.place(x=x_position, y=y_position + 75)
        dead_entry = Entry(window, justify="center")
        dead_entry.place(x=x_position + 150, y=y_position + 75)

        label_priority = Label(window, text="Prioridade:")
        label_priority.place(x=x_position, y=y_position + 100)
        pri_entry = Entry(window, justify="center")
        pri_entry.place(x=x_position + 150, y=y_position + 100)

        if len(processesData) > 0:
            init_entry.insert(0, processesData[actual_process][0])
            exec_entry.insert(0, processesData[actual_process][1])
            dead_entry.insert(0, processesData[actual_process][2])
            pri_entry.insert(0, processesData[actual_process][3])

        processes.append({"init":init_entry, "exec":exec_entry,"dead":dead_entry,"pri":pri_entry})

    algorithm = StringVar()
    algorithm.set("FIFO")
    algorithmMenu = OptionMenu(window, algorithm, "FIFO", "SJF", "Round Robin", "EDF")
    algorithmMenu.place(x=x_position + 50, y=y_position + 250)

    def simulate():    
        global processesData, quantum, overload, pagina

        processesData.clear()

        for process in processes:
            data = [process["init"].get(), process["exec"].get(), process["dead"].get(), process["pri"].get(), "1"]
            processesData.append(data)

        quantum = int(quantum_input.get())
        overload = int(overload_input.get())
        pagina = int(pagina_input.get())

        window.destroy()
        scheduler_window(numProcess, quantum, overload, processesData, algorithm.get(), select_memory.get(), pagina)

    proceed = Button(window, text="Simular", command=simulate)
    proceed.place(x=x_position + 130, y=y_position + 250)

    window.mainloop()

def scheduler_window(numProcess, quantum, overload, processesData, processAlgorithm, select_memory, pagina):
    window = Tk()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    window.title("Escalonador de Processos")
    window.geometry(f"{screen_width}x{screen_height}")
    window.configure(bg="#bcbcbc")
    window.focus()

    print(numProcess)
    y_position = 40
    x_position = 200
    box_width = 2

    progress_y = y_position + 150
    progress_n_rows = numProcess 
    progress_n_columns = 50 
    progress_table = pd.DataFrame(index=np.arange(progress_n_rows), columns=np.arange(progress_n_columns)) #Vai armazenar a tabela de grids

    for i in range(progress_n_rows):
        for j in range(progress_n_columns):
            progress_table.loc[i,j] = Entry(window, width=1, fg="black", font=("Arial", 16, "bold"))

            if j == 0:
                progress_table.loc[i,j].grid(row=i, column=j, padx=(x_position, 0))
            else:
                progress_table.loc[i,j].grid(row=i, column=j)

            if i == 0:
                progress_table.loc[i,j].grid(row=i, column=j, pady=(progress_y, 0))

    y = progress_y + 5
    for k in range(numProcess):
        lb = Label(window, text=str(k), font=("Arial", 8))
        lb.place(x=x_position-30, y=y)
        y = y + 28

        lb.configure(bg="#cf9416")

    x = x_position
    for k in range(progress_n_columns):
        lb = Label(window, text=str(k), font=("Arial", 8), width=1, justify='center')
        lb.place(x=x, y=progress_y - 22)

        x += 18.05

        lb.configure(bg="#cf9416")

    guide_exec = Entry(window, width=box_width, fg="black", font=("Arial",8))
    guide_exec.grid(row=0, column=0, padx=(x_position-100))
    guide_exec.configure(bg="Green")
    guide_exec_lb = Label(window, text="Executando", font=("Arial", 8))
    guide_exec_lb.place(x=x_position-80, y=95)
    guide_exec_lb.configure(bg="#cf9416")
    
    guide_exec = Entry(window, width=box_width, fg="black", font=("Arial",8))
    guide_exec.grid(row=0, column=0, padx=(x_position-100), pady=(30,0))
    guide_exec.configure(bg="Gray")
    guide_exec_lb = Label(window, text="Espera", font=("Arial", 8))
    guide_exec_lb.place(x=x_position-80, y=113)
    guide_exec_lb.configure(bg="#cf9416")
    
    guide_exec = Entry(window, width=box_width, fg="black", font=("Arial",8))
    guide_exec.grid(row=0, column=0, padx=(x_position-100), pady=(60,0))
    guide_exec.configure(bg="Red")
    guide_exec_lb = Label(window, text="Overload", font=("Arial", 8))
    guide_exec_lb.place(x=x_position-80, y=129)
    guide_exec_lb.configure(bg="#cf9416")
    
    guide_exec = Entry(window, width=box_width, fg="black", font=("Arial",8))
    guide_exec.grid(row=0, column=0, padx=(x_position-100), pady=(90,0))
    guide_exec.configure(bg="Blue")
    guide_exec_lb = Label(window, text="Estouro", font=("Arial", 8))
    guide_exec_lb.place(x=x_position-80, y=143)
    guide_exec_lb.configure(bg="#cf9416")

    var = IntVar()
    var.set(0)

    def stepByStep():
        var.set(0)
        return

    def automatic():
        var.set(1)
        return   
    
    def back():
        window.destroy()
        process_window(numProcess)

    step = Button(window,text =" Passo a Passo ", command = stepByStep)
    step.place(x=x_position, y=progress_y - 90)

    stop = Button(window,text =" Pausar ", command = stepByStep)
    stop.place(x=x_position + 120, y=progress_y - 90)

    proceed = Button(window,text =" Automático ", command = automatic)
    proceed.place(x=x_position + 190, y=progress_y - 90)

    turn_around_label = Label(window, text="", font=("Arial", 13))
    turn_around_label.place(x=x_position + 320, y=progress_y - 90)
    turn_around_label.configure(bg="#cf9416")

    voltar = Button(window,text =" Voltar ", command = back)
    voltar.place(x=x_position, y=progress_y - 55)

    print(numProcess)
    print(processesData)
    ProcessArray = [Process(processesData[i][0], processesData[i][1], processesData[i][2], processesData[i][3], processesData[i][4], i) for i in range(numProcess)]

    ##########################

    if select_memory == "FIFO":
        janelaFifo(pagina, window)

    ##########################

    process_interface_package = [window, progress_table, var, turn_around_label]

    fifo = Fifo(process_interface_package)
    sjf  = Sjf(process_interface_package)
    rr   = RoundRobin(quantum, overload, process_interface_package)
    edf  = Edf(quantum, overload, process_interface_package)

    print(processAlgorithm)
    if processAlgorithm == "FIFO":
        fifo.FIFO(ProcessArray)
    elif processAlgorithm == "SJF":
        sjf.Sjf(ProcessArray)
    elif processAlgorithm == "Round Robin":
        rr.RoundRobin(ProcessArray)
    elif processAlgorithm == "EDF":
        edf.Edf(ProcessArray)

    window.mainloop()
