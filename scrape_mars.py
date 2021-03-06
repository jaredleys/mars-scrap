from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd

def scrape():
    executable_path = {'executable_path':'C:\\Users\\jared\\Downloads\\chromedriver_win32\\chromedriver.exe'}
    browser = Browser('chrome', **executable_path)

    url = "https://redplanetscience.com/"
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    title = soup.find('div', class_='content_title').text
    blurb = soup.find('div', class_='article_teaser_body').text
    image = soup.find('div', class_='list_image').img['src']

    url = "https://galaxyfacts-mars.com"
    tables = pd.read_html(url)
    mars_df = tables[0]
    mars_df = mars_df.iloc[1:]
    headers = ['Measurement', 'Mars', 'Earth']
    mars_df.columns = headers
    mars_df = mars_df.drop("Earth", axis=1).set_index('Measurement')
    mars_table = mars_df.to_html()

    url = "https://marshemispheres.com/"
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='item')
    hemispheres = []
    img_url = []
    for x in items:
        href = x.find('a')['href']
        browser.visit(url + href)
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        hemisphere = soup.find('h2', class_='title').text.split(' Enhanced')
        hemispheres.append(hemisphere[0])
        div = soup.find('div', class_='downloads')
        images = div.find_all('a')
        image_href = images[0]['href']
        img_url.append(url + image_href)

    hemisphere_dicts = []
    for (i,j) in zip(hemispheres, img_url):
        dictionary = {"title":i,"img_url":j}
        hemisphere_dicts.append(dictionary)

    browser.quit()

    mars_info = {
        'news_title':title,
        'news_blurb':blurb,
        'news_img':image,
        'table':mars_table,
        'hemispheres':hemisphere_dicts
    }

    return mars_info