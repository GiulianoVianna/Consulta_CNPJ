from pathlib import Path
import sys

from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QRect
from PyQt5.QtWidgets import QMessageBox
import requests


CAMPOS_TELA = (
    "ln_cnpj",
    "ln_data_abertura",
    "ln_situacao_cadastral",
    "ln_capital_social",
    "ln_rsocial",
    "ln_nfantasia",
    "ln_endereco",
    "ln_numero",
    "ln_bairro",
    "ln_cidade",
    "ln_inscricao_estadual",
    "ln_uf",
    "ln_cep",
    "ln_complemento",
    "ln_telefone",
    "ln_email",
)


def caminho_recurso(nome_arquivo):
    base_path = getattr(sys, "_MEIPASS", Path(__file__).resolve().parent)
    return str(Path(base_path) / nome_arquivo)


def exibir_mensagem(titulo, texto, icone=QMessageBox.Information):
    msg = QMessageBox()
    msg.setIcon(icone)
    msg.setWindowTitle(titulo)
    msg.setText(texto)
    msg.exec()


def limpar_campos():
    for nome_campo in CAMPOS_TELA:
        getattr(tela, nome_campo).clear()
    atualizar_estilo_situacao("")
    atualizar_estilo_inscricao_estadual("")


def limpar_tela():
    limpar_campos()
    tela.ln_cons_cnpj.clear()
    tela.ln_cons_cnpj.setFocus()


def configurar_centralizacao():
    widgets = (
        tela.lb_titulo,
        tela.lb_subtitulo,
        tela.toolbar,
        tela.card,
    )
    geometrias_base = {widget.objectName(): QRect(widget.geometry()) for widget in widgets}

    esquerda = min(geometria.x() for geometria in geometrias_base.values())
    topo = min(geometria.y() for geometria in geometrias_base.values())
    direita = max(geometria.x() + geometria.width() for geometria in geometrias_base.values())
    base = max(geometria.y() + geometria.height() for geometria in geometrias_base.values())

    largura_conteudo = direita - esquerda
    altura_conteudo = base - topo
    resize_event_original = tela.resizeEvent

    def centralizar_conteudo():
        deslocamento_x = max((tela.width() - largura_conteudo) // 2 - esquerda, 0)
        deslocamento_y = max((tela.height() - altura_conteudo) // 2 - topo, 0)

        for widget in widgets:
            geometria_base = geometrias_base[widget.objectName()]
            widget.setGeometry(
                geometria_base.x() + deslocamento_x,
                geometria_base.y() + deslocamento_y,
                geometria_base.width(),
                geometria_base.height(),
            )

    def resize_event(event):
        centralizar_conteudo()
        if resize_event_original is not None:
            resize_event_original(event)

    tela.resizeEvent = resize_event
    centralizar_conteudo()


def montar_endereco(estabelecimento):
    tipo = estabelecimento.get("tipo_logradouro", "")
    logradouro = estabelecimento.get("logradouro", "")
    return " ".join(parte for parte in (tipo, logradouro) if parte).strip()


def montar_telefone(estabelecimento):
    ddd = estabelecimento.get("ddd1", "")
    telefone = estabelecimento.get("telefone1", "")
    return f"({ddd}) {telefone}".strip() if ddd or telefone else ""


def formatar_data(data_iso):
    if not data_iso or len(data_iso) != 10 or data_iso.count("-") != 2:
        return str(data_iso or "")

    ano, mes, dia = data_iso.split("-")
    return f"{dia}/{mes}/{ano}"


def formatar_cep(cep):
    cep_numerico = "".join(filter(str.isdigit, str(cep or "")))
    if len(cep_numerico) != 8:
        return str(cep or "")

    return f"{cep_numerico[:2]}.{cep_numerico[2:5]}-{cep_numerico[5:]}"


def atualizar_estilo_situacao(situacao):
    situacao_normalizada = str(situacao or "").strip().upper()
    cor_texto = "#10273f"
    cor_borda = "#ccd8e5"

    if situacao_normalizada == "ATIVA":
        cor_texto = "#1f8f4d"
        cor_borda = "#77c593"
    elif situacao_normalizada:
        cor_texto = "#c0392b"
        cor_borda = "#e4a29d"

    tela.ln_situacao_cadastral.setStyleSheet(
        f"""
        QLineEdit {{
            background-color: #f9fbfd;
            border: 1px solid {cor_borda};
            border-radius: 12px;
            padding: 8px 10px;
            color: {cor_texto};
            font: 700 10pt "Ubuntu";
            selection-background-color: #dbeafe;
        }}
        QLineEdit:focus {{
            border: 2px solid #2f80ed;
            background-color: #ffffff;
        }}
        """
    )


def atualizar_estilo_inscricao_estadual(inscricao_estadual):
    cor_texto = "#10273f"
    cor_borda = "#ccd8e5"
    fonte = ""
    inscricao_normalizada = str(inscricao_estadual or "").strip().upper()

    if inscricao_normalizada == "NAO TEM IE":
        cor_texto = "#c0392b"
        cor_borda = "#e4a29d"
        fonte = 'font: 700 10pt "Ubuntu";'

    tela.ln_inscricao_estadual.setStyleSheet(
        f"""
        QLineEdit {{
            background-color: #f9fbfd;
            border: 1px solid {cor_borda};
            border-radius: 12px;
            padding: 8px 10px;
            color: {cor_texto};
            {fonte}
            selection-background-color: #dbeafe;
        }}
        QLineEdit:focus {{
            border: 2px solid #2f80ed;
            background-color: #ffffff;
        }}
        """
    )


def montar_inscricao_estadual(estabelecimento):
    inscricoes = estabelecimento.get("inscricoes_estaduais") or []
    if not inscricoes:
        return "Nao tem IE"

    valores = []
    for inscricao in inscricoes:
        numero = inscricao.get("inscricao_estadual", "")
        estado = (inscricao.get("estado") or {}).get("sigla", "")
        texto = f"{estado}: {numero}" if estado else str(numero)
        valores.append(texto.strip(": "))

    return " | ".join(valor for valor in valores if valor)


def preencher_campos(retorno):
    estabelecimento = retorno.get("estabelecimento") or {}
    cidade = estabelecimento.get("cidade") or {}
    estado = estabelecimento.get("estado") or {}

    dados = {
        "ln_cnpj": estabelecimento.get("cnpj", ""),
        "ln_data_abertura": formatar_data(
            estabelecimento.get("data_inicio_atividade", "")
        ),
        "ln_situacao_cadastral": estabelecimento.get("situacao_cadastral", ""),
        "ln_capital_social": retorno.get("capital_social", ""),
        "ln_rsocial": retorno.get("razao_social", ""),
        "ln_nfantasia": estabelecimento.get("nome_fantasia", ""),
        "ln_endereco": montar_endereco(estabelecimento),
        "ln_numero": estabelecimento.get("numero", ""),
        "ln_bairro": estabelecimento.get("bairro", ""),
        "ln_cidade": cidade.get("nome", ""),
        "ln_inscricao_estadual": montar_inscricao_estadual(estabelecimento),
        "ln_uf": estado.get("sigla", ""),
        "ln_cep": formatar_cep(estabelecimento.get("cep", "")),
        "ln_complemento": estabelecimento.get("complemento", ""),
        "ln_telefone": montar_telefone(estabelecimento),
        "ln_email": estabelecimento.get("email", ""),
    }

    for nome_campo, valor in dados.items():
        getattr(tela, nome_campo).setText(str(valor or ""))

    atualizar_estilo_situacao(dados["ln_situacao_cadastral"])
    atualizar_estilo_inscricao_estadual(dados["ln_inscricao_estadual"])


def consulta_cnpj(cnpj):
    url = f"https://publica.cnpj.ws/cnpj/{cnpj}"

    try:
        response = requests.get(url, timeout=20)
        response.raise_for_status()
        retorno = response.json()
    except requests.exceptions.Timeout:
        raise RuntimeError("A consulta demorou demais para responder.")
    except requests.exceptions.ConnectionError:
        raise RuntimeError(
            "Nao foi possivel se conectar ao servico de consulta de CNPJ."
        )
    except requests.exceptions.HTTPError as erro:
        if response.status_code == 404:
            raise RuntimeError("CNPJ nao encontrado.") from erro
        if response.status_code == 429:
            raise RuntimeError(
                "Limite de consultas atingido. A API publica da CNPJ.ws permite ate 3 consultas por minuto."
            ) from erro
        raise RuntimeError(f"O servico retornou erro HTTP {response.status_code}.") from erro
    except ValueError as erro:
        raise RuntimeError("A API retornou uma resposta invalida.") from erro

    return retorno


def consultar():
    dados_cnpj = "".join(filter(str.isdigit, tela.ln_cons_cnpj.text()))

    if not dados_cnpj:
        exibir_mensagem("Informacao", "Favor informar o numero do CNPJ!")
        return

    if len(dados_cnpj) != 14:
        limpar_campos()
        exibir_mensagem(
            "CNPJ invalido",
            "Informe um CNPJ com 14 digitos numericos.",
            QMessageBox.Warning,
        )
        return

    try:
        retorno = consulta_cnpj(dados_cnpj)
    except RuntimeError as erro:
        limpar_campos()
        exibir_mensagem("Erro na consulta", str(erro), QMessageBox.Warning)
        return

    preencher_campos(retorno)


app = QtWidgets.QApplication([])
tela = uic.loadUi(caminho_recurso("consulta_cnpj.ui"))
configurar_centralizacao()
tela.ln_cons_cnpj.setInputMask("99.999.999/9999-99;_")
tela.bt_consultar.clicked.connect(consultar)
tela.bt_limpar.clicked.connect(limpar_tela)
tela.ln_cons_cnpj.returnPressed.connect(consultar)
tela.ln_cons_cnpj.setFocus()
tela.show()
app.exec()
