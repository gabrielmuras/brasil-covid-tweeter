# -*- coding: utf-8 -*-
import locale, dateutil, pytz
from dateutil.parser import parse
from obtemDados import *

obtemDados = ObtemDados()

urlPlanilha = "https://brasil.io/dataset/covid19/caso_full/?format=csv"
urlMinisterio = 'https://covid19-brazil-api.now.sh/api/report/v1/brazil'
urlJohnHopkins = 'https://coronavirus-tracker-api.herokuapp.com/v2/locations?country_code=BR'
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

class FormataDados:

    def apiMinisterio(self, chamada):


        dados_json = json.loads(chamada.content)
        try:
            pais = '{country}'.format(**dados_json["data"])
        except:
            pais = "Não há dados disponibilizados"
        try:
            mortes = '{0:n}'.format(int('{deaths}'.format(**dados_json["data"])))
        except:
            mortes = "Não há dados disponibilizados"
        #try:
        data = '{updated_at}'.format(**dados_json["data"])
        try:
            recuperados = '{0:n}'.format(int('{recovered}'.format(**dados_json["data"])))
        except:
            recuperados = "Não há dados disponibilizados"
        try:
            casosAtivos = '{0:n}'.format(int('{cases}'.format(**dados_json["data"])))
        except:
            casosAtivos = "Não há dados disponibilizados"
        try:
            casosTotais = '{0:n}'.format(int('{confirmed}'.format(**dados_json["data"])))
        except:
            casosTotais = "Não há dados disponibilizados"

        data      = dateutil.parser.isoparse(data)
        data      = data.astimezone(pytz.timezone("America/Sao_Paulo"))
        data      = "%s/%s/%s %s:%s" % (data.day, data.month, data.year, data.hour, data.minute)



        status_template = "Relatório Covid-19: \n \nPaís: Brasil \nCasos Totais: %s \nCasos Ativos: %s \nRecuperados: %s \nNúmero de Mortes: %s\n\n" +  "Dados disponibilizados em: " + data + "\nFonte: https://covid.saude.gov.br/"
        status_template = status_template % (casosTotais,casosAtivos,recuperados,mortes)

        return status_template

    def apiJohnHopkins(self, chamada):

        dados_json = json.loads(chamada.content)
        try:
            mortes      = '{0:n}'.format(int('{deaths}'.format(**dados_json["latest"])))
        except:
            mortes = "Não há dados disponibilizados"
        try:
            casosAtivos = '{0:n}'.format(int('{confirmed}'.format(**dados_json["latest"])))
        except:
            casosAtivos = "Não há dados disponibilizados"
        data        = '{last_updated}'.format(**dados_json["locations"][0])

        data      = dateutil.parser.isoparse(data)
        data      = data.astimezone(pytz.timezone("America/Sao_Paulo"))
        data      = "%s/%s/%s %s:%s" % (data.day, data.month, data.year, data.hour, data.minute)


        status_template = "Relatório Covid-19: \n\nPaís: Brasil \nCasos Totais: %s \nNúmero de Mortes: %s\n\n" + "Dados disponibilizados em: " + data + "\nFonte: Johns Hopkins University"
        status_template = status_template % (casosAtivos, mortes)


        return status_template


    def htmlWorldMeters(self, chamada):

        dados = chamada.find_all("div",class_ = "maincounter-number")

        try:
            mortes = '{0:n}'.format(int(dados[1].text.strip().replace(",", "")))
        except:
            mortes = "Não há dados disponibilizados"
        try:
            recuperados = '{0:n}'.format(int(dados[2].text.strip().replace(",", "")))
        except:
            recuperados = "Não há dados disponibilizados"
        try:
            casosTotais = '{0:n}'.format(int(dados[0].text.strip().replace(",", "")))
        except:
            casosTotais = "Não há dados disponibilizados"

        dados  = chamada.find_all("div",class_ = "number-table-main")

        try:
            casosAtivos = '{0:n}'.format(int(dados[0].text.strip().replace(",", "")))
        except:
            casosAtivos = "Não há dados disponibilizados"

        status_template = "Relatório Covid-19: \n \nPaís: Brasil \nCasos Totais: %s \nCasos Ativos: %s \nRecuperados: %s \nNúmero de Mortes: %s\n\nFonte: Worldometers"

        status_template = status_template % (casosTotais,casosAtivos,recuperados,mortes)

        return status_template


        #def estados ()
