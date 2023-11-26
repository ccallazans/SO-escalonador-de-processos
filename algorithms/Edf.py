from time import sleep
import numpy as np
from memories.FifoMemory import adicionar_valor_fis, adicionar_valor_vir
from windows.memory import janelaFifo

class Edf:
    ExecutingProcess = None

    def __init__(self, Quantum, Overload, process_interface):
        self.Quantum = Quantum
        self.Overload = Overload
        self.process_window = process_interface[0]
        self.progress_table = process_interface[1]
        self.var = process_interface[2]
        self.TurnAroundLabel = process_interface[3]
        self.alg_memoria = process_interface[4]
        self.num_paginas = process_interface[5]

    def TurnAround(self, ProcessList):
        Turnaround = 0

        for process in ProcessList:
            Turnaround += process.WaitTime + process.ExecutionTime

        self.TurnAroundLabel.config(text = "Turn Around = " + str(Turnaround/ProcessList.size))
        
        return Turnaround/ProcessList.size
    
    def Edf(self, ProcessArray):
        if self.alg_memoria == "FIFO":
            canvas, quadrados, canvas2, quadrados2, mem_fisica, mem_virtual, pegarValores = janelaFifo(10, self.process_window)

        WorkingArray = np.array([]) # lista de processos que serão executados

        for process in ProcessArray:
            WorkingArray = np.append(WorkingArray, process.clone())

        ProcessArrayCopy = np.array(WorkingArray)

        ReadyList = np.array([]) # lista de prontos
        TotalTime = 0 # conta o tempo decorrido
        ProcessCount = WorkingArray.size # quantidade de processos
        ExecutingProcess = None # processo em execução

        Overloading = False
        OverloadTime = self.Overload

        #execuçao dos processos
        while ProcessCount != 0:
            sleep(1)

            if self.var.get() == 0:
                self.process_window.wait_variable(self.var)

            for process in WorkingArray:# so coloca na lista de prontos se já chegou
                if process.StartTime <= TotalTime:
                    ReadyList = np.append(ReadyList, process)
                    WorkingArray = np.delete(WorkingArray, np.where(WorkingArray == process))

            if ExecutingProcess == None:  # so escolhe o proximo se nenhum estiver sendo executado
                for process in ReadyList:
                    if process.StartTime <= TotalTime : # so escolhe o proximo processo caso alguem ja tenho chegado
                        if ExecutingProcess == None: # escolhe o 1 para comparação
                            ExecutingProcess = process
                        else: # encontra o deadline mais cede dos que ja chegaram
                            if process.Deadline - (TotalTime - process.StartTime)  < ExecutingProcess.Deadline - (TotalTime - ExecutingProcess.StartTime):
                                ExecutingProcess = process

            TotalTime += 1

            # Executando
            if not Overloading:
                try:
                    ExecutingProcess.ExecutedTime += 1
                    ExecutingProcess.ExecutionTimePerQuantum += 1

                    if ExecutingProcess != None:
                        adicionar_valor_fis(self.process_window, int(ExecutingProcess.ProcessId), mem_fisica, mem_virtual, pegarValores, canvas, quadrados, self.num_paginas, canvas2, quadrados2)
                
                        self.progress_table.loc[int(ExecutingProcess.ProcessId),TotalTime-1].configure({"background":'Green'}) #Ao ler o processo marca ele como verde
                        for process in ReadyList:
                            if process != ExecutingProcess:
                                self.progress_table.loc[int(process.ProcessId),TotalTime-1].configure({"background":'Grey'})
                        self.process_window.update()
                    
                    if ExecutingProcess.Deadline - (TotalTime - ExecutingProcess.StartTime) < 0:
                        self.progress_table.loc[int(ExecutingProcess.ProcessId),TotalTime-1].configure({"background":'Blue'}) #Ao ler o processo marca ele como cinza
                        self.process_window.update()
                        ExecutingProcess.MetDeadline = False
                
                    if ExecutingProcess.ExecutedTime == ExecutingProcess.ExecutionTime: # Remove o processo caso tenha terminado
                            ReadyList = np.delete(ReadyList, np.where(ReadyList == ExecutingProcess))
                            ExecutingProcess = None
                            ProcessCount -= 1        

                    elif ExecutingProcess.ExecutionTimePerQuantum == self.Quantum and self.Overload > 0:# Chega se acabou o tempo dele 
                        ExecutingProcess.ExecutionTimePerQuantum = 0
                        Overloading = True        
                except:
                    pass

                #Tempo de espera para calculo de turnaround
                for process in ReadyList:
                    if (process == ExecutingProcess) or (process.StartTime >= TotalTime): # não conta caso esteja executando ou ainda "não chegou"
                        continue

                    process.WaitTime += 1
            else:
                # Overloading
                if ExecutingProcess != None:
                    self.progress_table.loc[int(ExecutingProcess.ProcessId), TotalTime - 1].configure({"background":'Red'}) #Ao ler o processo marca ele como vermelho
                    for process in ReadyList:
                        if process != ExecutingProcess:
                            self.progress_table.loc[int(process.ProcessId), TotalTime - 1].configure({"background":'Grey'})
                    self.process_window.update()

                ReadyList = np.delete(ReadyList, np.where(ReadyList == ExecutingProcess))
                ReadyList = np.append(ReadyList, ExecutingProcess)

                
                for process in ReadyList:
                    if process.StartTime > TotalTime:
                        continue
                    process.WaitTime += 1

                OverloadTime -= 1
                if OverloadTime <= 0: # terminando overload
                    OverloadTime = self.Overload
                    ExecutingProcess = None
                    Overloading = False

        self.TurnAround(ProcessArrayCopy)
                
        return
