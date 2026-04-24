from pathlib import Path
import importlib.util
import os
import platform
import shutil
import subprocess
import sys


APP_NAME = "consulta_cnpj"
BASE_DIR = Path(__file__).resolve().parent
ENTRYPOINT = BASE_DIR / "consulta_cnpj.py"
UI_FILE = BASE_DIR / "consulta_cnpj.ui"
BUILD_DIR = BASE_DIR / "build"
DIST_DIR = BASE_DIR / "dist"
SPEC_FILE = BASE_DIR / f"{APP_NAME}.spec"
VERSAO_PYTHON_RECOMENDADA_WINDOWS_ANTIGO = (3, 8)


def validar_arquivos():
    faltando = [str(path.name) for path in (ENTRYPOINT, UI_FILE) if not path.exists()]
    if faltando:
        raise FileNotFoundError(
            "Arquivos obrigatorios nao encontrados: " + ", ".join(faltando)
        )


def validar_dependencias():
    if importlib.util.find_spec("PyInstaller") is None:
        instalar_dependencias = (
            ".venv\\Scripts\\python -m pip install -r requirements-build.txt"
            if os.name == "nt"
            else ".venv/bin/python -m pip install -r requirements-build.txt"
        )
        raise RuntimeError(
            "PyInstaller nao esta instalado neste Python.\n"
            "Crie um ambiente virtual e instale as dependencias nele.\n"
            f"Exemplo:\n{sys.executable} -m venv .venv\n"
            f"{instalar_dependencias}"
        )


def avisar_compatibilidade_windows():
    if os.name != "nt":
        return

    versao = sys.version_info[:2]
    if versao >= (3, 12):
        print(
            "\nAVISO DE COMPATIBILIDADE:\n"
            f"Este build esta usando Python {versao[0]}.{versao[1]}.\n"
            "Executaveis gerados com Python 3.12 podem falhar em Windows antigo "
            "com erro envolvendo python312.dll/PssQuerySnapshot.\n"
            "Se a aplicacao precisar rodar em Windows 7, Windows 8.0 ou "
            "Windows Server antigo, gere o executavel com Python "
            f"{VERSAO_PYTHON_RECOMENDADA_WINDOWS_ANTIGO[0]}."
            f"{VERSAO_PYTHON_RECOMENDADA_WINDOWS_ANTIGO[1]} "
            "na mesma arquitetura do Windows de destino.\n"
        )


def separador_add_data():
    return ";" if os.name == "nt" else ":"


def limpar_saida():
    for path in (BUILD_DIR, DIST_DIR, SPEC_FILE):
        if path.is_dir():
            shutil.rmtree(path)
        elif path.exists():
            path.unlink()


def comando_pyinstaller():
    add_data = f"{UI_FILE}{separador_add_data()}."
    return [
        sys.executable,
        "-m",
        "PyInstaller",
        "--noconfirm",
        "--clean",
        "--windowed",
        "--name",
        APP_NAME,
        "--add-data",
        add_data,
        str(ENTRYPOINT),
    ]


def main():
    validar_arquivos()
    validar_dependencias()
    avisar_compatibilidade_windows()
    limpar_saida()

    sistema = platform.system()
    if sistema not in {"Linux", "Windows"}:
        raise RuntimeError(
            "Este script gera executavel apenas em Linux ou Windows."
        )

    print(f"Gerando executavel para {sistema}...")
    print(
        "Observacao: para gerar .exe do Windows, execute este script no Windows. "
        "Para gerar o binario do Linux, execute no Linux."
    )

    comando = comando_pyinstaller()
    print("Comando:", " ".join(comando))
    subprocess.run(comando, check=True, cwd=BASE_DIR)

    executavel = DIST_DIR / APP_NAME / (f"{APP_NAME}.exe" if os.name == "nt" else APP_NAME)
    if executavel.exists():
        print(f"Executavel gerado em: {executavel}")
    else:
        print(f"Build concluido. Verifique a pasta: {DIST_DIR / APP_NAME}")


if __name__ == "__main__":
    main()
