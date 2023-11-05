from algorithms.Process import Process
from algorithms.Fifo import Fifo
from algorithms.Sjf import Sjf
from algorithms.RoundRobin import RoundRobin
from algorithms.Edf import Edf
from tkinter import *
import pandas as pd
import numpy as np

prev_proccess_data = []
prev_quantum = []
prev_overload = []

def process_window(num_process):
    window = Tk()
    window.geometry("800x800")
    window.resizable(True, True)
    window.configure(bg="#bcbcbc")

    quantum_label = Label(window, text="Quantum", anchor="center")
    quantum_label.place(x=70, y=70)
    quantum_input = Entry(justify="center")
    quantum_input.place(x=70, y=120)

    if len(prev_quantum) > 0:
        quantum_input.insert(0, prev_quantum[0])

    overload_label = Label(window, text="Sobrecarga", anchor="center")
    overload_label.place(x=70, y=180)
    overload_input = Entry(justify="center")
    overload_input.place(x=70, y=220)

    if len(prev_overload) > 0:
        overload_input.insert(0, prev_overload[0])

    process_data = []

    y_position = 30
    x_position = 250

    procs = []
    for actual_process in range(num_process):
        y_position += 150  # Adjust this value as needed

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

        if len(prev_proccess_data) > 0:
            init_entry.insert(0, prev_proccess_data[actual_process][0])
            exec_entry.insert(0, prev_proccess_data[actual_process][1])
            dead_entry.insert(0, prev_proccess_data[actual_process][2])
            pri_entry.insert(0, prev_proccess_data[actual_process][3])

        procs.append({"init":init_entry, "exec":exec_entry,"dead":dead_entry,"pri":pri_entry})

    def save_data():
        prev_proccess_data.clear()
        process_data.clear()

        for p in procs:
            data = [
                p["init"].get(),
                p["exec"].get(),
                p["dead"].get(),
                p["pri"].get(),
                "1"
            ]
            prev_proccess_data.append(data)
            process_data.append(data)

    process = StringVar()
    process.set("FIFO")
    proc_menu = OptionMenu(window, process, "FIFO", "SJF", "Round Robin", "EDF")
    proc_menu.place(x=x_position + 50, y=y_position + 250)

    def transfer_data():    
        save_data()

        quantum = int(quantum_input.get())
        overload = int(overload_input.get())

        prev_quantum.clear()
        prev_overload.clear()

        prev_quantum.append(quantum)
        prev_overload.append(overload)

        window.destroy()
        scheduler_window(num_process, quantum, overload, process_data, process.get())

    proceed = Button(window, text="Simular", command=transfer_data)
    proceed.place(x=x_position + 130, y=y_position + 250)

    window.mainloop()

def scheduler_window(num_process, quantum, overload, process_data, process_algorithm):
    print(num_process)
    y_position = 40
    x_position = 200

    window = Tk()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    window.title("Escalonador de Processos")
    window.geometry(f"{screen_width}x{screen_height}")
    window.configure(bg="#bcbcbc")
    window.focus()

    box_width = 2

    progress_y = y_position + 150
    progress_n_rows = num_process 
    progress_n_columns = 50 
    progress_table = pd.DataFrame(index=np.arange(progress_n_rows), columns=np.arange(progress_n_columns)) #Vai armazenar a tabela de grids

    for i in range(progress_n_rows):
        for j in range(progress_n_columns):
            progress_table.loc[i,j] = Entry(window, width=1, fg="black", font=("Arial", 16, "bold"))

            if j == 0:
                progress_table.loc[i,j].grid(row=i, column=j, padx=(x_position,0))
            else:
                progress_table.loc[i,j].grid(row=i, column=j)

            if i ==0:
                progress_table.loc[i,j].grid(row=i, column=j, pady=(progress_y,0))

    y = progress_y + 5
    for k in range(num_process): 
        lb = Label(window, text=str(k), font=("Arial", 8))
        lb.place(x=x_position-30, y=y)
        y = y + 28
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

    x = x_position
    for k in range(progress_n_columns+1): 
        lb = Label(window, text=str(k), font=("Arial", 8))
        lb.place(x=x, y=progress_y - 22)

        if k < 10:
            x += 15
        else:
            x += 16

        lb.configure(bg="#cf9416")

    var = IntVar()
    var.set(0)

    def Step():
        var.set(0)
        return
    def Auto():
        var.set(1)
        return   
    
    def call_open2():
        window.destroy()
        process_window(num_process)

    step = Button(window,text =" passo-a-passo ", command = Step)
    step.place(x=x_position, y=progress_y - 90)

    stop = Button(window,text =" pause ", command = Step)
    stop.place(x=x_position + 120, y=progress_y - 90)

    proceed = Button(window,text =" total ", command = Auto)
    proceed.place(x=x_position + 190, y=progress_y - 90)

    turn_around_label = Label(window, text="", font=("Arial", 13))
    turn_around_label.place(x=x_position + 290, y=progress_y - 90)
    turn_around_label.configure(bg="#cf9416")

    voltar = Button(window,text =" voltar ", command = call_open2)
    voltar.place(x=x_position, y=progress_y - 55)

    print(num_process)
    print(process_data)
    ProcessArray = [Process(process_data[i][0], process_data[i][1], process_data[i][2], process_data[i][3], process_data[i][4], i) for i in range(num_process)]

    process_interface_package = [window, progress_table, var, turn_around_label]

    fifo = Fifo(quantum, overload, process_interface_package)
    sjf  = Sjf(quantum, overload, process_interface_package)
    rr   = RoundRobin(quantum, overload, process_interface_package)
    edf  = Edf(quantum, overload, process_interface_package)

    print(process_algorithm)
    if process_algorithm == "FIFO":
        fifo.FIFO(ProcessArray)
    elif process_algorithm == "SJF":
        sjf.Sjf(ProcessArray)
    elif process_algorithm == "Round Robin":
        rr.RoundRobin(ProcessArray)
    elif process_algorithm == "EDF":
        edf.Edf(ProcessArray)

    window.mainloop()
