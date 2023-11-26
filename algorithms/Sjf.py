from time import sleep
import numpy as np

class Sjf:
    def __init__(self, process_interface):
        self.process_window = process_interface[0]
        self.progress_table = process_interface[1]
        self.var = process_interface[2]
        self.TurnAroundLabel = process_interface[3]
        self.alg_memoria = process_interface[4]

    def TurnAround(self, ProcessList):
        Turnaround = 0
        for process in ProcessList:
            Turnaround += process.WaitTime + process.ExecutionTime

        self.TurnAroundLabel.config(text = "Turn Around = " + str(Turnaround/ProcessList.size))

        return Turnaround/ProcessList.size
    
    def Sjf(self, ProcessArray):
        ProcessArrayCopy = np.array([]) 

        for process in ProcessArray:
            ProcessArrayCopy = np.append(ProcessArrayCopy, process.clone())

        WorkingList = np.array(ProcessArrayCopy) # lista de processos que serão executados
        TotalTime = 0 # conta o tempo decorrido
        ProcessCount = ProcessArrayCopy.size # quantidade de processos
        ExecutingProcess = None # processo em execução
        ReadyList = np.array([]) # lista de processos que chegaram e esperam sua vez

        # execuçao dos processos
        while ProcessCount != 0:
            sleep(1)

            if self.var.get() == 0:
                self.process_window.wait_variable(self.var)

            for process in WorkingList: # só coloca na lista de prontos se já chegou
                if process.StartTime <= TotalTime:
                    ReadyList = np.append(ReadyList, process)
                    WorkingList = np.delete(WorkingList, np.where(WorkingList == process))

            #Escolhe o proximo processo para executar
            if ExecutingProcess == None: # so escolhe o proximo se nenhum estiver sendo executado
                for process in ReadyList:
                    if process.StartTime <= TotalTime : # so escolhe o proximo processo caso alguem ja tenho chegado
                        if ExecutingProcess == None: # escolhe o 1 para comparação
                            ExecutingProcess = process
                        else: # encontra o processo com menor job dos que ja chegaram
                            if process.ExecutionTime - process.ExecutedTime  < ExecutingProcess.ExecutionTime - ExecutingProcess.ExecutedTime:
                                ExecutingProcess = process

            #Ao executar um processo atualiza a janela
            if ExecutingProcess != None:
                self.progress_table.loc[int(ExecutingProcess.ProcessId), TotalTime].configure({"background":'Green'}) # ao ler o processo marca ele como verde
                for process in ReadyList:
                    if process != ExecutingProcess:
                        self.progress_table.loc[int(process.ProcessId), TotalTime].configure({"background":'Grey'}) # ao esperar o processo marca ele como cinza
                self.process_window.update()
            
            TotalTime += 1

            try:
                ExecutingProcess.ExecutedTime += 1

                if ExecutingProcess.Deadline - (TotalTime - ExecutingProcess.StartTime) < 0:
                        self.progress_table.loc[int(ExecutingProcess.ProcessId), TotalTime - 1].configure({"background":'Green'}) # ao ler o processo marca ele como cinza
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
                if (process == ExecutingProcess) or (process.StartTime >= TotalTime): # não conta caso esteja executando ou ainda "não chegou"
                    continue
                process.WaitTime += 1

        self.TurnAround(ProcessArrayCopy)

        return
