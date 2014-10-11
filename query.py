import urllib as ur
import json

base_url = "http://api.autoidlabs.ch/"

def printout(func):
    print(func.read())

def Products():
    #Product Info
    product_ean = "7610200243430"
    n = "1"
    #productinfo_url = base_url + "products/" + product_ean + "?n=" + n
    #f = ur.urlopen(productinfo_url)
    #printout(f)

    #Likes
    likes_url = base_url + "likes/" + product_ean
    f = ur.urlopen(likes_url)
    printout(f)

    #Rating
    rating_url = base_url + "rating/" + product_ean
    f = ur.urlopen(rating_url)
    printout(f)

    #Availability
    store_id = "0150116"
    avail_url = base_url + "availability/" + product_ean + "?store_id=" + store_id
    f = ur.urlopen(avail_url)
    printout(f)

    #Product Articles
    prodarticles_url = base_url + "prodarticles/" + product_ean
    f = ur.urlopen(prodarticles_url)
    printout(f)

    #Article Details
    article_id = "10000"
    article_url = base_url + "articles/" + article_id
    f = ur.urlopen(article_url)
    printout(f)

    #Discounts
    discounts_url = base_url + "discounts"
    f = ur.urlopen(discounts_url)
    printout(f)

    #Search
    text = "water"
    search_url = base_url + "search?text=" + text
    f = ur.urlopen(search_url)
    printout(f)

def Categories():
    #categories_url = base_url + "categories"
    #f = ur.urlopen(categories_url)
    #printout(f)
    category_id = "22415"
    categoryinfo_url = base_url + "/categories/" + category_id
    f = ur.urlopen(categoryinfo_url)
    printout(f)

def Brands():
    brands_url = base_url + "brands?search="
    brands_product_url = base_url + "/brandproducts/"
    term = "Lindt"
    #f = ur.urlopen(brands_url + "{" + term + "}")
    brand_id = "17"
    f = ur.urlopen(brands_product_url + brand_id )
    print(f.read())

def PoS():
    cusid_url = base_url + "customerids"
    f = ur.urlopen(cusid_url)
    cus_return = f.read()
    customer_ids = cus_return[1:-1].split(',')

def main():
    #Products()
    Categories()
    #Brands()
    #PoS()


if __name__ == "__main__":
    main()
