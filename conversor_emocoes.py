import requests
import pyttsx3
import matplotlib.pyplot as plt
from textblob import TextBlob

def analisar_sentimento(texto):
    analise = TextBlob(texto)
    polaridade = analise.sentiment.polarity

    if polaridade > 0:
        sentimento = "Positivo"
    elif polaridade < 0:
        sentimento = "Negativo"
    else:
        sentimento = "Neutro"

    return polaridade, sentimento


def transformar_em_audio(texto, sentimento):
    engine = pyttsx3.init()

    if sentimento == "Positivo":
        engine.setProperty("rate", 180)
    elif sentimento == "Negativo":
        engine.setProperty("rate", 130)
    else:
        engine.setProperty("rate", 150)

    nome_arquivo = f"audio_{sentimento.lower()}.mp3"

    engine.save_to_file(texto, nome_arquivo)
    engine.runAndWait()

    print(f"Áudio salvo: {nome_arquivo}")


textos = [
    "Estou muito feliz com o resultado do meu projeto!",
    "Estou muito triste porque meu projeto não funcionou.",
    "Hoje foi um dia normal."
]

polaridades = []
sentimentos = []

for texto in textos:
    polaridade, sentimento = analisar_sentimento(texto)

    polaridades.append(polaridade)
    sentimentos.append(sentimento)

    print("\nTexto:", texto)
    print("Sentimento:", sentimento)
    print("Polaridade:", polaridade)

    transformar_em_audio(texto, sentimento)


plt.bar(range(len(textos)), polaridades)

plt.axhline(0, linewidth=0.8)

plt.xticks(
    range(len(textos)),
    [f"Texto {i + 1}" for i in range(len(textos))]
)

plt.ylabel("Polaridade")
plt.title("Análise de Sentimentos")

plt.show()
