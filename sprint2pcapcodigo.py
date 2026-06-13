import tkinter as tk
from tkinter import messagebox

# =========================
# CONFIGURAÇÃO DO SISTEMA
# =========================

LIMITE_REDE = 100  # kW
TARIFA_KWH = 1.20

# Carregadores iniciais (interoperabilidade entre marcas)
carregadores = [
    {"nome": "GoodWe Charger", "potencia": 30},
    {"nome": "ABB Charger", "potencia": 25},
    {"nome": "WEG Charger", "potencia": 20},
]

novo_carregador_adicionado = False


# =========================
# FUNÇÕES DO SISTEMA
# =========================

def calcular_total():
    return sum(c["potencia"] for c in carregadores)


def calcular_receita():
    total_kwh = calcular_total()
    return total_kwh * TARIFA_KWH


def atualizar_interface():
    texto = "=================================\n"
    texto += "CHARGEGRID INTELLIGENCE\n"
    texto += "=================================\n\n"

    total = calcular_total()

    texto += f"Limite da rede: {LIMITE_REDE} kW\n\n"

    for c in carregadores:
        texto += f"{c['nome']}: {c['potencia']} kW\n"

    texto += f"\nConsumo Total: {total} kW\n"

    if total > LIMITE_REDE:
        texto += "\n⚠ SOBRECARGA DETECTADA\n"
    else:
        texto += "\nSTATUS: NORMAL\n"

    receita = calcular_receita()
    texto += f"\nReceita: R$ {receita:.2f}\n"

    output.config(state="normal")
    output.delete("1.0", tk.END)
    output.insert(tk.END, texto)
    output.config(state="disabled")


def redistribuir_energia():
    """Simulação de IA para balanceamento de carga"""
    total = calcular_total()

    if total <= LIMITE_REDE:
        messagebox.showinfo("IA", "Sistema está estável. Nenhuma ação necessária.")
        return

    excesso = total - LIMITE_REDE

    # reduz proporcionalmente cada carregador
    for c in carregadores:
        reducao = (c["potencia"] / total) * excesso
        c["potencia"] -= reducao

    messagebox.showwarning("IA ATIVADA", "Sobrecarga detectada! Redistribuindo energia...")

    atualizar_interface()


def adicionar_carregador():
    global novo_carregador_adicionado

    if not novo_carregador_adicionado:
        carregadores.append({"nome": "Novo EV Charger", "potencia": 40})
        novo_carregador_adicionado = True
        messagebox.showinfo("Conexão", "Novo veículo conectado!")
    else:
        messagebox.showinfo("Info", "Já existe um carregador extra conectado.")

    atualizar_interface()


def resetar():
    global carregadores, novo_carregador_adicionado

    carregadores = [
        {"nome": "GoodWe Charger", "potencia": 30},
        {"nome": "ABB Charger", "potencia": 25},
        {"nome": "WEG Charger", "potencia": 20},
    ]
    novo_carregador_adicionado = False

    atualizar_interface()


# =========================
# INTERFACE (TKINTER)
# =========================

janela = tk.Tk()
janela.title("ChargeGrid Intelligence")
janela.geometry("600x500")

titulo = tk.Label(janela, text="ChargeGrid Intelligence", font=("Arial", 16, "bold"))
titulo.pack(pady=10)

output = tk.Text(janela, height=18, width=70)
output.pack()
output.config(state="disabled")

frame_botoes = tk.Frame(janela)
frame_botoes.pack(pady=10)

btn1 = tk.Button(frame_botoes, text="Atualizar", command=atualizar_interface)
btn1.grid(row=0, column=0, padx=5)

btn2 = tk.Button(frame_botoes, text="Conectar Veículo", command=adicionar_carregador)
btn2.grid(row=0, column=1, padx=5)

btn3 = tk.Button(frame_botoes, text="Ativar IA", command=redistribuir_energia)
btn3.grid(row=0, column=2, padx=5)

btn4 = tk.Button(frame_botoes, text="Resetar Sistema", command=resetar)
btn4.grid(row=0, column=3, padx=5)

# inicializa interface
atualizar_interface()

janela.mainloop()