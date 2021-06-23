import sys
import time
import os
from selenium import webdriver
from PIL import Image
import requests
from datetime import datetime

#Coloque aqui o caminho para o seu webdriver selenium, atenção, ele deve estar na mesma versão do seu chrome
PATH_PARA_WEBDRIVER = '/usr/bin/chromedriver' # INSIRA_AQUI O SEU WEB DRIVER, leia o README.md'

#unidade do tempo de espera entre requisições para evitar bugs, em segundos, para conexão lenta usar 2 seg
WAIT_TIME = 0.75



#   função de limpeza da pasta temp, pode não ser sempre necessária
#   mas considere o seguinte, o capitulo seguinte a esse tem menos páginas
#   de tal modo o pŕoximo será renderizado com a mesma quantidade de páginas do atual
#   e a páginas a mais serão renderizadas também
def clear_temp():
    for x in os.listdir('.temp'):
        if not x.endswith('.txt'):
            local= os.path.join('.temp', x)
            os.remove(local)
#   Para facilitar o processo do driver de ir para alguma url em portugues
#   e também para definir um tempo de espera entre as requisições entre duas páginas
def ir_para(url, driver):
    driver.get(url)
    time.sleep(WAIT_TIME)
#   Essa função é parecida com a anterior, mas para facilitar a lógica, fiz outra que suprisse as necessidades
#   E ela também tem o tempo de espera, é utilizada praticamante para calcular o número de páginas que tem em um
#   capítulo
def buscar_elementos(elemento, driver, metodo):
    time.sleep(2*WAIT_TIME)
    if(metodo == 'nato'):
        elementos = driver.find_element_by_class_name(elemento)
    if(metodo == 'goiaba'):
        elementos = driver.find_element_by_id(elemento)

    return elementos
#   pode ser útil ao ter que selecionar uma língua de preferência, se houver para o mangá
def busca_capitulos(elemento, metodo, capitulos = {}):
    divs = []
    wrapper = ''
    chapter_box = ''
    title_tag_name = ''
    if(metodo == 'goiaba'):
        wrapper = 'boxTop10'
        chapter_box = 'top10Link'
        title_tag_name = 'span'
    if(metodo == 'nato'):
        wrapper = 'a-h'
        chapter_box = 'a-h'
        title_tag_name = 'a'
    time.sleep(WAIT_TIME)
    try:
        divs = elemento.find_elements_by_class_name(wrapper)
        print(divs)
    except Exception:
        print('Cool Down, acho que estou indo rápido demais')
        time.sleep(10*WAIT_TIME)
        divs = elemento.find_element_by_class_name(wrapper)
    #divs = []
    #for d in elemento.find_elements_by_class_name('boxTop10'):
    #    try:
    #        d.find_element_by_xpath('//img[@alt="Inglês"]')
    #    except Exception:
    #        divs.append(d)
    for div in divs:
        try:
            if(metodo == 'nato'):
                link = div.find_element_by_tag_name('a').get_attribute('href')
                number = div.find_element_by_tag_name(title_tag_name).text
                capitulos[number] = link
            if(metodo == 'goiaba'):
                chapter=div.find_element_by_class_name(chapter_box)
                link = chapter.find_element_by_tag_name('a').get_attribute('href')
                number = chapter.find_element_by_tag_name(title_tag_name).text
                capitulos[number] = link

        except Exception:
            time.sleep(WAIT_TIME)
            if(metodo == 'nato'):
                link = div.find_element_by_tag_name('a').get_attribute('href')
                number = div.find_element_by_tag_name(title_tag_name).text
                capitulos[number] = link
            if(metodo == 'goiaba'):
                chapter=div.find_element_by_class_name(chapter_box)
                link = chapter.find_element_by_tag_name('a').get_attribute('href')
                number = chapter.find_element_by_tag_name(title_tag_name).text
                capitulos[number] = link


    return capitulos
#   Apenas como simplificação dos comandos para selenium, funciona como um simplficador da clausula if dentro da execução
#   veriicando se existem mais capítulos a adicionados ao grande dicionário associando todos os links aos seus respectivos capitulos
def existem_mais_capitulos(capitulos, driver, ate = 1):
    time.sleep(4*WAIT_TIME)
    if str(ate) in capitulos:
        print('Finalizamos a busca pelos capitulos')
        return False
    else:
        print('Buscando o intervalo nos capítulos... Vamos para a próxima página')
        #print(capitulos)
        driver.find_element_by_xpath('//button[@title="Próxima Página"]').click()
        #print('Vamos para a página anterior')
        #driver.find_element_by_xpath('//button[@title="Página Anterior"]').click()
        return True
#   É o tempero específico para esse site, mas pode funcionar para vários outros, já que esse usa a estratégia de deixar imagens vazias
#   Para evitar o webscrapping, então utilizamos apenas a primeira url que nesse caso será modificada no cógigo
def url_tracker(url, numero):
    img_links = []
    url_split = url.split('/')
    url_split.pop(-1)
    base_url = "/"
    base_url = base_url.join(url_split)
    base_url += '/{}.jpg'
    for n in range(1, numero + 1):
        new_url = base_url.format(n)
        img_links.append(new_url)
    return img_links
#   Separação de código
def abrir_capitulo(capitulo_id,link,driver):
    ir_para(link, driver)
    div  = ''
    try:
        div = driver.find_element_by_class_name('capituloView')
        print('Identificando imagens do capitulo {}'.format(capitulo_id))
    except Exception:
        print('Cool down, acho que estou indo rápido demais')
        time.sleep(30*WAIT_TIME)
        print('Okay, vamos tentar de novo!')
        ir_para(link, driver)
        div = driver.find_element_by_class_name('capituloView')

    divs_paginas = div.find_elements_by_class_name('capituloViewBox')

    numero = len(divs_paginas)
    url = driver.find_element_by_xpath('//img[@data-id-image=1]').get_attribute('src')
    img_links = url_tracker(url, numero)

    return img_links
#   É uma fundionalidade a ser melhorada, afinal essa é a parte que se faz uma lista brutal com todos os capítulos vinculados a todos os links da suas respectivas imagens
def abrir_capitulos(capitulos, driver,inicio, fim):
    capitulo_vector = {}
    if fim == -1:
        fim = len(capitulos)
    for capitulo, link in capitulos.items():
        if(inicio<=int(capitulo.split('.')[0])<=fim):
            ir_para(link, driver)
            div = ''
            try:
                div = driver.find_element_by_class_name('capituloView')
                print('Identificando imagens do capitulo {}'.format(capitulo))
            except Exception:
                print('Cool down, acho que estou indo rápido demais')
                time.sleep(60)
                print('Okay, vamos tentar de novo!')
                ir_para(link, driver)
                div = driver.find_element_by_class_name('capituloView')


            divs_paginas = div.find_elements_by_class_name('capituloViewBox')

            numero = len(divs_paginas)
            url = driver.find_element_by_xpath('//img[@data-id-image=1]').get_attribute('src')

            img_links = url_tracker(url, numero)

            capitulo_vector[capitulo] = img_links
    return capitulo_vector
#   Essa função ficou um pouco mais geral, dado onde se deve baixar, o nome e o link das imagens ela vai baixar corretamente
def baixar_capitulo(path, capitulo, imgs_link, driver):
    imgs = []
    capitulo += '.pdf'
    progress = '-'
    print('Baixando {}'.format(capitulo))
    for img in imgs_link:
        series = img.split('/')
        if img == imgs_link[0]:
            print(series[-2])
        temp = os.path.join('.temp', series[-2] + '-' + series[-1])
        response =  requests.get(img)
        if response.status_code == requests.codes.OK:
            with open(temp, 'wb') as arquivo:
                arquivo.write(response.content)
            imgs.append(Image.open(temp))
            progress += '-'
            print(progress)
        else:
            print('Não foi possível encontrar a página {} do capítulo {}'.format(series[-1], capitulo))
            print(response.status_code)
            print('Tentando novamente...')
            time.sleep(4*WAIT_TIME)
            response =  requests.get(img)
            ir_para(img, driver)
            if response.status_code == requests.codes.OK:
                with open(temp, 'wb') as arquivo:
                    arquivo.write(response.content)
                imgs.append(Image.open(temp))
                progress += '-'
                print(progress)
            else:
                print('Vai dar certo')
                time.sleep(4*WAIT_TIME)
                response =  requests.get(img)
                ir_para(img, driver)
                if response.status_code == requests.codes.OK:
                    with open(temp, 'wb') as arquivo:
                        arquivo.write(response.content)
                    imgs.append(Image.open(temp))
                    progress += '-'
                    print(progress)
                else:
                    print("\033[1;31;40m Não deu mesmo \n")

    progress += '!'
    first = imgs[0]
    imgs.pop(0 )
    first.save(os.path.join(path, capitulo),save_all=True,append_images=imgs)
    print(progress)
    print('Capítulo {} baixado :)'.format(capitulo))
    clear_temp()
    return 'Okay... Próximo!'
#   Lógica de ajuda ao os.path e também serve para criar pastas de mangas
def create_path(manga):
    destino = os.path.join('output',manga)
    if not os.path.exists(destino):
        os.mkdir(destino)
    return destino

def super_goiabas(url, inicio,fim, driver):
    # formatação do nome do mangá, pode mudar de site para site
    manga = driver.title.replace('Manga ', '')
    print('Nome do mangá: {}'.format(manga))

    print('Okay, agora vou procurar o intervalo {}...{}'.format(inicio, fim))
    lista_de_conteudos = buscar_elementos('listaDeConteudo', driver, 'goiaba')
    capitulos = busca_capitulos(lista_de_conteudos, 'goiaba')

    while (existem_mais_capitulos(capitulos, driver, inicio)):
        lista_de_conteudos = buscar_elementos('listaDeConteudo', driver, 'goiaba')
        capitulos = busca_capitulos(lista_de_conteudos, 'goiaba' , capitulos)

    #capitulos_vector = abrir_capitulos(capitulos,driver, inicio, fim)
    #print(capitulos_vector)
    #Caminho para onde os mangás devem ser baixados
    path = create_path(manga)
    print('Vou guardar esses capitulos em {}'.format(path))

    #   Não gosto dessa parte do código, pois não está de acordo com o DRY, e a lógica não está bem abstraida
    for capitulo_id, link in capitulos.items():
        t_inicio = datetime.now()
        if fim == -1:
            fim = len(capitulos)
        # se o capítulo está dentro do intervalo
        if (inicio<= int(capitulo_id.split('.')[0]) <= fim ):
            img_links = abrir_capitulo(capitulo_id, link, driver)
            baixar_capitulo(path, capitulo_id, img_links, driver)
        t_fim = datetime.now()
        delta = t_fim - t_inicio
        print('Tempo de download {}'.format(delta))
    #Essa lógica pode tomar um pouco do rendimento do programa, pois o programa só começa a baixar depois de passar por todas as páginas...
    #for mangas, links in capitulos_vector.items():
    #    baixar_capitulo(path,mangas,links)

def verificar_origem(url):
    if(url.startswith('https://supermangas.site/')):
        return 'goiaba'
    if(url.startswith('https://readmanganato.com/')):
        return 'nato'
    else:
        print('Url ainda não suportada');
        exit(0)

def supernatural(url, inicio, fim ,driver):
    lista_de_conteudos = buscar_elementos('row-content-chapter', driver, 'nato')
    capitulos = busca_capitulos(lista_de_conteudos, 'nato')
    print(capitulos)

    print(len(capitulos))
    #titles, link = capitulos.items()
    #print(titles[332])
    print(tuple(capitulos.items()))

    
    #path = create_path(driver.title)
    #print('Vou guardar esses capitulos em {}'.format(path))

#execução do algonritmo
if __name__ == '__main__':
    #Verificando se a PATH_PARA_WEBDRIVER está preenchida com algo
    if(PATH_PARA_WEBDRIVER == ''):
        exit('ERRO: Você não definiu o PATH para o WEBDRIVER de seu browser no mangadownloader.py')

    #Recebendo as informações do terminal
    url = sys.argv[1]
    inicio = 1
    fim = -1
    #tratamento de erros caso algum valor não seja digitado
    try:
        inicio =  int(sys.argv[2])
    except Exception:
        inicio = 1
    try:
        fim = int(sys.argv[3])
    except Exception:
        print('O fim não está bem definido então vou baixar todos que encontrar')

    metodo = verificar_origem(url)

    #instânciando o webdriver
    driver = webdriver.Chrome(PATH_PARA_WEBDRIVER)

    #entrando na página inicial do mangá
    ir_para(url, driver)
    print('Escolha o idioma na página em 10 segundos ...')
    time.sleep(10)
    if metodo == "goiaba":
        super_goiabas(url, inicio, fim, driver)
    if metodo == "nato":
        supernatural(url, inicio, fim, driver)
    #cowsay

    driver.close()
    print(' ____________________________________')
    print('/ tudo vai bem quanto termina bem... \\')
    print('\ Aproveite seus mangás              /')
    print(' ------------------------------------')
    print('        \   ^__^')
    print('         \  (oo)\_______')
    print('            (__)\       )\/\\')
    print('                ||----w |')
    print('                ||     ||')
