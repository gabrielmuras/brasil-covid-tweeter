# -*- coding: utf-8 -*-
import os, json, tweepy, requests, schedule, time, datetime, dateutil, pytz, locale
from dateutil.parser import parse
from autentica import Autentica

autentica = Autentica()

def job():
    api           = autentica.api(os.environ['CONSUMER_KEY'], os.environ['CONSUMER_SECRET'], os.environ['ACCESS_TOKEN'], os.environ['ACCESS_TOKEN_SECRET'])
    user          = autentica.usuario(api)
    chamada       = requests.get('https://covid19-brazil-api.now.sh/api/report/v1/brazil')
    chamadaBackup = requests.get('https://coronavirus-tracker-api.herokuapp.com/v2/locations?country_code=BR')
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')


    if chamada.status_code == requests.codes.ok:

        chamada = requests.get('https://covid19-brazil-api.now.sh/api/report/v1/brazil')
        dados_json = json.loads(chamada.content)


        pais        = '{country}'.format(**dados_json["data"])
        mortes      = locale.format("%d", int('{deaths}'.format(**dados_json["data"])), grouping=True)
        data        = '{updated_at}'.format(**dados_json["data"])
        recuperados = locale.format("%d", int('{recovered}'.format(**dados_json["data"])), grouping=True)
        casosAtivos = locale.format("%d", int('{cases}'.format(**dados_json["data"])), grouping=True)
        casosTotais = locale.format("%d", int('{confirmed}'.format(**dados_json["data"])), grouping=True)

        data      = dateutil.parser.isoparse(data)
        data      = data.astimezone(pytz.timezone("America/Sao_Paulo"))
        dataCompleta = "%s/%s/%s %s:%s" % (data.day, data.month, data.year, data.hour, data.minute)


        status_template = "Relatório Covid-19: \n \nPaís: Brasil \nCasos Totais: %s \nCasos Ativos: %s \nRecuperados: %s \nNúmero de Mortes: %s\n\n" +  "Dados disponibilizados em: " +dataCompleta + "\nFonte: https://covid.saude.gov.br/"
        status_template = status_template % (casosTotais,casosAtivos,recuperados,mortes)

        try:
            api.update_status(status_template)
            print(status_template)
        except tweepy.TweepError as error:
            if error.api_code == 187:
                print('Mensagem Duplicada')
            else:
                raise error


    elif chamadaBackup.status_code == requests.codes.ok:

        chamada = requests.get('https://coronavirus-tracker-api.herokuapp.com/v2/locations?country_code=BR')
        dados_json = json.loads(chamada.content)


        mortes      = locale.format("%d", int('{deaths}'.format(**dados_json["latest"])), grouping=True)
        casosAtivos = locale.format("%d", int('{confirmed}'.format(**dados_json["latest"])), grouping=True)
        data        = '{last_updated}'.format(**dados_json["locations"][0])

        data      = dateutil.parser.isoparse(data)
        data      = data.astimezone(pytz.timezone("America/Sao_Paulo"))
        dataCompleta = "%s/%s/%s %s:%s" % (data.day, data.month, data.year, data.hour, data.minute)


        status_template = "Relatório Covid-19: \n\nPaís: Brasil \nCasos Totais: %s \nNúmero de Mortes: %s\n\n" + "Dados disponibilizados em: " + dataCompleta + "\nFonte: Johns Hopkins University"
        status          = status_template % (casosAtivos, mortes)

        try:
            api.update_status(status_template)
            print(status)
        except tweepy.TweepError as error:
            if error.api_code == 187:
                print('Mensagem Duplicada')
            else:
                raise error

    else:
        print("Infelizmente não há conexão com os dados")


periodicidade_minutos = 240
schedule.every(periodicidade_minutos).minutes.do(job)

while 1:

    schedule.run_pending()
    time.sleep(1)
