# ⚡ Análise de Dados: População de Veículos Elétricos (EV)

Repositório desenvolvido para o Projeto 1 da disciplina de C11 do Inatel. O objetivo deste projeto é aplicar o ciclo completo de Ciência de Dados utilizando Python, desde a limpeza de dados até a visualização de insights valiosos para o setor de mobilidade sustentável.

## 👥 Integrantes do Grupo
- Gabriel Machado Pivoto
- Otavio Augusto Silva Lima
- Hugo Henrique Reis Camilo

---

## 🎯 1. Objetivo do Projeto
Analisar o dataset de Veículos Elétricos (*EV Population Data*) para extrair tendências de mercado, evolução tecnológica das baterias, preferências de marcas e distribuição geográfica, respondendo a **10 perguntas estratégicas** de impacto socioambiental e tecnológico.

---

## 🛠️ 2. Tecnologias Utilizadas
O projeto foi desenvolvido em Python utilizando as seguintes bibliotecas:
- **Pandas e NumPy:** Para manipulação, limpeza e tratamento dos dados.
- **Matplotlib e Seaborn:** Para a construção de gráficos e análise exploratória visual.

---

## 📁 3. Estrutura do Repositório
```text
projeto-ciencia-de-dados-INATEL/
│
├── data/
│   └── Electric_Vehicle_Population_Data.csv  # Base de dados original
├── output/
│   └── graficos/                             # Gráficos gerados automaticamente (01 a 10)
├── src/
│   └── main.py                               # Script principal com as 10 análises
├── .gitignore
└── README.md

## 🚀 4. Como Executar o Projeto
Clone este repositório na sua máquina:
```bash
git clone [https://github.com/GPivoto/projeto-ciencia-de-dados-INATEL.git](https://github.com/GPivoto/projeto-ciencia-de-dados-INATEL.git)

Certifique-se de ter as bibliotecas necessárias instaladas (pandas, matplotlib, seaborn):
```bash
pip install pandas matplotlib seaborn

Execute o script principal na raiz do projeto para processar os dados e gerar os gráficos:
```bash
python src/main.py