import tkinter as tk
from tkinter import messagebox
from textblob import TextBlob
import pyttsx3


def analisar():
    texto = entrada.get("1.0", tk.END).strip()

    if not texto:
        messagebox.showwarning("Atenção", "Digite um texto.")
        return

    analise = TextBlob(texto)
    polaridade = analise.sentiment.polarity

    if polaridade > 0:
        sentimento = "Positivo"
    elif polaridade < 0:
        sentimento = "Negativo"
    else:
        sentimento = "Neutro"

    resultado.config(
        text=f"Sentimento: {sentimento}\n"
             f"Polaridade: {polaridade:.2f}"
    )

    gerar_audio(texto, sentimento)


def gerar_audio(texto, sentimento):
    engine = pyttsx3.init()

    if sentimento == "Positivo":
        engine.setProperty("rate", 180)
    elif sentimento == "Negativo":
        engine.setProperty("rate", 130)
    else:
        engine.setProperty("rate", 150)

    arquivo = f"audio_{sentimento.lower()}.mp3"

    engine.save_to_file(texto, arquivo)
    engine.runAndWait()

    messagebox.showinfo(
        "Áudio",
        f"Áudio salvo como:\n{arquivo}"
    )


# JANELA
janela = tk.Tk()
janela.title("Voz & Emoção")
janela.geometry("400x650")
janela.resizable(False, False)

titulo = tk.Label(
    janela,
    text="Conversor de Texto em Voz",
    font=("Arial", 18, "bold")
)

titulo.pack(pady=25)

tk.Label(
    janela,
    text="Digite seu texto:",
    font=("Arial", 12)
).pack()

entrada = tk.Text(
    janela,
    height=8,
    width=40
)

entrada.pack(pady=15)

botao = tk.Button(
    janela,
    text="ANALISAR",
    command=analisar,
    width=20,
    height=2
)

botao.pack(pady=10)

resultado = tk.Label(
    janela,
    text="Sentimento: -",
    font=("Arial", 13)
)

resultado.pack(pady=30)

janela.mainloop()
