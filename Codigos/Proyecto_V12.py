#Importar la libreria selenium
#!pip install selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
#Importar la libreria Webdriver para descargar la ultima version del driver
#!pip install webdriver-manager
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#Excepciones
from selenium.common.exceptions import NoSuchElementException
#Libreria para generar delays
import time 

from lxml import html

class Amazon():
    """Intento de instancia de Web Scrapping de Amazon"""
    #Init Method
    def __init__(self):
        #Inicializa el buscador
        self.driver=webdriver.Chrome(ChromeDriverManager().install())
        #Lista de atributos de los articulos
        self.ListaTitulo=[]
        self.ListaPrecio=[]
        #Inicializacion de los metodos
        self.Busqueda()
        self.CantidadArticulos()
        self.TituloArticulo()
        #self.PrecioArticulo()
        self.Cerrar()
    #Search Bar
    def Busqueda(self):
        self.driver.maximize_window()        #Maximiza ventana
        self.driver.get("http://amazon.com") #Dirige a la URL
        time.sleep(1)                        #Espera de 1 seg
        #Dirige hacia el xpath de la busqueda del nombre del articulo
        #Algunas veces sale otro buscador
        self.busqueda=self.driver.find_element(By.XPATH,'//*[@id="twotabsearchtextbox"]')   
        self.busqueda.send_keys("keyboard",Keys.ENTER) #ingresa "keyboard" y ENTER
        time.sleep(1)                        #Espera de 1 seg
    def CantidadArticulos(self):
        self.cantidad=0
        self.tree=html.fromstring(self.driver.page_source)  
        #self.valores=self.tree.xpath('.//div[contains(@data-cel-widget,"search_result_")]')
        self.valores=self.tree.xpath('.//div[contains(@data-asin,"B0")]')
        
        for i in range(len(self.valores)):
            print(self.valores[i].xpath('.//span[@class="a-size-medium a-color-base a-text-normal"]/text()'))
            if(self.valores[i].xpath('.//span[@class="a-size-medium a-color-base a-text-normal"]/text()')!=[]):
                self.cantidad+=1
        time.sleep(2)
    #Get Article ID
    def TituloArticulo(self):
        self.contador=0
        self.i=0
        while (self.contador<self.cantidad):
            #Dirige hacia el xpath del primer articulo
            try:
                self.articulo=self.driver.find_element(By.XPATH,'//*[@id="search"]/div[1]/div[1]/div/span[3]/div[2]/div['+str(2+self.i)+']/div/div/div/div/div/div/div/div[2]/div/div/div[1]/h2/a/span') 
                #self.articulo=WebDriverWait(self.driver,10).until(EC.presence_of_element_located((By.XPATH,'//*[@id="search"]/div[1]/div[1]/div/span[3]/div[2]/div['+str(2+self.i)+']/div/div/div/div/div/div/div/div[2]/div/div/div[1]/h2/a/span')))
            except NoSuchElementException:
                try:
                    self.articulo=self.driver.find_element(By.XPATH,'//*[@id="search"]/div[1]/div[1]/div/span[3]/div[2]/div['+str(2+self.i)+']/div/div/div/div/div/div[2]/div/div/div[1]/h2/a/span')
                    #self.articulo=WebDriverWait(self.driver,10).until(EC.presence_of_element_located((By.XPATH,'//*[@id="search"]/div[1]/div[1]/div/span[3]/div[2]/div['+str(2+self.i)+']/div/div/div/div/div/div[2]/div/div/div[1]/h2/a/span')))
                except NoSuchElementException:
                    self.i+=1
                    continue
            #Obtiene el titulo del articulo
            time.sleep(1)
            self.articulo.click()                #Hace click en el primer articulo
            
            try:
                self.precio=self.driver.find_element(By.XPATH,'//*[@id="corePrice_desktop"]/div/table/tbody/tr/td[2]/span[1]/span[2]')   
                
            except NoSuchElementException:
                try: 
                    self.precio=self.driver.find_element(By.XPATH,'//*[@id="olp_feature_div"]/div[2]/span/a/span[2]')
                    #self.TituloPrecio=self.precio.get_attribute("innerHTML")
                except NoSuchElementException:
                    self.TituloPrecio=''
      
            self.TituloPrecio=self.precio.get_attribute("innerHTML")
            self.titulo=self.driver.find_element(By.XPATH,'//*[@id="productTitle"]')   
            self.TituloArticulo=self.titulo.get_attribute("innerHTML").splitlines()[0]
            self.i+=1
            self.contador+=1  
            time.sleep(1)
            print('cantidad: ',self.cantidad)
            print(self.contador)
            self.driver.back()
            time.sleep(2)

    #Get Article Price
    def PrecioArticulo(self):   
        #Dirige hacia el xpath del precio del primer articulo                 
        self.precio=self.driver.find_element_by_xpath('//*[@id="corePrice_feature_div"]/div/span/span[2]')   
        #Obtiene el precio del primer articulo
        self.TituloPrecio=self.precio.get_attribute("innerHTML")
        time.sleep(2)
    #Close the browser
    def Cerrar(self):
        self.driver.close()                  #Cierra el buscador

if __name__=='__main__':
    Prueba=Amazon()