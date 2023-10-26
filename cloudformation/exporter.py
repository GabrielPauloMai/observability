import requests # Importa o módulo requests para fazer requisições HTTP
import json # Importa o módulo json para converter o resultado em JSON
import time # Importa o módulo time para fazer o sleep
from prometheus_client import start_http_server, Gauge

url_numero_pessoas = 'http://api.open-notify.org/astros.json'

def pega_numero_astronautas():
    try:
        """
        Pegar o número de astronautas no espaço
        """
        response = requests.get(url_numero_pessoas)
        data = response.json()
        return data['number']
    except Exception as e:
        print("Não foi possível acessar a url!")
        raise e

def atualiza_metricas():
    try:
        """
        Atualiza as métricas com o número de astronautas e local da estação espacial internacional
        """
        numero_pessoas = Gauge('numero_de_astronautas', 'Número de astronautas no espaço')

        while True:
            numero_pessoas.set(pega_numero_astronautas())
            time.sleep(10)
            print("O número atual de astronautas no espaço é: %s" % pega_numero_astronautas())
    except Exception as e:
        print("A quantidade de astronautas não pode ser atualizada!")
        raise e

def inicia_exporter():
    try:
        """
        Iniciar o exporter
        """
        start_http_server(8895)
        return True
    except Exception as e:
        print("O Servidor não pode ser iniciado!")
        raise e

def main():
    try:
        inicia_exporter()
        print('Exporter Iniciado')
        atualiza_metricas()
    except Exception as e:
        print('\nExporter Falhou e Foi Finalizado! \n\n======> %s\n' % e)
        exit(1)


if __name__ == '__main__':
    main()
    exit(0)