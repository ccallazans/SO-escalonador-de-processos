import time
import numpy as np
from os import system, name
from time import sleep

import tkinter as tk
from tkinter import *
from tkinter import ttk

class RoundRobin:

    ExecutingProcess = None

    def __init__(self, Quantum, Overload,process_interface):
        self.Quantum = Quantum
        self.Overload = Overload
        self.process_window = process_interface[0]
        self.progress_table = process_interface[2]
        self.var = process_interface[6]
        self.TurnAroundLabel = process_interface[7]

    def TurnAround(self, ProcessList):

        Turnaround = 0
        for process in ProcessList:
            Turnaround += process.WaitTime + process.ExecutionTime
        self.TurnAroundLabel.config(text = "Turn Around = " + str(Turnaround/ProcessList.size) )
        return Turnaround/ProcessList.size

    def RoundRobin(self, ProcessArray):

        WorkingArray = np.array([]) # lista de processos que serão executados, mas talvez ainda não esteja prontos

        for process in ProcessArray: # copia pq python é so por referencia
            WorkingArray = np.append(WorkingArray, process.clone() )

        CopyArray = np.array(WorkingArray)

        ReadyList = np.array([]) # lista de prontos
        TotalTime = 0 # conta tempo decorrido
        ProcessCount = WorkingArray.size # qtd de processos a serem executados
        ExecutingProcess = None # processo no estado executando

        Overloading = False
        OverloadTime = self.Overload

        #execuçao dos processos
        while ProcessCount != 0:

            for process in WorkingArray: # so coloca na lista de prontos se já chegou
                if process.StartTime <= TotalTime:
                    ReadyList = np.append(ReadyList, process)
                    WorkingArray = np.delete(WorkingArray, np.where(WorkingArray == process))
                    for i in range(TotalTime):
                        process.PrintList.append(" ")
            

            if ExecutingProcess == None: # escolhe o primeiro dos prontos se nenhum estiver sendo executado
                for process in ReadyList:
                    ExecutingProcess = process
                    break

            TotalTime += 1

            # Executando
            if not Overloading:
                if ExecutingProcess != None:
                    self.progress_table.loc[int(ExecutingProcess.ProcessId),TotalTime-1].configure({"background":'Green'}) #Ao ler o processo marca ele como verde
                    for process in ReadyList:
                        if process != ExecutingProcess:
                            self.progress_table.loc[int(process.ProcessId),TotalTime-1].configure({"background":'Grey'})
                    self.process_window.update()

                try:
                    ExecutingProcess.ExecutedTime += 1
                    ExecutingProcess.ExecutionTimePerQuantum += 1
                    ExecutingProcess.PrintList.append("X")

                    if ExecutingProcess.ExecutedTime == ExecutingProcess.ExecutionTime: # Remove o processo caso tenha terminado
                            ReadyList = np.delete(ReadyList, np.where(ReadyList == ExecutingProcess))
                            ExecutingProcess = None
                            ProcessCount -= 1        

                    elif ExecutingProcess.ExecutionTimePerQuantum == self.Quantum and self.Overload > 0: # Chega se acabou o tempo dele 
                        ExecutingProcess.ExecutionTimePerQuantum = 0
                        Overloading = True        

                except:
                    pass

                #Tempo de espera para calculo de turnaround
                for process in ReadyList:
                    if (process == ExecutingProcess) or (process.StartTime >= TotalTime):#não conta se é o que ta execuntado ou ainda "não chegou"
                        continue
                    process.PrintList.append("O")
                    process.WaitTime += 1

            else:
                self.progress_table.loc[int(ExecutingProcess.ProcessId),TotalTime-1].configure({"background":'Red'}) #Ao ler o processo marca ele como vermelho
                for process in ReadyList:
                    if process != ExecutingProcess:
                        self.progress_table.loc[int(process.ProcessId),TotalTime-1].configure({"background":'Grey'})
                self.process_window.update()

                ReadyList = np.delete(ReadyList, np.where(ReadyList == ExecutingProcess))
                ReadyList = np.append(ReadyList, ExecutingProcess)

                
                for process in ReadyList:
                    if process.StartTime > TotalTime:#não sei se é necessario mas ta funcionando com
                        continue
                    process.PrintList.append("#")
                    process.WaitTime += 1
                OverloadTime -= 1
                
                if OverloadTime <= 0: # terminando overload
                    OverloadTime = self.Overload
                    ExecutingProcess = None
                    Overloading = False
              
            for process in CopyArray:
                for i in range(process.WaitTime + process.ExecutedTime + process.StartTime ,TotalTime):
                    process.PrintList.append(" ")
            
            self.PrintProcess(CopyArray, TotalTime)

            if self.var.get() == 0:
                self.process_window.wait_variable(self.var)

                
        print("----------------------------------")
        
        print(f"Tempo total : {str(TotalTime)}")
        print("----------------------------------")
        

        print(f"Turnaround : {str(self.TurnAround(CopyArray))}")
        print("----------------------------------")
        return
    
    def PrintProcess(self,ProcessArray, TotalTime):
        # for windows
        if name == 'nt':
            _ = system('cls')
    
        # for mac and linux(here, os.name is 'posix')
        else:
            _ = system('clear')

       
        
        for process in ProcessArray:
            print(process.ProcessId, end = "")
            if process.StartTime < TotalTime:
                for j in range(TotalTime):
                    print(process.PrintList[j], end = "")
                if not process.MetDeadline:
                    print(" Estourou", end="")

        self.process_window.update_idletasks()
        time.sleep(1)               

        return