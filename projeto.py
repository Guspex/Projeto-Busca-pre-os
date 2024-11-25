import streamlit as st
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

def add_background(image_url):
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("{image_url}");
            background-size: contain;
            background-repeat: no-repeat;
            background-position: center;
        }}
        .stButton > button {{
            display: block;
            margin: 0 auto;
        }}
        .result-container {{
            width: 100%;
            max-width: 700px;
        }}

        </style>
        """,
        unsafe_allow_html=True
    )

image_url = "https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/20fc0797-715c-40bf-812a-a2206be0df60/dbnjkk4-166b6b8e-1eaf-4dcf-8be5-106b94c3c9d1.jpg/v1/fill/w_907,h_881,q_70,strp/second_mtg_mana_symbols_commission_by_vitrigeek_dbnjkk4-pre.jpg?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOjdlMGQxODg5ODIyNjQzNzNhNWYwZDQxNWVhMGQyNmUwIiwiaXNzIjoidXJuOmFwcDo3ZTBkMTg4OTgyMjY0MzczYTVmMGQ0MTVlYTBkMjZlMCIsIm9iaiI6W1t7ImhlaWdodCI6Ijw9OTk0IiwicGF0aCI6IlwvZlwvMjBmYzA3OTctNzE1Yy00MGJmLTgxMmEtYTIyMDZiZTBkZjYwXC9kYm5qa2s0LTE2NmI2YjhlLTFlYWYtNGRjZi04YmU1LTEwNmI5NGMzYzlkMS5qcGciLCJ3aWR0aCI6Ijw9MTAyNCJ9XV0sImF1ZCI6WyJ1cm46c2VydmljZTppbWFnZS5vcGVyYXRpb25zIl19.lqLkQK089T1oiDsAR28hixWoNMh-KddcbTsSXSe0aiU"
add_background(image_url)

def fetch_card_prices_with_selenium(card_list):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    base_url = "https://www.ligamagic.com.br/"
    data = []

    for card in card_list:
        try:
            query = card.replace(" ", "+")
            url = f"{base_url}?view=cards/card&card={query}"
            driver.get(url)

            price_element = driver.find_element(By.XPATH, '//*[@id="container-price-mkp-card"]/div[2]/div[2]/div[1]/div')
            price = price_element.text.strip()

            data.append({"Card": card, "Preço": price})
        except Exception as e:
            data.append({"Card": card, "Preço": f"Erro: {e}"})

    driver.quit()

    df = pd.DataFrame(data)
    return df

# Interface Streamlit
st.title("Consulta de Preços de Cartas Magic")

# Caixa de texto para os nomes dos cards
card_input = st.text_area("Digite os nomes dos cards separados por ponto e vírgula (;):", height=200)

if st.button("Pesquisar"):
    if card_input:
        cards = [card.strip() for card in card_input.split(";")]

        # Buscar preços
        card_prices_df = fetch_card_prices_with_selenium(cards)

        # Exibe os resultados centralizados
        with st.container():
            st.markdown('<div class="result-container">', unsafe_allow_html=True)
            st.write("**Resultados encontrados:**")
            st.dataframe(card_prices_df, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        st.success("Busca concluída com sucesso!")
    else:
        st.error("Por favor, insira ao menos um nome de card.")
