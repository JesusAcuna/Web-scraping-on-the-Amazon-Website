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
- 2.[Objective](#2-objective)
- 3.[Data description](#3-data-description)
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
  
