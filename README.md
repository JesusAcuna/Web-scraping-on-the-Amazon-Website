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
  

- 4.[Setting up the virtual environment](#4-setting-up-the-virtual-environment)
- 5.[Importing data](#5-importing-data)
- 6.[Notebook](#6-notebook)
  - 6.1.[Exploratory Data Analysis (EDA)](#61-exploratory-data-analysis-eda)
  - 6.2.[Model selection and parameter tuning](#62-model-selection-and-parameter-tuning)
- 7.[Instructions on how to run the project](#7-instructions-on-how-to-run-the-project)
- 8.[Locally deployment](#8-locally-deployment)
- 9.[Google Cloud deployment (GCP)](#9-google-cloud-deployment-gcp)
- 10.[References](#10-references)
---
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

## 10. References

  - Web
  
      https://selenium-python.readthedocs.io/
  
  - Youtube
  
      Tech Path

      https://www.youtube.com/watch?v=WIExbhe_GWc&t
      
      NovelTech Media

      https://www.youtube.com/watch?v=RMPpS6KBkgg

      Nicolas Alvarez

      https://www.youtube.com/watch?v=AjTpmMw-Pe4&list=PLas30d-GGNa2UW9-1H-NCNrUocvWD9cyh&index=1
  
