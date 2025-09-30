# 📑 5W1H

---

## 1. What (O que é?)

Um projeto em Python para coletar automaticamente stats de Pokemon do site [PokemonDB](https://pokemondb.net). O projeto utiliza Requests e BeautifulSoup para web scraping e Pandas para o tratamento e exportação dos dados para arquivos CSV.

O projeto possui dois modos de uso:

* Modo Individual: Busca e salva os stats de um Pokemon individualmente em um arquivo CSV.

* Modo Pokedex de Jogos: Permite selecionar a pokedex de um jogo (ou a pokedex completa) e fazer o web scrapping dos stats de todos os Pokémon daquela lista, os organizando em um único arquivo CSV.

## 2. Why (Por que?)

O objetivo é praticar a automação de coleta de dados, a manipulação de dados com Pandas e a organização em um formato de fácil consulta.

## 3. Who (Quem participa?)

* Desenvolvedores (Iniciantes/Intermediários): Que desejam aprender sobre scraping e coleta de dados em lote.
* Fãs de Pokémon/Analistas de Dados: Usuários que precisam dos dados de stats para uso próprio ou projetos.

## 4. Where (Onde será usado?)

* O script pode ser executado em qualquer ambiente que suporte Python 3 e suas dependências (Windows, Linux, macOS).
* Os resultados são salvos em arquivos CSV em `src/pokemon/individual` para operações individuais e `src/pokemon/jogo` para operações da pokedex de jogos completa, prontos para serem usados em qualquer software de análise de dados.

## 5. When (Quando usar?)

Sempre que necessário para obter os stats de um pokemon especifico no caso do uso individual, caso contrário obter datasets pelo uso do de jogos completos

## 6. How (Como funciona?)

1.  O usuário clona o repositório.

2.  Instala as dependências (`pip install -r requirements.txt`).

3.  Escolha entre scrapper_jogo.py e scrapper_pokemon.py, decidindo o jogo/pokemon desejado

4.  O programa então, por meio da biblioteca Request solicita os dados brutos da página
    que BeautifulSoup analisa e converte os dados para um formato entendivel para python.

5.  Assim é convertido para um dataframe do Pandas e o resultado final é convertido novamente
    para um arquivo CSV.

Integrantes:
[Antônio Gabriel](https://github.com/Anton-Gabriel-code) | [Danilo Soares de Matos](https://github.com/danilosmatos) | [Eudes de Oliveira Rocha](https://github.com/eudesolv)

Professor:
[Marcos Vinícius](https://github.com/marcmec)

