# src/load_to_db.py

import sqlite3
import json

# --- Configurações ---
JSON_FILE_PATH = 'animes_data.json'  # O arquivo que geramos na etapa anterior
DB_PATH = 'animes_catalog.db'      # O nome do arquivo do nosso banco de dados SQLite

# --- 1. Conectar ao Banco de Dados ---
# O comando connect() cria o arquivo do banco de dados se ele não existir.
print(f"Conectando ao banco de dados em '{DB_PATH}'...")
conn = sqlite3.connect(DB_PATH)
# Criamos um 'cursor', que é o objeto que executa os comandos SQL.
cursor = conn.cursor()

# --- 2. Modelar e Criar a Tabela ---
# Usamos "IF NOT EXISTS" para que o script não dê erro se a tabela já existir.
# Definimos as colunas e seus tipos:
# - INTEGER PRIMARY KEY AUTOINCREMENT: Um ID numérico único para cada anime.
# - TEXT: Para armazenar textos (títulos, formato, status).
# - INTEGER: Para números inteiros (ano, episódios).
# - REAL: Para números com casas decimais (nota).
# - UNIQUE(id_anilist): Garante que não vamos inserir o mesmo anime duas vezes.
print("Criando a tabela 'animes' (se não existir)...")
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
print("Tabela 'animes' pronta.")

# --- 3. Ler os Dados do Arquivo JSON ---
print(f"Lendo os dados do arquivo '{JSON_FILE_PATH}'...")
with open(JSON_FILE_PATH, 'r', encoding='utf-8') as f:
    animes_data = json.load(f)
print(f"{len(animes_data)} animes carregados do JSON.")

# --- 4. Inserir os Dados na Tabela ---
print("Iniciando a inserção dos dados no banco...")
animes_inseridos = 0
animes_ignorados = 0

for anime in animes_data:
    # O bloco try-except lida com possíveis duplicatas.
    # Se tentarmos inserir um 'id_anilist' que já existe, o UNIQUE vai gerar um erro.
    # Nós capturamos esse erro e simplesmente ignoramos a inserção.
    try:
        # Preparamos os dados para inserção, tratando campos que podem ser nulos (None)
        cursor.execute('''
            INSERT INTO animes (
                id_anilist, title_romaji, title_english, format, status, 
                season_year, episodes, average_score
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            anime.get('id'),
            anime['title'].get('romaji'),
            anime['title'].get('english'),
            anime.get('format'),
            anime.get('status'),
            anime.get('seasonYear'),
            anime.get('episodes'),
            anime.get('averageScore')
        ))
        animes_inseridos += 1
    except sqlite3.IntegrityError:
        # Este erro acontece se o 'id_anilist' já existir no banco.
        animes_ignorados += 1
    except Exception as e:
        print(f"Ocorreu um erro inesperado ao inserir o anime ID {anime.get('id')}: {e}")

# --- 5. Finalizar a Transação ---
# conn.commit() salva todas as alterações que fizemos no banco de dados.
conn.commit()
# conn.close() fecha a conexão com o banco.
conn.close()

print("\n----------------------------------------------------")
print("Processo de carga finalizado!")
print(f"Animes inseridos com sucesso: {animes_inseridos}")
print(f"Animes ignorados (duplicados): {animes_ignorados}")
print(f"Banco de dados '{DB_PATH}' foi criado/atualizado.")
print("----------------------------------------------------")
