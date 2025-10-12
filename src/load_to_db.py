# -*- coding: utf-8 -*-
"""
Módulo de Carregamento de Dados para o Banco de Dados SQLite.

Este script lê os dados de animes extraídos do arquivo JSON e os carrega
em uma tabela em um banco de dados SQLite. Ele cria o banco e a tabela
se não existirem e lida com a inserção de dados, evitando duplicatas.

Autor: Newman Lira
Data: 12 de Outubro de 2025
"""

import sqlite3
import json
import os

# --- Constantes e Configuração ---

# Caminho para o arquivo JSON gerado pelo script de extração.
JSON_FILE_PATH = 'animes_data.json'

# Caminho para o arquivo do banco de dados SQLite.
DB_PATH = 'animes_catalog.db'

# --- Funções ---

def load_json_data(filepath):
    """
    Carrega os dados de um arquivo JSON.

    Args:
        filepath (str): O caminho para o arquivo JSON.

    Returns:
        list: Uma lista de dicionários contendo os dados.
              Retorna None se o arquivo não for encontrado ou ocorrer um erro.
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Erro: O arquivo de dados '{filepath}' não foi encontrado.")
        return None
    except json.JSONDecodeError:
        print(f"Erro: O arquivo '{filepath}' não é um JSON válido.")
        return None

def create_database_and_table(conn):
    """
    Cria a tabela 'animes' no banco de dados se ela não existir.

    A tabela é projetada com uma restrição UNIQUE em 'id_anilist' para
    prevenir a inserção de registros duplicados.

    Args:
        conn (sqlite3.Connection): Objeto de conexão com o banco de dados.
    """
    try:
        cursor = conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS animes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_anilist INTEGER UNIQUE,
            title_romaji TEXT,
            title_english TEXT,
            format TEXT,
            status TEXT,
            season_year INTEGER,
            episodes INTEGER,
            average_score REAL
        )
        ''')
        print("Tabela 'animes' verificada/criada com sucesso.")
    except sqlite3.Error as e:
        print(f"Erro ao criar a tabela: {e}")
        raise

def insert_data_into_db(conn, animes_data):
    """
    Insere uma lista de animes no banco de dados.

    Utiliza um bloco try-except para ignorar animes que já existem no banco,
    baseando-se na restrição UNIQUE da coluna 'id_anilist'.

    Args:
        conn (sqlite3.Connection): Objeto de conexão com o banco de dados.
        animes_data (list): Lista de dicionários de animes.

    Returns:
        tuple: Uma tupla contendo o número de animes inseridos e ignorados.
    """
    cursor = conn.cursor()
    animes_inseridos = 0
    animes_ignorados = 0

    for anime in animes_data:
        try:
            # Extrai os dados do dicionário, usando .get() para segurança.
            data_tuple = (
                anime.get('id'),
                anime.get('title', {}).get('romaji'),
                anime.get('title', {}).get('english'),
                anime.get('format'),
                anime.get('status'),
                anime.get('seasonYear'),
                anime.get('episodes'),
                anime.get('averageScore')
            )
            
            cursor.execute('''
                INSERT INTO animes (
                    id_anilist, title_romaji, title_english, format, status, 
                    season_year, episodes, average_score
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', data_tuple)
            animes_inseridos += 1
        except sqlite3.IntegrityError:
            # Ocorre se 'id_anilist' já existir.
            animes_ignorados += 1
        except sqlite3.Error as e:
            print(f"Erro de banco de dados ao inserir o anime ID {anime.get('id')}: {e}")

    return animes_inseridos, animes_ignorados

# --- Execução Principal ---

def main():
    """Função principal que orquestra o carregamento dos dados para o banco."""
    print("--- Iniciando Pipeline de Carregamento para o Banco de Dados ---")

    animes_data = load_json_data(JSON_FILE_PATH)
    if animes_data is None:
        print("Processo interrompido devido à falha na leitura dos dados.")
        return

    print(f"{len(animes_data)} registros de animes carregados do arquivo JSON.")

    try:
        # O uso de 'with' garante que a conexão será fechada automaticamente,
        # mesmo que ocorram erros. O commit é feito automaticamente se o bloco
        # for concluído com sucesso.
        with sqlite3.connect(DB_PATH) as conn:
            print(f"Conexão com o banco de dados '{DB_PATH}' estabelecida.")
            create_database_and_table(conn)
            
            print("Iniciando a inserção dos dados...")
            inseridos, ignorados = insert_data_into_db(conn, animes_data)

        print("\n----------------------------------------------------")
        print("Processo de carga finalizado!")
        print(f"Animes inseridos com sucesso: {inseridos}")
        print(f"Animes ignorados (duplicados): {ignorados}")
        print(f"Banco de dados '{DB_PATH}' foi criado/atualizado.")
        print("----------------------------------------------------")

    except sqlite3.Error as e:
        print(f"\nOcorreu um erro crítico de banco de dados: {e}")
        print("O processo foi interrompido.")

if __name__ == "__main__":
    main()
