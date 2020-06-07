import os, json, requests, wget, csv, shutil
from array import *
from bs4 import BeautifulSoup
from collections import defaultdict

class ObtemDados:

    def chamaAPI(self, url):
        chamada = requests.get(url)
        return chamada

    def consomeHTML(self, url):
        chamada = self.chamaAPI(url)
        chamada = BeautifulSoup(chamada.text, "html.parser")
        return chamada

    def apagaArquivos(self):
        os.remove('dados/brutos/planilha.csv')
        os.remove('dados/brutos/estadosTodoPeriodo.txt')
        pass

    def formataPlanilha(self, url):
        planilha = wget.download(url, out='dados/brutos/planilha.csv')
        estadosBruto = open('dados/brutos/estadosTodoPeriodo.txt', 'w')
        with open(planilha, 'r') as csvfile:
            for row in csv.DictReader(csvfile):
                if row['place_type'] == 'state':
                    dados = row['date'] + "," + row['state'] + "," + row['last_available_confirmed'] + "," + row['new_confirmed'] + "," + row['last_available_deaths'] + "," + row['new_deaths'] + "\n"
                    estadosBruto.writelines(dados)

        estadosBruto.close()
        pass

    def abreEstados(self):
        with open('dados/brutos/estadosTodoPeriodo.txt', 'r') as estadosBruto:
            dados = estadosBruto.readlines()
        return dados

    def geraNorte(self, dados):
        with open('dados/tratados/regiaoNorte.txt', 'w') as regiaoNorte:
            regiaoNorte.writelines(dados[0] + dados[2]  + dados[3]  + dados[13]  + dados[20]  + dados[21]  + dados[26])
        pass

    def geraNordeste(self, dados):
        with open('dados/tratados/regiaoNordeste.txt', 'w') as regiaoNordeste:
            regiaoNordeste.writelines(dados[1] + dados[4]  + dados[5]  + dados[9]  + dados[14]  + dados[15]  + dados[16] + dados[19] + dados[24])
        pass

    def geraCentro(self, dados):
        with open('dados/tratados/regiaoCentro.txt', 'w') as regiaoCentro:
            regiaoCentro.writelines(dados[6] + dados[8]  + dados[11]  + dados[12])
        pass

    def geraSudeste(self, dados):
        with open('dados/tratados/regiaoSudeste.txt', 'w') as regiaoSudeste:
            regiaoSudeste.writelines(dados[7] + dados[10]  + dados[18]  + dados[25])
        pass

    def geraSul(self, dados):
        with open('dados/tratados/regiaoSul.txt', 'w') as regiaoSul:
            regiaoSul.writelines(dados[23] + dados[22]  + dados[17])
        pass
