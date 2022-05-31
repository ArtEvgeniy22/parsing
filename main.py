import json

import requests
from bs4 import BeautifulSoup
import os


# Getting main page src
def get_src():
    # Getting src
    url = 'https://atlas.ru/blog/'
    req = requests.get(url)
    src = req.text

    # Saving src
    with open('index.html', 'w', encoding='utf-8') as file:
        file.write(src)


# Categories pages src
categories_list = []

# Articles
articles_list = []


# Getting src of category's pages
def categories():
    # Getting src
    with open('index.html', 'r', encoding='utf-8') as file:
        src = file.read()

    # Soup tool
    soup = BeautifulSoup(src, 'lxml')

    # Getting categories info
    all_categories = soup.find_all(class_='col-md-3 col-xs-4 col-xxs-6 col-12')

    for category in all_categories:
        page = 1
        while True:
            category_name = f"{category.find(class_='tag__info').find(class_='tag__name').text}_{page}"
            category_href = \
                f"https://atlas.ru/{category.find(class_='tag__info').find(class_='tag__name').get('href')}page/{page}/"

            req = requests.get(category_href)
            category_src = req.text
            soup = BeautifulSoup(category_src, 'lxml')

            error = soup.find(class_='p-404__img')

            if error:
                break
            else:
                categories_dict = {category_name: category_href}
                categories_list.append(categories_dict)
                print(categories_dict)
                page += 1

    # Saving html-code of all categories
    n = 1
    for dictionary in categories_list:
        title = list(dictionary.keys())[0]
        href = list(dictionary.values())[0]

        req = requests.get(href)
        category_src = req.text

        # Writing down page's src
        try:
            # Creating directory
            os.mkdir('categories')
            with open(f'categories/{title}.html', 'w', encoding='utf-8') as file:
                file.write(category_src)
        except FileExistsError:
            # If directory exists
            check_file = os.path.exists(f'categories/{title}.html')
            # If file exists
            if check_file:
                continue
            else:
                with open(f'categories/{title}.html', 'w', encoding='utf-8') as file:
                    file.write(category_src)

        print(f'#{n} File {title}.html successfully created')
        n += 1


# Getting article's info
def articles():
    files_names = os.listdir('categories')

    # Reading categories src files
    for name in files_names:
        with open(f'categories/{name}', 'r', encoding='utf-8') as file:
            src = file.read()

        soup = BeautifulSoup(src, 'lxml')

        # Getting articles info
        all_articles = \
            soup.find(class_='posts-list').find_all(class_='posts-list__item col-lg-3 col-sm-4 col-xs-6 col-12')
        for article in all_articles:
            article_category = name.split('_')[0]
            article_title = article.find(class_='item-post__info').find(class_='item-post__title').text
            article_date = article.find(class_='item-post__info').find(class_='post-meta__date').text
            article_timing = article.find(class_='item-post__info').find(class_='post-meta__reading').text
            article_href = \
                f"https://atlas.ru/{article.find(class_='item-post__info').find(class_='item-post__title').get('href')}"

            article_dict = {
                'category': article_category,
                'title': article_title,
                'date': article_date,
                'timing': article_timing,
                'url': article_href
            }
            articles_list.append(article_dict)


# Saving article's info in json-file
def articles_csv():
    with open('data.json', 'a', encoding='utf-8') as file:
        json.dump(articles_list, file, indent=4, ensure_ascii=False)


def main():
    # get_src()
    # categories()
    articles()
    articles_csv()


if __name__ == '__main__':
    main()
