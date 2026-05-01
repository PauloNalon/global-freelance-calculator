import tkinter as tk
from tkinter import messagebox
import requests
from fpdf import FPDF
from datetime import datetime
import os

def gerar_pdf_completo():
    try:
        # 1. PEGAR DADOS DA JANELA
        cliente = ent_cliente.get().strip() or "Cliente_Generico"
        renda_alvo = float(ent_renda.get())
        horas_dia = float(ent_horas.get())
        dias_mes = float(ent_dias.get())

        # 2. BUSCAR COTAÇÃO (API)
        url = "https://economia.awesomeapi.com.br/last/USD-BRL,EUR-BRL"
        dados = requests.get(url).json()
        usd = float(dados['USDBRL']['bid'])
        eur = float(dados['EURBRL']['bid'])

        # 3. CÁLCULOS
        v_brl = renda_alvo / (horas_dia * dias_mes)
        v_usd = v_brl / usd
        v_eur = v_brl / eur
        data_hoje = datetime.now().strftime("%d/%m/%Y %H:%M")
        
        # 4. ORGANIZAÇÃO DE PASTAS
        if not os.path.exists("orcamentos"):
            os.makedirs("orcamentos")
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M")
        nome_arquivo = f"orcamentos/Orcamento_{cliente}_{timestamp}.pdf"

        # 5. CRIAR O PDF
        pdf = FPDF()
        pdf.add_page()
        
        # Logo
        if os.path.exists("logo.png"):
            pdf.image("logo.png", x=10, y=8, w=30)
            pdf.set_font("Arial", "B", 16)
            pdf.cell(45)
            pdf.cell(150, 10, txt="ORCAMENTO INTERNACIONAL", ln=True, align="L")
        else:
            pdf.set_font("Arial", "B", 16)
            pdf.cell(200, 10, txt="ORCAMENTO INTERNACIONAL", ln=True, align="C")
            
        pdf.ln(20)
        
        # Informações do Cliente e Valores
        pdf.set_font("Arial", "B", 12)
        pdf.cell(200, 10, txt=f"Cliente: {cliente}", ln=True)
        pdf.set_font("Arial", "", 12)
        pdf.cell(200, 10, txt=f"Data: {data_hoje}", ln=True)
        pdf.ln(5)
        pdf.cell(200, 10, txt=f"Valor/Hora Reais: R$ {v_brl:.2f}", ln=True)
        pdf.cell(200, 10, txt=f"Valor/Hora Dolar: $ {v_usd:.2f}", ln=True)
        pdf.cell(200, 10, txt=f"Valor/Hora Euro: EUR {v_eur:.2f}", ln=True) # "EUR" garante compatibilidade
        
        # 6. SALVAR E ABRIR PASTA
        pdf.output(nome_arquivo)
        
        # Pega o caminho absoluto da pasta e abre no explorador do Windows
        caminho_pasta = os.path.abspath("orcamentos")
        os.startfile(caminho_pasta) 

        messagebox.showinfo("Sucesso!", f"Orcamento de {cliente} gerado!\nA pasta de arquivos foi aberta.")

    except ValueError:
        messagebox.showerror("Erro", "Preencha os valores numericos corretamente!")
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro: {e}")

# --- INTERFACE GRAFICA ---
janela = tk.Tk()
janela.title("Freelance Global UI")
janela.geometry("400x550")
janela.configure(bg="#f0f0f0")

tk.Label(janela, text="Calculadora de Orcamentos", font=("Arial", 16, "bold"), bg="#f0f0f0").pack(pady=20)

tk.Label(janela, text="Nome do Cliente:", bg="#f0f0f0", font=("Arial", 10, "bold")).pack()
ent_cliente = tk.Entry(janela, width=30)
ent_cliente.pack(pady=5)

tk.Label(janela, text="Quanto quer ganhar (R$)?", bg="#f0f0f0").pack()
ent_renda = tk.Entry(janela, width=30)
ent_renda.pack(pady=5)

tk.Label(janela, text="Horas de trabalho por dia:", bg="#f0f0f0").pack()
ent_horas = tk.Entry(janela, width=30)
ent_horas.pack(pady=5)

tk.Label(janela, text="Dias de trabalho por mes:", bg="#f0f0f0").pack()
ent_dias = tk.Entry(janela, width=30)
ent_dias.pack(pady=5)

btn_gerar = tk.Button(janela, text="GERAR ORCAMENTO PERSONALIZADO", command=gerar_pdf_completo, 
                      bg="#28a745", fg="white", font=("Arial", 10, "bold"), padx=10, pady=10)
btn_gerar.pack(pady=30)

janela.mainloop()