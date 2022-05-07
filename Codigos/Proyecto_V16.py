#Importar la libreria selenium
#!pip install selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
#Importar la libreria Webdriver para descargar la ultima version del driver
#!pip install webdriver-manager
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#Excepciones
from selenium.common.exceptions import NoSuchElementException
#Libreria para generar delays
import time 
import pandas as pd

from lxml import html

class Amazon():
    """Intento de instancia de Web Scrapping de Amazon"""
    #Init Method
    def __init__(self):
        #Inicializa el buscador
        self.driver=webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        #Lista de atributos de los articulos
        self.ListaTitulo=[]
        self.ListaPrecio=[]
        #Inicializacion de los metodos
        self.Busqueda()
        self.CantidadArticulos()
        self.CantidadPaginas()
        self.DataArticulo()
        self.Cerrar()
        self.DataFrame()
    #Search Bar
    def Busqueda(self):
        self.driver.maximize_window()        #Maximiza ventana
        #Algunas veces sale otro buscador
        self.driver.get("http://amazon.com") #Dirige a la URL
        time.sleep(1)                        #Espera de 1 seg
        #Dirige hacia el xpath de la busqueda del nombre del articulo
        self.busqueda=self.driver.find_element(By.XPATH,'//*[@id="twotabsearchtextbox"]')   
        self.busqueda.send_keys("keyboard",Keys.ENTER) #ingresa "keyboard" y ENTER
        time.sleep(1)                        #Espera de 1 seg
    #Number of Articles
    def CantidadArticulos(self):
        self.cantidadArticulos=0
        #Calcula el directorio de la ubcacion actual del driver(pagina de "keyboard")
        self.tree=html.fromstring(self.driver.page_source)  
        #Encuentra valores(LISTA) que contengan el atributo @data-asin="B0....."
        self.valores=self.tree.xpath('//div[contains(@data-asin,"B0")]')
        #Hay algunos valores que son [], por lo que se ceunta aquellos que tengan valor !=[]
        print("********************* Titulo de los Articulos ******************")
        for i in range(len(self.valores)):
            #self.tree
            if(self.valores[i].xpath('.//span[@class="a-size-medium a-color-base a-text-normal"]/text()')!=[]):
                print(self.valores[i].xpath('.//span[@class="a-size-medium a-color-base a-text-normal"]/text()'))
                self.cantidadArticulos+=1
        print("Cantidad total de articulos: ",self.cantidadArticulos)
    #Number of Pages
    def CantidadPaginas(self):
        #self.driver
        self.paginas=self.driver.find_element(By.XPATH,'//*[@id="search"]/div[1]/div[1]/div/span[3]/div[2]/div[29]/div/div/span/span[4]')
        self.cantidadPaginas=self.paginas.get_attribute("innerHTML")
        print("Cantidad total de paginas: ",self.cantidadPaginas)
        print("***************************************************************")
        time.sleep(1)                           #Espera de 1 seg
    #Get Data
    def DataArticulo(self):
        self.contador=0                         #Contador del # de Articulos
        i=0                                     #Iterador para aumentar la direccion del PathX[Titulo] en 1
        #while (self.contador<self.cantidad):   #Condicion mientras contador<cantidad
        while (self.contador<2):
            try:                                #Verifica si existe el Path1[Titulo]
                #Los xpath de los articulos comienzan con: //*[@id="search"]/div[1]/div[1]/div/span[3]/div[2]/div[2]/...
                self.articulo=self.driver.find_element(By.XPATH,'//*[@id="search"]/div[1]/div[1]/div/span[3]/div[2]/div['+str(2+i)+']/div/div/div/div/div/div/div/div[2]/div/div/div[1]/h2/a/span') 
            except NoSuchElementException:
                try:                            #Verifica si existe el Path2[Titulo]
                    self.articulo=self.driver.find_element(By.XPATH,'//*[@id="search"]/div[1]/div[1]/div/span[3]/div[2]/div['+str(2+i)+']/div/div/div/div/div/div[2]/div/div/div[1]/h2/a/span')
                except NoSuchElementException:  #No existe ni Path1 ni Path2
                    i+=1                        #Aumenta en 1 la direccion del PathX
                    continue                    #Se ubica en el while
            time.sleep(1)                       #Espera de 1 seg
            self.articulo.click()               #Hace click en el articulo
            #********************************************************************************************#
            #Obtiene el titulo del articulo
            self.titulo=self.driver.find_element(By.XPATH,'//*[@id="productTitle"]')   
            self.ListaTitulo.append(self.titulo.get_attribute("innerHTML").splitlines()[0].strip())
            #********************************************************************************************#
            #Obtener el precio del articulo
            try:                                #Verifica si existe el precio en el Path1[Precio]
                self.precio=self.driver.find_element(By.XPATH,'//*[@id="corePrice_desktop"]/div/table/tbody/tr/td[2]/span[1]/span[2]')   
            except NoSuchElementException:
                try:                            #Verifica si existe el precio en el Path2[Precio]
                    self.precio=self.driver.find_element(By.XPATH,'//*[@id="olp_feature_div"]/div[2]/span/a/span[2]')
                except NoSuchElementException:
                    self.ListaPrecio.append('') #Si no existe el precio en ningun Path coloca ''
                else:
                    self.ListaPrecio.append(self.precio.get_attribute("innerHTML"))    
            else:
                #Obtiene el precio del articulo
                self.ListaPrecio.append(self.precio.get_attribute("innerHTML"))
            #********************************************************************************************#
            
            i+=1                                #Aumenta en 1 la direccion del PathX
            self.contador+=1                    #Aumenta en 1 el contador de Articulos
            time.sleep(1)                       #Espera de 1 seg
            print(self.contador)                #Indica el # de articulos contados
            self.driver.back()                  #Retorna a la pagina anterior
            time.sleep(2)                       #Espera de 2 seg

    #Close the browser
    def Cerrar(self):
        self.driver.close()
             
    #DataFrame Building  
    def DataFrame(self):
        #Diccionario de Titulo,Precio de los articulos
        DataArticulo={'Titulo':self.ListaTitulo,'Precio':self.ListaPrecio}
        #Construccion del DataFrame
        df=pd.DataFrame(DataArticulo,columns=['Titulo','Precio'])
        print("***************************************************************")
        print(df)
        df.to_excel('DatosArticulos.xlsx')
        
if __name__=='__main__':
    Prueba=Amazon()