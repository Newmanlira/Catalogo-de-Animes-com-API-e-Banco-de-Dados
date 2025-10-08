import requests
import json
import time # Essencial para não sobrecarregar a API

# --- Configurações ---
url = 'https://graphql.anilist.co'
# Vamos aumentar a quantidade de animes por página para o máximo permitido, que é 50.
# Isso torna nossa coleta de dados muito mais eficiente.
ITEMS_PER_PAGE = 50

# --- Query GraphQL (a mesma de antes ) ---
query = '''
query ($page: Int, $perPage: Int) {
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

# --- Lógica de Paginação Automática ---

# 1. Inicializamos as variáveis de controle do loop
page_num = 1
has_next_page = True
all_animes = [] # Lista para guardar TODOS os animes que coletarmos

while has_next_page:
    variables = {
        'page': page_num,
        'perPage': ITEMS_PER_PAGE
    }

    payload = {
        'query': query,
        'variables': variables
    }
    
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    }

    print(f"Buscando página {page_num}...")

    # 2. Fazemos a requisição
    response = requests.post(url, headers=headers, json=payload)

    # 3. Verificamos se a requisição foi bem-sucedida
    if response.status_code == 200:
        data = response.json()
        page_data = data.get('data', {}).get('Page', {})
        
        # 4. Adicionamos os animes da página atual à nossa lista principal
        animes_on_page = page_data.get('media', [])
        if animes_on_page:
            all_animes.extend(animes_on_page)
            print(f"  -> {len(animes_on_page)} animes encontrados. Total acumulado: {len(all_animes)}")
        
        # 5. Atualizamos a condição de parada do loop
        page_info = page_data.get('pageInfo', {})
        has_next_page = page_info.get('hasNextPage', False)
        
        # 6. Incrementamos o número da página para a próxima iteração
        page_num += 1

        # 7. PAUSA ESTRATÉGICA: Respeitar o limite da API (90 requisições/minuto)
        # Fazemos uma pequena pausa de 0.7 segundos para garantir que não excederemos o limite.
        time.sleep(0.7) 

    else:
        # Se uma requisição falhar, paramos o loop para não continuar com erros.
        print(f"Erro na página {page_num}. Status Code: {response.status_code}")
        print(response.text)
        break # Interrompe o loop em caso de erro

# --- Exibição do Resultado Final ---
print("\n----------------------------------------------------")
print(f"Coleta de dados finalizada!")
print(f"Total de animes coletados: {len(all_animes)}")
print("Amostra dos 5 primeiros animes coletados:")

# Imprime os 5 primeiros animes da lista para verificação
for anime in all_animes[:5]:
    titulo = anime['title']['english'] if anime['title']['english'] else anime['title']['romaji']
    print(f"- {titulo}")

# Opcional: Salvar os resultados em um arquivo JSON para não perdermos o progresso
with open('animes_data.json', 'w', encoding='utf-8') as f:
    json.dump(all_animes, f, ensure_ascii=False, indent=4)

print("\nTodos os dados foram salvos em 'animes_data.json'")
print("----------------------------------------------------")

