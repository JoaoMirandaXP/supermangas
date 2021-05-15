# supermangas
Baixa..... mangás!

## Para usar esse programa você vai precisar
------

- Ter o python3 instalado no seu computador (lembre de adicionar o python as VARIAVEIS DE AMBIENTE ou PATH)
https://www.python.org/downloads/

- Instalar os requirements do programa
(basta ir na pasta em que foi baixado e digitar)
```
pip install -r requirements.txt
```
ou no windows
```
python -m pip install -r requirements.txt
```
- Baixar o webdriver selenium de acordo com seu navegador
https://pypi.org/project/selenium/#drivers
coloque num local confortável e não esqueça de descompactá-lo(veja o caminho para o seu arquivo, vamos usar a seguir!)

- Abrir o aquivo, ```mangadownloader.py``` no seu bloco de notas ou sei lá e substituir a constante PATH_PARA_WEBDRIVER do programa pelo caminho do webdriver que você conseguiu no passo anterior
------

## Agora é só baixar!
Encontre a URL do seu manga e atualmente, o aplicativo vai procurar por todas os capitulos que estiverem disponiveis no site e vai salvar na pasta ```output```

```
python supermangas.py [URL] [inicio] [fim]
```
* os parâmetros ```[incio]``` e ```[fim]``` podem ser ignorados caso se desejar baixar todos os episódios, coloque números ou seus valores serão ignorados, honestamente, eu não sei o que acontece se você colocar um capítulo que não exista... Então se você quiser descobrir e me contar eu agradeceria!  
