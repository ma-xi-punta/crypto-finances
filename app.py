import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt

API_URL = "http://127.0.0.1:8000"  

st.set_page_config(layout="wide")

# Estilo y título centrado
st.markdown(
    """
    <style>
        .title-container {
            text-align: center;
            margin-top: -60px;
        }
    </style>
    <div class="title-container">
        <h1>🪙 Crypto Portfolio Tracker 💰</h1>
    </div>
    """,
    unsafe_allow_html=True
)

# Función para cachear la obtención de datos
@st.cache_data(ttl=300)  # Cachea por 5 minutos
def get_transactions():
    response = requests.get(f"{API_URL}/api/transactions/")
    if response.status_code == 200:
        return response.json()
    return []

@st.cache_data(ttl=300)
def get_portfolio():
    response = requests.get(f"{API_URL}/api/portfolio/")
    if response.status_code == 200:
        return response.json().get("portfolio", {})
    return {}

# Dividir en columnas
col1, spacer, col2 = st.columns([3, 1, 3])

# Columna 1: Formulario y tabla de historial
with col1:
    st.header("➕ Agregar Transacción")
    crypto = st.text_input("Criptomoneda (ej: BTC, ETH, USDT)").upper()
    amount = st.number_input("Cantidad", min_value=0.0, format="%.6f")

    if st.button("Agregar"):
        if crypto and amount > 0:
            try:
                response = requests.post(f"{API_URL}/api/transactions/", json={"crypto": crypto, "amount": amount})
                if response.status_code == 200:
                    st.success("✅ Transacción agregada exitosamente")
                    st.cache_data.clear()  # Limpiar caché para actualizar
                    st.rerun()
                else:
                    st.error(f"❌ Error al agregar la transacción: {response.text}")
            except requests.exceptions.RequestException:
                st.error("🚨 No se pudo conectar con la API. Asegúrate de que está corriendo.")

    # Mostrar historial de transacciones
    st.header("📋 Historial de Transacciones")
    transactions = get_transactions()

    # Corregir calculo del total comprado
    total_price_at_purchase = sum(t["amount"] * t["price_at_purchase"] for t in transactions)

    if transactions:
        df = pd.DataFrame(transactions)
        df = df.sort_values(by="date", ascending=False)
        st.dataframe(df[["crypto", "amount", "price_at_purchase", "date"]])
    else:
        st.info("ℹ️ No hay transacciones registradas aún.")

# Espaciador vacío
with spacer:
    st.write("")

# Columna 2: Gráfico del portafolio
with col2:
    st.header(f"📈 Valor actual del Portafolio: ${total_price_at_purchase:.2f}")

    portfolio = get_portfolio()

    if portfolio:
        fig, ax = plt.subplots(figsize=(1, 3))

        # Establecer el fondo del gráfico y de la figura en negro
        fig.patch.set_facecolor('black')
        ax.set_facecolor('black')

        cryptos = list(portfolio.keys())
        values = [portfolio[c]["total_value"] for c in cryptos]

        # Crear gráfico de torta optimizado
        ax.pie(values, 
               labels=cryptos, 
               autopct="%1.1f%%", 
               startangle=140, 
               normalize=True,
               colors=plt.cm.Paired.colors,
               textprops={"fontsize": 5, "color": "white"})

        ax.set_title("Distribución del Portafolio", fontsize=8, pad=-10, color="white")

        st.pyplot(fig)

        # Tabla de resumen del portafolio
        st.header("📊 Resumen del Portafolio")
        portfolio_data = {"Criptomoneda": cryptos, "Valor Total ($)": values}
        st.table(pd.DataFrame(portfolio_data))

    else:
        st.info("ℹ️ No hay datos suficientes para mostrar el portafolio.")
