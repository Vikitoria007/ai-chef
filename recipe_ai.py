import streamlit as st 
import pandas as pd
import os 

st.set_page_config(page_title="ИИ Шеф-Повар", page_icon="🧑‍🍳", layout="centered")

st.title("🧑‍🍳 Персональный ИИ Шеф-Повар")
st.markdown("### Найди идеальный рецепт по любому запросу с помощью искусственного интеллекта!")

st.info("Введите продукты, которые у вас есть дома, и наш ИИ подберет рецепты из базы данных!")

if os.path.exists("recipes_database.csv"):
    df = pd.read_csv ("recipes_database.csv")
else: 
    st.error("База данных не найдена! Сначала запустите parcer.py!")
    st.stop()

BASE_INGREDIENTS = ['соль', 'сахар', 'вода', 'перец', 'масло', 'мука']

user_query = st.text_input(
    "Что у вас в холодильнике? (Введите продукты через запятую)",
    placeholder="Например: курица, сыр, чеснок, томаты"
)

if st.button("Найти рецепт", type="primary"):
    if user_query: 
        fridge = [i.strip().lower() for i in user_query.split(',')]
        allowed_products = fridge + BASE_INGREDIENTS

        st.write("### Вот что нашел наш ИИ Шеф в собранной бае:")
        found_any = False

        for index, row in df.iterrows():
            recipe_text = row['Ингредиенты'].lower()
            recipe_name = row['Название']
            recipe_link = row['Ссылка']
            recipe_steps = row['Шаги']

            keywords = ['курица', 'сыр', 'чеснок', 'томат', 'лук', 'картошка', 'бекон', 'молоко', 'яйца', 'грибы']
            needed_in_recipe = [word for word in keywords if word in recipe_text or word in recipe_name.lower()]

            missing_ingredients = [ing for ing in needed_in_recipe if ing not in allowed_products]

            if len(missing_ingredients) == 0 and len(needed_in_recipe) > 0: 
                found_any = True 
                with st.expander(f"{recipe_name}"):
                    st.write(f"**Состав:** {row['Ингредиенты']}")
                    st.write(f"**Инструкция по приготовлению:** {recipe_steps}")
                    st.markdown(f"[Открыть оригинальный рецепт на Allrecipes]{recipe_link}")

        if not found_any:
            st.error("К сожалению, из этих ингредиентов ничего не найдено в нашей базы.")
    else: 
        st.warning("Пожалуйста, введите ингредиенты!")
