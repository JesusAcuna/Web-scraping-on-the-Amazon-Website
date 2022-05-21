#Importar la libreria selenium
#!pip install selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

#
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#Excepciones
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
#Importar la libreria Webdriver para descargar la ultima version del driver
#!pip install webdriver-manager
from webdriver_manager.chrome import ChromeDriverManager
#Libreria para generar delays

#Libreria para el Dataframe
import pandas as pd
#Libreria para determinar el codigo HTML de la pagina
from lxml import html

class Amazon():
    """Intento de instancia de Web Scrapping de Amazon"""
    #Init Method
    def __init__(self):
        self.start_time = time.time()
        chrome_options = Options()
        chrome_options.add_experimental_option("detach", True)
        self.driver=webdriver.Chrome(service=Service(r"C:\Users\jesus\OneDrive\Escritorio\chromedriver_win32\chromedriver.exe"),options=chrome_options)
        #Lista de atributos de los articulos
        self.ListaTitulo=[]
        self.ListaPrecio=[]
        self.ListaCantidadRating=[]
        #Inicializacion de los metodos
        self.Busqueda()
        self.CantidadPaginas()
        #self.CantidadArticulos()
        self.DataArticulo()
        self.Cerrar()
        self.DataFrame()
        
        print("--- %s seconds ---" % (time.time() - self.start_time))
    #Search Bar
    def Busqueda(self):
        #self.driver.maximize_window()        #Maximiza ventana
        self.url="http://amazon.com"
        self.PaginaPrincipal=self.driver.get(self.url) #Dirige a la URL
        while(True):
            try: 
                #self.busqueda=self.driver.find_element(By.XPATH,'//*[@id="twotabsearchtextbox"]')
                # self.busqueda=self.driver.find_element(By.ID,"twotabsearchtextbox")
                self.busqueda=WebDriverWait(self.driver,3).until(EC.presence_of_element_located((By.ID, "twotabsearchtextbox")))
            except TimeoutException:
                try:
                    # self.busqueda=self.driver.find_element(By.XPATH,'//*[@id="nav-bb-search"]')
                    #self.busqueda=self.driver.find_element(By.ID,"nav-bb-search")
                    self.busqueda=WebDriverWait(self.driver,3).until(EC.presence_of_element_located((By.ID, "nav-bb-search")))
                except TimeoutException:
                    #self.PaginaPrincipal.send_keys(Keys.F5)
                    self.driver.refresh()
                    #self.driver.get(self.url)
                    #time.sleep(1) 
                    continue
                else:
                    break
            else:
                break
        self.articlename="keyboard"
        self.busqueda.send_keys(self.articlename,Keys.ENTER) #ingresa "keyboard" y ENTER
        
    #Number of Pages
    def CantidadPaginas(self):
        while(True):
            try: 
                self.cantidadPaginas=WebDriverWait(self.driver,3).until(EC.presence_of_element_located((By.XPATH, "//*[@class='s-pagination-item s-pagination-disabled']"))).text
                #self.cantidadPaginas=self.driver.find_element(By.XPATH,"//*[@class='s-pagination-item s-pagination-disabled']").text
            except TimeoutException: 
                print("No se encontro la cantidad total de paginas")
                #self.Busqueda()
                self.driver.refresh()
                continue
            else:
                break
        print("Cantidad total de paginas: ",self.cantidadPaginas)
    #Number of Articles
    def CantidadArticulos(self):
        ##Arreglar
        while(True):
            try: 
                #self.valores5=WebDriverWait(self.driver,5).until(EC.presence_of_all_elements_located((By.XPATH,'//*[contains(@data-cel-widget,"search_result_") and contains(@data-asin,"B0")]')))
                self.valores5=WebDriverWait(self.driver,5).until(EC.visibility_of_all_elements_located((By.XPATH,'//*[contains(@data-cel-widget,"search_result_") and contains(@data-asin,"B0")]')))
            except TimeoutException: 
                print("No se encontro la cantidad total de articulos")
                #self.Busqueda()
                self.driver.refresh()
                continue
            else:
                break
        
        print("Primer filtro de cantidad de articulos",len(self.valores5))
        
        self.cantidadArticulos=0        
        for i in self.valores5:
            try:
                i.find_element(By.XPATH,".//span[@class = 'a-size-medium a-color-base a-text-normal']").text
            except:
                continue
            else:
                self.cantidadArticulos+=1
        print("Segundo filtro de cantidad de articulos",self.cantidadArticulos)

        print("***************************************************************")

    def Tabla1(self):
        #ListaTabla1ParcialCaracteristica=[]
        #ListaTabla1ParcialValor=[]
        print("***************************************************************")
        try:
            WebDriverWait(self.driver,5).until(EC.presence_of_element_located((By.XPATH,'//*[@id="productOverview_feature_div"]')))
            #self.driver.find_element(By.XPATH,'//*[@id="productOverview_feature_div"]')
        except NoSuchElementException:
            print("Tabla1: No se encontro el Path principal")
            pass
        else:
            try:
                WebDriverWait(self.driver,5).until(EC.presence_of_element_located((By.XPATH,'//*[@id="poExpander"]/div[1]/div/table/tbody')))
                #self.driver.find_element(By.XPATH,'//*[@id="poExpander"]/div[1]/div/table/tbody')
            except TimeoutException:
                self.filasTabla1=len(self.driver.find_elements(By.XPATH,'//*[@id="productOverview_feature_div"]/div/table/tbody/tr'))
                print("filasTabla1 con 1erPath: ",self.filasTabla1)    
                for i in range(self.filasTabla1):
                    self.ListaTablasCaracteristica.append(self.driver.find_element(By.XPATH,'//*[@id="productOverview_feature_div"]/div/table/tbody/tr['+str(i+1)+']/td[1]').text)
                    self.ListaTablasValor.append(self.driver.find_element(By.XPATH,'//*[@id="productOverview_feature_div"]/div/table/tbody/tr['+str(i+1)+']/td[2]').text)
            else:
                #Click on See more
                WebDriverWait(self.driver,5).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="poToggleButton"]/a/span'))).click()

                # self.driver.find_element(By.XPATH,'//*[@id="poToggleButton"]/a/span').click()
                #
                self.filasTabla1=len(self.driver.find_elements(By.XPATH,'//*[@id="poExpander"]/div[1]/div/table/tbody/tr'))
                print("filasTabla1 con 2doPath: ",self.filasTabla1)    
                for i in range(self.filasTabla1):
                    
                    self.ListaTablasCaracteristica.append(self.driver.find_element(By.XPATH,'//*[@id="poExpander"]/div[1]/div/table/tbody/tr['+str(i+1)+']/td[1]').text)
                    self.ListaTablasValor.append(self.driver.find_element(By.XPATH,'//*[@id="poExpander"]/div[1]/div/table/tbody/tr['+str(i+1)+']/td[2]').text)                


    def Tabla2(self):
        #ListaTabla2ParcialCaracteristica=[]
        #ListaTabla2ParcialValor=[]
        try:
            WebDriverWait(self.driver,5).until(EC.presence_of_element_located((By.XPATH,'//*[@id="productDetails_techSpec_section_1"]/tbody/tr')))
            #self.driver.find_element(By.XPATH,'//*[@id="productDetails_techSpec_section_1"]/tbody/tr')
        except TimeoutException:
            print("\nTabla2: No se encontro el Path principal")
            pass
        else:
            self.filasTabla2=len(self.driver.find_elements(By.XPATH,'//*[@id="productDetails_techSpec_section_1"]/tbody/tr'))
            print("\nfilasTabla2: ",self.filasTabla2)
            for i in range(self.filasTabla2):
                self.ListaTablasCaracteristica.append(self.driver.find_element(By.XPATH,'//*[@id="productDetails_techSpec_section_1"]/tbody/tr['+str(i+1)+']/th').text)
                self.ListaTablasValor.append(self.driver.find_element(By.XPATH,'//*[@id="productDetails_techSpec_section_1"]/tbody/tr['+str(i+1)+']/td').text)

    def Tabla3(self):
        #ListaTabla3ParcialCaracteristica=[]
        #ListaTabla3ParcialValor=[]
        try:
            WebDriverWait(self.driver,5).until(EC.presence_of_element_located((By.XPATH,'//*[@id="productDetails_detailBullets_sections1"]/tbody/tr')))
            #self.driver.find_element(By.XPATH,'//*[@id="productDetails_detailBullets_sections1"]/tbody/tr')
        except TimeoutException:
             print("\nTabla3: No se encontro el Path principal")
             pass
        else:
            self.filasTabla3=len(self.driver.find_elements(By.XPATH,'//*[@id="productDetails_detailBullets_sections1"]/tbody/tr'))
            print("\nfilasTabla3: ",self.filasTabla3)
            for i in range(self.filasTabla3):
                self.ListaTablasCaracteristica.append(self.driver.find_element(By.XPATH,'//*[@id="productDetails_detailBullets_sections1"]/tbody/tr['+str(i+1)+']/th').text)
                self.ListaTablasValor.append(self.driver.find_element(By.XPATH,'//*[@id="productDetails_detailBullets_sections1"]/tbody/tr['+str(i+1)+']/td').text)
            
        
    #Get Rating 
    """
    def Rating(self):

        try:
            self.CantidadRating=self.driver.find_element(By.XPATH,'//*[@id="acrCustomerReviewText"]') 
        except NoSuchElementException:
            self.ListaCantidadRating.append('')
        else:
            self.ListaCantidadRating.append(self.CantidadRating.get_attribute("innerHTML"))
    """
    #Get Price information
    def Precio(self):
        
        try: 
            self.precio=WebDriverWait(self.driver,3).until(EC.presence_of_element_located((By.XPATH, '//*[@id="corePrice_desktop"]/div/table/tbody/tr/td[2]/span[1]/span[2]'))).text
            #self.cantidadPaginas=self.driver.find_element(By.XPATH,"//*[@class='s-pagination-item s-pagination-disabled']").text
        except TimeoutException: 
            try: 
                self.precio=WebDriverWait(self.driver,3).until(EC.presence_of_element_located((By.XPATH, '//*[@id="corePriceDisplay_desktop_feature_div"]/div[1]/span/span[2]/span[2]'))).text
                #self.cantidadPaginas=self.driver.find_element(By.XPATH,"//*[@class='s-pagination-item s-pagination-disabled']").text
            except TimeoutException: 
                self.ListaPrecio.append('')
            else:
                #self.ListaTitulo.append(self.titulo.get_attribute("innerHTML").splitlines()[0].strip())
                self.ListaPrecio.append(self.precio)
        else:
            #self.ListaTitulo.append(self.titulo.get_attribute("innerHTML").splitlines()[0].strip())
            self.ListaPrecio.append(self.precio)
        

    #Get Title information
    def Titulo(self):
  
        try: 
            self.titulo=WebDriverWait(self.driver,3).until(EC.presence_of_element_located((By.XPATH, '//*[@id="productTitle"]'))).text
            #self.cantidadPaginas=self.driver.find_element(By.XPATH,"//*[@class='s-pagination-item s-pagination-disabled']").text
        except TimeoutException: 
            self.ListaTitulo.append('')
        else:
            #self.ListaTitulo.append(self.titulo.get_attribute("innerHTML").splitlines()[0].strip())
            self.ListaTitulo.append(self.titulo)
    def DataArticulo(self):
        self.ListaCaracteristicas=[]
        self.ListaValores=[]    
        #self.cantidadPaginas=1         #Borrar
        self.cantidadArticulosTotal=0 
        for j in range(int(self.cantidadPaginas)):
        #for j in range(1):
            if j>0:
                self.driver.get('https://www.amazon.com/s?k='+self.articlename+'&page='+str(j+1))
            self.CantidadArticulos()
            #self.elements =self.driver.find_elements_by_class_name('sg-col-inner')
            print("Cantidad de articulos de la pagina: ",j+1,"es igual a: ",self.cantidadArticulos)
            #
            self.contador=0                         #Contador del # de Articulos
            i=0                                     #Iterador para aumentar la direccion del PathX[Titulo] en 1
            #while (self.contador<self.cantidadArticulos):   #Condicion mientras contador<cantidad
            #self.cantidadArticulos=2                   #Borrar
            self.cantidadArticulosTotal+=self.cantidadArticulos
            #Tabla2
        
            while (self.contador<self.cantidadArticulos):
                ##Verifico si existen los PathX[Titulo] 
                try:         
                       #Verifica si existe el Path1[Titulo]
                    #Los xpath de los articulos comienzan con: //*[@id="search"]/div[1]/div[1]/div/span[3]/div[2]/div[2]/...
                    self.articulo=WebDriverWait(self.driver,3).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="search"]/div[1]/div[1]/div/span[3]/div[2]/div['+str(2+i)+']/div/div/div/div/div/div/div/div[2]/div/div/div[1]/h2/a/span'))).click()
                    # self.articulo=self.driver.find_element(By.XPATH,'//*[@id="search"]/div[1]/div[1]/div/span[3]/div[2]/div['+str(2+i)+']/div/div/div/div/div/div/div/div[2]/div/div/div[1]/h2/a/span') 
                    #self.articulo=WebDriverWait(self.driver,5).until(EC.visibility_of_element_located((By.XPATH,'//*[@id="search"]/div[1]/div[1]/div/span[3]/div[2]/div['+str(2+i)+']/div/div/div/div/div/div/div/div[2]/div/div/div[1]/h2/a/span')))

                except TimeoutException:
                    try:                            #Verifica si existe el Path2[Titulo]
                        self.articulo=WebDriverWait(self.driver,3).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="search"]/div[1]/div[1]/div/span[3]/div[2]/div['+str(2+i)+']/div/div/div/div/div/div[2]/div/div/div[1]/h2/a/span'))).click()
                        #self.articulo=self.driver.find_element(By.XPATH,'//*[@id="search"]/div[1]/div[1]/div/span[3]/div[2]/div['+str(2+i)+']/div/div/div/div/div/div[2]/div/div/div[1]/h2/a/span')
                    except TimeoutException:  #No existe ni Path1 ni Path2
                        i+=1                        #Aumenta en 1 la direccion del PathX
                        continue                    #Se ubica en el while
                #Verifico si el PathX[Titulo] esta habilitado
                """
                try:
                    self.articulo.is_enabled()      
                except:
                    self.articulo.send_keys(Keys.F5)
                    continue                        #Se ubica en el while
                """    

                #self.articulo.click()               #Hace click en el articulo
                
                #time.sleep(1)                       #Espera de 1 seg
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
                #self.Rating()
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
                #time.sleep(1)                       #Espera de 1 seg
                #
                print("***************************************************************")
                print("Producto #",self.contador,"de la pagina #",j+1) #Indica el # de articulos contados
                print("Longitud de caracteristicas de las tablas(duplicados): ",len(self.ListaTablasCaracteristica)) #Indica el # de articulos contados
                #print(self.ListaTablasCaracteristica)
                print("Longitud de valores de las tablas(duplicados): ",len(self.ListaTablasValor)) #Indica el # de articulos contados
                #print(self.ListaTablasValor)
                #
                self.ListaCaracteristicas.append(self.ListaTablasCaracteristica)
                self.ListaValores.append(self.ListaTablasValor)
                
                #
                self.driver.back()                  #Retorna a la pagina anterior
                #time.sleep(2)                       #Espera de 2 seg
           
    #Close the browser
    def Cerrar(self):
        #self.driver.close()
        self.driver.quit()
             
    #DataFrame Building  
    def DataFrame(self): 
        #Diccionario de Titulo,Precio de los articulos
        DataArticulo={}
        #DataArticulo['Rating']=self.ListaCantidadRating
        DataArticulo['Price']=self.ListaPrecio
        DataArticulo['Title']=self.ListaTitulo
        #Construccion del conjunto
        self.ConjuntoCaracteristicas=set()
        for l in range(self.cantidadArticulosTotal):
            self.ConjuntoCaracteristicas=self.ConjuntoCaracteristicas | set(self.ListaCaracteristicas[l])
        
        
        #print('\n',self.ConjuntoCaracteristicas,'\n')
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
        columnasDF=['Title','Price']
        for i in self.ConjuntoCaracteristicas:
            columnasDF.append(i)
        df=pd.DataFrame(DataArticulo,columns=columnasDF)
        print("***************************************************************")
        print(df)
        df.to_excel('DatosArticulos.xlsx')
if __name__=='__main__':
    
    Prueba=Amazon()