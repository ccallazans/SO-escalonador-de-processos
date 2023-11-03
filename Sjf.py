import time
import numpy as np
from os import system, name
from time import sleep

import tkinter as tk
from tkinter import *
from tkinter import ttk

class Sjf:

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
    
    def Sjf(self, ProcessArray):
        CopyArray = np.array([]) 

        for process in ProcessArray: # copia pq python é so por referencia
            CopyArray = np.append(CopyArray, process.clone() )

        WorkingList = np.array(CopyArray) # lista de processos que serão executados, mas talvez ainda não esteja prontos
        TotalTime = 0 # conta o tempo decorrido
        ProcessCount = CopyArray.size
        ExecutingProcess = None #processo no estado executando
        ReadyList = np.array([]) #lista de processos que chegaram e esperam sua vez

        #execuçao dos processos
        while ProcessCount != 0:

            for process in WorkingList: # so coloca na lista de prontos se já chegou
                if process.StartTime <= TotalTime:
                    ReadyList = np.append(ReadyList, process)
                    WorkingList = np.delete(WorkingList, np.where(WorkingList == process))
                    for i in range(TotalTime):
                        process.PrintList.append(" ")

            #Escolhe o proximo
            if ExecutingProcess == None: # so escolhe o proximo se nenhum estiver sendo executado
                for process in ReadyList:
                    if process.StartTime <= TotalTime : # so escolhe o proximo caso alguem ja tenho chegado
                        if ExecutingProcess == None: # escolhe o 1 para comparação
                            ExecutingProcess = process
                        else: # encontra o com menor job dos que ja chegaram
                            if process.ExecutionTime - process.ExecutedTime  < ExecutingProcess.ExecutionTime - ExecutingProcess.ExecutedTime:
                                ExecutingProcess = process

            TotalTime += 1
            #Ao executar um processo atualiza a janela
            if ExecutingProcess != None:
                print(f'TotalTime: {TotalTime}') #Codigo de debug
                print(f'ProcessId: {int(ExecutingProcess.ProcessId)}') #Codigo de debug
                self.progress_table.loc[int(ExecutingProcess.ProcessId),TotalTime-1].configure({"background":'Green'}) #Ao ler o processo marca ele como verde
                for process in ReadyList:
                    if process != ExecutingProcess:
                        self.progress_table.loc[int(process.ProcessId),TotalTime-1].configure({"background":'Grey'})
                self.process_window.update()
            
            try:
                ExecutingProcess.ExecutedTime += 1
                ExecutingProcess.PrintList.append("X")

                if ExecutingProcess.Deadline - (TotalTime - ExecutingProcess.StartTime) < 0:
                        self.progress_table.loc[int(ExecutingProcess.ProcessId),TotalTime-1].configure({"background":'Green'}) #Ao ler o processo marca ele como cinza
                        self.process_window.update()
                        ExecutingProcess.MetDeadline = False

                if ExecutingProcess.ExecutedTime == ExecutingProcess.ExecutionTime: # Remove o processo caso tenha terminado
                        ReadyList = np.delete(ReadyList, np.where(ReadyList == ExecutingProcess))
                        ExecutingProcess = None
                        ProcessCount -= 1
          
            except:
                pass
            #Tempo de espera para calculo de turnaround
            for process in ReadyList:
                if (process == ExecutingProcess) or (process.StartTime >= TotalTime):#não conta se é o que ta execuntado ou ainda "não chegou"
                    continue
                process.PrintList.append("O")
                process.WaitTime += 1

            for process in CopyArray:
                for i in range(process.WaitTime + process.ExecutedTime + process.StartTime ,TotalTime):
                    process.PrintList.append(" ")
            
            self.PrintProcess(CopyArray, TotalTime)
            
            if self.var.get() == 0:
                self.process_window.wait_variable(self.var)
         


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