import requests 
from bs4 import BeautifulSoup
import pandas as pd 
import time 
from deep_translator import GoogleTranslator

url = "https://allrecipes.com"

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

translator = GoogleTranslator(source='en', target='ru')

print("Робот-парсер запущен. Заходим на сайт...")

try:
    response = requests.get(url, headers=headers, timeout=10)

    if response.status_code == 200: 
        soup = BeautifulSoup(response.text, 'html.parser')

        recipe_cards = soup.find_all('a', class_='mntl-card-list-items')

        titles = []
        links = []
        real_ingredients = [] 
        real_steps = []

        print(f" Найдено реальных блюд на странице: {len(recipe_cards)}. Начинаем чистый сбор...")

        count = 0 
        for card in recipe_cards:
            title_element = card.find('span', class_='card__title-text')
            recipe_url = card.get('href')

            if title_element and recipe_url:
                title_en = title_element.text.strip()

                time.sleep(1)
                inner_response = requests.get(recipe_url, headers=headers, timeout=10)
                if inner_response.status_code == 200:
                    inner_soup = BeautifulSoup(inner_response.text, 'html.parser')

                    ing_tags = inner_soup.find_all('span', class_='mm-recipes-structured-ingredients__list-item')
                    if not ing_tags:
                        ing_tags = inner_soup.find_all('li', class_='mm-recipes-structured-ingredients__list-item')

                    ings_en = ",".join([ing.text.strip() for ing in ing_tags])

                    step_tags = inner_soup.find_all('p', class_='comp mntl-sc-block mntl-sc-block-html')
                    steps_en = " ".join([f"{i+1}. {step.text.strip()}" for i, step in enumerate(step_tags)])

                    if ings_en and steps_en:
                        title_ru = translator.translate(title_en)
                        ings_ru = translator.translate(ings_en)
                        steps_ru = translator.translate(steps_en)

                        titles.append(title_ru)
                        links.append(recipe_url)
                        real_ingredients.append(ings_ru)
                        real_steps.append(steps_ru)
                        print(f"Успешно выкачан оригинальный состав и шаги!")
                        count += 1
                    else: 
                        print("Не удалось разобрать структуру этой страницы, пропускаем...")

                if count >= 3: 
                    break 

        df_scraped = pd.DataFrame({
            'Название': titles, 
            'Ссылка': links,
            'Ингредиенты': real_ingredients, 
            'Шаги': real_steps 
        })

        df_scraped.to_csv("recipes_database.csv", index=False, encoding="utf-8")
        print("\n База данных успешно создана и сохранена в файл 'recipes_database.csv' !")

except Exception as e: 
    print(f" Произошла ошибка при парсинге: {e}")
