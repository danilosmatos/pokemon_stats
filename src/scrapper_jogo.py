import requests as rq
from bs4 import BeautifulSoup as bs
import pandas as pd
import os 

DIR = "src/pokemon/jogo"
BASE_URL = "https://pokemondb.net/pokedex/"

GAME_NAMES = {
    "National Dex (Gen 9)": "national-dex", 
    "Scarlet & Violet (Paldea)": "scarlet-violet",
    "Legends: Arceus (Hisui)": "legends-arceus",
    "Brilliant Diamond & Shining Pearl (Sinnoh)": "brilliant-diamond-shining-pearl",
    "Sword & Shield (Galar)": "sword-shield",
    "Let's Go Pikachu & Eevee (Kanto)": "lets-go-pikachu-eevee",
    "Ultra Sun & Ultra Moon (Alola)": "ultra-sun-ultra-moon",
    "Sun & Moon (Alola)": "sun-moon",
    "Omega Ruby & Alpha Sapphire (Hoenn)": "omega-ruby-alpha-sapphire",
    "X & Y (Kalos)": "x-y",
    "Black 2 & White 2 (Unova)": "black-2-white-2",
    "Black & White (Unova)": "black-white",
    "HeartGold & SoulSilver (Johto)": "heartgold-soulsilver",
    "Platinum (Sinnoh)": "platinum",
    "Diamond & Pearl (Sinnoh)": "diamond-pearl",
    "FireRed & LeafGreen (Kanto)": "firered-leafgreen",
    "Ruby, Sapphire & Emerald (Hoenn)": "ruby-sapphire-emerald",
    "Gold, Silver & Crystal (Johto)": "gold-silver-crystal",
    "Red, Blue & Yellow (Kanto)": "red-blue-yellow",
}

# PEga o link do jogo e lista todos os pokemons que tem nele
def scrape_pokemon_list(game_name):    
    if game_name == "national-dex":
        url = BASE_URL + "all"
        print("Acessando National Dex Completa...")
    else:
        url = BASE_URL + "game/" + game_name
        print(f"Acessando Pokedex de Jogo: {url}")
        
    pokemon_names = []
    
    response = rq.get(url, timeout=15)
    response.raise_for_status()
    soup = bs(response.content, 'html.parser')
    
    infocards = soup.find_all('div', class_='infocard')
    
    if infocards:
        for card in infocards:
            a_tag = card.find('a', class_='ent-name')
            if a_tag:
                pokemon_names.append(a_tag.text.strip())
        return pokemon_names
    
    full_table = soup.find('table', {'id': 'pokedex'})
    if full_table:
        for row in full_table.find('tbody').find_all('tr'):
            name_cell = row.find('td', class_='cell-name')
            if name_cell:
                a_tag = name_cell.find('a', class_='ent-name')
                if a_tag:
                    pokemon_names.append(a_tag.text.strip())
        return pokemon_names
    
    return None

def get_pokemon_stats(poke_name):
    og_name = poke_name
    name_poke_url = poke_name.strip().lower().replace(' ', '-').replace('.', '').replace("'", "")
    url = f"https://pokemondb.net/pokedex/{name_poke_url}"
    
    try:
        response = rq.get(url, timeout=10)
        response.raise_for_status()
    except rq.exceptions.RequestException:
        print(f"Pulando '{og_name}': Não foi possível acessar a URL ou o Pokémon não existe.")
        return None
    
    soup = bs(response.content,'html.parser')
    h2_tag = soup.find('h2', string='Base stats')
    stats_table = h2_tag.find_next('table') if h2_tag else soup.find('table', class_='vitals-table')

    if not stats_table:
        print(f"Pulando '{og_name}': Tabela de stats não encontrada.")
        return None

    poke_stats_data = {'Name': og_name} 
    
    for row in stats_table.find_all('tr'): 
        cell_name_tag = row.find('th')
        cell_data = row.find_all('td')
        
        if cell_name_tag and len(cell_data) >= 1:
            stat_name = cell_name_tag.text.strip().replace('.', '').replace(' ', '')
            stat_value = cell_data[0].text.strip()
            
            if stat_value.isdigit():
                poke_stats_data[stat_name] = int(stat_value)
    
    if len(poke_stats_data) <= 6: 
        return None
        
    return poke_stats_data

def scrape_all_stats(game_name, game_slug):
    output_filename = f"pokemon_stats_{game_slug}.csv"
    output_path = os.path.join(DIR, output_filename)    
    # Verifica se o csv já existe
    if os.path.exists(output_path):
        print("\n=======================================================")
        print(f"O arquivo para '{game_name}' já existe!")
        overwrite = input("Deseja sobrescrever o arquivo existente? (s/n): ").strip().lower()
        if overwrite != 's':
            print("Operação cancelada. Saindo.")
            return

    pokemon_list = scrape_pokemon_list(game_slug)

    print(f"\nLista de {len(pokemon_list)} Pokemons de '{game_name}'...")
    all_stats_data = []
    
    for i, name in enumerate(pokemon_list):
        print(f"  [{i+1}/{len(pokemon_list)}] Raspando stats para: {name}")
        stats = get_pokemon_stats(name)
        
        if stats:
            all_stats_data.append(stats)
        
    df_final = pd.DataFrame(all_stats_data)
    col_order = ['Name', 'HP', 'Attack', 'Defense', 'SpAtk', 'SpDef', 'Speed', 'Total']
    df_final = df_final.reindex(columns=col_order)

    df_final.to_csv(output_path, index=False, encoding='utf-8')
    
    print("\n"+"="*40)
    print(f"Dados de {len(all_stats_data)} Pokémon de '{game_name}' salvos em:")
    print(f"  -> {output_path}")
    print("="*40)

def main():
    print("\n"+"="*40)
    print("--- SCRAPER DE STATS POKÉMON POR JOGO ---")
    print("="*40)
    
    game_names = list(GAME_NAMES.keys())
    print("\nEscolha qual Pokedex você gostaria de raspar:")
    
    for i, name in enumerate(game_names):
        print(f"  {i+1:02d}. {name}")
    
    while True:
        try:
            choice = input("\nDigite o número do jogo (ou 0 para sair): ").strip()
            
            if choice == "0":
                print("Saindo do programa.")
                return

            choice_index = int(choice) - 1
            
            if 0 <= choice_index < len(game_names):
                selected_game_name = game_names[choice_index]
                selected_game_slug = GAME_NAMES[selected_game_name]
                break
            else:
                print("Escolha inválida. Por favor, digite um número da lista.")
                
        except ValueError:
            print("Entrada inválida. Por favor, digite um número.")
        except Exception as e:
            print(f"Ocorreu um erro inesperado: {e}")
            return

    scrape_all_stats(selected_game_name, selected_game_slug)

if __name__ == '__main__':
    main()