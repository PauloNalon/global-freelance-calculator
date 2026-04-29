import tkinter as tk
from tkinter import messagebox

def mostrar_mensagem():
    # Esta função roda quando clicamos no botão
    nome = entrada.get()
    messagebox.showinfo("Sucesso", f"Bonjour {nome}! Vamos gerar seu orçamento?")

# 1. Criar a janela principal
janela = tk.Tk()
janela.title("Global Freelance Calculator")
janela.geometry("400x300")

# 2. Adicionar um texto (Label)
label_titulo = tk.Label(janela, text="Bem-vindo ao seu App Internacional", font=("Arial", 14))
label_titulo.pack(pady=20)

# 3. Campo para digitar (Entry)
label_instrucao = tk.Label(janela, text="Digite seu nome:")
label_instrucao.pack()
entrada = tk.Entry(janela)
entrada.pack(pady=10)

# 4. Botão
botao = tk.Button(janela, text="Iniciar Processo", command=mostrar_mensagem, bg="blue", fg="white")
botao.pack(pady=20)

# 5. Manter a janela aberta
janela.mainloop()