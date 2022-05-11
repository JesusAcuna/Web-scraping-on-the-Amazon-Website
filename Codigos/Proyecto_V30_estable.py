#Importar la libreria selenium
#!pip install selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
#
from selenium.webdriver.common.by import By
#from selenium.webdriver.support.ui import WebDriverWait
#from selenium.webdriver.support import expected_conditions as EC
#Excepciones
from selenium.common.exceptions import NoSuchElementException
#Importar la libreria Webdriver para descargar la ultima version del driver
#!pip install webdriver-manager
from webdriver_manager.chrome import ChromeDriverManager
#Libreria para generar delays
import time
#Libreria para el Dataframe
import pandas as pd
#Libreria para determinar el codigo HTML de la pagina
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
        self.ListaCantidadRating=[]
        #Inicializacion de los metodos
        self.Busqueda()
        self.CantidadPaginas()
        self.DataArticulo()
        self.Cerrar()
        self.DataFrame()
    #Search Bar
    def Busqueda(self):
        self.driver.maximize_window()        #Maximiza ventana
        self.driver.get("http://amazon.com") #Dirige a la URL
        time.sleep(1)                        #Espera de 1 seg
        #Dirige hacia el xpath de la busqueda del nombre del articulo
        #Algunas veces sale otro buscador
        while(True):
            try: 
                self.busqueda=self.driver.find_element(By.XPATH,'//*[@id="twotabsearchtextbox"]')
            except NoSuchElementException:
                try:
                    self.busqueda=self.driver.find_element(By.XPATH,'//*[@id="nav-bb-search"]')
                except NoSuchElementException:
                    self.driver.get("http://amazon.com")
                    time.sleep(1) 
                    continue
                else:
                    break
            else:
                break
        self.articlename="keyboard"
        self.busqueda.send_keys(self.articlename,Keys.ENTER) #ingresa "keyboard" y ENTER
        time.sleep(2)                        #Espera de 2 seg
    #Number of Pages
    def CantidadPaginas(self):
        #Calcula el directorio de la ubcacion actual del driver(pagina de "keyboard")
        self.tree=html.fromstring(self.driver.page_source)
        #Encuentra valores(LISTA) que contengan el atributo @class="s-widget-container....."
        self.valores_p=self.tree.xpath('//div[contains(@class,"s-widget-container s-spacing-medium s-widget-container-height-medium celwidget slot=MAIN template=PAGINATION widgetId=pagination-button")]')
        self.cantidadPaginas=int(self.valores_p[0].xpath('.//span[@class="s-pagination-item s-pagination-disabled"]/text()')[0])
        print("***************************************************************")
        print("Cantidad total de paginas: ",self.cantidadPaginas)
        #time.sleep(1)                           #Espera de 1 seg
    #Number of Articles
    def CantidadArticulos(self):
        self.cantidadArticulos=0
        #Encuentra valores(LISTA) que contengan el atributo @data-asin="B0....."
        self.valores=self.tree.xpath('//div[contains(@data-asin,"B0")]')
        #Hay algunos valores que son [], por lo que se ceunta aquellos que tengan valor !=[]
        print("***************************************************************")
        for i in range(len(self.valores)):
            #self.tree
            if(self.valores[i].xpath('.//span[@class="a-size-medium a-color-base a-text-normal"]/text()')!=[]):
                #print(self.valores[i].xpath('.//span[@class="a-size-medium a-color-base a-text-normal"]/text()'))
                self.cantidadArticulos+=1
    def Tabla1(self):
        ListaTabla1ParcialCaracteristica=[]
        ListaTabla1ParcialValor=[]
        print("***************************************************************")
        try:
            self.driver.find_element(By.XPATH,'//*[@id="productOverview_feature_div"]')
        except NoSuchElementException:
            print("\nTabla1: No se encontro el Path principal")
            pass
        else:
            try:
                self.driver.find_element(By.XPATH,'//*[@id="poExpander"]/div[1]/div/table/tbody')
            except NoSuchElementException:
                self.filasTabla1=len(self.driver.find_elements(By.XPATH,'//*[@id="productOverview_feature_div"]/div/table/tbody/tr'))
                print("\nfilasTabla1 con 1erPath: ",self.filasTabla1)    
                for i in range(self.filasTabla1):
                    self.ListaTablasCaracteristica.append(self.driver.find_element(By.XPATH,'//*[@id="productOverview_feature_div"]/div/table/tbody/tr['+str(i+1)+']/td[1]').text)
                    self.ListaTablasValor.append(self.driver.find_element(By.XPATH,'//*[@id="productOverview_feature_div"]/div/table/tbody/tr['+str(i+1)+']/td[2]').text)
                    #
                    ListaTabla1ParcialCaracteristica.append(self.driver.find_element(By.XPATH,'//*[@id="productOverview_feature_div"]/div/table/tbody/tr['+str(i+1)+']/td[1]').text)
                    ListaTabla1ParcialValor.append(self.driver.find_element(By.XPATH,'//*[@id="productOverview_feature_div"]/div/table/tbody/tr['+str(i+1)+']/td[2]').text)
                print(ListaTabla1ParcialCaracteristica)
                print(ListaTabla1ParcialValor)    
            else:
                #Click on See more
                self.driver.find_element(By.XPATH,'//*[@id="poToggleButton"]/a/span').click()
                #
                self.filasTabla1=len(self.driver.find_elements(By.XPATH,'//*[@id="poExpander"]/div[1]/div/table/tbody/tr'))
                print("\nfilasTabla1 con 2doPath: ",self.filasTabla1)    
                for i in range(self.filasTabla1):
                    
                    self.ListaTablasCaracteristica.append(self.driver.find_element(By.XPATH,'//*[@id="poExpander"]/div[1]/div/table/tbody/tr['+str(i+1)+']/td[1]').text)
                    self.ListaTablasValor.append(self.driver.find_element(By.XPATH,'//*[@id="poExpander"]/div[1]/div/table/tbody/tr['+str(i+1)+']/td[2]').text)                
                    ListaTabla1ParcialCaracteristica.append(self.driver.find_element(By.XPATH,'//*[@id="poExpander"]/div[1]/div/table/tbody/tr['+str(i+1)+']/td[1]').text)
                    ListaTabla1ParcialValor.append(self.driver.find_element(By.XPATH,'//*[@id="poExpander"]/div[1]/div/table/tbody/tr['+str(i+1)+']/td[2]').text)       
                print(ListaTabla1ParcialCaracteristica)
                print(ListaTabla1ParcialValor)    

    def Tabla2(self):
        ListaTabla2ParcialCaracteristica=[]
        ListaTabla2ParcialValor=[]
        try:
            self.driver.find_element(By.XPATH,'//*[@id="productDetails_techSpec_section_1"]/tbody/tr')
        except NoSuchElementException:
            print("\nTabla2: No se encontro el Path principal")
            pass
        else:
            self.filasTabla2=len(self.driver.find_elements(By.XPATH,'//*[@id="productDetails_techSpec_section_1"]/tbody/tr'))
            print("\nfilasTabla2: ",self.filasTabla2)
            for i in range(self.filasTabla2):
                self.ListaTablasCaracteristica.append(self.driver.find_element(By.XPATH,'//*[@id="productDetails_techSpec_section_1"]/tbody/tr['+str(i+1)+']/th').text)
                self.ListaTablasValor.append(self.driver.find_element(By.XPATH,'//*[@id="productDetails_techSpec_section_1"]/tbody/tr['+str(i+1)+']/td').text)
                ListaTabla2ParcialCaracteristica.append(self.driver.find_element(By.XPATH,'//*[@id="productDetails_techSpec_section_1"]/tbody/tr['+str(i+1)+']/th').text)
                ListaTabla2ParcialValor.append(self.driver.find_element(By.XPATH,'//*[@id="productDetails_techSpec_section_1"]/tbody/tr['+str(i+1)+']/td').text)
            print(ListaTabla2ParcialCaracteristica)
            print(ListaTabla2ParcialValor) 
    def Tabla3(self):
        ListaTabla3ParcialCaracteristica=[]
        ListaTabla3ParcialValor=[]
        try:
            self.driver.find_element(By.XPATH,'//*[@id="productDetails_detailBullets_sections1"]/tbody/tr')
        except NoSuchElementException:
             print("\nTabla3: No se encontro el Path principal")
             pass
        else:
            self.filasTabla3=len(self.driver.find_elements(By.XPATH,'//*[@id="productDetails_detailBullets_sections1"]/tbody/tr'))
            print("\nfilasTabla3: ",self.filasTabla3)
            for i in range(self.filasTabla3):
                self.ListaTablasCaracteristica.append(self.driver.find_element(By.XPATH,'//*[@id="productDetails_detailBullets_sections1"]/tbody/tr['+str(i+1)+']/th').text)
                self.ListaTablasValor.append(self.driver.find_element(By.XPATH,'//*[@id="productDetails_detailBullets_sections1"]/tbody/tr['+str(i+1)+']/td').text)
                ListaTabla3ParcialCaracteristica.append(self.driver.find_element(By.XPATH,'//*[@id="productDetails_detailBullets_sections1"]/tbody/tr['+str(i+1)+']/th').text)
                ListaTabla3ParcialValor.append(self.driver.find_element(By.XPATH,'//*[@id="productDetails_detailBullets_sections1"]/tbody/tr['+str(i+1)+']/td').text)
            print(ListaTabla3ParcialCaracteristica)
            print(ListaTabla3ParcialValor)  
        
    #Get Rating information
    def Rating(self):

        try:
            self.CantidadRating=self.driver.find_element(By.XPATH,'//*[@id="acrCustomerReviewText"]') 
        except NoSuchElementException:
            self.ListaCantidadRating.append('')
        else:
            self.ListaCantidadRating.append(self.CantidadRating.get_attribute("innerHTML"))
    #Get Price information
    def Precio(self):

        try:                                #Verifica si existe el precio en el Path1[Precio]
            self.precio=self.driver.find_element(By.XPATH,'//*[@id="corePrice_feature_div"]/div/span/span[2]') 
        except NoSuchElementException:
            try:                            #Verifica si existe el precio en el Path2[Precio]
                self.precio=self.driver.find_element(By.XPATH,'//*[@id="olp_feature_div"]/div[2]/span/a/span[2]')
            except NoSuchElementException:
                self.ListaPrecio.append('') #Si no existe el precio en ningun Path coloca ''
            else:
                self.ListaPrecio.append(self.precio.get_attribute("innerHTML")) 
        else:
            self.ListaPrecio.append(self.precio.get_attribute("innerHTML")) 
    #Get Title information
    def Titulo(self):

        self.titulo=self.driver.find_element(By.XPATH,'//*[@id="productTitle"]')
        self.ListaTitulo.append(self.titulo.get_attribute("innerHTML").splitlines()[0].strip())
    def DataArticulo(self):
        self.ListaCaracteristicas=[]
        self.ListaValores=[]   
        self.cantidadPaginas=1          #Borrar
        self.cantidadArticulosTotal=0 
        for j in range(self.cantidadPaginas):
            if j>0:
                self.driver.get('https://www.amazon.com/s?k='+self.articlename+'&page='+str(j+1))
            self.CantidadArticulos()
            print("Cantidad de articulos de la pagina: ",j+1,"es igual a: ",self.cantidadArticulos)
            #
            self.contador=0                         #Contador del # de Articulos
            i=0                                     #Iterador para aumentar la direccion del PathX[Titulo] en 1
            #while (self.contador<self.cantidadArticulos):   #Condicion mientras contador<cantidad
            self.cantidadArticulos=6                      #Borrar
            self.cantidadArticulosTotal+=self.cantidadArticulos
            #Tabla2
        
            while (self.contador<self.cantidadArticulos):
                ##Verifico si existen los PathX[Titulo] 
                try:                                #Verifica si existe el Path1[Titulo]
                    #Los xpath de los articulos comienzan con: //*[@id="search"]/div[1]/div[1]/div/span[3]/div[2]/div[2]/...
                    self.articulo=self.driver.find_element(By.XPATH,'//*[@id="search"]/div[1]/div[1]/div/span[3]/div[2]/div['+str(2+i)+']/div/div/div/div/div/div/div/div[2]/div/div/div[1]/h2/a/span') 
                except NoSuchElementException:
                    try:                            #Verifica si existe el Path2[Titulo]
                        self.articulo=self.driver.find_element(By.XPATH,'//*[@id="search"]/div[1]/div[1]/div/span[3]/div[2]/div['+str(2+i)+']/div/div/div/div/div/div[2]/div/div/div[1]/h2/a/span')
                    except NoSuchElementException:  #No existe ni Path1 ni Path2
                        i+=1                        #Aumenta en 1 la direccion del PathX
                        continue                    #Se ubica en el while
                #Verifico si el PathX[Titulo] esta habilitado
                try:
                    self.articulo.is_enabled()      
                except:
                    self.articulo.send_keys(Keys.F5)
                    continue                        #Se ubica en el while
                    
                self.articulo.click()               #Hace click en el articulo
                time.sleep(1)                       #Espera de 1 seg
                #self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
                #time.sleep(1)
                #*************************************************************#
                #Obtiene el titulo del articulo
                self.Titulo()
                #*************************************************************#
                #Obtiene el precio del articulo
                self.Precio()
                #*************************************************************#
                #Obtiene la cantidad de calificaciones del articulo
                self.Rating()
                #*************************************************************#
                #Obtener Informacion de las Tablas
                self.ListaTablasCaracteristica=[]
                self.ListaTablasValor=[]
                #Obtienee informacion de la tabla1
                self.Tabla1()
                #*************************************************************#
                #Obtienee informacion de la tabla2
                self.Tabla2()
                #*************************************************************#
                #Obtienee informacion de la tabla2
                self.Tabla3()
                #*************************************************************#
                i+=1                                #Aumenta en 1 la direccion del PathX
                self.contador+=1                    #Aumenta en 1 el contador de Articulos
                time.sleep(1)                       #Espera de 1 seg
                #
                print("***************************************************************")
                print("\nProducto #",self.contador,"de la pagina #",j+1) #Indica el # de articulos contados
                print("Longitud de carcteristicas de las tablas(duplicados): ",len(self.ListaTablasCaracteristica)) #Indica el # de articulos contados
                print(self.ListaTablasCaracteristica)
                print("\nLongitud de valores de las tablas(duplicados): ",len(self.ListaTablasValor)) #Indica el # de articulos contados
                print(self.ListaTablasValor)
                #
                self.ListaCaracteristicas.append(self.ListaTablasCaracteristica)
                self.ListaValores.append(self.ListaTablasValor)
                
                #
                self.driver.back()                  #Retorna a la pagina anterior
                time.sleep(2)                       #Espera de 2 seg
           
    #Close the browser
    def Cerrar(self):
        self.driver.close()
             
    #DataFrame Building  
    def DataFrame(self): 
        #Diccionario de Titulo,Precio de los articulos
        DataArticulo={}
        DataArticulo['Rating']=self.ListaCantidadRating
        DataArticulo['Price']=self.ListaPrecio
        DataArticulo['Title']=self.ListaTitulo
        #Construccion del conjunto
        self.ConjuntoCaracteristicas=set()
        for l in range(self.cantidadArticulosTotal):
            self.ConjuntoCaracteristicas=self.ConjuntoCaracteristicas | set(self.ListaCaracteristicas[l])
        
        print('\n',self.ConjuntoCaracteristicas,'\n')
        for m in self.ConjuntoCaracteristicas:
            lista=[]
            for n in range(self.cantidadArticulosTotal):
                if(m in set(self.ListaCaracteristicas[n])):
                    indice=self.ListaCaracteristicas[n].index(m)
                    lista.append(self.ListaValores[n][indice])
                else:
                    lista.append('')
            DataArticulo[m]=lista
        #Construccion del DataFrame
        columnasDF=['Title','Price','Rating']
        for i in self.ConjuntoCaracteristicas:
            columnasDF.append(i)
        df=pd.DataFrame(DataArticulo,columns=columnasDF)
        print("***************************************************************")
        print(df)
        df.to_excel('DatosArticulos.xlsx')
if __name__=='__main__':
    Prueba=Amazon()