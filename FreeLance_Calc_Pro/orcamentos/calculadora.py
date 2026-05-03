import requests
import csv
from datetime import datetime
from fpdf import FPDF

# --- PARTE 1: BUSCA DE DADOS ---
try:
    url = "https://economia.awesomeapi.com.br/last/USD-BRL,EUR-BRL"
    dados = requests.get(url).json()
    usd = float(dados['USDBRL']['bid'])
    eur = float(dados['EURBRL']['bid'])

    print(f"Cotações obtidas: USD {usd:.2f} | EUR {eur:.2f}")

    # --- PARTE 2: ENTRADAS ---
    renda = float(input("Quanto você quer ganhar por mês (R$)? "))
    h_dia = float(input("Horas por dia: "))
    d_mes = float(input("Dias por mês: "))

    # --- PARTE 3: CÁLCULOS ---
    v_brl = renda / (h_dia * d_mes)
    v_usd = v_brl / usd
    v_eur = v_brl / eur
    data_hoje = datetime.now().strftime("%d/%m/%Y %H:%M")

    # --- PARTE 4: GERAR PDF (BAOJIA) ---
    pdf = FPDF()
    pdf.add_page()
    
    # Cabeçalho
    pdf.set_font("Arial", "B", 20)
    pdf.set_text_color(40, 70, 150) # Azul profissional
    pdf.cell(200, 10, txt="ORÇAMENTO FREELANCE INTERNACIONAL", ln=True, align="C")
    
    pdf.set_font("Arial", "", 12)
    pdf.set_text_color(0, 0, 0) # Preto
    pdf.ln(10) # Pula linha
    pdf.cell(200, 10, txt=f"Data: {data_hoje}", ln=True)
    pdf.cell(200, 10, txt=f"Profissional: Paulo Nalon", ln=True)
    pdf.ln(10)

    # Tabela de Valores
    pdf.set_font("Arial", "B", 14)
    pdf.cell(200, 10, txt="Cálculo de Valor/Hora:", ln=True)
    pdf.set_font("Arial", "", 12)
    pdf.cell(200, 10, txt=f"- Valor em Reais: R$ {v_brl:.2f}", ln=True)
    pdf.cell(200, 10, txt=f"- Valor em Dólares: $ {v_usd:.2f} (Cotação: {usd:.2f})", ln=True)
    pdf.cell(200, 10, txt=f"- Valor em Euros:  euro {v_eur:.2f} (Cotação: {eur:.2f})", ln=True)

    pdf.ln(20)
    pdf.set_font("Arial", "I", 10)
    pdf.multi_cell(0, 10, txt="Este documento foi gerado automaticamente por um sistema Python para fins de planejamento de carreira internacional.")

    # Salva o PDF
    pdf.output("orcamento_freelance.pdf")

    # --- PARTE 5: SALVAR NO CSV (HISTÓRICO) ---
    with open('historico_orcamentos.csv', mode='a', newline='', encoding='utf-8') as f:
        csv.writer(f).writerow([data_hoje, renda, h_dia, d_mes, f"{v_brl:.2f}", f"{v_usd:.2f}", f"{v_eur:.2f}"])

    print("\n--- SUCESSO! ---")
    print("1. Histórico CSV atualizado.")
    print("2. 'orcamento_freelance.pdf' gerado com sucesso!")

except Exception as e:
    print(f"Ocorreu um erro: {e}")