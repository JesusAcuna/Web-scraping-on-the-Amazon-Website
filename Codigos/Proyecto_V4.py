#Importar la libreria selenium
#!pip install selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
#Importar la libreria Webdriver para descargar la ultima version del driver
#!pip install webdriver-manager
from webdriver_manager.chrome import ChromeDriverManager
#Libreria para generar delays
import time 


class Amazon():
    """Intento de instancia de Web Scrapping de Amazon"""
    #Init Method
    def __init__(self):
        #Inicializa el buscador
        self.driver=webdriver.Chrome(ChromeDriverManager().install())    
        #Inicializacion de los metodos
        self.Busqueda()
        self.Articulo()
        self.Precio()
        self.Cerrar()
    #Search Bar
    def Busqueda(self):
        self.driver.maximize_window()        #Maximiza ventana
        self.driver.get("http://amazon.com") #Dirige a la URL
        time.sleep(1)                        #Espera de 1 seg
        #Dirige hacia el xpath de la busqueda del nombre del articulo
        self.busqueda=self.driver.find_element_by_xpath('//*[@id="twotabsearchtextbox"]')   
        self.busqueda.send_keys("keyboard",Keys.ENTER) #ingresa "keyboard" y ENTER
        time.sleep(1)                        #Espera de 1 seg
    #Get Article ID
    def Articulo(self):
        #Dirige hacia el xpath del primer articulo
        self.articulo=self.driver.find_element_by_xpath('//*[@id="search"]/div[1]/div[1]/div/span[3]/div[2]/div[2]/div/div/div/div/div/div/div/div[2]/div/div/div[1]/h2/a/span')   
        #Obtiene el titulo del articulo
        self.TituloArticulo=self.articulo.get_attribute("innerHTML").splitlines()[0]
        self.articulo.click()                #Hace click en el primer articulo
        time.sleep(2)    
    #Get Article Price
    def Precio(self):   
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