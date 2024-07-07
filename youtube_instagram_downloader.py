from pytube import YouTube
from instaloader import Instaloader, Post
from pathlib import Path
from os import startfile, remove, makedirs
import re
from winotify import Notification, audio
import flet as ft
import os



# Diretório padrão para os downloads dentro do diretório do programa
CURRENT_DIR = Path(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_DOWNLOAD_DIR = CURRENT_DIR / "downloads"
makedirs(DEFAULT_DOWNLOAD_DIR, exist_ok=True)

def notificador(msg, duracao):
    app = "Download de Media"
    titulo = "Baixador de Midias"
    notificacao = Notification(app_id=app, title=titulo, msg=msg, duration=duracao)
    notificacao.set_audio(audio.LoopingAlarm, loop=False)
    notificacao.show()

def sanitize_filename(name):
    return re.sub(r'[\\/*?:"<>|]', "", name)

def download_youtube(video_link, download_option, path_to_download):
    try:
        video_url = YouTube(video_link)
    except Exception as e:
        return f"Erro ao acessar o vídeo: {str(e)}"
    
    if download_option in ["Video Completo", "Ambos"]:
        try:
            video_stream = video_url.streams.get_highest_resolution()
            sanitized_title = sanitize_filename(video_url.title)
            video_file_path = path_to_download / f"{sanitized_title} - video.mp4"
            video_stream.download(output_path=str(path_to_download), filename=video_file_path.name)
            notificador("Seu vídeo do YouTube foi baixado com sucesso!", "short")
        except Exception as e:
            return f"Erro ao baixar o vídeo: {str(e)}"
    
    if download_option in ["Apenas Áudio", "Ambos"]:
        try:
            audio_stream = video_url.streams.filter(only_audio=True).first()
            sanitized_title = sanitize_filename(video_url.title)
            audio_file_path = path_to_download / f"{sanitized_title} - audio.mp4"
            audio_stream.download(output_path=str(path_to_download), filename=audio_file_path.name)
            notificador("Seu áudio do YouTube foi baixado com sucesso!", "short")
        except Exception as e:
            return f"Erro ao baixar o áudio: {str(e)}"
    
    return "Sucesso"

def download_instagram(video_link, path_to_download):
    try:
        loader = Instaloader()
        post = Post.from_shortcode(loader.context, video_link.split('/')[-2])
        loader.download_post(post, target=str(path_to_download))
        
        for file in path_to_download.iterdir():
            if file.suffix != '.mp4':
                remove(file)
        
        notificador("Seu vídeo do Instagram foi baixado com sucesso!", "short")
    except Exception as e:
        return f"Erro ao baixar o vídeo do Instagram: {str(e)}"
    
    return "Sucesso"

def main(page: ft.Page):
    page.title = "Baixador de Mídias" 
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.bgcolor = ft.colors.WHITE  # Fundo branco inicialmente

    logo_var = ft.Image(src="image/Instagram_icon.png", width=100, height=100)  # Adicione o caminho correto do logo do Instagram
    title_var = ft.Text("Instagram", size=30, color=ft.colors.BLACK)  # Texto em preto

    def update_background():
        platform = platform_var.value
        if platform == "YouTube":
            download_option_var.visible = True
            page.bgcolor = ft.colors.BLACK  # Fundo preto
            logo_var.src = "image/Youtube_logo.png"  # Altere para o caminho correto do logo do YouTube
            title_var.value = "YouTube"
            title_var.color = ft.colors.WHITE  # Texto branco
            url_entry.color = ft.colors.WHITE
            folder_path_var.color = ft.colors.WHITE
            platform_text.color = ft.colors.WHITE
            url_text.color = ft.colors.WHITE
        elif platform == "Instagram":
            download_option_var.visible = False
            page.bgcolor = ft.colors.WHITE  # Fundo branco
            logo_var.src = "image/Instagram_icon.png"  # Altere para o caminho correto do logo do Instagram
            title_var.value = "Instagram"
            title_var.color = ft.colors.BLACK  # Texto preto
            url_entry.color = ft.colors.BLACK
            folder_path_var.color = ft.colors.BLACK
            platform_text.color = ft.colors.BLACK
            url_text.color = ft.colors.BLACK
        page.update()

    platform_var = ft.Dropdown(
        options=[
            ft.dropdown.Option("YouTube"),
            ft.dropdown.Option("Instagram"),
        ],
        on_change=lambda e: update_background(),
    )

    url_entry = ft.TextField(
        width=400,
        hint_text="Insira a URL do vídeo",
        color=ft.colors.BLACK  # Texto preto
    )

    download_option_var = ft.Dropdown(
        options=[
            ft.dropdown.Option("Video Completo"),
            ft.dropdown.Option("Apenas Áudio"),
            ft.dropdown.Option("Ambos"),
        ],
        visible=False,
    )

    folder_path_var = ft.TextField(
        width=400,
        value=DEFAULT_DOWNLOAD_DIR,  # Definindo o diretório padrão
        hint_text="Selecione um diretório",
        disabled=True,
        color=ft.colors.BLACK  # Texto preto
    )

    async def start_download(e):
        platform = platform_var.value
        video_link = url_entry.value
        folder_path = folder_path_var.value

        if not folder_path:
            page.dialog.info("Nenhum diretório selecionado.")
            return

        path_to_download = Path(folder_path)
        path_to_download.mkdir(parents=True, exist_ok=True)

        if platform == "YouTube":
            download_option = download_option_var.value
            result = download_youtube(video_link, download_option, path_to_download)
            page.dialog.info(result)
        elif platform == "Instagram":
            result = download_instagram(video_link, path_to_download)
            page.dialog.info(result)

        startfile(path_to_download.resolve())

    def select_folder(e):
        page.dialog.show_html_dialog(
            html="""
            <html>
            <body>
                <input type="file" id="fileDialog" webkitdirectory directory multiple />
                <script>
                    document.getElementById('fileDialog').addEventListener('change', function() {
                        var path = this.files[0].webkitRelativePath;
                        var folders = path.split('/');
                        folders.pop();
                        var folderPath = folders.join('/');
                        window.parent.postMessage(folderPath, '*');
                    });
                </script>
            </body>
            </html>
            """,
            on_message=lambda folder: folder_path_var.update(value=folder),
        )

    platform_text = ft.Text("Escolha a plataforma:", size=20, color=ft.colors.BLACK)  # Texto em preto
    url_text = ft.Text("URL do vídeo:", size=20, color=ft.colors.BLACK)  # Texto em preto

    page.add(
        logo_var,
        title_var,
        platform_text,
        platform_var,
        url_text,
        url_entry,
        folder_path_var,
        download_option_var,
        ft.ElevatedButton("Baixar", on_click=start_download, bgcolor=ft.colors.BLUE, color=ft.colors.WHITE),  # Botão azul com texto branco
    )

    update_background()  # Inicializa o fundo com a plataforma selecionada por padrão

ft.app(target=main)
