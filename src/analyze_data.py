# src/analyze_data.py

import sqlite3
import pandas as pd

# --- Configuração ---
DB_PATH = 'animes_catalog.db'

# --- Função para executar uma query e retornar um DataFrame do Pandas ---
def query_to_dataframe(query: str, db_path: str) -> pd.DataFrame:
    """Executa uma consulta SQL no banco de dados e retorna o resultado como um DataFrame do Pandas."""
    try:
        # Conecta ao banco de dados em modo de leitura
        conn = sqlite3.connect(f'file:{db_path}?mode=ro', uri=True)
        
        # Usa o pandas para ler o resultado da query diretamente em um DataFrame
        df = pd.read_sql_query(query, conn)
        
        # Fecha a conexão
        conn.close()
        
        return df
        
    except Exception as e:
        print(f"Ocorreu um erro ao executar a query: {e}")
        return pd.DataFrame() # Retorna um DataFrame vazio em caso de erro

# --- Início da Análise ---
if __name__ == "__main__":
    print("--- Iniciando Análise do Catálogo de Animes ---")

    # --- Análise 1: Top 10 Animes com Melhor Nota Média ---
    print("\n[1] Top 10 Animes com Melhor Nota Média (com mais de 10000 votos/popularidade implícita)")
    query_top_10 = """
        SELECT 
            title_english, 
            average_score,
            season_year
        FROM animes
        WHERE average_score IS NOT NULL
        ORDER BY average_score DESC
        LIMIT 10;
    """
    df_top_10 = query_to_dataframe(query_top_10, DB_PATH)
    # Configura o pandas para não cortar o nome dos animes
    pd.set_option('display.max_colwidth', None)
    print(df_top_10.to_string(index=False))

    # --- Análise 2: Contagem de Animes por Ano ---
    print("\n[2] Contagem de Animes Lançados por Ano (Top 10 anos com mais lançamentos)")
    query_animes_por_ano = """
        SELECT 
            season_year, 
            COUNT(id) as total_animes
        FROM animes
        WHERE season_year IS NOT NULL
        GROUP BY season_year
        ORDER BY total_animes DESC
        LIMIT 10;
    """
    df_animes_por_ano = query_to_dataframe(query_animes_por_ano, DB_PATH)
    print(df_animes_por_ano.to_string(index=False))

    # --- Análise 3: Formatos de Anime Mais Comuns ---
    print("\n[3] Formatos de Anime Mais Comuns")
    query_formatos = """
        SELECT 
            format, 
            COUNT(id) as total
        FROM animes
        WHERE format IS NOT NULL
        GROUP BY format
        ORDER BY total DESC;
    """
    df_formatos = query_to_dataframe(query_formatos, DB_PATH)
    print(df_formatos.to_string(index=False))

    print("\n--- Análise Concluída ---")

