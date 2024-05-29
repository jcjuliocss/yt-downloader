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
    page.window_height = 400
    page.update()

    def download_mp3(urls):
        progress_bar_label = ft.Column([ft.Text('Baixando MP3...'), pb])
        page.add(progress_bar_label)
        def progress_bar(d):
            def fecha_alert(e):
                alert.open = False
                page.update()


            if d['status'] == 'finished':
                alert = ft.AlertDialog(
                    title=ft.Text('Download Concluído.'),
                    actions=[
                        ft.TextButton("Ok", on_click=fecha_alert),
                    ],
                    actions_alignment=ft.MainAxisAlignment.END,)
                page.dialog = alert
                alert.open = True
                pb.value = 0
                page.remove(progress_bar_label)
                page.update()
            if d['status'] == 'downloading':
                progresso = round(
                    float(d['downloaded_bytes'])/float(d['total_bytes'])*100,1)
                pb.value = float(progresso)

                page.update()

        URLS = [urls]

        caminho = carregar_config().get('pasta_destino', '')

        ydl_opts = {
            'format': 'bestaudio',
            'extract_audio': True,
            'outtmpl': caminho + '%(title)s.mp3',
            'progress_hooks': [progress_bar]
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download(URLS)

    def atualiza_caminho(e: ft.FilePickerResultEvent):
        txt_caminho.value = e.path
        txt_caminho.update()
        config = {'pasta_destino': '{}'.format(e.path + '/')}
        salvar_config(config)

    def check_url_download():
        """Verifica se tem url digitada e faz download."""
        if not campo_url.value:
            def fecha_alert(e):
                alert.open = False
                page.update()

            alert = ft.AlertDialog(
                title=ft.Text('Insira a URL.'),
                actions=[
                    ft.TextButton("Ok", on_click=fecha_alert),
                ],
                actions_alignment=ft.MainAxisAlignment.END,)
            page.dialog = alert
            alert.open = True
            page.update()

            return

        url = campo_url.value
        download_mp3(urls=url)

    file_picker = ft.FilePicker(on_result=atualiza_caminho)
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
                    "Download MP3",
                    on_click=lambda _: check_url_download()
                ),
                ft.ElevatedButton(
                    "Selecionar local",
                    on_click=lambda _: file_picker.get_directory_path()
                ),
            ]
        )
    )

ft.app(target=main)
