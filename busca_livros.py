import tkinter as tk
from tkinter import messagebox
import requests
import pandas as pd
import matplotlib.pyplot as plt


def buscar_livros():
    pesquisa = entrada.get().strip()

    if not pesquisa:
        messagebox.showwarning(
            "Atenção",
            "Digite o nome de um livro ou autor."
        )
        return

    url = "https://www.googleapis.com/books/v1/volumes"

    parametros = {
        "q": pesquisa,
        "maxResults": 20
    }

    try:
        resposta = requests.get(
            url,
            params=parametros
        )

        if resposta.status_code != 200:
            messagebox.showerror(
                "Erro",
                "Não foi possível acessar a API."
            )
            return

        dados = resposta.json()

        livros = []

        for item in dados.get("items", []):
            volume = item.get("volumeInfo", {})

            titulo = volume.get(
                "title",
                "Título não informado"
            )

            autores = ", ".join(
                volume.get(
                    "authors",
                    ["Autor não informado"]
                )
            )

            categorias = ", ".join(
                volume.get(
                    "categories",
                    ["Não informado"]
                )
            )

            ano = volume.get(
                "publishedDate",
                "Não informado"
            )

            livros.append({
                "Título": titulo,
                "Autor": autores,
                "Gênero": categorias,
                "Ano": ano
            })

        if not livros:
            messagebox.showinfo(
                "Resultado",
                "Nenhum livro encontrado."
            )
            return

        mostrar_resultados(livros)

    except requests.exceptions.RequestException:
        messagebox.showerror(
            "Erro",
            "Verifique sua conexão com a internet."
        )


def mostrar_resultados(livros):

    for widget in frame_resultados.winfo_children():
        widget.destroy()

    for livro in livros:

        card = tk.Frame(
            frame_resultados,
            bd=1,
            relief="solid",
            padx=10,
            pady=8
        )

        card.pack(
            fill="x",
            pady=5
        )

        tk.Label(
            card,
            text=livro["Título"],
            font=("Arial", 11, "bold"),
            anchor="w"
        ).pack(fill="x")

        tk.Label(
            card,
            text=f"Autor: {livro['Autor']}",
            anchor="w"
        ).pack(fill="x")

        tk.Label(
            card,
            text=f"Gênero: {livro['Gênero']}",
            anchor="w"
        ).pack(fill="x")

        tk.Label(
            card,
            text=f"Ano: {livro['Ano']}",
            anchor="w"
        ).pack(fill="x")


def mostrar_graficos():

    pesquisa = entrada.get().strip()

    if not pesquisa:
        messagebox.showwarning(
            "Atenção",
            "Faça uma busca primeiro."
        )
        return

    url = "https://www.googleapis.com/books/v1/volumes"

    parametros = {
        "q": pesquisa,
        "maxResults": 40
    }

    try:
        resposta = requests.get(
            url,
            params=parametros
        )

        dados = resposta.json()

        livros = []

        for item in dados.get("items", []):

            volume = item.get("volumeInfo", {})

            categorias = volume.get(
                "categories",
                ["Não informado"]
            )

            ano = volume.get(
                "publishedDate",
                ""
            )

            livros.append({
                "Gênero": categorias[0],
                "Ano": str(ano)[:4]
            })

        if not livros:
            return

        df = pd.DataFrame(livros)

        # Gráfico de gêneros
        generos = df["Gênero"].value_counts().head(10)

        plt.figure(figsize=(8, 5))

        generos.plot(kind="bar")

        plt.title("Gêneros mais encontrados")
        plt.xlabel("Gênero")
        plt.ylabel("Quantidade")

        plt.xticks(rotation=45)
        plt.tight_layout()

        plt.show()

        # Gráfico de anos
        df["Ano"] = pd.to_numeric(
            df["Ano"],
            errors="coerce"
        )

        anos = (
            df.dropna(subset=["Ano"])["Ano"]
            .value_counts()
            .sort_index()
        )

        plt.figure(figsize=(8, 5))

        anos.plot(kind="bar")

        plt.title("Livros por ano de publicação")
        plt.xlabel("Ano")
        plt.ylabel("Quantidade")

        plt.tight_layout()

        plt.show()

    except Exception as erro:
        messagebox.showerror(
            "Erro",
            str(erro)
        )


# ==========================
# INTERFACE
# ==========================

janela = tk.Tk()

janela.title("Busca de Livros")
janela.geometry("420x700")
janela.resizable(False, False)

titulo = tk.Label(
    janela,
    text="Busca de Livros",
    font=("Arial", 20, "bold")
)

titulo.pack(pady=20)

subtitulo = tk.Label(
    janela,
    text="Pesquise por título ou autor",
    font=("Arial", 11)
)

subtitulo.pack()

entrada = tk.Entry(
    janela,
    width=38,
    font=("Arial", 12)
)

entrada.pack(pady=15)

botao_buscar = tk.Button(
    janela,
    text="🔍 BUSCAR",
    command=buscar_livros,
    width=20,
    height=2
)

botao_buscar.pack()

botao_graficos = tk.Button(
    janela,
    text="📊 VER GRÁFICOS",
    command=mostrar_graficos,
    width=20,
    height=2
)

botao_graficos.pack(pady=10)

tk.Label(
    janela,
    text="Resultados",
    font=("Arial", 13, "bold")
).pack(pady=10)

# Área com rolagem
canvas = tk.Canvas(janela)

scrollbar = tk.Scrollbar(
    janela,
    orient="vertical",
    command=canvas.yview
)

frame_resultados = tk.Frame(canvas)

frame_resultados.bind(
    "<Configure>",
    lambda e: canvas.configure(
        scrollregion=canvas.bbox("all")
    )
)

canvas.create_window(
    (0, 0),
    window=frame_resultados,
    anchor="nw",
    width=380
)

canvas.configure(
    yscrollcommand=scrollbar.set
)

canvas.pack(
    side="left",
    fill="both",
    expand=True,
    padx=(15, 0)
)

scrollbar.pack(
    side="right",
    fill="y"
)

janela.mainloop()
