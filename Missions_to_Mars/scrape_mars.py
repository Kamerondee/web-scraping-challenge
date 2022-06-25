# Import your dependancies
from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager

# Store as dictionary and return your list
def scrape_all():

    # Create the path and browser
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=True)
    
    news_title, news_paragraph = mars_news(browser)

    listing = {
        "news_title": news_title(),
        "news paragraph": news_paragraph(),
        "mars_img": mars_img(browser),
        "mars_facts": mars_facts(),
        "mars_hems": mars_hems()
    }
    return listing

def mars_news(browser):

    url = "https://data-class-mars.s3.amazonaws.com/Mars/index.html"
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')
    
    news_title = soup.find_all('div', class_="content_title")[0].text
    news_paragraph = soup.find_all('div', class_="article_teaser_body")[0].text
    
    browser.quit()
    return news_title, news_paragraph


def mars_img(browser):
    url = "https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html"
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')
    feat_images = soup.find_all('img', class_="headerimage")
    feat_jpg_url = url + feat_images[0].attrs['src']
    
    browser.quit()
    return {"feat_img_url": feat_jpg_url}

def mars_facts():
    try:
        mars_df = pd.read_html('https://data-class-mars-facts.s3.amazonaws.com/Mars_Facts/index.html')[0]

    except BaseException:
        return None

    mars_df.columns=['Description', 'Mars', 'Earth']
    mars_df.set_index('Description', inplace=True)

    return mars_df.to_html(classes="table table-striped")

def mars_hems(browser):
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)
    
    hemisphere_image_urls = []

    imgs_links= browser.find_by_css("a.product-item h3")

    for x in range(len(imgs_links)):
        hemisphere={}

        browser.find_by_css("a.product-item h3")[x].click()

        sample_img= browser.links.find_link_by_text("Sample").first
        hemisphere['img_url']=sample_img['href']

        hemisphere['title']=browser.find_by_css("h2.title").text

        hemisphere_image_urls.append(hemisphere)

        browser.back()
    return hemisphere_image_urls
    
if __name__ == "__main__":

    print(scrape_all())