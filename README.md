# Auto Anki Flashcards

## Sobre o projeto

O projeto consiste em automatizar a tarefa de criar flash cards na aplicação web do Anki. O processo de automatização visa desde a extração de textos base para o front side do flashcard, sejam estes em arquivos .txt ou imagens, até a inserção do flashcard no seu deck escolhido.

## Por que?

Esse projeto foi concebido da necessidade de automatizar uma tarefa frequente de criar flash cards para revisar novas palavras que aprendidas ao assistir seriados com legendas em inglês. Com isso, houve menos trabalho, tempo, tédio e imprecisão ao passar as frases das legendas para a maravilhosa aplicação de revisão espaçada do Anki.

## Funcionalidades

O projeto em si foi pensado para ser escalado a medida em que se aprendia as tecnologias que possibilitaram a alcançar o nível atual de funcionalidades. Atualmente são elas as escalas:

### Escala 1 [Descontinuada]:

- Gerar as traduções dos textos em arquivo .txt e tornar essas traduções o conteúdo do back side do flash card.

*Esta escala foi descontinuada pois é possível obter a tradução do conteúdo do front side utilizando um app como o Google Translate ou um app de dicionário em inglês.*

### Escala 2:

- Obter frases a partir de um arquivo .txt pré-configurado pelo usuário, em que cada frase é considerada pela quebra de linha;

- Organizar todas as frases obtidas em uma estrutura, e cada frase é atribuida a um objeto que modela um flash card;


- Executar um bot que acessa a conta no Anki, seleciona o deck configurado e adiciona os flash cards criados.

### Escala 3:

- Obter as frases a partir de imagens, neste caso utilizando o Google Vision para a extração de textos. Até esta escala é necessário que as imagens estejam armazenadas localmente;

- Realizar os mesmos processos da Escala 2 para organizar e inserir os flash cards.

### Escala 4:

- Possibilitar obter as imagens a partir do Google Drive;

- Realizar os mesmo processos da Escala 3 para obter, organizar e inserir os flash cards.

## Features

Algumas das ferramentas utilizadas:

* Selenium Web Driver

* Google Vision API

* Google Drive API

## Como executar esse projeto

### Pré-requisitos

#### Requisitos gerais:

- Python 3.8+

- Ter uma conta no AnkiWeb

- Ter um navegador web como o Firefox ou o Chrome

- Configurar o web driver dos navegadores acima

#### A partir da Escala 3:

- Uma conta no Google Cloud Plataform e uma chave para a utilizar o Google Vision API

#### A partir da Escala 4:

- Uma chave pra utilizar o Google Drive API

### Instalando

Após obter este repositório. No diretório do Projeto:

- Crie e ative o ambiente virtual do python 3;

- instale as dependencias do projeto:
`pip install -r requirements.txt`;

- execute o programa pela primeira vez: `python run.py`;

no arquivo **config.json** criado após a etapa acima, obrigatoriamente, insira:
- **deck[name]**: o nome do baralho a ser criado novos cartões;
- **application_file_name**: o nome da escala ou aplicação que deseja executar;
*O arquivo desta aplicação deverá estar contido na pasta **src/apps**, no diretório raíz deste projeto.*
- **web_driver_user_settings[browser]** o nome do navegador instalado na sua máquina para a finalidade;

#### Notas sobre o arquivo config.json: 
- O parâmetro **auto_executable_path** é por padrão configurado como **true**, utilizando a fantástica aplicação [webdriver manager](https://github.com/SergeyPirogov/webdriver_manager), facilitando a configuração do webdriver. Você pode configurar como **false** esse parâmetro e configurar manualmente o webdriver no seu sistema.

#### Para utilizar as funcionalidades da Escala 2:

- Preencha as frases no arquivo de texto **frases.txt** que faz parte desse repositório e das configurações da aplicação;

- execute o programa: `python run.py`

*Lembre-se que cada frase é contabilizada pela quebra de linha no arquivo .txt.*

#### Para utilizar as funcionalidades da Escala 3:

- Crie um projeto no Google Cloud Plataform utilizando a Vision API. Ative a cobrança do projeto para liberar a utilização;

- obtenha a chave secreta da Vision API. Certifique-se de que o arquivo desta chave esteja no mesmo diretório raiz dessa aplicação, com o nome de **serviceAccountToken.json**;

- em seguida, no arquivo **config.json**, insira o caminho deste diretório local no campo **imgPath**. 

*É conveniente criar um diretório a parte a qual será usado para servir as imagens para a aplicação pois estas serão removidas no processo*. 

#### Para utilizar as funcionalidades da Escala 4:

- Obtenha a chave secreta da Vision API conforme mencionado acima, para utilização da Escala 3;

- crie um projeto no Google Cloud Plaraform para o Drive API;

- obtenha a chave secreta do Drive API. Certifique-se de que o arquivo referente a esta chave terá o nome de **client_drive_key.json** e que este arquivo esteja no mesmo diretório raíz dessa aplicação;

- crie um diretório no seu Drive e envie as imagens que gostaria de extrair as legendas. Certifique-se que estará na pasta raíz do Drive;

- no arquivo **config.json**, insira no campo **drive_folder_name** o nome do respectivo diretório do Drive a qual ficará as imagens;

- execute o programa: `python run.py`

*Há tutoriais ensinando a configurar a parte do Vision API e do Drive API.*

## Observações

- A aplicação foi projetada de modo a ser aberta para modificações, desde que as suas implementações implementem as abstrações e/ou interfaces que as originais implementam;

- a partir da observação acima, é possível substituir as implementações como o Vision API e Drive API, bem qualquer outra implementação parte da lógica do processo desta aplicação;

- no diretório **src/apps** é possível ver os arquivos dos programas corespondentes a cada escala. Para criar suas próprias implementações, é necessário que todas elas estejam nesse diretório e seguindo as configurações dos programas das escalas existentes;

- para inserir o back side do flash card deve-se alterar manualmente no arquivo **src/clss/cardWriter.py** no método **return_written_cards** da classe **DictBasedCardWriter**, ou substituir essa implementação;

- a parte do back side foi atribuida um valor padrão pois a finalidade inicial (revisão de novas palavras em inglês) não a necessitava, uma vez em que é utilizado uma aplicação de tradução a parte no conteúdo do front side do flash card;

- o autor e esta aplicação não possuem quaisquer vínculo com o Anki e sua aplicação padrão, nem com os representantes das ferramentas utilizadas para a finalidade desse projeto.

- O projeto tem o caráter de aprendizado e aperfeiçoamento.
