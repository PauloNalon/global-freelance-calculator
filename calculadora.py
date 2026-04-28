import requests
import csv
from datetime import datetime

print("--- Calculadora Pro: Cotação Real + Histórico ---")

try:
    # 1. Busca cotação real
    url = "https://economia.awesomeapi.com.br/last/USD-BRL,EUR-BRL"
    dados = requests.get(url).json()
    usd = float(dados['USDBRL']['bid'])
    eur = float(dados['EURBRL']['bid'])

    # 2. Entradas
    renda = float(input("Renda mensal desejada (R$): "))
    h_dia = float(input("Horas de trabalho por dia: "))
    d_mes = float(input("Dias de trabalho por mês: "))

    # 3. Cálculos
    v_brl = renda / (h_dia * d_mes)
    v_usd = v_brl / usd
    v_eur = v_brl / eur

    # 4. Exibe no Terminal
    print(f"\nRESULTADO (Cotação USD: {usd:.2f} | EUR: {eur:.2f})")
    print(f"-> Valor/Hora: R$ {v_brl:.2f} | $ {v_usd:.2f} | € {v_eur:.2f}")

    # 5. O PULO DO GATO: Gravar no Banco de Dados (CSV)
    data_hoje = datetime.now().strftime("%d/%m/%Y %H:%M")
    
    # Abre o ficheiro em modo 'a' (append) para adicionar linhas sem apagar as antigas
    with open('historico_orcamentos.csv', mode='a', newline='', encoding='utf-8') as ficheiro:
        escritor = csv.writer(ficheiro)
        # Se o ficheiro estiver vazio, podes querer adicionar cabeçalhos (opcional)
        escritor.writerow([data_hoje, renda, h_dia, d_mes, f"{v_brl:.2f}", f"{v_usd:.2f}", f"{v_eur:.2f}"])

    print("\n[SUCESSO] Cálculo guardado no histórico (historico_orcamentos.csv)!")

except Exception as e:
    print(f"Erro: {e}")