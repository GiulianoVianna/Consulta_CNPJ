# Gerar Executavel

## Ambiente virtual

Em distribuicoes como Ubuntu e Debian, o Python do sistema pode bloquear `pip install` direto com o erro `externally-managed-environment`.
Nesse caso, use um ambiente virtual na pasta do projeto:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements-build.txt
```

## Comando

Execute na raiz do projeto:

```bash
python build_executavel.py
```

## Saida

O executavel sera gerado em:

- Linux: `dist/consulta_cnpj/consulta_cnpj`
- Windows: `dist/consulta_cnpj/consulta_cnpj.exe`

## Importante

- Para gerar o executavel do Linux, rode o script no Linux.
- Para gerar o executavel do Windows, rode o script no Windows.
- O PyInstaller nao faz cross-compile confiavel entre Linux e Windows.
- Se o comando `python3 -m venv .venv` falhar, instale o suporte a venv no sistema, por exemplo com `sudo apt install python3-venv`.
