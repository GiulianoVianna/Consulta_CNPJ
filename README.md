# Consulta_CNPJ

> Aplicacao desktop em Python com PyQt5 para consultar dados cadastrais de empresas brasileiras a partir do CNPJ.

<p align="center">
  <strong>Interface desktop moderna</strong> •
  <strong>Consulta rapida</strong> •
  <strong>Build com PyInstaller</strong>
</p>

## Visao Geral

O `Consulta_CNPJ` e um aplicativo desktop focado em produtividade para consultas cadastrais.
Ele consome a API publica da `CNPJ.ws`, organiza os dados principais da empresa em uma interface clara e destaca visualmente informacoes importantes como situacao cadastral e inscricao estadual.

O projeto foi desenvolvido para rodar de forma simples no desktop e tambem gerar executaveis para distribuicao.

## Recursos

- Consulta de CNPJ com validacao de entrada antes da requisicao.
- Exibicao de razao social, nome fantasia, capital social, endereco, contato e dados cadastrais.
- Formatacao automatica de data, CEP, endereco e telefone.
- Destaque visual para situacao cadastral e ausencia de inscricao estadual.
- Layout centralizado ao redimensionar ou maximizar a janela.
- Tratamento de erros para timeout, CNPJ inexistente, limite de requisicoes e falhas de conexao.
- Empacotamento do app com `PyInstaller`.

## Stack

- `Python`
- `PyQt5`
- `requests`
- `PyInstaller`

## Estrutura do Projeto

```text
consulta_cnpj.py          Aplicacao principal
consulta_cnpj.ui          Interface grafica Qt Designer
build_executavel.py       Script para gerar o executavel
consulta_cnpj.spec        Configuracao de build do PyInstaller
requirements-build.txt    Dependencias para build
BUILD.md                  Instrucoes resumidas de empacotamento
```

## Como Executar

### 1. Criar ambiente virtual

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Instalar dependencias

```bash
python -m pip install --upgrade pip
python -m pip install PyQt5 requests
```

### 3. Iniciar a aplicacao

```bash
python consulta_cnpj.py
```

## Como Gerar o Executavel

Para instalar as dependencias de build:

```bash
python -m pip install -r requirements-build.txt
```

Para gerar o executavel:

```bash
python build_executavel.py
```

Saida esperada:

- Linux: `dist/consulta_cnpj/consulta_cnpj`
- Windows: `dist/consulta_cnpj/consulta_cnpj.exe`

## Regras de Build

- O executavel de Linux deve ser gerado no Linux.
- O executavel de Windows deve ser gerado no Windows.
- O `PyInstaller` nao faz cross-compile confiavel entre Linux e Windows.
- O arquivo `consulta_cnpj.ui` e incluido automaticamente no build.

## Fonte dos Dados

As consultas utilizam a API publica:

- `https://publica.cnpj.ws/cnpj/{cnpj}`

Observacao:
- A API publica da `CNPJ.ws` possui limite de consultas. O aplicativo ja trata esse retorno e informa o usuario quando o limite e atingido.

## Diferenciais da Interface

- Campos organizados em card principal.
- Feedback visual para estados importantes.
- Tela com foco em leitura rapida dos dados retornados.
- Comportamento responsivo para centralizar o conteudo em janelas maiores.

## Status

Projeto funcional e em evolucao, com foco em melhorar a experiencia visual, o fluxo de consulta e a distribuicao do executavel.
