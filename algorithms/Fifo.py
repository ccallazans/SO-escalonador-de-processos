from time import sleep
import numpy as np
from memories.FifoMemory import adicionar_valor_fis, adicionar_valor_vir
from windows.memory import janelaFifo

class Fifo:
    ExecutingProcess = None

    def __init__(self, process_interface):
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

    def FIFO(self, ProcessArray):
        if self.alg_memoria == "FIFO":
            canvas, quadrados, canvas2, quadrados2, mem_fisica, mem_virtual, pegarValores = janelaFifo(10, self.process_window)

        ProcessArrayCopy = np.array([])

        for process in ProcessArray:
            ProcessArrayCopy = np.append(ProcessArrayCopy, process.clone())

        WorkingList = np.array(ProcessArrayCopy) # lista de processos que serão executados
        TotalTime = 0 # conta o tempo decorrido
        ProcessCount = ProcessArrayCopy.size # quantidade de processos
        ExecutingProcess = None # processo em execução 
        ReadyList = np.array([]) # lista de processos que chegaram e esperam sua vez

        # execução dos processos
        while ProcessCount != 0:
            sleep(1)

            if self.var.get() == 0:
                self.process_window.wait_variable(self.var)

            for process in WorkingList: # só coloca na lista de prontos se já chegou
                if process.StartTime <= TotalTime:
                    ReadyList = np.append(ReadyList, process)
                    WorkingList = np.delete(WorkingList, np.where(WorkingList == process))

            # escolhe o próximo processo para executar
            if ExecutingProcess == None: # só escolhe o proximo se nenhum estiver sendo executado
                for process in ReadyList:
                    if process.StartTime <= TotalTime: # escolhe o primeiro caso alguem ja tenho chegado
                        ExecutingProcess = process
                        break

            # atualizando a janela ao executar um processo
            if ExecutingProcess != None:
                adicionar_valor_fis(self.process_window, int(ExecutingProcess.ProcessId), mem_fisica, mem_virtual, pegarValores, canvas, quadrados, self.num_paginas, canvas2, quadrados2)
                self.progress_table.loc[int(ExecutingProcess.ProcessId), TotalTime].configure({"background":"Green"}) # ao executar o processo marca ele como verde
                for process in ReadyList:
                    if process != ExecutingProcess:
                        self.progress_table.loc[int(process.ProcessId), TotalTime].configure({"background":"Grey"}) # ao esperar o processo marca ele como cinza
                self.process_window.update()

            TotalTime += 1

            try:
                ExecutingProcess.ExecutedTime += 1

                if ExecutingProcess.ExecutedTime == ExecutingProcess.ExecutionTime: # remove o processo caso tenha terminado
                    ReadyList = np.delete(ReadyList, np.where(ReadyList == ExecutingProcess))
                    ExecutingProcess = None
                    ProcessCount -= 1
            except:
                pass

            # tempo de espera para calculo de turnaround
            for process in ReadyList:
                if (process == ExecutingProcess) or (process.StartTime >= TotalTime): # não conta se é o que ta execuntado ou ainda "não chegou"
                    continue
                process.WaitTime += 1

        self.TurnAround(ProcessArrayCopy)

        return
