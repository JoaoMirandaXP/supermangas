import sys
import time
import os
from selenium import webdriver
from PIL import Image
import requests


#unidade do tempo de espera entre requisições para evitar bugs, em segundos, para conexão lenta usar 2 seg
WAIT_TIME = .75
#Coloque aqui o caminho para o seu webdriver selenium, atenção, ele deve estar na mesma versão do seu chrome
PATH_PARA_WEBDRIVER = 'INSIRA AQUI'


#   função de limpeza da pasta temp, pode não ser sempre necessária
#   mas considere o seguinte, o capitulo seguinte a esse tem menos páginas
#   de tal modo o pŕoximo será renderizado com a mesma quantidade de páginas do atual
#   e a páginas a mais serão renderizadas também
def clear_temp():
    for x in os.listdir('.temp'):
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
def buscar_elementos(elemento, driver):
    elementos = driver.find_element_by_id(elemento)
    time.sleep(2*WAIT_TIME)
    return elementos
#   pode ser útil ao ter que selecionar uma língua de preferência, se houver para o mangá
def busca_capitulos(elemento, capitulos = {}):
    divs = []
    try:
        divs = elemento.find_elements_by_class_name('boxTop10')
    except Exception:
        print('Cool Down, acho que estou indo rápido demais')
        time.sleep(10*WAIT_TIME)
        divs = elemento.find_element_by_class_name('boxTop10')
    #divs = []
    #for d in elemento.find_elements_by_class_name('boxTop10'):
    #    try:
    #        d.find_element_by_xpath('//img[@alt="Inglês"]')
    #    except Exception:
    #        divs.append(d)
    for div in divs:
        chapter=div.find_element_by_class_name('top10Link')
        link = chapter.find_element_by_tag_name('a').get_attribute('href')
        number = chapter.find_element_by_tag_name('span').text
        capitulos[number] = link
    return capitulos
#   Apenas como simplificação dos comandos para selenium, funciona como um simplficador da clausula if dentro da execução
#   veriicando se existem mais capítulos a adicionados ao grande dicionário associando todos os links aos seus respectivos capitulos
def existem_mais_capitulos(capitulos, driver, ate = 1):
    time.sleep(4*WAIT_TIME)
    if ate in capitulos:
        print('Finalizamos a busca pelos capitulos')
        return False
    else:
        print('Vamos para a próxima página')
        driver.find_element_by_xpath('//button[@title="Próxima Página"]').click()
        #print('Vamos para a página anterior')
        #driver.find_element_by_xpath('//button[@title="Página Anterior"]').click()
        return True
#   É o tempero específico para esse site, mas pode funcionar para vários outros, já que esse usa a estratégia de deixar imagens vazias
#   Para evitar o webscrapping, então utilizamos apenas a primeira url que nesse caso será fixa
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
#   É uma fundionalidade a ser melhorada, afinal essa é a parte que se faz uma lista brutal com todos os capítulos vinculados a todos os links da suas respectivas imagens
def abrir_capitulos(capitulos, driver):
    capitulo_vector = {}
    for capitulo, link in capitulos.items():
        
        ir_para(link, driver)
        div = ''
        try:
            div = driver.find_element_by_class_name('capituloView')
            print('Identificando imagens do capitulo {}'.format(capitulo))
        except Exception:
            print('Cool down, adcho que estou indo rápido demais')
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
def baixar_capitulo(path, capitulo, imgs_link):
    imgs = []
    capitulo += '.pdf'
    progress = '-'
    for img in imgs_link:
        series = img.split('/')
        print(series[-2])
        temp = os.path.join('.temp', series[-2] + '-' + series[-1]+ '.jpg') 
        response =  requests.get(img)
        #if respectivos.status_code == requests.codes.OK:
        #    with open(temp, 'wb') as arquivo:
        #        arquivo.write(response.content)
        #    imgs.append(Image.open(temp))
        #    progress += '-'
        #else :
        #    time.sleep(60*WAIT_TIME)
        #    with open(temp, 'wb') as arquivo:
        #        arquivo.write(response.content)
        #    imgs.append(Image.open(temp))
        with open(temp, 'wb') as arquivo:
            arquivo.write(response.content)
        imgs.append(Image.open(temp))
        progress += '-'
        print(progress)
    progress += '!'
    first = imgs[0]
    imgs.pop(0 ) 
    first.save(os.path.join(path, capitulo),save_all=True,append_images=imgs)
    print('Capítulo {} baixado :)'.format(capitulo))
    print(progress)
    clear_temp()
    return 'Okay... Próximo!'
#   Lógica de ajuda ao os.path e também serve para criar pastas de mangas
def create_path(manga):
    destino = os.path.join('output',manga)
    if not os.path.exists(destino):
        os.mkdir(destino)
    return destino 
def baixar_intervalo(capitulos_vector,path, inicio, fim):
    if fim == -1:
        fim = len(capitulos_vector)
    for capitulo, imgs_link in capitulos_vector.items():
        if (inicio<=int(capitulo)<=fim):
            resultado = baixar_capitulo(path, capitulo, imgs_link)
            print(resultado)
#execução do algonritmo
if __name__ == '__main__':
    
    url = sys.argv[1]
    inicio = 1
    fim = -1
    try:
        inicio =  int(sys.argv[2])
    except Exception:
        inicio = 1
    try:
        fim = int(sys.argv[3])
    except Exception:
        print('O fim não está bem definido então vou baixar todos que encontrar')
        
    driver = webdriver.Chrome(PATH_PARA_WEBDRIVER)
    ir_para(url, driver)
    manga = driver.title.replace('Manga ', '')
    print('Nome do mangá: {}'.format(manga))

    print('Escolha o idioma na página em 10 segundos ...')
    time.sleep(10)
    
    lista_de_conteudos = buscar_elementos('listaDeConteudo', driver)
    capitulos = busca_capitulos(lista_de_conteudos)
    
    while (existem_mais_capitulos(capitulos, driver, ate)):
        lista_de_conteudos = buscar_elementos('listaDeConteudo', driver)
        capitulos = busca_capitulos(lista_de_conteudos, capitulos)
    #print(capitulos)
    capitulos_vector = abrir_capitulos(capitulos,driver)
    print(capitulos_vector)
    path = create_path(manga)
    print('Vou guardar esses capitulos em {}'.format(path))
    driver.close()
    baixar_intervalo(capitulos_vector, path,inicio, fim)
