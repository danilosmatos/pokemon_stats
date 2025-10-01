from scrapper_jogo import scrape_pokemon_list as game
from scrapper_pokemon import web_scrapping as pokemon


def main():
    print("Bem - Vindo!!")
    print("\nO que deseja consultar: ")
    print("\nDeseja consultar a pokedex de jogos inteiros ou de pokémons individuais? ")
    print("\nPokedex de jogos completos (1)\nPokémons individuais(2)")
    while True:
        choice = int(input("Digite a sua escolha 1 ou 2 ( Ou 0 para sair do programa): "))
        if choice == 0:
            print("Saindo do programa.")
            break
        elif choice == 1:
            name_game = str(input("Insira o nome do jogo: "))
            rt = game(name_game)
            print(rt)
        elif choice == 2:
            poke_name = str(input("Digite o nome do Pokémon (ou 0 para sair): "))
            if poke_name == "0":
                print("Saindo do programa.")
                break
            if not poke_name:
                print("Por favor, digite um nome válido.")
                continue
            rt = pokemon(poke_name)
            print(f"Dados disponiveis do {poke_name}:\n{rt}")
        else: 
            print("Opção inválida")

if __name__ == "__main__":
    main()

