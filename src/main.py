# -*- coding: utf-8 -*-
import tweepy, schedule, time, os
from obtemDados import *
from autentica import *
from formataDados import *

auth   = Autentica()
dados  = ObtemDados()
format = FormataDados()

urlMeters     = "https://www.worldometers.info/coronavirus/country/brazil/"
urlHopkins    = "https://coronavirus-tracker-api.herokuapp.com/v2/locations?country_code=BR"

def job():
    api           = auth.api(os.environ['CONSUMER_KEY'], os.environ['CONSUMER_SECRET'], os.environ['ACCESS_TOKEN'], os.environ['ACCESS_TOKEN_SECRET'])
    user          = auth.usuario(api)

    if dados.chamaAPI(urlMeters).status_code == requests.codes.ok:

        chamada = dados.consomeHTML(urlMeters)

        try:
            api.update_status(format.htmlWorldMeters(chamada))
            print(format.htmlWorldMeters(chamada))

        except tweepy.TweepError as error:

            if error.api_code == 187:
                print('Mensagem Duplicada')

            else:
                raise error


    elif dados.chamaAPI(urlHopkins).status_code == requests.codes.ok:

        chamada = dados.chamaAPI(urlHopkins)

        try:
            api.update_status(format.apiJohnHopkins(chamada))
            print(format.apiJohnHopkins(chamada))

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
