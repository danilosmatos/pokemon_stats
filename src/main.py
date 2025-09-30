import requests as rq
from bs4 import BeautifulSoup as bs
import pandas as pd

def web_scrapping(name_poke):
    og_name = name_poke
    name_poke = name_poke.strip()
    name_poke = name_poke.lower()
    name_poke = name_poke.replace(' ', '-')
    name_poke = name_poke.replace('.', '') 
    name_poke = name_poke.replace("'", "")
    url = f"https://pokemondb.net/pokedex/{name_poke}"
    try:
        response = rq.get(url, timeout=10) # Adiciona timeout para segurança
        response.raise_for_status() # Lança exceção para códigos de status 4xx/5xx (Página não encontrada)
    except rq.exceptions.HTTPError as e:
        print(f"Erro: O Pokémon '{og_name}' não foi encontrado (Código: {response.status_code}).")
        return None
    except rq.exceptions.RequestException as e:
        print(f"Erro de conexão: Não foi possível acessar a URL. Verifique sua internet.")
        return None
    
    soup = bs(response.content,'html.parser')
    
    # Encontra aonde a tabela onde estão os stats base do pokemon fica
    h2_tag = soup.find('h2', string='Base stats')
    # Encontra a tabela de fato pela localização que achou na linha anterior
    stats_table = h2_tag.find_next('table')

    poke_stats = {} 
    
    for row in stats_table.find_all('tr'): 
        
        # A celula th é onde ta o nome do stat no html
        cell_name = row.find('th')
        
        # Celula do dado em si, incluindo o mais importante que é o valor númerico
        cell_data = row.find_all('td')
        
        # Verifica se encontrou o nome do stat e pelo menos uma célula de dado 
        if cell_name and len(cell_data) >= 1:
            cell_name = cell_name.text.strip()
            
            # Pega o valor do stat e converte para int
            stat_value = cell_data[0].text.strip()
            poke_stats[cell_name] = int(stat_value)
    
    return poke_stats

# --- FUNÇÃO DE MENU E EXECUÇÃO ---

def menu_principal():
    print("\n--- POKÉMON STATS SCRAPER ---")
    while True:
        try:
            name_input = input("Digite o nome do Pokémon ou 0 para sair: ")
            
            if name_input == "0":
                quit()
            
            if not name_input:
                print("Por favor, digite um nome válido.")
                continue

            stats = web_scrapping(name_input)
            
            if stats:
                print(f"\nStats Base de {name_input.title()}:")
                for nome, valor in stats.items():
                    print(f"  > {nome: <10}: {valor}")
            else:
                pass
                
        except Exception as e:
            # Captura qualquer erro inesperado durante o input ou processamento
            print(f"\nOcorreu um erro: {e}")
            print("Tente novamente.")

if __name__ == '__main__':
    menu_principal()