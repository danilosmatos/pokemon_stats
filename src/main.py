from scrapper_jogo import scrape_pokemon_list as game
from scrapper_pokemon import web_scrapping as pokemon


def main():
    print("="*60+"\n"+"Bem - Vindo!!")
    print("\nDeseja consultar a pokedex de jogos inteiros, de pokémons individuais ou sair? ")
    print("\n(1) Pokedex de jogos completos \n\n(2) Pokémons individuais")
    print("\n(0) Sair\n"+"="*60)
    while True:
        choice = int(input("\nDigite 1 ou 2 para escolher ou 0 para sair do programa): "))
        if choice == 0:
            print("\nSaindo do programa.\n")
            break
        elif choice == 1:
            name_game = str(input("\nInsira o nome do jogo: "))
            rt = game(name_game)
            print(rt)
        elif choice == 2:
            poke_name = str(input("\nDigite o nome do Pokémon (ou 0 para sair): "))
            if poke_name == "0":
                print("Saindo do programa.")
                break
            if not poke_name:
                print("\nPor favor, digite um nome válido.")
                continue
            rt = pokemon(poke_name)
            #print(f"\nDados disponiveis do {poke_name}:\n{rt}")
            print("\n Tabela de Estatísticas\n"+" "+"-"*22)
            for key, value in rt.items():
                print(f"|    {key:<{10}}|  {value:<{3}}  |")
            print(" "+"-"*22)
        else: 
            print("Opção inválida")

if __name__ == "__main__":
    main()

