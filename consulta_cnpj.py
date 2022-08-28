
from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import QMessageBox
import requests
import json


def consulta_cnpj(cnpj):
    url = f'https://receitaws.com.br/v1/cnpj/{cnpj}'
    # Token para cessar a base de dados da receita federal
    querystring = {"token":"XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX","cnpj":"06990590000123","plugin":"RF"}
    response = requests.request("GET", url, params=querystring)
    retorno = json.loads(response.text)    
    tela.ln_cnpj.setText(retorno['cnpj'])
    tela.ln_data_abertura.setText(retorno['abertura'])
    tela.ln_situacao_cadastral.setText(retorno['situacao'])
    tela.ln_capital_social.setText(retorno['capital_social'])
    tela.ln_rsocial.setText(retorno['nome'])
    tela.ln_nfantasia.setText(retorno['fantasia'])
    tela.ln_endereco.setText(retorno['logradouro'])
    tela.ln_numero.setText(retorno['numero'])
    tela.ln_bairro.setText(retorno['bairro'])
    tela.ln_cidade.setText(retorno['municipio'])
    tela.ln_uf.setText(retorno['uf'])
    tela.ln_cep.setText(retorno['cep'])
    tela.ln_complemento.setText(retorno['complemento'])
    tela.ln_telefone.setText(retorno['telefone'])
    tela.ln_email.setText(retorno['email'])


def mensagem():
        msg1 = QMessageBox()
        msg1.setIcon(QMessageBox.Information)
        msg1.setWindowTitle('Informação!')
        msg1.setText('Favor informar o número do CNPJ!')
        x = msg1.exec()


def consultar():
    dados_cnpj = tela.ln_cons_cnpj.text()
    if dados_cnpj != "":
        consulta_cnpj(dados_cnpj)
    else:
        mensagem()



app = QtWidgets.QApplication([])
tela = uic.loadUi("consulta_cnpj.ui")
tela.bt_consultar.clicked.connect(consultar)

tela.show()
app.exec()