
# Dependencies
from bs4 import BeautifulSoup

import requests
import pymongo
import pandas as pd

#from selenium import webdriver
from splinter import Browser
from bs4 import BeautifulSoup

import fileinput

import os

def scrape_mars_func():

    # ## Step 1 - Scraping

    # ### NASA Mars News

    print('\n\n\n############## 1) NASA Mars News ##############\n')
    # URL of page to be scraped
    url = 'https://mars.nasa.gov/news/'
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'

    print(url)
    # Retrieve page with the requests module
    response = requests.get(url)
    print(response)
    # Create BeautifulSoup object; parse with 'lxml'
    soup = BeautifulSoup(response.text, 'lxml')

    #print(soup)

    # Examine the results, then determine element that contains sought info
    # results are returned as an iterable list
    results = soup.find_all('div', class_='slide')

    errores = 0

    posts_list = []

    #print(results)
    # Loop through returned results
    for result in results:
        # Error handling
        try:
            # Identify and return title of listing
            news_title = result.find('div', class_='content_title').a.text
            
            news_title = news_title.replace('\n', '').replace('\r', '')
            #title = title.find('a').text
            #print(title)
            
            # Identify and return price of listing
            news_p = result.find('div', class_='rollover_description_inner').text
            
            news_p = news_p.replace('\n', '').replace('\r', '')
            #print(description)
            
            # Identify and return link to listing
            news_link = result.find('div', class_='content_title').a['href']
            #print(link)
            
            # Run only if title, price, and link are available
            if (news_title and news_p and news_link):
                # Print results
                #print('-------------')
                #print(news_title)
                #print(news_p)
                #print(news_link)


                # Dictionary to be inserted as a MongoDB document
                post = {
                    'news_title': news_title,
                    'news_p': news_p,
                    'news_link': news_link
                }
                #print(post)
                #collection.insert_one(post)
                posts_list.append(post)


        except Exception as e:
            errores =+ 1


    print(posts_list)


    # 
    # ### JPL Mars Space Images - Featured Image

    print('\n\n\n############## 2) JPL Mars Space Images - Featured Image ##############\n')

    os.system('which chromedriver')

    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)


    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    #print(soup)


    quotes = soup.find_all('article')

    pre = 'https://www.jpl.nasa.gov'
    url = ""

    for quote in quotes:
        try:
            #print(quote['style'])
            url = quote['style']
            s = url.split("'")
            featured_image_url = pre + s[1]


        except Exception as e:
            print(f'Error: {e}')



    #print(soup)

    #quotes = soup.find_all('img')

    #for quote in quotes:
    #   if 'spaceimages' in quote['src']:
    #      print(quote['src'])
        


    print(featured_image_url)


    # 
    # ### Mars Weather - Twitter: @marswxreport

    print('\n\n\n############## 3) Mars Weather - Twitter: @marswxreport ##############\n')

    os.system('which chromedriver')

    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)

    url = 'https://twitter.com/marswxreport'
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    #soup

    results = soup.find_all('p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text')

    errores = 0

    mars_weather = ''

    #print(results)
    # Loop through returned results
    for result in results:
        # Error handling
        try:
            # Identify and return title of listing
            if 'high' in result.text and 'low' in result.text:
                #print(result.text)
                s = result.text.split("pic.")
                print(s[0])
                mars_weather = s[0]
                break
            

        except Exception as e:
            print(e)
    

    print(mars_weather)


    # ### Mars Facts - space-facts.com/mars/
    print('\n\n\n############## 4) Mars Facts - space-facts.com/mars/ ##############\n')


    url = 'https://space-facts.com/mars/'

    tables = pd.read_html(url)


    type(tables)

    df = tables[0]
    df.columns = ['KPI', 'Data']
    df.head()


    html_table = df.to_html(index=False, border=None)


    html_table = html_table.replace('\n', '')


    html_table = html_table.replace('<table border="1" class="dataframe">', '<table class="table">')
    html_table = html_table.replace('<thead>', '<thead class="thead-dark">')
    html_table = html_table.replace('<tr style="text-align: right;">', '<tr>')

    html_table = html_table.replace('<th>', '<th scope="col">')


    df.to_html(buf='output/table.html',index=False, border=None)


    with fileinput.FileInput('output/table.html', inplace=True) as file:
        for line in file:
            print(line.replace('<table border="1" class="dataframe">', '<table class="table">').replace('<thead>', '<thead class="thead-dark">').replace('<tr style="text-align: right;">', '<tr>').replace('<th>', '<th scope="col">'),end='')


    #os.system('open output/table.html')




    # ### Mars Hemispheres - USGS Astrogeology site
    print('\n\n\n############## 5) Mars Hemispheres - USGS Astrogeology site ##############\n')

    os.system('which chromedriver')

    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)

    url = 'https://astrogeology.usgs.gov/maps/mars-viking-hemisphere-point-perspectives'
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    #print(soup)


    utl_pt = 'https://astrogeology.usgs.gov'

    page_list = []

    results = soup.find_all('a', class_='item')

    for resl in results:
        try:
            #print(quote['style'])
            #print(resl['href'])
            url_to_process = resl['href']
            new_url = utl_pt + url_to_process
            page_list.append(new_url)

        except Exception as e:
            print(f'Error: {e}')

    print(page_list)



    hemisphere_image_urls = []

    for url_to_process in page_list:
        print('--------------------')
        print('processing: ' + url_to_process)
        browser.visit(url_to_process)

        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')

        #print(soup)
        
        ## find title
        result_title = soup.find_all('h2', class_='title')

        title = ''

        try:
            print(result_title[0].text)
            title = result_title[0].text
        except Exception as e:
            print(f'Error: {e}')
            title = 'Error'


        result_img = soup.find_all('img', class_='wide-image')

        #print(results)

        try:
            print(result_img[0]['src'])
            img_url = result_img[0]['src']
        except Exception as e:
            print(f'Error: {e}')
            img_url = 'Error'

        dict_tmp = {}
        dict_tmp['title'] = title
        dict_tmp['img_url'] = utl_pt + img_url
        #print(resl['href'])
        hemisphere_image_urls.append(dict_tmp)


    print('\n')

    print(hemisphere_image_urls)

    ##### Passing into a dictionary
    print('\n\n##### Passing into a dictionary\n\n')
    dict_info = {}
    dict_info['posts_list'] = posts_list
    dict_info['featured_image_url'] = featured_image_url
    dict_info['mars_weather'] = mars_weather
    dict_info['space_facts_html'] = 'output/table.html'
    dict_info['hemisphere_image_urls'] = hemisphere_image_urls

    return dict_info





