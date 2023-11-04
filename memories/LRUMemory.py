from windows.memory import *
from tkinter import *
from tkinter import messagebox

def janelaLRU():
    def page_fault(pf):
        if pf == "yes":
            texto = "Page Fault"
            textoPF = Label(window, text=texto, anchor="center", fg="blue", font=("Arial", 13))
            textoPF.place(x=485, y=185)

        if pf == "no":
            textoPF = Label(window, anchor="center", fg="blue", font=("Arial", 13), text="                  ")
            textoPF.place(x=485, y=185)
            textoPF.grid_remove()

    def candidato_a_sair():
        titCandidato = Label(window, text="Valor candidato a sair", anchor="center", fg="black", font=("Arial", 16))
        titCandidato.place(x=70, y=130)

        txtCandidato = Label(window, text=mem_fisica[0], anchor="center", fg="red", font=("Arial", 16))
        txtCandidato.place(x=150, y=160)

        if len(pegarValores) > len(mem_fisica):
            tam = len(pegarValores) - len(mem_fisica)
            textoForaMem = Label(window, text="Valores retirados da memória: ", anchor="center", fg="red", font=("Arial", 13))
            textoForaMem.place(x=335, y=385)
            x=10
            for i in range(tam):              
                textoForaMem2 = Label(window, text=pegarValores[i], anchor="center", font=("Arial", 13))
                textoForaMem2.place(x=x+335, y=405)
                x+=25
    
    def armazenar_valores():
        if entrada.get() != "":
            adicionar_valor_fis(entrada.get())
            entrada.delete(0, "end")
        else:
            messagebox.showinfo("VALOR INVÁLIDO!", "Insira um dado não vazio!")

    #Adiciona valor na memoria fisica
    def adicionar_valor_fis(num): 
        valor = num

        if valor not in mem_fisica:
            pegarValores.append(valor)

            if len(mem_fisica) >= 8:
                mem_fisica.pop(0)

            mem_fisica.append(valor)
            atualizar_pilha()
            page_fault("yes")
        else:
            mem_fisica.remove(valor)
            mem_fisica.append(valor)
            pegarValores.remove(valor)
            pegarValores.append(valor)
            atualizar_pilha()
            page_fault("no") 

    def atualizar_pilha():
        for i in range(8):
            if i < len(mem_fisica):
                canvas.itemconfigure(quadrados[i], text=mem_fisica[i])
            else:
                canvas.itemconfigure(quadrados[i], text="")

        candidato_a_sair()
    # --------------------------------------------------------------------------

    # Criar a janela
    window = Tk()
    window.title("Simulação de LRU")
    window.geometry("650x450+500+150")
    #window.resizable(height=False, width=False)

    # Criar o canvas para exibir os quadrados de memoria fisica
    canvas = Canvas(window, width=100, height=205)
    canvas.place(x=340, y=160)
    
    titulo = Label(window, text="Memoria Fisica", anchor="center")
    titulo.place(x=340, y=130)

    # Criar os quadrados dentro do canvas de memoria fisica
    quadrados = []
    x, y = 10, 10
    for i in range(8):
        quadrado = canvas.create_rectangle(x, y, x+80, y+20, outline="black")
        texto = canvas.create_text(x+40, y+10, text="")
        quadrados.append(texto)
        y += 25
        
        #imprime o valor de indice ao lado da tabela
        textoIndice = Label(window, text=i, anchor="center")
        textoIndice.place(x=335, y= y+135)

    # Criar os widgets
    entrada = Entry(window)
    entrada.place(x=40, y=45)    

    botao_adicionar = Button(window, text="Adicionar", command=armazenar_valores)
    botao_adicionar.place(x=40, y=15)

    mem_fisica   = []
    pegarValores = []

    # Iniciar o loop principal
    window.mainloop()
