import os
from glob import glob
from bs4 import BeautifulSoup

prices = []
images = []
sizes = []
description = {}
colors = []
final_list = []
second_list = []


def first(soup):
    title = soup.find('h1').text

    product_price = ''
    product_price_items = ''

    try:
        product_price = soup.find(class_='productView-info-bulkPricing').find(class_='price-list').findAll(class_='price')
        product_price_items = soup.find(class_='productView-info-bulkPricing').find(class_='price-list'). \
        findAll(class_='range')
    except:
        pass

    if product_price and product_price_items:
        for price, items in zip(product_price, product_price_items):
            price = price.text.strip()
            item = items.text
            prices.append({
                'price': price,
                'count': item
            })

    try:
        size = soup.find(class_='size-container').findAll(class_="size-option-container")
        for s in size:
            s = s.find(class_='form-option-variant').text
            sizes.append({
                "name": s
            })
    except:
        pass

    try:
        pictures = soup.find(class_='slick-track').findAll(class_='zoomImg')
        for picture in pictures:
            picture = picture.get('src')
            images.append(picture)
    except:
        pass

    try:
        desc_name = soup.find(class_='description').find(class_='title').text
        desc_content = soup.find(class_='description').find(class_='content').text
        description[desc_name] = desc_content
    except:
        pass

    first_dict = {
        "title": title,
        "prices": prices,
        "size": sizes,
        "pictures": images,
        "description": description
    }

    final_list.append(first_dict)
    return final_list


def second(soup):
    try:
        colour_name = soup.find("span", {"id": 'colour-value-container'}).text
        if colour_name:
            img = soup.find(class_='zoomImg').get('src')
        cols = soup.find(class_='swatch-container').findAll(class_='form-option-swatch')
        for col in cols:
            col_title = col.find(class_='form-option-variant').get('title')
            if col_title == colour_name:
                col_bg = col.find(class_='form-option-variant').get('style').split(': ')[1]
                colors.append({
                    "name": col_title,
                    "code": col_bg,
                    "img": img
                })
    except:
        pass
    second_dict = {
        "colors": colors
    }

    second_list.append(second_dict)
    return second_list


def main():
    paths = glob(os.path.join('html', '*', '*', '*.html'))

    data = {}
    for path in paths:
        _, gender, category, filepath = path.split('\\')

        if gender not in data:
            data[gender] = {}

        if category not in data[gender]:
            data[gender][category] = {}

        filename = filepath.split('.')[0]

        if filename not in data[gender][category]:
            data[gender][category][filename] = []

        data[gender][category][filename].append(filepath)

    for gender, categories in data.items():
        for category, _pages in categories.items():
            for page_name, pages in _pages.items():
                for i, page in enumerate(pages):
                    file_path = os.path.join("html", gender, category, page)

                    with open(file_path, 'r', encoding='utf-8') as f:
                        read_file = f.read()

                    soup = BeautifulSoup(read_file, 'lxml')
                    if i == 0:
                        first(soup)
                    else:
                        second(soup)

                    for x in second_list:
                        for key, value in x.items():
                            for z in final_list:
                                z[key] = value
            print(final_list)


if __name__ == '__main__':
    main()







