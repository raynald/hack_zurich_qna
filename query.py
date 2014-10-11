import urllib as ur
import json
import sys
import random

base_url = "http://api.autoidlabs.ch"


def load(y,x):
    iurl = '%s/%s/%s' % (base_url, y, x)
    print iurl
    f = ur.urlopen(iurl)
    data = f.read()
    return data

OneArg = lambda y:  lambda x: load(y, x)

ProductsRating = OneArg('rating')
ProductsLikes = OneArg('likes')
ProductsArticles = OneArg('prodarticles')
ArticlesDetail = OneArg('articles')


def ProductsInfo(product_ean, n):
    """
        Product Info
        product_ean = "7617027539036"
        n = "0"
    """
    productinfo_url = '%s/products/%s?n=%s' % (base_url,  product_ean, n)
    f = ur.urlopen(productinfo_url)
    productout = json.loads(f.read())
    return productout

def ProductsAvail():
    #Availability
    store_id = "0150116"
    avail_url = base_url + "/availability/" + product_ean + "?store_id=" + store_id
    f = ur.urlopen(avail_url)
    print(f.read())

def ProductsDetails(article_id):
    #Article Details
    #article_id = "10000"
    article_url = base_url + "/articles/" + str(article_id)
    f = ur.urlopen(article_url)
    print(f.read())

def ProductsDiscounts():
    #Discounts
    discounts_url = base_url + "/discounts"
    f = ur.urlopen(discounts_url)
    print(f.read())

def ProductsSearch():
    #Search
    text = "wasser"
    search_url = base_url + "/search?text=" + text
    f = ur.urlopen(search_url)
    print(f.read())

def AllCategories():
    categories_url = base_url + "/categories"
    f = ur.urlopen(categories_url)
    cateout = json.loads(f.read())
    return cateout

def AllLeafCategories():
    all_cat = AllCategories()

    def AllLeaves(cat):
        if 'catMbrs' not in cat:
            yield cat
        else:
            for subcat in cat['catMbrs']:
                for mbrs in AllLeaves(subcat):
                    yield mbrs

    return AllLeaves(all_cat)

def Categories_info(category_id):
    #category_id = "22415"
    categoryinfo_url = base_url + "/categories/" + category_id
    f = ur.urlopen(categoryinfo_url)
    cateout = json.loads(f.read())
    return cateout

def Brands():
    brands_url = base_url + "/brands?search="
    brands_product_url = base_url + "/brandproducts/"
    term = "Lindt"
    #f = ur.urlopen(brands_url + "{" + term + "}")
    brand_id = "17"
    f = ur.urlopen(brands_product_url + brand_id )
    print(f.read())

def transaction(customer_id):
    """
    Example:
    u'quantNorm': 1, u'pricePerUnit': 0.99, u'migrosEan': u'7617027659239', u'receiptId': u'1714034704', u'id': 106, u'rDate': u'2014-10-01T00:00Z', u'custId': 115883, u'price': 0.99}, {u'quantNorm': 1, u'pricePerUnit': 2.19, u'migrosEan': u'7613269310006', u'receiptId': u'1718833507', u'id': 3629, u'rDate': u'2014-10-05T00:00Z', u'custId': 115883, u'price': 2.19}
    """
    #customer_id = "115883"
    posdata_url = '%s/pos/%s' % (base_url, customer_id)
    f = ur.urlopen(posdata_url)
    posout = json.loads(f.read())
    return posout


def all_customer_id():
    cusid_url = '%s/customerids' % base_url
    f = ur.urlopen(cusid_url)
    cus_return = f.read()
    return cus_return[1:-1].split(',')

def main():
    Products()
    #Categories()
    #Brands()
    #PoS()

if __name__ == "__main__":
    pass
