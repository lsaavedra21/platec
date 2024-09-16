from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from selenium.webdriver.common.action_chains import ActionChains
import time
import os
import xlwings as xw
import pyautogui
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import sys

# Defina o número máximo de tentativas de reinicialização
max_tentativas = 6
tentativas = 0

while tentativas < max_tentativas:
    try:
        # Abrir Chrome
        driver = webdriver.Chrome()
        driver.get('https://grouperenault.sharepoint.com/sites/generalmaintenance--brazil/Shared%20Documents/Forms/AllItems.aspx')
        sleep(15)

        # Clicar em pesquisa
        elemento_pesquisa = driver.find_element(By.XPATH, "//*[@id='O365_SearchBoxContainer_container']/div/div")
        elemento_pesquisa.click()
        sleep(3)

        elemento_pesquisa = driver.find_element(By.XPATH, "//*[@id='sbcId']/form/input")
        elemento_pesquisa.send_keys("Fechamento GERAL - Dashboards 2023 Teste.xlsx")

        # Enviar a pesquisa (pressionar Enter)
        elemento_pesquisa.send_keys(Keys.RETURN)
        sleep(10)

        # clicar no arquivo xlsx
        elemento_arquivo = driver.find_element(By.XPATH, '//button[text()="Fechamento GERAL - Dashboards 2023 Teste.xlsx"]')
        action_chains = ActionChains(driver)
        action_chains.context_click(elemento_arquivo).perform()
        sleep(5)

        # Clicar no Abrir
        elemento_abrir = driver.find_element(By.XPATH, "//i[@data-icon-name='ChevronRight']")
        elemento_abrir.click()
        sleep(3)

        elemento_aplicativo = driver.find_element(By.XPATH, "//div[contains(@class, 'contextualMenuItemLinkContent_d20e3f44') and span[text()='Abrir no aplicativo']]")
        elemento_aplicativo.click()
        sleep(20)

        # Permitir abrir excel
        pyautogui.press('left')
        sleep(2)
        pyautogui.press('enter')
        sleep(10)

        driver.quit()

        # Abrir Chrome
        driver = webdriver.Chrome()
        driver.get('https://spotfire-m8.abi.int.gcp.renault.com/spotfire/wp/analysis?file=/MGD/OPE/TCR/BOTH/REPORT_PUBLISHED/ACR_PROD_GCP&waid=lnGCGDieCkaBhGg5RthqC-29010058d81ndG&wavid=0')
        sleep(15)

        # Clicar em login IDP
        elemento = driver.find_element(By.XPATH, "//span[@class='tss-provider-link-label ng-binding' and text()='IDP-Renault']")
        elemento.click()
        sleep(20)

        # CLicar Iniciar Sessao
        elemento2 = driver.find_element(By.XPATH, "//span[@class='nam-signin-but action-but' and text()='Iniciar sessão']")
        elemento2.click()
        sleep(90)

        # Clicar em Reload Date Filter
        elemento_data = driver.find_element(By.XPATH, '//*[@id="e905107f4e6c4aa2be103200ae0385aa"]')
        elemento_data.click()
        sleep(30)

        # Clicar em Rawdata
        elemento_raw = driver.find_element(By.XPATH, "/html/body/div/div[2]/div/div[1]/div/div/div[2]/div/div/div/div/div/div/div/div/div[5]/div/div[1]/div[1]/span/p[9]/a")
        elemento_raw.click()
        sleep(20)

        # Clicar em Bak
        elemento_bak = driver.find_element(By.XPATH, '//*[@id="id114"]/div[3]/div[1]/div/div[1]/div[1]')
        elemento_bak.click()
        sleep(50)

        # Tirar marcações de Usinas
        elemento_usina = driver.find_element(By.XPATH, '//div[@class="sf-element-list-box-item" and @title="(Todos) 19 valores"]')
        elemento_usina.click()
        sleep(20)

        # Marcar CVP
        elemento_CVP = driver.find_element(By.XPATH, '//div[@class="sf-element-list-box-item" and @title="CVP"]')
        elemento_CVP.click()
        sleep(20)

        # Selecionar CVU
        elemento_CVU = driver.find_element(By.XPATH, '//div[@class="sf-element-list-box-item" and @title="CVU"]')
        elemento_CVU.click()
        sleep(20)

        # Clicar com botao direito para exportar
        botao_direito = driver.find_element(By.XPATH, '//*[@id="id88"]')
        actions = ActionChains(driver)
        actions.context_click(botao_direito).perform()
        sleep(20)

        # Clicar em Exportar
        elemento_exportar = driver.find_element(By.XPATH, '//div[@class="contextMenuItemLabel" and @title="Exportar"]')
        elemento_exportar.click()
        sleep(5)

        elemento_tabela = driver.find_element(By.XPATH, '//div[@class="contextMenuItemLabel" and @title="Exportar tabela"]')
        elemento_tabela.click()
        sleep(10)
        pyautogui.hotkey("Alt", "F4")
        time.sleep(10)

        # O caminho para o diretório de downloads onde o arquivo Excel foi baixado
        caminho_download = "C:\\Users\\pm22885\\Downloads"
        time.sleep(10)

        # Liste todos os arquivos no diretório de downloads
        arquivos = os.listdir(caminho_download)

        # Liste todos os arquivos no diretório de downloads e ordene-os por data de modificação
        arquivos = os.listdir(caminho_download)
        arquivos = [os.path.join(caminho_download, arquivo) for arquivo in arquivos]
        arquivos = [arquivo for arquivo in arquivos if arquivo.endswith(".csv")]
        arquivos.sort(key=os.path.getmtime, reverse=True)  # Ordenar por data de modificação, o último será o primeiro

        # Encontre o arquivo Excel baixado (você pode ajustar essa parte para corresponder ao nome do arquivo)
        arquivo_excel = None
        for arquivo in arquivos:
            if arquivo.endswith(".csv"):  # Verifique a extensão do arquivo
                arquivo_excel = arquivo
                break

        # Verifique se encontrou o arquivo Excel
        if arquivo_excel:
            caminho_arquivo_excel = os.path.join(caminho_download, arquivo_excel)

            # Abra o arquivo Excel
            os.system(f'start excel "{caminho_arquivo_excel}"')
        else:
            print("Arquivo Excel não encontrado no diretório de downloads.")
        time.sleep(10)

        # O caminho para o diretório de downloads onde o arquivo Excel foi baixado
        caminho_download = "C:\\Users\\pm22885\\Downloads\\AUTO-RGU"
        time.sleep(10)

        # Liste todos os arquivos no diretório de downloads
        arquivos = os.listdir(caminho_download)

        # Liste todos os arquivos no diretório de downloads e ordene-os por data de modificação
        arquivos = os.listdir(caminho_download)
        arquivos = [os.path.join(caminho_download, arquivo) for arquivo in arquivos]
        arquivos = [arquivo for arquivo in arquivos if arquivo.endswith(".xlsm")]
        arquivos.sort(key=os.path.getmtime, reverse=True)  # Ordenar por data de modificação, o último será o primeiro

        # Encontre o arquivo Excel baixado (você pode ajustar essa parte para corresponder ao nome do arquivo)
        arquivo_excel = None
        for arquivo in arquivos:
            if arquivo.endswith(".xlsm"):  # Verifique a extensão do arquivo
                arquivo_excel = arquivo
                break

        # Verifique se encontrou o arquivo Excel
        if arquivo_excel:
            caminho_arquivo_excel = os.path.join(caminho_download, arquivo_excel)

            # Abra o arquivo Excel
            os.system(f'start excel "{caminho_arquivo_excel}"')
        else:
            print("Arquivo Excel não encontrado no diretório de downloads.")
        time.sleep(10)

        # Abra o Excel
        wb = xw.books.active

        # Agora, você pode executar a macro usando o atalho do teclado
        pyautogui.hotkey("Alt", "F8")  # Abre a caixa de diálogo "Macro"
        time.sleep(2)  # Aguarde um pouco para a caixa de diálogo abrir

        # Digite o nome da macro (substitua 'SuaMacro' pelo nome real da sua macro)
        pyautogui.write("Buscardata")

        # Pressione Enter para executar a macro
        pyautogui.press("Enter")
        time.sleep(30)

        # Fechar o Excel
        pyautogui.hotkey("Alt", "F4")
        time.sleep(20)

        # Caminho para a pasta onde os arquivos devem ser excluídos
        pasta_exclusao = "C:\\Users\\pm22885\\Downloads"

        # Lista dos nomes dos arquivos que devem ser excluídos
        arquivos_para_excluir = [
            "ACR_PROD_GCP - 22 colunas de bak.csv",
        ]

        # Excluir os arquivos da pasta
        for arquivo in arquivos_para_excluir:
            caminho_arquivo = os.path.join(pasta_exclusao, arquivo)
            if os.path.exists(caminho_arquivo):
                os.remove(caminho_arquivo)
            else:
                print(f"O arquivo {arquivo} não foi encontrado na pasta de exclusão.")

        # Se tudo funcionar sem erros, saia do loop
        break
    except NoSuchElementException as e:
        # Capturar exceção quando um elemento não for encontrado
        print(f"Erro: {e}")
        print("Reiniciando o processo...")

        # Coloque aqui o código para reabrir o Chrome e retomar o processo desde o início
        driver.quit()
        tentativas += 1
else:
    print("Número máximo de tentativas atingido. O processo foi interrompido.")

sys.exit(0)