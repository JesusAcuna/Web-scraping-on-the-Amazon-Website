# Web Scraping with Selenium [Python]
<p align="center">
  <img src="https://selenium-python.readthedocs.io/_static/logo.png">
</p>

---
<p align="justify">
Web Scraping is a technique that consists of extracting information from web pages. In this case I extracted information from the 20 featured pages of an Amazon product, since Amazon only shows you up to page 20. With this method you can extract information from products such as title, price, style, brand, manufacturer, domestic shipping, country of origin, series, special features, item model number, ASIN, generation, material, best sellers rank and many others, but the quantity of features depend on the product you are looking for.
</p>

---
## Index

- 1.[Basic notions](#1-basic-notions)
  - 1.1.[Locating elements](#11-locating-elements) 
  - 1.2.[Finding elements by ID](#12-finding-elements-by-id) 
  - 1.3.[Finding elements by XPATH](#13-finding-elements-by-xpath) 
- 2.[Starting](#2-starting)
  - 2.1.[Import selenium library and chrome driver](#21-import-selenium-library-and-chrome-driver)  
  - 2.2.[Create a driver with options](#22-create-a-driver-with-options) 
- 3.[Initializing search](#3-initializig-search)
  - 3.1.[Enter the URL](#31-enter-the-url) 
  - 3.2.[Create Explicit Waits to locate the search bar](#32-create-explicit-waits-to-locate-the-search-bar)
  - 3.3.[Enter the product](#33-enter-the-product) 
- 4.[Number of pages](#4-number-of-pages) 
  - 4.1.[Finding the number of pages](#41-finding-the-number-of-pages) 
- 5.[Functions](#5-functions)
  - 5.1.[Number of articles](#51-number-of-articles) 
  - 5.2.[Article title](#52-article-title)
  - 5.3.[Article price](#53-article-price)
  - 5.4.[Table1 information](#54-table1-information)
  - 5.5.[Table2 information](#55-table2-information)
  - 5.6.[Table3 information](#56-table3-information)
- 6.[Data article](#6-data-article)
- 7.[Get Dataframe](#7-get-dataframe)
- 8.[References](#8-references)
---

## Structure of the repository

The repository contains the next files and folders:

- `web-scraping-on-amazon-with-selenium-python.ipynb`: notebook from kaggle where I ran the code, so you can check it out in the link below to see the output of each line of code, the notebook is also in the repository :

  https://www.kaggle.com/code/jesusacunamorillo/web-scraping-on-amazon-with-selenium-python/notebook
  
- `data`: directory where the the data in csv format is stored, in this case for the 'keyboard' product.
  

## 1. Basic notions

The HTML5 standar includes HTML, CSS and JavaScript, but for web scraping I only used part of HTML programation, essentially the use of tags.

### 1.1. Locating elements

There are various strategies to locate elements in a page. You can use the most appropriate one for your case. Selenium provides the following methods to locate elements in a page:

- find_element_by_id
- find_element_by_name
- find_element_by_xpath
- find_element_by_link_text
- find_element_by_partial_link_text
- find_element_by_tag_name
- find_element_by_class_name
- find_element_by_css_selector

### 1.2. Finding elements by ID

For example, to find out the searth bar ID on Amazon web, go to amazon web, then right click on search bar and inspect.

In the red box image you'll see id="twotabsearchtextbox", and the method using the code above is:

<p align="center">  
<b>find_element_by_id("twotabsearchtextbox") or find_element(By.ID,"twotabsearchtextbox")</b>
</>

<p align="center">
  <img src="https://github.com/JesusAcuna/Web-scraping-on-the-Amazon-Website/blob/main/images/image_1.jpg">
</p>

### 1.3. Finding elements by XPATH

<p align="justify">
XPath is the language used for locating nodes in an XML document. One of the main reasons for using XPath is when you don’t have a suitable id or name attribute for the element you wish to locate. You can use XPath to either locate the element in absolute terms (not advised), or relative to an element that does have an id or name attribute.
</p>

To find the XPath just right click on the HTML code and copy the XPath,and the method using the locations elements is:


<p align="center">  
<b>find_element_by_xpath(//*[@id="twotabsearchtextbox"]) or find_element(By.XPATH,//*[@id="twotabsearchtextbox"])</b>
</>

<p align="center">
  <img src="https://github.com/JesusAcuna/Web-scraping-on-the-Amazon-Website/blob/main/images/image_2.jpg">
</p>

Reference: https://selenium-python.readthedocs.io/locating-elements.html

## 2. Starting

To begin first import the selenium and chrome driver libraries and create the driver object.

### 2.1. Import selenium library and chrome driver

    !pip install selenium                                 # Install selenium
    !apt-get update                                       # To update ubuntu to correctly run apt install
    !apt install chromium-chromedriver -y                 # Install chrome driver
    !cp /usr/lib/chromium-browser/chromedriver /usr/bin   # Adding the driver path 

    import sys                                                    
    sys.path.insert(0,'/usr/lib/chromium-browser/chromedriver')

### 2.2. Create a driver with options


    from selenium import webdriver                                  # Import webdriver

    chrome_options = webdriver.ChromeOptions()                      # Create object ChromeOptions()
    chrome_options.add_argument('--headless')           
    chrome_options.add_argument('--no-sandbox')                             
    chrome_options.add_argument('--disable-dev-shm-usage')
    driver= webdriver.Chrome('chromedriver',options=chrome_options) # Create driver
    
In Spyder IDE this first part is:

    !pip install selenium
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    driver=webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=chrome_options)

Then the rest of the below code is the same

## 3. Initializing search

In this part enter the URL, create the explicit waits, that is a better tool than the time.sleep(s), and enter the product.

### 3.1. Enter the URL

    url="http://amazon.com"        # Page URL
    driver.get(url)                # Go to that URL
    
### 3.2. Create Explicit Waits to locate the search bar

<p align="justify">
An explicit wait is a code you define to wait for a certain condition to occur before proceeding further in the code. The extreme case of this is time.sleep(), which sets the condition to an exact time period to wait.    
</p>

Reference: https://selenium-python.readthedocs.io/waits.html

- The first condition is "presence_of_element_located" that checks that element is on the page source.

- The page sometimes gives you two IDs, that's why I decided to try with two ID's: <b>'twotabsearchtextbox', 'nav-bb-search'</b>

- This ExplicitWait waits by 3 seconds, in this case, to find that element by ID before the TimeException occurs, and if this is executed just refresh the page until the condition is fulfilled

      #These 3 methods are for ExplicitWaits
      from selenium.webdriver.common.by import By
      from selenium.webdriver.support.ui import WebDriverWait
      from selenium.webdriver.support import expected_conditions as EC

      #Exception library
      from selenium.common.exceptions import TimeoutException

      while(True):
          try: 
              search=WebDriverWait(driver,3).until(EC.presence_of_element_located((By.ID, "twotabsearchtextbox")))
          except TimeoutException:
              try:
                  search=WebDriverWait(driver,3).until(EC.presence_of_element_located((By.ID, "nav-bb-search")))
              except TimeoutException:       #Exception when the ExplicitWait condition occurs
                  driver.refresh()
                  continue
              else:
                  break
          else:
              break
            
### 3.3. Enter the product

This code below makes: first type the product in the search bar and press ENTER

    from selenium.webdriver.common.keys import Keys       #Import the Keys object

    articlename="keyboard"                    
    search.send_keys(articlename,Keys.ENTER)  
    
Now we are on the main page of the product


## 4. Number of pages

### 4.1. Finding the number of pages

- To find the number of pages I used a ExplicitWait with the condition "presence_of_element_located" by XPATH
- The method 'WebDriverWait(driver,3).until(EC.presence_of_element_located((By.XPATH,"..."))).**text**' gets the text included inside the HTML code
- If the exception occurs a message will be printed and the page will be refresed


      while(True):
          try: 
              numberofpages=WebDriverWait(driver,3).until(EC.presence_of_element_located((By.XPATH, "//*[@class='s-pagination-item s-pagination-disabled']"))).text
          except TimeoutException: 
              print("The total number of pages was not found.")
              driver.refresh()
              continue
          else:
              break
      print("Total number of pages: ",numberofpages)
    
## 5. Functions

### 5.1. Number of articles

This is going to be a function, since each page has a different number of products or articles.

1. First part

- To find the number of articles I used a ExplicitWait with the condition "presence_of_all_elements_located" by XPATH
- To find out the products path, that contains several tags, I used two tags "@data-cel-widget","@data-asin" and their start values "search_result_", "B0" respectively as a filter.
- If the exception occurs a message will be printed and the page will be refresed.

2. Second part

- "elements" is going to give me all the products XPATH on the page even the advertising products and others, so to avoid the latter I'm going to count all the products that have the tag @class='a-size-medium a-color-base a-text-normal' .

      def NumberofArticles():    
          while(True):
              try: 
                  elements=WebDriverWait(driver,5).until(EC.presence_of_all_elements_located((By.XPATH,'//*[contains(@data-cel-widget,"search_result_") and contains(@data-asin,"B0")]')))
              except TimeoutException: 
                  print("No elements found")
                  driver.refresh()
                  continue
              else:
                  break      
          print("Items found with the filter: ",len(elements))
          # Second part
          numberofarticles=0        
          for i in elements:
              try:
                  i.find_element(By.XPATH,".//span[@class = 'a-size-medium a-color-base a-text-normal']").text
              except:
                  continue
              else:
                  numberofarticles+=1
          print("Total number of articles: ",numberofarticles)
          print("***************************************************************")
          return numberofarticles
          
### 5.2. Article title

- To find the article title I used a ExplicitWait with the condition "presence_of_element_located" by XPATH.
- If exists return the article title, if not '', and append it to TitleList

      def Title():
          try: 
              title=WebDriverWait(driver,3).until(EC.presence_of_element_located((By.XPATH, '//*[@id="productTitle"]'))).text
          except TimeoutException: 
              return ''
          else:
              return title

### 5.3. Article price

- To find the article price I used a ExplicitWait with the condition "presence_of_element_located" by XPATH. There are two XPATHS where article prices appear
- If exists return the article price, if not '', and append it to PriceList

      def Price():
          try: 
              price=WebDriverWait(driver,3).until(EC.presence_of_element_located((By.XPATH, '//*[@id="corePrice_desktop"]/div/table/tbody/tr/td[2]/span[1]/span[2]'))).text
          except TimeoutException: 
              try: 
                  price=WebDriverWait(driver,3).until(EC.presence_of_element_located((By.XPATH, '//*[@id="corePriceDisplay_desktop_feature_div"]/div[1]/span/span[2]/span[2]'))).text
              except TimeoutException: 
                  return ''
              else:
                  return price
          else:
              return price

### 5.4. Table1 information

At point 6.[Data article](#6-data-article) I explained what is the information in the table.

- To find out if the article has a expander prompt I used a ExplicitWait with the condition "presence_of_element_located" by XPATH. If exists click on it and if not return nothing.
- Then to find the length of that table I used a find_elements by XPATH, with the length I returned the features and values of the table.

      def Table1():
          FeatureTable1List=[]
          ValueTable1List=[]
          print("***************************************************************")
          try:
              WebDriverWait(driver,5).until(EC.presence_of_element_located((By.XPATH,'//*[@id="productOverview_feature_div"]')))
          except TimeoutException:
              print("Table1: Primary path not found")
              return [],[]       
          else:
              #Second part
              try:
                  WebDriverWait(driver,5).until(EC.presence_of_element_located((By.XPATH,'//*[@id="poExpander"]/div[1]/div/table/tbody')))
              except TimeoutException:
                  table1rows=len(driver.find_elements(By.XPATH,'//*[@id="productOverview_feature_div"]/div/table/tbody/tr'))
                  print("Table1rows with the first Path: ",table1rows)    
                  for i in range(table1rows):
                      FeatureTable1List.append(driver.find_element(By.XPATH,'//*[@id="productOverview_feature_div"]/div/table/tbody/tr['+str(i+1)+']/td[1]').text)
                      ValueTable1List.append(driver.find_element(By.XPATH,'//*[@id="productOverview_feature_div"]/div/table/tbody/tr['+str(i+1)+']/td[2]').text)
                  return FeatureTable1List,ValueTable1List       
              else:
                  #Click on See more
                  WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="poToggleButton"]/a/span'))).click()
                  table1rows=len(driver.find_elements(By.XPATH,'//*[@id="poExpander"]/div[1]/div/table/tbody/tr'))
                  print("Table1rows with the second Path: ",table1rows)    
                  for i in range(table1rows):
                      FeatureTable1List.append(driver.find_element(By.XPATH,'//*[@id="poExpander"]/div[1]/div/table/tbody/tr['+str(i+1)+']/td[1]').text)
                      ValueTable1List.append(driver.find_element(By.XPATH,'//*[@id="poExpander"]/div[1]/div/table/tbody/tr['+str(i+1)+']/td[2]').text)                
                  return FeatureTable1List,ValueTable1List 
                  
### 5.5. Table2 information

The code is similar to the second part of the point 5.4.[Table1 information](#54-table1-information), but this is anohter table located below of the first table.

    def Table2():
        FeatureTable2List=[]
        ValueTable2List=[]
        try:
            WebDriverWait(driver,5).until(EC.presence_of_element_located((By.XPATH,'//*[@id="productDetails_techSpec_section_1"]/tbody/tr')))
        except TimeoutException:
            print("\nTable2: Primary path not found")
            return [],[]
        else:
            table2rows=len(driver.find_elements(By.XPATH,'//*[@id="productDetails_techSpec_section_1"]/tbody/tr'))
            print("\nTable2rows: ",table2rows)
            for i in range(table2rows):
                FeatureTable2List.append(driver.find_element(By.XPATH,'//*[@id="productDetails_techSpec_section_1"]/tbody/tr['+str(i+1)+']/th').text)
                ValueTable2List.append(driver.find_element(By.XPATH,'//*[@id="productDetails_techSpec_section_1"]/tbody/tr['+str(i+1)+']/td').text)
            return FeatureTable2List,ValueTable2List
              
### 5.6. Table3 information

The code is similar to the second part of the point 5.4.[Table1 information](#54-table1-information), but this is anohter table located by the second table.

    def Table3():
        FeatureTable3List=[]
        ValueTable3List=[]
        try:
            WebDriverWait(driver,5).until(EC.presence_of_element_located((By.XPATH,'//*[@id="productDetails_detailBullets_sections1"]/tbody/tr')))
        except TimeoutException:
             print("\nTable3: Primary path not found")
             return [],[]
        else:
            table3rows=len(driver.find_elements(By.XPATH,'//*[@id="productDetails_detailBullets_sections1"]/tbody/tr'))
            print("\nTable3rows: ",table3rows)
            for i in range(table3rows):
                FeatureTable3List.append(driver.find_element(By.XPATH,'//*[@id="productDetails_detailBullets_sections1"]/tbody/tr['+str(i+1)+']/th').text)
                ValueTable3List.append(driver.find_element(By.XPATH,'//*[@id="productDetails_detailBullets_sections1"]/tbody/tr['+str(i+1)+']/td').text)
            return FeatureTable3List,ValueTable3List

## 6. Data Article

<p align="justify">
In this part I'm going to extract information such as title, price and table information from three tables are on the page of a product or article. The picture below is the first Table, and sometimes there is a expander prompt, it's necessary click on that expander to reveal the information.
</p>

<p align="center">
  <img src="https://github.com/JesusAcuna/Web-scraping-on-the-Amazon-Website/blob/main/images/image_3.jpg">
</p>

1. First part

* In the first **for** loop, set the number of pages, and skip the first page since we are on the first page.
* Then I got the number of articles with the function "**NumberofArticles()**". See point 5.1.[Number of articles](#51-number-of-articles) 

2. Second part

* The **while** loop will move through all products on a specific page
* All the products on a specific page start with a XPATH: //[@id="search"]/div[1]/div[1]/div/span[3]/div[2]/div[2+i], also there are two XPATHS that the products have.
* Then I got the article title with the function "**Title()**". See point 5.2.[Article title](#52-article-title)
* Then I got the article price with the function "**Price()**". See point 5.3.[Article price](#53-article-price)
* Then I got the Table1 information with the function "**Table1()**". See point 5.4.[Table1 information](#54-table1-information), and so on with the Table2 and Table3

3. Third part

* The information of the tables are integrated in one variable for both values[**ValueTableList**] and features[**FeatureTableList**]

4. Fourth part

* The information of the tables about one product is append to **FeaturesList**, **ValuesList**
* driver.back() return to the previous page
* driver.quit() shut down the web driver object

      #List of product titles and prices 
      TitleList=[]
      PriceList=[]
      #List of product table features
      FeaturesList=[]
      ValuesList=[] 
      #Total number of articles
      TotalNumberofArticles=0 
      for j in range(int(numberofpages)):
          if j>0:
              driver.get(url+'/s?k='+articlename+'&page='+str(j+1))
          #Go to point 5. Number or articles 
          numberofarticles=NumberofArticles()
          print("Number of articles on page: ",j+1,"is equal to: ",numberofarticles)
          counter=0                                    #article number counter
          i=0                                          #iterator to increment XPATH
          TotalNumberofArticles+=numberofarticles
          #Second part
          while (counter<numberofarticles):
              try:         
                  WebDriverWait(driver,3).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="search"]/div[1]/div[1]/div/span[3]/div[2]/div['+str(2+i)+']/div/div/div/div/div/div/div/div[2]/div/div/div[1]/h2/a/span'))).click()
              except TimeoutException:
                  try:                            
                      WebDriverWait(driver,3).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="search"]/div[1]/div[1]/div/span[3]/div[2]/div['+str(2+i)+']/div/div/div/div/div/div[2]/div/div/div[1]/h2/a/span'))).click()                
                  except TimeoutException:  
                      i+=1                        
                      continue                    
              #********** Get article titles **********#Go to point 5.2. Article title
              TitleList.append(Title())
              #********** Get article prices **********#Go to point 5.3. Article price
              PriceList.append(Price())
              #******** Get Table1 information ********#Go to point 5.4. Table1 Information
              FeatureTable1List,ValueTable1List=Table1()
              #******** Get Table2 information ********#Go to point 5.5. Table2 Information
              FeatureTable2List,ValueTable2List=Table2()
              #******** Get Table3 information ********#Go to point 5.6. Table3 Information
              FeatureTable3List,ValueTable3List=Table3()
              #Third part
              #**************************  Get Table information ************************#
              FeatureTableList=FeatureTable1List+FeatureTable2List+FeatureTable3List
              ValueTableList=ValueTable1List+ValueTable2List+ValueTable3List
              #**************************************************************************#
              i+=1                                
              counter+=1                          
              print("***************************************************************")
              print("Article #",counter,"Page #",j+1) 
              print("Feature length of tables: ",len(FeatureTableList)) 
              print("Value length of tables: ",len(ValueTableList))
              #Fourth Part
              FeaturesList.append(FeatureTableList)
              ValuesList.append(ValueTableList)
              driver.back()                          #return to the previous page
      driver.quit()                                  #shut down the web driver object

## 7. Get Dataframe

<p align="justify">
Now we have information about the price and title of the products,but I need to generate a union of the features, that's why I created a FeatureSet=set() with all the features of all the products.
</p>

Then I started filling the lists, if a product possessed that feature it was placed, if it was not placed blank.

      import pandas as pd

      DataArticle={}
      DataArticle['Price']=PriceList
      DataArticle['Title']=TitleList
      FeaturesSet=set()
      for l in range(TotalNumberofArticles):
          FeaturesSet=FeaturesSet | set(FeaturesList[l])
      for m in FeaturesSet:
          List=[]
          for n in range(TotalNumberofArticles):
              if(m in set(FeaturesList[n])):
                  Index=FeaturesList[n].index(m)
                  List.append(ValuesList[n][Index])
              else:
                  List.append('')
          DataArticle[m]=List
      #Data frame building
      columnsDF=['Title','Price']
      for i in FeaturesSet:
          columnsDF.append(i)
      df=pd.DataFrame(DataArticle,columns=columnsDF)
      print("***************************************************************")
      df
      df.to_csv('ArticleData.csv')

## 8. References

  - Web
  
      https://selenium-python.readthedocs.io/
      
  - Kaggle notebook
  
      https://www.kaggle.com/code/jesusacunamorillo/web-scraping-on-amazon-with-selenium-python/notebook
      
  - Youtube
  
      Tech Path

      https://www.youtube.com/watch?v=WIExbhe_GWc&t
      
      NovelTech Media

      https://www.youtube.com/watch?v=RMPpS6KBkgg

      Nicolas Alvarez

      https://www.youtube.com/watch?v=AjTpmMw-Pe4&list=PLas30d-GGNa2UW9-1H-NCNrUocvWD9cyh&index=1
  
