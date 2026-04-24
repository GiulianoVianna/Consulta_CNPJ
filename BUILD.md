# Build do Executavel

## Erro `python312.dll` / `PssQuerySnapshot`

Se o executavel abre em uma maquina e falha em outra com mensagens como:

- `Failed to load Python DLL ... python312.dll`
- `PssQuerySnapshot nao foi localizado na biblioteca de vinculo dinamico ... python312.dll`

o problema normalmente nao esta no codigo da aplicacao. Ele indica que o `.exe`
foi gerado com Python 3.12 e esta sendo executado em uma versao antiga do
Windows que nao possui a API esperada por essa DLL.

A documentacao oficial do Python informa que Python 3.12 suporta Windows 8.1
ou superior. Para Windows 7, use Python 3.8.

## Build recomendado para maquinas antigas

Em uma maquina Windows, instale Python 3.8.x na mesma arquitetura do Windows de
destino:

- Windows 64 bits: Python 3.8.x 64 bits.
- Windows 32 bits: Python 3.8.x 32 bits.

Depois confirme se o Python 3.8 foi reconhecido pelo launcher:

```powershell
py -0p
```

Se aparecer um caminho para `Python38\python.exe`, gere o executavel usando
esse Python:

```powershell
py -3.8 -m venv .venv38
.\.venv38\Scripts\python -m pip install --upgrade pip
.\.venv38\Scripts\python -m pip install -r requirements-build.txt
.\.venv38\Scripts\python build_executavel.py
```

Distribua a pasta inteira gerada em `dist\consulta_cnpj`, nao apenas o arquivo
`consulta_cnpj.exe`, porque o modo atual do PyInstaller gera dependencias dentro
da mesma pasta.

## Build para Windows moderno

Para Windows 10/11 atualizados, o build com Python 3.12 deve funcionar:

```powershell
python -m pip install -r requirements-build.txt
python build_executavel.py
```

## Observacoes

- Gere o `.exe` no Windows. O PyInstaller nao faz cross-compile confiavel.
- Se o destino for Windows antigo, gere com uma versao de Python compativel com
  esse Windows.
- Se o destino for 32 bits, o build tambem precisa ser feito com Python 32 bits.
