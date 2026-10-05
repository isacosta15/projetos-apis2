import tkinter as tk
from tkinter import ttk, messagebox
import requests
import pandas as pd
import matplotlib.pyplot as plt


API_KEY = "SUA_API_KEY"

BASE_URL = "https://api.balldontlie.io/v1"

HEADERS = {
    "Authorization": API_KEY
}


def buscar_jogadores():

    url = f"{BASE_URL}/players"

    parametros = {
        "per_page": 100
    }

    try:

        resposta = requests.get(
            url,
            headers=HEADERS,
            params=parametros
        )

        if resposta.status_code != 200:
            messagebox.showerror(
                "Erro",
                "Não foi possível acessar a API."
            )
            return

        dados = resposta.json()

        jogadores = dados.get(
            "data",
            []
        )

        nomes = []

        for jogador in jogadores:

            nome = (
                jogador["first_name"]
                + " "
                + jogador["last_name"]
            )

            nomes.append(
                (
                    nome,
                    jogador["id"]
                )
            )

        combo_jogadores["values"] = [
            nome for nome, _ in nomes
        ]

        # Guardar IDs
        combo_jogadores.jogadores = nomes

        if nomes:
            combo_jogadores.current(0)

    except requests.exceptions.RequestException:

        messagebox.showerror(
            "Erro",
            "Verifique sua conexão com a internet."
        )


def buscar_estatisticas():

    selecionado = combo_jogadores.get()

    if not selecionado:
        messagebox.showwarning(
            "Atenção",
            "Selecione um jogador."
        )
        return

    jogador_id = None

    for nome, id_jogador in combo_jogadores.jogadores:

        if nome == selecionado:
            jogador_id = id_jogador
            break

    url = f"{BASE_URL}/stats"

    parametros = {
        "player_ids[]": jogador_id,
        "per_page": 100
    }

    try:

        resposta = requests.get(
            url,
            headers=HEADERS,
            params=parametros
        )

        if resposta.status_code != 200:

            messagebox.showerror(
                "Erro",
                "Não foi possível buscar as estatísticas."
            )

            return

        dados = resposta.json()

        estatisticas = dados.get(
            "data",
            []
        )

        if not estatisticas:

            messagebox.showinfo(
                "Resultado",
                "Nenhuma estatística encontrada."
            )

            return

        registros = []

        for jogo in estatisticas:

            registros.append({
                "Pontos": jogo.get("pts", 0) or 0,
                "Assistências": jogo.get("ast", 0) or 0,
                "Rebotes": jogo.get("reb", 0) or 0
            })

        df = pd.DataFrame(
            registros
        )

        pontos = df["Pontos"].mean()
        assistencias = df["Assistências"].mean()
        rebotes = df["Rebotes"].mean()

        label_pontos.config(
            text=f"{pontos:.1f}"
        )

        label_assistencias.config(
            text=f"{assistencias:.1f}"
        )

        label_rebotes.config(
            text=f"{rebotes:.1f}"
        )

        mostrar_grafico(
            pontos,
            assistencias,
            rebotes
        )

    except Exception as erro:

        messagebox.showerror(
            "Erro",
            str(erro)
        )


def mostrar_grafico(
    pontos,
    assistencias,
    rebotes
):

    estatisticas = {
        "Pontos": pontos,
        "Assistências": assistencias,
        "Rebotes": rebotes
    }

    plt.figure(
        figsize=(7, 5)
    )

    plt.bar(
        estatisticas.keys(),
        estatisticas.values()
    )

    plt.title(
        "Média de Estatísticas"
    )

    plt.ylabel(
        "Média"
    )

    plt.tight_layout()

    plt.show()


# ==========================
# INTERFACE
# ==========================

janela = tk.Tk()

janela.title(
    "Estatísticas Esportivas"
)

janela.geometry(
    "400x650"
)

janela.resizable(
    False,
    False
)


titulo = tk.Label(
    janela,
    text="Estatísticas Esportivas",
    font=("Arial", 19, "bold")
)

titulo.pack(
    pady=25
)


tk.Label(
    janela,
    text="Selecione um jogador:",
    font=("Arial", 11)
).pack()


combo_jogadores = ttk.Combobox(
    janela,
    width=30,
    state="readonly"
)

combo_jogadores.pack(
    pady=15
)


botao_buscar = tk.Button(
    janela,
    text="BUSCAR ESTATÍSTICAS",
    command=buscar_estatisticas,
    width=25,
    height=2
)

botao_buscar.pack(
    pady=10
)


# Pontos

tk.Label(
    janela,
    text="PONTOS",
    font=("Arial", 11)
).pack(
    pady=(25, 0)
)

label_pontos = tk.Label(
    janela,
    text="-",
    font=("Arial", 24, "bold")
)

label_pontos.pack()


# Assistências

tk.Label(
    janela,
    text="ASSISTÊNCIAS",
    font=("Arial", 11)
).pack(
    pady=(20, 0)
)

label_assistencias = tk.Label(
    janela,
    text="-",
    font=("Arial", 24, "bold")
)

label_assistencias.pack()


# Rebotes

tk.Label(
    janela,
    text="REBOTES",
    font=("Arial", 11)
).pack(
    pady=(20, 0)
)

label_rebotes = tk.Label(
    janela,
    text="-",
    font=("Arial", 24, "bold")
)

label_rebotes.pack()


# Carregar jogadores

buscar_jogadores()


janela.mainloop()
