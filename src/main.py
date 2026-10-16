"""Análise exploratória da população de veículos elétricos.

O script reúne as análises desta etapa e salva os gráficos em ``output/graficos``.
Execute a partir de qualquer pasta com:
    python src/main.py
"""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


# Os caminhos partem da pasta do projeto, mesmo se o script for iniciado de outro lugar.
PASTA_PROJETO = Path(__file__).resolve().parent.parent
CAMINHO_CSV = PASTA_PROJETO / "data" / "Electric_Vehicle_Population_Data.csv"
PASTA_GRAFICOS = PASTA_PROJETO / "output" / "graficos"

# Nomes exatos das colunas usadas nas análises deste arquivo.
COLUNA_TIPO = "Electric Vehicle Type"
COLUNA_MARCA = "Make"
COLUNA_ANO = "Model Year"
COLUNA_CIDADE = "City"
COLUNA_AUTONOMIA = "Electric Range"


def carregar_dados():
    """Lê o CSV e prepara os campos usados nas análises deste arquivo."""
    if not CAMINHO_CSV.exists():
        raise FileNotFoundError(f"Não encontrei o arquivo de dados: {CAMINHO_CSV}")

    dados = pd.read_csv(CAMINHO_CSV, low_memory=False)

    # Conferimos as colunas logo no início para apontar claramente se o CSV mudou.
    colunas_necessarias = {
        COLUNA_TIPO,
        COLUNA_MARCA,
        COLUNA_ANO,
        COLUNA_CIDADE,
        COLUNA_AUTONOMIA,
    }
    faltantes = colunas_necessarias.difference(dados.columns)
    if faltantes:
        raise ValueError(f"Colunas esperadas não encontradas no CSV: {sorted(faltantes)}")

    # Remover espaços evita contar a mesma marca ou cidade como categorias diferentes.
    for coluna in (COLUNA_TIPO, COLUNA_MARCA, COLUNA_CIDADE):
        dados[coluna] = dados[coluna].astype("string").str.strip()
        dados[coluna] = dados[coluna].replace("", pd.NA)

    dados[COLUNA_ANO] = pd.to_numeric(dados[COLUNA_ANO], errors="coerce")
    dados[COLUNA_AUTONOMIA] = pd.to_numeric(dados[COLUNA_AUTONOMIA], errors="coerce")
    return dados


def salvar_grafico(nome_arquivo):
    """Padroniza a saída dos gráficos e fecha a figura após salvá-la."""
    PASTA_GRAFICOS.mkdir(parents=True, exist_ok=True)
    caminho = PASTA_GRAFICOS / nome_arquivo
    plt.tight_layout()
    plt.savefig(caminho, dpi=160, bbox_inches="tight")
    plt.close()
    print(f"Gráfico salvo em: {caminho.relative_to(PASTA_PROJETO)}")


def analisar_marcas(dados):
    """Pergunta 1: quais cinco marcas aparecem mais na base?"""
    contagem = dados[COLUNA_MARCA].dropna().value_counts().head(5).sort_values()
    print("\n1) Cinco marcas com mais veículos registrados:")
    print(contagem.sort_values(ascending=False).to_string())

    plt.figure(figsize=(9, 5))
    sns.barplot(x=contagem.values, y=contagem.index, color="#168aad")
    plt.title("As 5 marcas com mais veículos na base")
    plt.xlabel("Quantidade de veículos")
    plt.ylabel("Marca")
    salvar_grafico("01_top_5_marcas.png")


def analisar_tipos(dados):
    """Pergunta 2: qual é a participação de BEV e PHEV na frota?"""
    contagem = dados[COLUNA_TIPO].dropna().value_counts()
    proporcao = contagem / contagem.sum() * 100
    print("\n2) Proporção dos tipos de veículo:")
    for tipo, percentual in proporcao.items():
        print(f"{tipo}: {percentual:.2f}% ({contagem[tipo]:,} veículos)")

    # Mostramos todas as categorias encontradas para que nenhum tipo fique de fora.
    plt.figure(figsize=(8, 6))
    plt.pie(
        contagem.values,
        labels=contagem.index,
        autopct="%1.1f%%",
        startangle=90,
        colors=sns.color_palette("Set2", n_colors=len(contagem)),
    )
    plt.title("Participação por tipo de veículo elétrico")
    plt.axis("equal")
    salvar_grafico("02_proporcao_tipos.png")


def analisar_anos_modelo(dados):
    """Pergunta 3: como varia o volume por ano de fabricação do modelo?"""
    base = dados.dropna(subset=[COLUNA_ANO]).copy()
    if base.empty:
        print("\n3) Não há anos de modelo válidos para analisar.")
        return

    base[COLUNA_ANO] = base[COLUNA_ANO].astype(int)
    ano_final = int(base[COLUNA_ANO].max())
    ano_inicial = ano_final - 9
    contagem = (
        base.loc[base[COLUNA_ANO].between(ano_inicial, ano_final), COLUNA_ANO]
        .value_counts()
        .sort_index()
    )
    # Anos sem veículos ficam como zero, mantendo a linha contínua no gráfico.
    contagem = contagem.reindex(range(ano_inicial, ano_final + 1), fill_value=0)
    print(f"\n3) Veículos por ano de modelo ({ano_inicial}–{ano_final}):")
    print(contagem.to_string())

    plt.figure(figsize=(10, 5))
    sns.lineplot(x=contagem.index, y=contagem.values, marker="o", color="#168aad")
    plt.title("Veículos na base por ano do modelo (últimos 10 anos disponíveis)")
    plt.xlabel("Ano do modelo")
    plt.ylabel("Quantidade na base")
    plt.xticks(list(contagem.index), rotation=45)
    # Model Year é o ano do modelo, não o ano em que o registro entrou na base.
    salvar_grafico("03_veiculos_por_ano_modelo.png")


def analisar_autonomia(dados):
    """Pergunta 4: a autonomia média muda conforme o ano do modelo?"""
    base = dados.dropna(subset=[COLUNA_ANO, COLUNA_AUTONOMIA]).copy()
    # Autonomia zero costuma indicar dado não informado; incluí-la reduziria a média artificialmente.
    base = base.loc[base[COLUNA_AUTONOMIA] > 0]
    if base.empty:
        print("\n4) Não há valores positivos de autonomia para analisar.")
        return

    media = base.groupby(COLUNA_ANO)[COLUNA_AUTONOMIA].mean().sort_index()
    print("\n4) Autonomia elétrica média por ano de modelo (valores acima de zero):")
    print(media.round(1).to_string())

    plt.figure(figsize=(10, 5))
    sns.lineplot(x=media.index, y=media.values, marker="o", color="#2a9d8f")
    plt.title("Autonomia elétrica média por ano do modelo")
    plt.xlabel("Ano do modelo")
    plt.ylabel("Autonomia média (milhas)")
    plt.xticks(rotation=45)
    salvar_grafico("04_autonomia_media_por_ano.png")


def analisar_cidades(dados):
    """Pergunta 5: quais dez cidades concentram mais veículos na base?"""
    contagem = dados[COLUNA_CIDADE].dropna().value_counts().head(10).sort_values()
    print("\n5) Dez cidades com mais veículos registrados:")
    print(contagem.sort_values(ascending=False).to_string())

    plt.figure(figsize=(10, 6))
    sns.barplot(x=contagem.values, y=contagem.index, color="#e76f51")
    plt.title("Top 10 cidades por quantidade de veículos elétricos")
    plt.xlabel("Quantidade de veículos")
    plt.ylabel("Cidade")
    salvar_grafico("05_top_10_cidades.png")


def main():
    sns.set_theme(style="whitegrid")
    dados = carregar_dados()
    print(f"Base carregada: {len(dados):,} registros e {len(dados.columns)} colunas.")
    print("As análises abaixo usam os registros disponíveis no arquivo atual.")

    analisar_marcas(dados)
    analisar_tipos(dados)
    analisar_anos_modelo(dados)
    analisar_autonomia(dados)
    analisar_cidades(dados)

    print(f"\nConcluído. Os gráficos desta etapa estão em: {PASTA_GRAFICOS.relative_to(PASTA_PROJETO)}")


if __name__ == "__main__":
    main()
