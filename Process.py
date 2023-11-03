class process:
    def __init__(self, StartTime = 0, ExecutionTime = 0, Deadline = 0, Priority = 0, MemoryPages = 0, ProcessId = 0 ):
        self.StartTime = int(StartTime) # tempo que o processo entrou na fila
        self.ExecutionTime = int(ExecutionTime) # tempo para execucao
        self.ExecutedTime = 0 # tempo ja executado
        self.ExecutionTimePerQuantum = 0
        self.WaitTime = 0 # tempo na fila de espera
        self.Deadline = int(Deadline) # prazo para concluir o processo
        self.Priority = int(Priority) # nivel de prioridade do processo
        self.ProcessId = int(ProcessId) # identificador do processo
        self.MemoryPages = int(MemoryPages) # numero de paginas que ocupa na memoria
        # self.MemorySize = 4 # mudar para 4098 ?
        self.MetDeadline = True #verificador se a deadline foi cumprida
        self.PrintList = []

    def clone(self):
        proc = process()
        proc.ProcessId = self.ProcessId
        proc.StartTime = self.StartTime
        proc.ExecutionTime = self.ExecutionTime
        proc.ExecutedTime = self.ExecutedTime
        proc.ExecutionTimePerQuantum = self.ExecutionTimePerQuantum
        proc.WaitTime = self.WaitTime
        proc.Deadline = self.Deadline
        proc.Priority = self.Priority
        proc.MemoryPages = self.MemoryPages
        #proc.MemorySize = self.MemorySize
        proc.MetDeadline = self.MetDeadline
        return proc

    def print_process(self):
        # aqui da pra quebra linha
        # no de baixo não
        # qual usar ?(- Fernando)
        # print(  "ProcessId: " + str(self.ProcessId) +
        #         " Chegada: " + str(self.StartTime) + 
        #         " Job: " + str(self.ExecutionTime) + 
        #         " Tempo executado : " + str(self.ExecutedTime) + 
        #         " Tempo de Espera : " + str(self.WaitTime) + 
        #         ("   Estourou Deadline" if not self.MetDeadline else "") )        

        #print em uma linha
        print(  f"ProcessId: {str(self.ProcessId)}" 
                f" Chegada: {str(self.StartTime)}" 
                f" Job: {str(self.ExecutionTime)}"
                f" Tempo executado: {str(self.ExecutedTime)}" 
                f" Tempo de Espera: {str(self.WaitTime)}")       
        return
