import requests
import sqlite3
import json
import kanboard

redwing = 'https://www.nordstromrack.com/api/search2/catalog/search?includeFlash=true&includePersistent=true&limit=99&page=1&query=red%20wing&sort=relevancy&nestedColors=false&site=nordstromrack'


def kanboardpost(board, content):
    #enable API access in kanboard and get url + token
    url = ''
    name = ''
    token = ''
    kb = kanboard.Client(url, name, token)
    newsubtask = kb.create_subtask(task_id=board, title=content)

def scrape(brand):
    sql = sqlite3.connect('bootsdb.db')
    cur = sql.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS boots(brand TEXT, product TEXT, price TEXT, link TEXT)')
    
    html_doc = requests.get(brand)
    results = []
    result = json.loads(html_doc.content)
    for each in result["_embedded"]["http://hautelook.com/rels/products"]:
        brand = each['brand_name']
        if (brand == 'RED WING'):
            name = each['name']
            price = each['_embedded']['http://hautelook.com/rels/skus'][0]['price_sale']
            link = each['_links']['alternate']['href']
            sizes = each['_embedded']['http://hautelook.com/rels/skus'][0]['size']
            products = cur.execute("SELECT product FROM boots").fetchall()
            if name not in str(products):
                link = link.replace("//","").split('{')[0]
                results.append([brand, name, price, link, sizes])
                cur.execute('INSERT INTO boots VALUES(?, ?, ?, ?)', [brand, name, price, link])
                kanboardpost(120, f'new item: {brand} - {name} ${price} | {link} | {sizes} available')
                print(brand, name, price, link, sizes)
    sql.commit()
    sql.close()
    return results
    
scrape(redwing)
