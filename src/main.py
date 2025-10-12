# -*- coding: utf-8 -*-
"""
Módulo de Extração de Dados da API AniList.

Este script conecta-se à API GraphQL da AniList para extrair uma lista
completa de animes, tratando a paginação e os limites de requisição.
Os dados extraídos são salvos em um arquivo JSON para processamento posterior.

Autor: Newman Lira
Data: 12 de Outubro de 2025
"""

import requests
import json
import time
import os

# --- Constantes e Configuração ---

# URL do endpoint da API GraphQL da AniList.
API_URL = 'https://graphql.anilist.co'

# Número de itens por página. O máximo permitido pela API é 50.
ITEMS_PER_PAGE = 50

# Nome do arquivo de saída para os dados extraídos.
OUTPUT_FILENAME = 'animes_data.json'

# Query GraphQL para buscar dados de animes.
# Seleciona campos essenciais e ordena por popularidade decrescente.
GRAPHQL_QUERY = '''
query ($page: Int, $perPage: Int ) {
  Page (page: $page, perPage: $perPage) {
    pageInfo {
      total
      currentPage
      lastPage
      hasNextPage
    }
    media (type: ANIME, sort: POPULARITY_DESC) {
      id
      title {
        romaji
        english
      }
      format
      status
      seasonYear
      episodes
      averageScore
    }
  }
}
'''

# --- Funções ---

def fetch_animes_from_api():
    """
    Executa o processo de extração de dados da API AniList.

    Itera através das páginas da API, coleta os dados dos animes e os
    armazena em uma lista. Inclui um delay para respeitar o rate limit da API.

    Returns:
        list: Uma lista de dicionários, onde cada dicionário representa um anime.
              Retorna uma lista vazia em caso de falha na primeira requisição.
    """
    page_num = 1
    has_next_page = True
    all_animes = []

    while has_next_page:
        variables = {'page': page_num, 'perPage': ITEMS_PER_PAGE}
        payload = {'query': GRAPHQL_QUERY, 'variables': variables}
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        }

        print(f"Buscando página {page_num}...")

        try:
            response = requests.post(API_URL, headers=headers, json=payload, timeout=30)
            response.raise_for_status()  # Lança um erro para status codes HTTP >= 400

            data = response.json()
            page_data = data.get('data', {}).get('Page', {})
            
            animes_on_page = page_data.get('media', [])
            if animes_on_page:
                all_animes.extend(animes_on_page)
                print(f"  -> {len(animes_on_page)} animes encontrados. Total acumulado: {len(all_animes)}")
            
            page_info = page_data.get('pageInfo', {})
            has_next_page = page_info.get('hasNextPage', False)
            
            page_num += 1

            # Pausa estratégica para respeitar o rate limit da API (90 reqs/min).
            time.sleep(0.7)

        except requests.exceptions.RequestException as e:
            print(f"Erro de rede ou HTTP na página {page_num}: {e}")
            break
        except json.JSONDecodeError:
            print(f"Erro ao decodificar a resposta JSON na página {page_num}.")
            break

    return all_animes

def save_data_to_json(data, filename):
    """
    Salva os dados coletados em um arquivo JSON.

    Args:
        data (list): A lista de dados a ser salva.
        filename (str): O nome do arquivo de saída.
    """
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print(f"\nTodos os dados foram salvos com sucesso em '{filename}'")
    except IOError as e:
        print(f"Erro ao salvar o arquivo '{filename}': {e}")

# --- Execução Principal ---

def main():
    """Função principal que orquestra a extração e salvamento dos dados."""
    print("--- Iniciando Pipeline de Extração de Dados de Animes ---")
    
    animes_data = fetch_animes_from_api()

    if animes_data:
        print("\n----------------------------------------------------")
        print("Coleta de dados finalizada!")
        print(f"Total de animes coletados: {len(animes_data)}")
        
        save_data_to_json(animes_data, OUTPUT_FILENAME)
        
        print("\nAmostra dos 5 primeiros animes coletados:")
        for anime in animes_data[:5]:
            titulo = anime.get('title', {}).get('english') or anime.get('title', {}).get('romaji', 'N/A')
            print(f"- {titulo}")
    else:
        print("\nNenhum dado foi coletado. O processo foi interrompido.")

    print("----------------------------------------------------")

if __name__ == "__main__":
    main()
