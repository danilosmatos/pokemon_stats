import requests as rq
from bs4 import BeautifulSoup as bs
import pandas as pd
import os 

DIR = "src/pokemon/individual" 

def web_scrapping(name_poke):
    og_name = name_poke
    name_poke_url = name_poke.strip().lower().replace(' ', '-').replace('.', '').replace("'", "")
    csv_filename = f"{name_poke_url}.csv"
    
    url = f"https://pokemondb.net/pokedex/{name_poke_url}"
    
    try:
        response = rq.get(url, timeout=10)
        response.raise_for_status()
    except rq.exceptions.HTTPError as e:
        status_code = response.status_code if 'response' in locals() and response is not None else 'N/A'
        print(f"Erro: O Pokémon '{og_name}' não foi encontrado (Código: {status_code}).")
        return None
    except rq.exceptions.RequestException as e:
        print(f"Erro de conexão: Não foi possível acessar a URL. Verifique sua internet.")
        return None
    
    #traduz o request para algo que o programa possa ler
    soup = bs(response.content,'html.parser')
    
    # Encontra aonde a tabela onde estão os stats base do pokemon fica
    h2_tag = soup.find('h2', string='Base stats')
    
    if not h2_tag:
        print(f"Erro de raspagem: A seção 'Base stats' não foi encontrada para '{og_name}'.")
        return None

    # Encontra a tabela de fato pela localização que achou na linha anterior
    stats_table = h2_tag.find_next('table')

    poke_stats_data = {} 
    
    for row in stats_table.find_all('tr'): 
        
        # A celula th é onde ta o nome do stat no html
        cell_name_tag = row.find('th')
        
        # Celula do dado em si, incluindo o mais importante que é o valor númerico
        cell_data = row.find_all('td')
        
        # Verifica se encontrou o nome do stat e pelo menos uma célula de dado 
        if cell_name_tag and len(cell_data) >= 1:
            stat_name = cell_name_tag.text.strip()
            
            # Pega o valor do stat e converte para int
            stat_value = cell_data[0].text.strip()
            
            if stat_value.isdigit():
                poke_stats_data[stat_name] = int(stat_value)
    
    if not poke_stats_data:
        return None
            
    df = pd.DataFrame(
        list(poke_stats_data.items()), 
        columns=['Stat', 'Valor Base']
    )
    
    output_path = os.path.join(DIR, csv_filename)
    df.to_csv(output_path, index=False)
    
    print(f" Dados salvos com sucesso em: {output_path}")
    return poke_stats_data 


def main():
    print("\n--- SCRAPER DE STATUS POKEMON ---")

    while True:
        try:
            name_input = input("Digite o nome do Pokémon ou 0 para sair: ").strip()
            
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
    main()