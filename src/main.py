#Tentando de novo
import requests as rq
from bs4 import BeautifulSoup as bs
import pandas as pd

def main():
    user_poke= input()
    url = f"https://pokemondb.net/pokedex/{user_poke}"
    response = rq.get(url)
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
            
            # Pega o valor do stat
            stat_value = cell_data[0].text.strip()
            
            poke_stats[cell_name] = int(stat_value)
    
    print(f"Status Base do {user_poke}:")
    print(poke_stats)

if __name__ == '__main__':
    main()