import yt_dlp
import json
import os

def download_mp3(urls):
    URLS = [urls]

    caminho = carregar_config().get('pasta_destino', '')

    ydl_opts = {
        'format': 'bestaudio',
        'extract_audio': True,
        'outtmpl': caminho + '%(title)s.mp3'
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        error_code = ydl.download(URLS)

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

def selecionar_pasta_destino():
    caminho = input('Caminho: ')

    config = {'pasta_destino': '{}'.format(caminho + '/')}

    salvar_config(config=config)

def menu():
    print('*-----YT DONWLOADER-----*\n')
    print('[1] Selecionar pasta de destino\n')
    print('[2] Baixar MP3\n')
    print('[3] Sair\n')

    opcao = int(input())

    if opcao == 1:
        selecionar_pasta_destino()
    elif opcao == 2:
        url = input('URL: ')
        download_mp3(url)
    elif opcao == 3:
        os._exit(0)

    menu()

menu()
