
# Projeto Media Downloader

Este projeto é um baixador de mídias que permite aos usuários baixar vídeos do YouTube e do Instagram. Oferece opções para baixar vídeos completos, apenas áudio ou ambos do YouTube, e vídeos do Instagram. O projeto utiliza várias bibliotecas Python, incluindo pytube, instaloader e flet para suas funcionalidades. Abaixo está uma descrição detalhada da configuração e funcionalidade do projeto.

## Configuração do projeto

- pytube: Para baixar vídeos e áudio do YouTube.
- instaloader: Para baixar vídeos do Instagram.
- pathlib: Para manipulação de caminhos de arquivo.
- os: Para interagir com o sistema operacional.
- re: Para sanitizar nomes de arquivos.
- winotify: Para exibir notificações no Windows.
- flet: Para criar a aplicação GUI.

## Estrutura do diretorio

O projeto possui um diretório padrão para downloads dentro da estrutura de diretórios do programa:

CURRENT_DIR = Path(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_DOWNLOAD_DIR = CURRENT_DIR / "downloads"
makedirs(DEFAULT_DOWNLOAD_DIR, exist_ok=True)


## Funções

notificador(msg, duracao)
Exibe uma notificação com a mensagem e duração fornecidas.

sanitize_filename(name)
Sanitiza nomes de arquivos para remover caracteres que não são permitidos em nomes de arquivos.

download_youtube(video_link, download_option, path_to_download)
Baixa vídeos e/ou áudio do YouTube com base na opção de download selecionada.

download_instagram(video_link, path_to_download)
Baixa vídeos do Instagram.


## Instalação 

1. Clone o repositório:
git clone https://github.com/Brendo-will/MediaDownloader.git
cd MediaDownloader

2. Crie um ambiente virtual (opcional, mas recomendado):
python -m venv venv
source venv/bin/activate # No Windows use `venv\Scripts\activate`

4. Instale as dependências:
pip install -r requirements.txt

5 - crie uma pasta chamada imagem e adicione as duas imagens dentro dela 

##Uso 
1. Execute o script:
python youtube_instagram_downloader.py

## Utilização

Selecione a plataforma (YouTube ou Instagram).

Insira o URL do vídeo.

Escolha a opção de download (para o YouTube).

Selecione o diretório de download.

Clique no botão "Baixar" para iniciar o download.

Os arquivos de mídia baixados serão salvos no diretório especificado, e notificações serão exibidas após os downloads bem-sucedidos.

