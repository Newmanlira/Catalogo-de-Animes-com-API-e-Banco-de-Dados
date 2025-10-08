# Catálogo de Animes - Projeto de Engenharia de Dados

Este projeto é um pipeline completo de engenharia de dados que extrai informações de milhares de animes da API da AniList, processa esses dados e os armazena em um banco de dados SQLite local para futuras análises.

---

🚀 Funcionalidades

*   Extração (ETL - Extract): Conecta-se à API GraphQL da AniList e coleta dados de mais de 20.000 animes, lidando com paginação e limites de requisição.
*   Carregamento (ETL - Load): Cria um banco de dados SQLite estruturado e insere todos os dados coletados de forma eficiente.
*   Análise: Executa consultas SQL no banco de dados para extrair insights, como os animes mais bem avaliados e a quantidade de lançamentos por ano.

---

🛠️ Tecnologias Utilizadas

*   Linguagem: Python 3
*   Bibliotecas Principais: `requests` (para chamadas de API), `pandas` (para análise e exibição de dados), `sqlite3` (para o banco de dados).
*   API: [AniList GraphQL API](https://anilist.gitbook.io/anilist-apiv2-docs )
*   Banco de Dados: SQLite

---

📋 Como Executar o Projeto

1.  Clone o repositório:
    ```bash
    git clone https://github.com/Newmanlira/Cat-logo-de-Animes-com-API-e-Banco-de-Dados.git
    cd Cat-logo-de-Animes-com-API-e-Banco-de-Dados
    ```

2.  Instale as dependências:
    ```bash
    pip install requests pandas
    ```

3.  Execute o Pipeline:
    *   Passo 1: Extrair os dados da API (cria o `animes_data.json` )
      ```bash
      python src/main.py
      ```
    *   Passo 2: Carregar os dados no banco (cria o `animes_catalog.db`)
      ```bash
      python src/load_to_db.py
      ```

4.  Execute a Análise (Opcional):
    ```bash
    python src/analyze_data.py
    ```

---

📊 Exemplo de Análise

Abaixo estão alguns dos insights gerados pelo script `analyze_data.py`:

--- Iniciando Análise do Catálogo de Animes ---

[1] Top 10 Animes com Melhor Nota Média (com mais de 10000 votos/popularidade implícita)
                            title_english  average_score  season_year
            Frieren: Beyond Journey’s End           91.0         2023
                         Gintama Season 4           91.0         2015
                  Gintama: THE VERY FINAL           91.0         2021
         Fullmetal Alchemist: Brotherhood           90.0         2009
                     ONE PIECE FAN LETTER           90.0         2024
                   Hunter x Hunter (2011)           89.0         2011
          Attack on Titan Season 3 Part 2           89.0         2019
                              Steins;Gate           89.0         2011
Kaguya-sama: Love is War -Ultra Romantic-           89.0         2022
           Fruits Basket The Final Season           89.0         2021

[2] Contagem de Animes Lançados por Ano (Top 10 anos com mais lançamentos)
 season_year  total_animes
        2016           578
        2014           551
        2017           550
        2018           518
        2015           507
        2021           502
        2023           489
        2012           483
        2013           478
        2022           465

[3] Formatos de Anime Mais Comuns
  format  total
      TV   4803
   MOVIE   3965
     OVA   3779
     ONA   3227
   MUSIC   2661
 SPECIAL   1799
TV_SHORT   1305

--- Análise Concluída ---
