import yt_dlp
import json
import os
import flet as ft

def carregar_config():
    try:
        arquivo = open('config.json', 'r')
        config = json.loads(arquivo.read())
        arquivo.close()
    except FileNotFoundError:
        config = {}

    return config

def salvar_config(config):
    cfg = carregar_config()

    cfg.update(config)

    arquivo_config = open('config.json', 'w')

    arquivo_config.write(json.dumps(cfg))
    arquivo_config.close()

def main(page: ft.Page):
    txt = ft.Text(value='YT Downloader', size=30)
    page.controls.append(txt)
    page.window_width = 1000
    page.window_max_width = 1000
    page.window_height = 400
    page.window_max_height = 400
    page.update()

    def cria_alert(text):
        def fecha_alert(e):
            alert.open = False
            page.update()

        alert = ft.AlertDialog(
            title=ft.Text(text),
            actions=[
                ft.TextButton("Ok", on_click=fecha_alert),
            ],
            actions_alignment=ft.MainAxisAlignment.END,)

        return alert

    def progress_bar(d):
        if d['status'] == 'finished':
            alert = cria_alert(text='Download Concluído.')
            page.dialog = alert
            alert.open = True

            pb.value = 0

        if d['status'] == 'downloading':
            progresso = float(
                d['downloaded_bytes']) / float(d['total_bytes'] * 100) * 100
            pb.value = float(progresso)

            page.update()

    def progress_bar_playlist(d):
        if d['status'] == 'finished':
            pb.value = 0
        if d['status'] == 'downloading':
            progresso = float(
                d['downloaded_bytes']) / float(d['total_bytes'] * 100) * 100
            pb.value = float(progresso)

            page.update()

    def download_mp3(url):
        progress_bar_label = ft.Column([ft.Text('Baixando MP3...'), pb])
        page.add(progress_bar_label)

        URLS = [url]

        caminho = carregar_config().get('pasta_destino', '')

        ydl_opts = {
            'ignoreerrors': True,
            'format': 'bestaudio',
            'extract_audio': True,
            'outtmpl': caminho + '%(title)s.mp3',
            'progress_hooks': [progress_bar]
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download(URLS)

        page.remove(progress_bar_label)
        page.update()

    def download_video(url):
        progress_bar_label = ft.Column([ft.Text('Baixando Vídeo...'), pb])
        page.add(progress_bar_label)

        URLS = [url]

        caminho = carregar_config().get('pasta_destino', '')


        ydl_opts = {
            'format': 'bestvideo+bestaudio/best',
            'ignoreerrors': True,
            'outtmpl': caminho + '%(title)s.%(ext)s',
            'progress_hooks': [progress_bar]
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download(URLS)

        page.remove(progress_bar_label)
        page.update()

    def download_playlist(url, audio=False):
        progress_bar_label = ft.Text('Baixando Playlist...')
        progress_column = ft.Column([progress_bar_label, pb])
        page.add(progress_column)

        URLS = [url]

        caminho = carregar_config().get('pasta_destino', '')

        ydl_opts = {
            'ignoreerrors': True,
            'format': 'bestaudio',
            'extract_audio': True,
            'outtmpl': caminho + '%(title)s.mp3',
            'progress_hooks': [progress_bar_playlist]
        }

        if not audio:
            ydl_opts = {
                'ignoreerrors': True,
                'format': 'bestvideo+bestaudio/best',
                'outtmpl': caminho + '%(title)s.%(ext)s',
                'progress_hooks': [progress_bar_playlist]
            }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download(URLS)

        page.remove(progress_bar_label)
        page.update()

    def atualiza_local_destino(e: ft.FilePickerResultEvent):
        txt_caminho.value = e.path
        txt_caminho.update()
        config = {'pasta_destino': '{}'.format(e.path + '/')}
        salvar_config(config)

    def check_url_download(tipo_download):
        """Verifica se tem url digitada e faz download."""
        if not campo_url.value:
            alert = cria_alert(text='Insira a URL.')
            page.dialog = alert
            alert.open = True
            page.update()

            return

        if not campo_url.value.startswith((
                'https://www.youtube.com',
                'www.youtube.com',
                'https://youtube.com',
                'youtube.com')):
            alert = cria_alert(text='URL inválida.')
            page.dialog = alert
            alert.open = True
            page.update()

            return

        url = campo_url.value

        if tipo_download == 1:
            download_mp3(url=url)
        elif tipo_download == 2:
            download_video(url=url)
        elif tipo_download == 3:
            download_playlist(url=url)
        elif tipo_download == 4:
            download_playlist(url=url, audio=True)

    file_picker = ft.FilePicker(on_result=atualiza_local_destino)
    page.overlay.append(file_picker)

    label_caminho = ft.Text('Local de destino:')
    caminho = carregar_config().get('pasta_destino', '')
    txt_caminho = ft.Text(weight=ft.FontWeight.BOLD, value=caminho)

    page.add(
        ft.Row(
            [
                label_caminho,
                txt_caminho,
            ]
        )
    )

    campo_url = ft.TextField(label='URL', icon=ft.icons.LINK_SHARP)
    page.add(campo_url)

    pb = ft.ProgressBar(width=1000)

    page.add(
        ft.Row(
            [
                ft.ElevatedButton(
                    "Baixar MP3",
                    on_click=lambda _: check_url_download(tipo_download=1)
                ),
                ft.ElevatedButton(
                    "Baixar Vídeo",
                    on_click=lambda _: check_url_download(tipo_download=2)
                ),
                ft.ElevatedButton(
                    "Baixar Playlist",
                    on_click=lambda _: check_url_download(tipo_download=3)
                ),
                ft.ElevatedButton(
                    "Baixar Playlist (MP3)",
                    on_click=lambda _: check_url_download(tipo_download=4)
                ),
                ft.ElevatedButton(
                    "Selecionar local",
                    on_click=lambda _: file_picker.get_directory_path()
                ),
            ]
        )
    )

ft.app(target=main)
