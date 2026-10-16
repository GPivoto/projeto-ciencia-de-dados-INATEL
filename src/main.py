from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


PASTA_PROJETO = Path(__file__).resolve().parent.parent
CAMINHO_CSV = PASTA_PROJETO / "data" / "Electric_Vehicle_Population_Data.csv"
PASTA_GRAFICOS = PASTA_PROJETO / "output" / "graficos"

COLUNA_TIPO = "Electric Vehicle Type"
COLUNA_MARCA = "Make"
COLUNA_ANO = "Model Year"
COLUNA_CIDADE = "City"
COLUNA_AUTONOMIA = "Electric Range"
COLUNA_CAFV = "Clean Alternative Fuel Vehicle (CAFV) Eligibility"
COLUNA_CONDADO = "County"


def carregar_dados():
    if not CAMINHO_CSV.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {CAMINHO_CSV}")

    dados = pd.read_csv(CAMINHO_CSV, low_memory=False)

    colunas_necessarias = {
        COLUNA_TIPO,
        COLUNA_MARCA,
        COLUNA_ANO,
        COLUNA_CIDADE,
        COLUNA_AUTONOMIA,
    }
    faltantes = colunas_necessarias.difference(dados.columns)
    if faltantes:
        raise ValueError(f"Colunas ausentes no CSV: {sorted(faltantes)}")

    for coluna in (COLUNA_TIPO, COLUNA_MARCA, COLUNA_CIDADE):
        if coluna in dados.columns:
            dados[coluna] = dados[coluna].astype("string").str.strip()
            dados[coluna] = dados[coluna].replace("", pd.NA)

    if COLUNA_CAFV in dados.columns:
        dados[COLUNA_CAFV] = dados[COLUNA_CAFV].astype("string").str.strip()

    if COLUNA_CONDADO in dados.columns:
        dados[COLUNA_CONDADO] = dados[COLUNA_CONDADO].astype("string").str.strip()

    dados[COLUNA_ANO] = pd.to_numeric(dados[COLUNA_ANO], errors="coerce")
    dados[COLUNA_AUTONOMIA] = pd.to_numeric(dados[COLUNA_AUTONOMIA], errors="coerce")
    return dados


def salvar_grafico(nome_arquivo):
    PASTA_GRAFICOS.mkdir(parents=True, exist_ok=True)
    caminho = PASTA_GRAFICOS / nome_arquivo
    plt.tight_layout()
    plt.savefig(caminho, dpi=160, bbox_inches="tight")
    plt.close()
    print(f"Salvo: {caminho.relative_to(PASTA_PROJETO)}")


def analisar_marcas(dados):
    contagem = dados[COLUNA_MARCA].dropna().value_counts().head(5).sort_values()
    print("\n1) Top 5 marcas:")
    print(contagem.sort_values(ascending=False).to_string())

    plt.figure(figsize=(9, 5))
    sns.barplot(x=contagem.values, y=contagem.index, color="#168aad")
    plt.title("As 5 marcas com mais veículos na base")
    plt.xlabel("Quantidade de veículos")
    plt.ylabel("Marca")
    salvar_grafico("01_top_5_marcas.png")


def analisar_tipos(dados):
    contagem = dados[COLUNA_TIPO].dropna().value_counts()
    proporcao = contagem / contagem.sum() * 100
    print("\n2) Proporção de tipos:")
    for tipo, percentual in proporcao.items():
        print(f"{tipo}: {percentual:.2f}% ({contagem[tipo]:,} veículos)")

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
    base = dados.dropna(subset=[COLUNA_ANO]).copy()
    if base.empty:
        return

    base[COLUNA_ANO] = base[COLUNA_ANO].astype(int)
    ano_final = int(base[COLUNA_ANO].max())
    ano_inicial = ano_final - 9
    contagem = (
        base.loc[base[COLUNA_ANO].between(ano_inicial, ano_final), COLUNA_ANO]
        .value_counts()
        .sort_index()
    )
    contagem = contagem.reindex(range(ano_inicial, ano_final + 1), fill_value=0)
    print(f"\n3) Veículos por ano ({ano_inicial}–{ano_final}):")
    print(contagem.to_string())

    plt.figure(figsize=(10, 5))
    sns.lineplot(x=contagem.index, y=contagem.values, marker="o", color="#168aad")
    plt.title("Veículos na base por ano do modelo (últimos 10 anos)")
    plt.xlabel("Ano do modelo")
    plt.ylabel("Quantidade na base")
    plt.xticks(list(contagem.index), rotation=45)
    salvar_grafico("03_veiculos_por_ano_modelo.png")


def analisar_autonomia(dados):
    base = dados.dropna(subset=[COLUNA_ANO, COLUNA_AUTONOMIA]).copy()
    base = base.loc[base[COLUNA_AUTONOMIA] > 0]
    if base.empty:
        return

    media = base.groupby(COLUNA_ANO)[COLUNA_AUTONOMIA].mean().sort_index()
    print("\n4) Autonomia média por ano:")
    print(media.round(1).to_string())

    plt.figure(figsize=(10, 5))
    sns.lineplot(x=media.index, y=media.values, marker="o", color="#2a9d8f")
    plt.title("Autonomia elétrica média por ano do modelo")
    plt.xlabel("Ano do modelo")
    plt.ylabel("Autonomia média (milhas)")
    plt.xticks(rotation=45)
    salvar_grafico("04_autonomia_media_por_ano.png")


def analisar_cidades(dados):
    contagem = dados[COLUNA_CIDADE].dropna().value_counts().head(10).sort_values()
    print("\n5) Top 10 cidades:")
    print(contagem.sort_values(ascending=False).to_string())

    plt.figure(figsize=(10, 6))
    sns.barplot(x=contagem.values, y=contagem.index, color="#e76f51")
    plt.title("Top 10 cidades por quantidade de veículos elétricos")
    plt.xlabel("Quantidade de veículos")
    plt.ylabel("Cidade")
    salvar_grafico("05_top_10_cidades.png")


def analisar_cafv(dados):
    if COLUNA_CAFV not in dados.columns:
        return
    contagem = dados[COLUNA_CAFV].dropna().value_counts().sort_values()
    print("\n6) Elegibilidade CAFV:")
    print(contagem.sort_values(ascending=False).to_string())

    plt.figure(figsize=(10, 5))
    sns.barplot(x=contagem.values, y=contagem.index, color="#457b9d")
    plt.title("Elegibilidade para Incentivos de Combustíveis Limpos (CAFV)")
    plt.xlabel("Quantidade de veículos")
    plt.ylabel("Status de Elegibilidade")
    salvar_grafico("06_elegibilidade_cafv.png")


def analisar_autonomia_por_tipo(dados):
    base = dados.dropna(subset=[COLUNA_TIPO, COLUNA_AUTONOMIA]).copy()
    base = base.loc[base[COLUNA_AUTONOMIA] > 0]
    media = base.groupby(COLUNA_TIPO)[COLUNA_AUTONOMIA].mean()
    print("\n7) Autonomia média por tipo:")
    print(media.round(1).to_string())

    plt.figure(figsize=(8, 5))
    sns.barplot(x=media.index, y=media.values, hue=media.index, palette="Blues_d", legend=False)
    plt.title("Autonomia Média por Tipo de Veículo (BEV vs PHEV)")
    plt.xlabel("Tipo de Veículo")
    plt.ylabel("Autonomia Média (milhas)")
    salvar_grafico("07_autonomia_por_tipo.png")


def analisar_top_marcas_autonomia(dados):
    base = dados.dropna(subset=[COLUNA_MARCA, COLUNA_AUTONOMIA]).copy()
    base = base.loc[base[COLUNA_AUTONOMIA] > 0]
    contagem_marcas = base[COLUNA_MARCA].value_counts()
    marcas_validas = contagem_marcas[contagem_marcas >= 10].index
    base_filtrada = base[base[COLUNA_MARCA].isin(marcas_validas)]
    
    media = base_filtrada.groupby(COLUNA_MARCA)[COLUNA_AUTONOMIA].mean().nlargest(10).sort_values()
    print("\n8) Top marcas por autonomia:")
    print(media.round(1).sort_values(ascending=False).to_string())

    plt.figure(figsize=(10, 5))
    sns.barplot(x=media.values, y=media.index, color="#2a9d8f")
    plt.title("Top 10 Marcas com Maior Autonomia Média")
    plt.xlabel("Autonomia Média (milhas)")
    plt.ylabel("Marca")
    salvar_grafico("08_top_marcas_autonomia.png")


def analisar_condados(dados):
    if COLUNA_CONDADO not in dados.columns:
        return
    contagem = dados[COLUNA_CONDADO].dropna().value_counts().head(5).sort_values()
    print("\n9) Top 5 condados:")
    print(contagem.sort_values(ascending=False).to_string())

    plt.figure(figsize=(9, 5))
    sns.barplot(x=contagem.values, y=contagem.index, color="#f4a261")
    plt.title("Top 5 Condados com Maior Concentração de Veículos")
    plt.xlabel("Quantidade de veículos")
    plt.ylabel("Condado")
    salvar_grafico("09_top_5_condados.png")


def analisar_pico_recente(dados):
    base = dados.dropna(subset=[COLUNA_ANO]).copy()
    if base.empty:
        return

    base[COLUNA_ANO] = base[COLUNA_ANO].astype(int)
    ano_final = int(base[COLUNA_ANO].max())
    ano_inicial = ano_final - 4
    contagem = base.loc[base[COLUNA_ANO].between(ano_inicial, ano_final), COLUNA_ANO].value_counts().sort_index()
    print(f"\n10) Pico de fabricação ({ano_inicial}–{ano_final}):")
    print(contagem.to_string())

    plt.figure(figsize=(8, 5))
    sns.barplot(x=contagem.index.astype(str), y=contagem.values, color="#e76f51")
    plt.title("Volume de Veículos por Ano de Fabricação (Últimos 5 Anos)")
    plt.xlabel("Ano do Modelo")
    plt.ylabel("Quantidade de Veículos")
    salvar_grafico("10_pico_fabricacao_recente.png")


def main():
    sns.set_theme(style="whitegrid")
    dados = carregar_dados()
    print(f"Base carregada: {len(dados):,} registros e {len(dados.columns)} colunas.")

    analisar_marcas(dados)
    analisar_tipos(dados)
    analisar_anos_modelo(dados)
    analisar_autonomia(dados)
    analisar_cidades(dados)
    analisar_cafv(dados)
    analisar_autonomia_por_tipo(dados)
    analisar_top_marcas_autonomia(dados)
    analisar_condados(dados)
    analisar_pico_recente(dados)

    print(f"\nProcesso concluído. Gráficos salvos em: {PASTA_GRAFICOS.relative_to(PASTA_PROJETO)}")


if __name__ == "__main__":
    main()