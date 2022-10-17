from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium import webdriver
import os
import pandas as pd
import logging
import time
import json
import pyautogui as pyg

def verificarPausa():
    while True:
        try:
            os.chdir(diretorio_robo)
            with open("pause.json", "r") as infile:
                parametros = json.load(infile)
            if parametros["statuspausa"]:
                time.sleep(2)
                print("Robô em pausa")
            else:
                break
        except:
            time.sleep(2)
            print('verificar')
            pass

def carregarParametros():
    with open("parametros.json", "r") as infile:
        parametros = json.load(infile)
    return parametros

def apagarCSVs():
    os.chdir(r'C:\\Users\\'+ user_name +'\\Downloads')
    try:
        nomesDosArquivos = [nomesDosArquivos for nomesDosArquivos in os.listdir() if ('.csv' in nomesDosArquivos) and ('.part' not in nomesDosArquivos)]
        print('Pasta de download limpa.')
        for arquivo in nomesDosArquivos:
            os.remove(arquivo)
        os.chdir(diretorio_robo)
    except IndexError:
        pass
    except Exception as e:
        logging.debug('Erro na funcao apagarCSVs - ' + str(e))

def gerarLinkTMS():
    data_15 = time.strftime('%Y-%m-%d',time.gmtime(time.time()-(60*60*17)))
    h_15 = time.strftime('%H',time.gmtime(time.time()-(60*60*17)))
    data_hoje = time.strftime('%Y-%m-%d',time.gmtime(time.time()))
    hora_hoje = time.strftime('%H',time.gmtime(time.time()))
    minuto, segundo = time.strftime('%M',time.gmtime(time.time())),time.strftime('%S',time.gmtime(time.time()))
    IncludedAtDateStart = data_15 + 'T' + h_15 + '%3A' + minuto + '%3A' + segundo + 'Z'
    IncludedAtDateEnd = data_hoje + 'T' + hora_hoje + '%3A' + minuto + '%3A' + segundo + 'Z'
    getLink = 'https://tms.mercadolivre.com.br/packages/list?inboundIncludedAtDateStart=' + IncludedAtDateStart + '&inboundIncludedAtDateEnd=' + IncludedAtDateEnd + '&columnSort=shipment_id&orderSort=asc&page=1&limit=10'
    return getLink

def moverArquivos():
    os.chdir(f'C:\\Users\\{user_name}\\Downloads')
    nomeDoArquivo = [nomeDoArquivo for nomeDoArquivo in os.listdir() if ('.csv' in nomeDoArquivo) and ('.part' not in nomeDoArquivo)][0]
    os.replace(f'C:\\Users\\{user_name}\\Downloads\\{nomeDoArquivo}',f'{diretorio_robo}\\{nomeDoArquivo}')
    os.chdir(f'{diretorio_robo}')
    print(f'Arquivo {nomeDoArquivo} movido!')

def locateComDelay(caminho,delay):
    while True:
        try:
            time.sleep(delay)
            imagem = pyg.locateOnScreen(caminho, confidence=0.7, grayscale=True)
            if imagem == None:
                print(imagem)
            else:
                pyg.click(imagem)
                print(imagem)
                break
        except Exception as e:
            # print(e)
            pass

def publicarPowerBI():
    locateComDelay(r'C:\Users\vdiassob\Desktop\Python\robo-atualizacao-expedicao\screenshots\publicar.png',1)
    locateComDelay(r'C:\Users\vdiassob\Desktop\Python\robo-atualizacao-expedicao\screenshots\salvar.png',1)
    locateComDelay(r'C:\Users\vdiassob\Desktop\Python\robo-atualizacao-expedicao\screenshots\pesquisar.png',1)

def funcao_principal():
    apagarCSVs()
    logging.debug('Robô iniciado')
    while True:
        try:
            verificarPausa()
            driver.get(gerarLinkTMS())
            time.sleep(int(carregarParametros()["delayclicweb"]))
            driver.find_element(By.XPATH,'/html/body/main/div/div/div[2]/div/div/div/div/div[3]/div/div[2]/ul[2]/li[2]/a').click()
            moverArquivos()
            driver2.get(carregarParametros()["linkdolooker"])
            driver2.refresh()
            time.sleep(int(carregarParametros()["delayclicweb"]))
            driver2.find_element(By.ID,'dashboard-layout-wrapper').click()
            time.sleep(int(carregarParametros()["delayclicweb"]))
            driver2.find_element(By.XPATH,'/html/body/div[2]/div/div/div/div/section/div/div[2]/div[1]/div/div[2]/div/section/div/div[1]/div/button[1]/div[2]').click()
            time.sleep(int(carregarParametros()["delayclicweb"]))
            driver2.find_element(By.XPATH,'/html/body/div[3]/div/div/div/div/div/ul/li[2]/button').click()
            time.sleep(int(carregarParametros()["delayclicweb"]))
            driver2.find_element(By.XPATH,'/html/body/div[3]/div/div/div[2]/footer/div[1]/button[1]').click()
            moverArquivos()
            print(f'Pausa para acompanhamento. ({carregarParametros()["delayacompanhamento"]} min)')
            time.sleep(60*int(carregarParametros()["delayacompanhamento"]))
        except Exception as e:
            logging.debug('Erro na função funcao_principal - ' + str(e))
            print('Não foi possível completar processo de download.')
            pass

publicarPowerBI()
# user_name = os.getlogin()
# diretorio_robo = os.getcwd()

# log_filename_start = os.getcwd() + '\\Logs\\' + time.strftime('%d_%m_%Y %H_%M_%S') + '.log'
# logging.basicConfig(filename=log_filename_start, level=logging.DEBUG, format='%(asctime)s, %(message)s',datefmt='%m/%d/%Y %H:%M:%S')

# options = Options()
# options.set_preference('network.proxy.type',0)
# options.binary_location = carregarParametros()["caminhonavegador"]

# driver = webdriver.Firefox(options=options)
# driver2 = webdriver.Firefox(options=options)
# driver.get('https://tms.mercadolivre.com.br/')
# driver2.get(carregarParametros()["linkdolooker"])

# os.system('pause')
# time.sleep(3)
# moverArquivos()

# funcao_principal()