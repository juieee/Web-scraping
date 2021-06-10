from requests_html import HTMLSession
import pandas as pd
import time


s = HTMLSession()



#this code will not work with the other def getdata() as only 1 HTML Session
def get_asins(url):
    headers = {
    'user-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36'
    }
    s = HTMLSession()
    r = s.get(url, headers=headers)
    asins = r.html.find('div.s-main-slot div[data-asin]')
    return [asin.attrs['data-asin'] for asin in asins if asin.attrs['data-asin'] != '']


def getdata(asin, x):
    headers = {
    'user-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36'
    }
    s = HTMLSession()
    r = s.get(f'https://www.amazon.co.uk/dp/{asin}', headers = headers)
    #print(r.html.html)
    productname = r.html.find('#productTitle', first=True).full_text.strip()
    try:
        ratingscount = r.html.find('#acrCustomerReviewText', first = True).full_text.strip()
        ratingscount = ratingscount.replace(' ratings','')
    except:
        ratingscount = 0
    
    try:
        ratings = r.html.find('span[id=acrPopover]', first = True).full_text.strip()
        ratings = ratings.replace(' out of 5 stars','')
    except:
        ratings = 'NA'
    
    
    try:
        productdetail1 = r.html.xpath('//*[@id="detailBullets_feature_div"]/ul/li[1]/span/span[1]', first = True).text.strip()
        productdetail1value = r.html.xpath('//*[@id="detailBullets_feature_div"]/ul/li[1]/span/span[2]', first = True).text.strip()
    except:
        productdetail1 = 0
        productdetail1value = 0
    
    try: 
        productdetail2 = r.html.xpath('//*[@id="detailBullets_feature_div"]/ul/li[2]/span/span[1]', first = True).text.strip()
        productdetail2value = r.html.xpath('//*[@id="detailBullets_feature_div"]/ul/li[2]/span/span[2]', first = True).text.strip()
    except:
        productdetail2 = 0
        productdetail2value = 0
    
    try:
        productdetail3 = r.html.xpath('//*[@id="detailBullets_feature_div"]/ul/li[3]/span/span[1]', first = True).text.strip()
        productdetail3value = r.html.xpath('//*[@id="detailBullets_feature_div"]/ul/li[3]/span/span[2]', first = True).text.strip()
    except:
        productdetail3 = 0
        productdetail3value = 0
    
    try:
        productdetail4 = r.html.xpath('//*[@id="detailBullets_feature_div"]/ul/li[4]/span/span[1]', first = True).text.strip()
        productdetail4value = r.html.xpath('//*[@id="detailBullets_feature_div"]/ul/li[4]/span/span[2]', first = True).text.strip()
    except:
        productdetail4 = 0
        productdetail4value = 0
        
    try:     
        productdetail5 = r.html.xpath('//*[@id="detailBullets_feature_div"]/ul/li[5]/span/span[1]', first = True).text.strip()
        productdetail5value = r.html.xpath('//*[@id="detailBullets_feature_div"]/ul/li[5]/span/span[2]', first = True).text.strip()
    except:
        productdetail5 = 0
        productdetail5value = 0
    
    try:
        productdetail6 = r.html.xpath('//*[@id="detailBullets_feature_div"]/ul/li[6]/span/span[1]', first = True).text.strip()
        productdetail6value = r.html.xpath('//*[@id="detailBullets_feature_div"]/ul/li[6]/span/span[2]', first = True).text.strip()
    except:
        productdetail6 = 0
        productdetail6value = 0
    
    try:
        productdetail7 = r.html.xpath('//*[@id="detailBullets_feature_div"]/ul/li[7]/span/span[1]', first = True).text.strip()
        productdetail7value = r.html.xpath('//*[@id="detailBullets_feature_div"]/ul/li[7]/span/span[2]', first = True).text.strip()      
    except:
        productdetail7 = 0
        productdetail7value = 0

    #bestsellersrank = r.html.xpath('/html/body/div[2]/div[2]/div[5]/div[10]/div/div/ul[1]/li/span/span' , first = True).text.strip()
    #bestsellersrank = r.html.find('#detailBulletsWrapper_feature_div > ul:nth-child(5)', first = True)
    

    books = {
        'url_page': x,
        'bookname': productname,
        'asin': asin,
        'ratingscount': ratingscount,
        'ratings': ratings,
        'productdetail1': productdetail1,
        'productdetail1value': productdetail1value,
        'productdetail2': productdetail2,
        'productdetail2value': productdetail2value,
        'productdetail3': productdetail3,
        'productdetail3value': productdetail3value,
        'productdetail4': productdetail4,
        'productdetail4value': productdetail4value,
        'productdetail5': productdetail5,
        'productdetail5value': productdetail5value,
        'productdetail6': productdetail6,
        'productdetail6value': productdetail6value,
        'productdetail7': productdetail7,
        'productdetail7value': productdetail7value,
        #'bestsellersrank': bestsellersrank
        }
    print(books)
    return books
    

booksdatalist = []

    
for x in range (1,21):
    search = 'julia+donaldson+books'    
    url = f'https://www.amazon.co.uk/s?k={search}&page={x}'
    
    #Save the asins in a list
    asins = get_asins(url)
        # Print the number of asins with a f string
    print(f'Found {len(asins)} asins')
    print(asins)
    
    # Need to run the getdata for each asin, use list comprehension to have in one line
    for asin in asins:
        booksdatalist.append(getdata(asin, x))
        time.sleep(3)
    time.sleep(3)




# Create a csv, index is default to fals not to have Panda default index
df = pd.DataFrame(booksdatalist)
df.to_csv(search + '.csv', index=False)


