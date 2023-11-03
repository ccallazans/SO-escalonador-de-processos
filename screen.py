import pandas as pd
import tkinter as tk
from tkinter import *
import Process
from Fifo import *
from Sjf import *
from RoundRobin import *
from Edf import *
from menuMemoria import *
import os

def window():
    window = Tk()
    window.title('Escalonador: Processos e Memória')
    window.geometry("400x400")
    window.resizable(False, False)
    window.configure(bg='#cf9416')
    current_working_directory = os.getcwd()
    # window.iconbitmap(current_working_directory + '/images/icon.ico')

    def chamarMemoria():
        window.destroy()
        menuMemoria()

    memory_button = Button(window, text ="Memoria", command = chamarMemoria)
    memory_button.place(x=70, y=70)

    process_label = Label(window, text='Qtd de processos', anchor='center')
    process_label.place(x=70, y=120)
    process_input = Entry(justify='center')
    process_input.place(x=200, y=120)

    quantum_label = Label(window, text='Quantum', anchor='center')
    quantum_label.place(x=70, y=150)
    quantum_input = Entry(justify='center')
    quantum_input.place(x=200, y=150)

    overload_label = Label(window, text='Sobrecarga', anchor='center')
    overload_label.place(x=70, y=180)
    overload_input = Entry(justify='center')
    overload_input.place(x=200, y=180)

    def next_window():
        num_process = int(process_input.get())
        quantum = int(quantum_input.get())
        overload = int(overload_input.get())
        window.destroy()
        process_window(num_process,quantum,overload)

    conffirm_button = Button(window,
                  text ="Confirmar",
                  command = next_window)
    conffirm_button.place(x=260, y=260)
    window.mainloop()

def process_window(num_process,quantum,overload):
    root= Tk()
    root.geometry('600x600')
    root.resizable(False, False)
    # root.iconbitmap('./images/icon.ico')
    root.configure(bg='#cf9416')

    process_data = {} 
    actual_process = 0 
    y_position = 70 
    x_position = 120 
    
    
    label_process = Label(root, text=f'Id Processo: {actual_process}')
    label_process.place(x=x_position, y=y_position)

    label_t0 = Label(root, text=f'Tempo Início:')
    label_t0.place(x=x_position, y=y_position + 25)
    init_entry = Entry(root, text='Tempo Início:')
    init_entry.place(x=x_position + 150, y=y_position + 25)

    label_t_exec = Label(root, text=f'Tempo de execução:')
    label_t_exec.place(x=x_position, y=y_position + 50)
    exec_entry = Entry(root, text='Tempo de execução:')
    exec_entry.place(x=x_position + 150, y=y_position + 50)

    label_deadline   = Label(root, text=f'Deadline:')  
    label_deadline.place(x=x_position, y=y_position + 75)
    dead_entry = Entry(root, text='Deadline:')
    dead_entry.place(x=x_position + 150, y=y_position + 75)

    label_priority = Label(root, text=f'Prioridade:')
    label_priority.place(x=x_position, y=y_position + 100)
    pri_entry = Entry(root, text='Prioridade:')
    pri_entry.place(x=x_position + 150, y=y_position + 100)

    def check_if_all_fields_are_occupied():
        filled = False
        values = [  init_entry.get(), 
                    exec_entry.get(), 
                    dead_entry.get(), 
                    pri_entry.get(),  
                    '1']
        if "" not in values:
            print("Filled")
            filled = True

        return filled

    def clean_fields():
        init_entry.delete(0, END)
        exec_entry.delete(0, END)
        dead_entry.delete(0, END)
        pri_entry.delete(0, END)

    def next_process():
        nonlocal actual_process
        init_entry.focus()
        if check_if_all_fields_are_occupied(): 
            if actual_process < num_process: 
                
                process_data[str(actual_process)] = [init_entry.get(), 
                                              exec_entry.get(), 
                                              dead_entry.get(), 
                                              pri_entry.get(),  
                                              '1']
                actual_process += 1 
                if actual_process < num_process: 
                    label_process.configure(text=f'Processo(Id): {actual_process}')
                    clean_fields()
        else:
            messagebox.showinfo(message="Preencha todos os campos!")

    next = Button(root,text ="Preencher Próximo", command = next_process)
    next.place(x=x_position + 225, y=y_position + 175)

    label_scheduler = Label(root, text='Escalonador de processos')
    label_scheduler.place(x=x_position, y=y_position + 230)

    process = StringVar()
    process.set( "FIFO" )
    proc_menu = OptionMenu(root, process, "FIFO", "SJF", "Round Robin", "EDF")
    proc_menu.place(x=x_position + 180, y=y_position + 230)

    """label_memory = Label(root, text='Escalonador de memoria')
    label_memory.place(x=x_position, y=y_position + 280)

    memory = StringVar()
    memory.set( "FIFO" )
    mem_menu = OptionMenu(root, memory, "FIFO", "MRU")
    mem_menu.place(x=x_position + 180, y=y_position + 280)"""

    def transfer_data():
        if len(process_data) == num_process-1 and check_if_all_fields_are_occupied():
            nonlocal actual_process
            process_data[str(actual_process)] = [init_entry.get(), 
                                              exec_entry.get(), 
                                              dead_entry.get(), 
                                              pri_entry.get(),  
                                              '1']
            actual_process += 1
        elif len(process_data) != num_process: 
            messagebox.showinfo(message="Ainda faltam processos a serem cadastrados")
            return
    
        process_algorithm = process.get()
        root.destroy()
        sheduler_window(num_process, quantum, overload, process_data, process_algorithm)

    proceed = Button(root,text ="Simular", command = transfer_data)
    proceed.place(x=x_position + 100, y=y_position + 330)

def sheduler_window(num_process, quantum, overload, process_data,process_algorithm):
    y_position = 40
    x_position = 200

    process_window = Tk()
    screen_width = process_window.winfo_screenwidth()
    screen_height = process_window.winfo_screenheight()
    process_window.title('Escalonador de Processos')
    process_window.geometry(f"{screen_width}x{screen_height}")
    process_window.configure(bg='#cf9416')
    # process_window.iconbitmap('./images/icon.ico')
    process_window.focus()

    box_width = 2
    info_n_rows = num_process 
    info_n_columns = 6 
    info_table = pd.DataFrame(index=np.arange(info_n_rows), columns=np.arange(info_n_columns)) #Vai armazenar a tabela de grids

    progress_y = y_position + 150
    progress_n_rows = num_process 
    progress_n_columns = 50 
    progress_table = pd.DataFrame(index=np.arange(progress_n_rows), columns=np.arange(progress_n_columns)) #Vai armazenar a tabela de grids

    for i in range(progress_n_rows):
        for j in range(progress_n_columns):
            progress_table.loc[i,j] = Entry(process_window, width=1, fg='black',
                        font=('Arial',16,'bold'))
            if j == 0:
                progress_table.loc[i,j].grid(row=i, column=j, padx=(x_position,0))
            else:
                progress_table.loc[i,j].grid(row=i, column=j)

            if i ==0:
                progress_table.loc[i,j].grid(row=i, column=j, pady=(progress_y,0))

    y = progress_y + 5
    for k in range(num_process): 
        lb = Label(process_window, text=str(k), font=("Arial", 8))
        lb.place(x=x_position-30, y=y)
        y = y + 28
        lb.configure(bg='#cf9416')


    guide_exec = Entry(process_window, width=box_width, fg='black',
                        font=('Arial',8))
    guide_exec.grid(row=0, column=0, padx=(x_position-100))
    guide_exec.configure(bg='Green')
    guide_exec_lb = Label(process_window, text='Executando', font=("Arial", 8))
    guide_exec_lb.place(x=x_position-80, y=95)
    guide_exec_lb.configure(bg='#cf9416')
    
    guide_exec = Entry(process_window, width=box_width, fg='black',
                        font=('Arial',8))
    guide_exec.grid(row=0, column=0, padx=(x_position-100), pady=(30,0))
    guide_exec.configure(bg='Gray')
    guide_exec_lb = Label(process_window, text='Espera', font=("Arial", 8))
    guide_exec_lb.place(x=x_position-80, y=113)
    guide_exec_lb.configure(bg='#cf9416')
    
    guide_exec = Entry(process_window, width=box_width, fg='black',
                        font=('Arial',8))
    guide_exec.grid(row=0, column=0, padx=(x_position-100), pady=(60,0))
    guide_exec.configure(bg='Red')
    guide_exec_lb = Label(process_window, text='Overload', font=("Arial", 8))
    guide_exec_lb.place(x=x_position-80, y=129)
    guide_exec_lb.configure(bg='#cf9416')
    
    guide_exec = Entry(process_window, width=box_width, fg='black',
                        font=('Arial',8))
    guide_exec.grid(row=0, column=0, padx=(x_position-100), pady=(90,0))
    guide_exec.configure(bg='Blue')
    guide_exec_lb = Label(process_window, text='Estouro', font=("Arial", 8))
    guide_exec_lb.place(x=x_position-80, y=143)
    guide_exec_lb.configure(bg='#cf9416')

    x = x_position
    for k in range(progress_n_columns+1): 
        lb = Label(process_window, text=str(k), font=("Arial", 8))
        lb.place(x=x, y=progress_y - 22)
        if k < 10:
            x += 15
        else:
            x += 16
        lb.configure(bg='#cf9416')

    var = tk.IntVar()
    var.set(0)

    def Step():
        var.set(0)
        return
    def Auto():
        var.set(1)
        return   
    
    def call_open2():
        process_window.destroy()
        window()

    step = Button(process_window,text =" passo-a-passo ", command = Step)
    step.place(x=x_position, y=progress_y - 90)

    stop = Button(process_window,text =" pause ", command = Step)
    stop.place(x=x_position + 120, y=progress_y - 90)

    proceed = Button(process_window,text =" total ", command = Auto)
    proceed.place(x=x_position + 190, y=progress_y - 90)

    turn_around_label = Label(process_window, text='', font=("Arial", 13))
    turn_around_label.place(x=x_position + 290, y=progress_y - 90)
    turn_around_label.configure(bg='#cf9416')

    voltar = Button(process_window,text =" voltar ", command = call_open2)
    voltar.place(x=x_position, y=progress_y - 55)



    ProcessArray = [Process.process(process_data[str(i)][0],process_data[str(i)][1],process_data[str(i)][2],process_data[str(i)][3],process_data[str(i)][4],i) for i in range(num_process)]

    process_interface_package = [process_window, info_table, progress_table, step, stop, proceed, var , turn_around_label]

    fifo = Fifo(quantum, overload, process_interface_package)
    sjf  = Sjf(quantum, overload, process_interface_package)
    rr   = RoundRobin(quantum, overload, process_interface_package)
    edf  = Edf(quantum, overload, process_interface_package)

    print(process_algorithm)
    if process_algorithm == 'FIFO':
        fifo.FIFO(ProcessArray)
    elif process_algorithm == 'SJF':
        sjf.Sjf(ProcessArray)
    elif process_algorithm == 'Round Robin':
        rr.RoundRobin(ProcessArray)
    elif process_algorithm == 'EDF':
        edf.Edf(ProcessArray)

    process_window.mainloop()