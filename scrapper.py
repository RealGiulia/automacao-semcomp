
"""This files implements the scarapper to get financial info"""
import pandas as pd

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.expected_conditions import visibility_of_element_located as visibility
from selenium.webdriver.common.keys import Keys


# Configurando o driver
# options = Options()
# options.binary_location = r'C:\Program Files\Mozilla Firefox\firefox.exe'
driver = webdriver.Firefox(executable_path=r'geckodriver.exe')
driver.get('https://03felipesampaio.github.io')

xpath_login_box = r'//*[@id="usuario"]'
login_box = driver.find_element("xpath",xpath_login_box)
login_box.click()

usuario = 'giulia@gmail.com'
login_box.send_keys(usuario)

xpath_senha = r'//*[@id="senha"]'
caixa_senha =  driver.find_element("xpath", xpath_senha)
caixa_senha.click()

caixa_senha.send_keys('senha')

# Clicando no 'enter':
xpath_enter = r'//*[@id="btn-entrar"]'
enter = driver.find_element("xpath", xpath_enter)
enter.click()

# Captando o saldo:
saldo_xpath = r'/html/body/div[1]/div[1]/p'
saldo = driver.find_element("xpath", saldo_xpath).text
print("Saldo: %s" %saldo)

# Filtrando as transações por mês:
periodo_xpath = r'//*[@id="periodo"]'
dropdown_element = driver.find_element("xpath",periodo_xpath)
dropdown_element.click()
periodo = Select(dropdown_element)
periodo.select_by_visible_text("Mês atual")

#Captando as linhas da tabelas:
linhas = driver.find_elements("xpath","/html/body/div[2]/table/tbody/tr")
tamanho_tabela = len(linhas)

# Obtendo as colunas da tabela
cols = []
for i in range(1,4):
	xpath_col = r'/html/body/div[2]/table/tbody/tr[1]/th[{}]'
	xpath_col = xpath_col.format(i)
	conteudo_celula = driver.find_element("xpath",xpath_col)
	conteudo_celula = conteudo_celula.text
	cols.append(conteudo_celula)

# Obtendo as linhas da tabela
conteudo_linhas = []
for linha in linhas:
    for i in range(2, tamanho_tabela+1):
        celulas_linha = []
        for x in range(1,4):
            xpath_celula = '/html/body/div[2]/table/tbody/tr[{}]/td[{}]'
            xpath_celula = xpath_celula.format(i,x)
            conteudo_celula = driver.find_element("xpath",xpath_celula)
            conteudo =  conteudo_celula.text
            celulas_linha.append(conteudo)
        conteudo_linhas.append(celulas_linha)

# Inserindo os dados da tabela no arquivo csv
data = pd.DataFrame(conteudo_linhas)
data_csv = data.to_csv('transacoes.csv',header=cols,index=False)

# Fechando o driver
driver.quit()
