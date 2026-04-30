import tkinter as tk
from tkinter import messagebox
import requests
from fpdf import FPDF
from datetime import datetime
import os # Importamos para criar a pasta

def gerar_pdf_completo():
    try:
        # 1. PEGAR DADOS DA JANELA
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
        
        # 4. ORGANIZAÇÃO DE PASTAS E ARQUIVO
        if not os.path.exists("orcamentos"):
            os.makedirs("orcamentos")
        
        # Gera um nome único com data e hora para não sobrescrever
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        nome_arquivo = f"orcamentos/orcamento_{timestamp}.pdf"

        # 5. CRIAR O PDF (APENAS UMA VEZ)
        pdf = FPDF()
        pdf.add_page()
        
        # Tenta colocar a logo (verifica se o arquivo logo.png existe)
        if os.path.exists("logo.png"):
            pdf.image("logo.png", x=10, y=8, w=30)
            pdf.set_font("Arial", "B", 16)
            pdf.cell(45) # Espaço para a logo
            pdf.cell(150, 10, txt="ORÇAMENTO INTERNACIONAL", ln=True, align="L")
        else:
            pdf.set_font("Arial", "B", 16)
            pdf.cell(200, 10, txt="ORÇAMENTO INTERNACIONAL", ln=True, align="C")
            
        pdf.ln(20)
        
        pdf.set_font("Arial", "", 12)
        pdf.cell(200, 10, txt=f"Data: {data_hoje}", ln=True)
        pdf.cell(200, 10, txt=f"Valor/Hora Reais: R$ {v_brl:.2f}", ln=True)
        pdf.cell(200, 10, txt=f"Valor/Hora Dólar: $ {v_usd:.2f}", ln=True)
        pdf.cell(200, 10, txt=f"Valor/Hora Euro:  $ {v_eur:.2f}", ln=True)
        
        # 6. SALVAR 
        pdf.output(nome_arquivo)

        messagebox.showinfo("Sucesso!", f"Orçamento salvo em:\n{nome_arquivo}")

    except ValueError:
        messagebox.showerror("Erro", "Por favor, digite apenas números nos campos!")
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro: {e}")

# --- INTERFACE GRÁFICA ---
janela = tk.Tk()
janela.title("Freelance Global UI")
janela.geometry("400x450")
janela.configure(bg="#f0f0f0")

tk.Label(janela, text="Calculadora de Orçamentos", font=("Arial", 16, "bold"), bg="#f0f0f0").pack(pady=20)

tk.Label(janela, text="Quanto quer ganhar (R$)?", bg="#f0f0f0").pack()
ent_renda = tk.Entry(janela)
ent_renda.pack(pady=5)

tk.Label(janela, text="Horas de trabalho por dia:", bg="#f0f0f0").pack()
ent_horas = tk.Entry(janela)
ent_horas.pack(pady=5)

tk.Label(janela, text="Dias de trabalho por mês:", bg="#f0f0f0").pack()
ent_dias = tk.Entry(janela)
ent_dias.pack(pady=5)

btn_gerar = tk.Button(janela, text="GERAR ORÇAMENTO PDF", command=gerar_pdf_completo, 
                      bg="#28a745", fg="white", font=("Arial", 10, "bold"), padx=10, pady=10)
btn_gerar.pack(pady=30)

janela.mainloop()