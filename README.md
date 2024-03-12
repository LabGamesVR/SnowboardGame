# Snowboard Game

Para fins de testes, a movimentação está sendo feita pelo teclado utilizando as teclas A (Anda para esquerda) e D (Anda para direita)

Links para referência de pseudo 3D: 
* Explicação geral de como funciona: <http://www.extentofthejam.com/pseudo/>
* Projeto feito em pygame de jogo pseudo 3d estilo Outrun: <https://github.com/buntine/SwervinMervin/tree/master/swervin_mervin>

## Arquivo results.csv
Atualmente o arquivo armazena todos os dados coletados em uma linha só, delimitando os valores por vírgula(,):

NOME,PONTUAÇÃO,TEMPO DE JOGO,Nº DE OBSTÁCULOS,NÚMERO DE MOVIMENTOS ERRADOS


## Modo de uso

### Vá para pasta de desenvolvimento
    cd python

### Inicie um ambiente virtual
    python -m venv local-env

### Ative o ambiente
UNIX:

    source local-env/bin/activate

Windows:

    local-env\Scripts\activate
    
### Instale pacotes necessarios

    pip install -r requirements.txt


### Inicie o script

    python3 src/main.py

## Salvando
Antes de salvar backup, faça:

    pip freeze > requirements.txt
