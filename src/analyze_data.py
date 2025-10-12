# -*- coding: utf-8 -*-
"""
Módulo de Análise de Dados do Catálogo de Animes.

Este script conecta-se ao banco de dados SQLite, executa uma série de
consultas SQL para extrair insights e exibe os resultados no console
utilizando a biblioteca Pandas.

Autor: Newman Lira
Data: 12 de Outubro de 2025
"""

import sqlite3
import pandas as pd
import os

# --- Constantes e Configuração ---

# Caminho para o arquivo do banco de dados SQLite.
DB_PATH = 'animes_catalog.db'

# Configuração do Pandas para exibir nomes completos nas saídas.
pd.set_option('display.max_colwidth', None)

# --- Funções ---

def execute_query(conn, query):
    """
    Executa uma consulta SQL e retorna o resultado como um DataFrame do Pandas.

    Args:
        conn (sqlite3.Connection): Objeto de conexão com o banco de dados.
        query (str): A consulta SQL a ser executada.

    Returns:
        pd.DataFrame: Um DataFrame contendo os resultados da consulta.
                      Retorna um DataFrame vazio em caso de erro.
    """
    try:
        return pd.read_sql_query(query, conn)
    except sqlite3.Error as e:
        print(f"Erro ao executar a query: {e}")
        return pd.DataFrame()

def run_analysis_suite(db_path):
    """
    Conecta-se ao banco de dados e executa um conjunto de análises predefinidas.

    Args:
        db_path (str): O caminho para o arquivo do banco de dados.
    """
    if not os.path.exists(db_path):
        print(f"Erro: O arquivo de banco de dados '{db_path}' não foi encontrado.")
        print("Por favor, execute o script 'load_to_db.py' primeiro.")
        return

    print("--- Iniciando Análise do Catálogo de Animes ---")

    try:
        # Conecta-se ao banco de dados em modo somente leitura para segurança.
        with sqlite3.connect(f'file:{db_path}?mode=ro', uri=True) as conn:
            print(f"Conexão com o banco de dados '{db_path}' estabelecida.\n")

            # Análise 1: Top 10 Animes por Nota Média
            print("[1] Top 10 Animes com Melhor Nota Média")
            query_top_10 = """
                SELECT title_english, average_score, season_year
                FROM animes
                WHERE average_score IS NOT NULL
                ORDER BY average_score DESC, title_english ASC
                LIMIT 10;
            """
            df_top_10 = execute_query(conn, query_top_10)
            print(df_top_10.to_string(index=False))

            # Análise 2: Contagem de Animes por Ano
            print("\n[2] Contagem de Animes Lançados por Ano (Top 10)")
            query_animes_por_ano = """
                SELECT season_year, COUNT(id) as total_animes
                FROM animes
                WHERE season_year IS NOT NULL
                GROUP BY season_year
                ORDER BY total_animes DESC
                LIMIT 10;
            """
            df_animes_por_ano = execute_query(conn, query_animes_por_ano)
            print(df_animes_por_ano.to_string(index=False))

            # Análise 3: Formatos de Anime Mais Comuns
            print("\n[3] Formatos de Anime Mais Comuns")
            query_formatos = """
                SELECT format, COUNT(id) as total
                FROM animes
                WHERE format IS NOT NULL
                GROUP BY format
                ORDER BY total DESC;
            """
            df_formatos = execute_query(conn, query_formatos)
            print(df_formatos.to_string(index=False))

    except sqlite3.Error as e:
        print(f"\nOcorreu um erro crítico de banco de dados: {e}")

    finally:
        print("\n--- Análise Concluída ---")

# --- Execução Principal ---

def main():
    """Função principal que inicia o processo de análise."""
    run_analysis_suite(DB_PATH)

if __name__ == "__main__":
    main()
