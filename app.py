import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt

API_URL = "http://127.0.0.1:8000"  # Asegúrate de que FastAPI esté corriendo

st.set_page_config(layout="wide")  # Configuración para pantalla ancha

# 🔹 Centrar título con CSS y reducir espacio superior
st.markdown(
    """
    <style>
        .title-container {
            text-align: center;
            margin-top: -60px;  /* Reduce el espacio vacío arriba del título */
        }
    </style>
    <div class="title-container">
        <h1>🪙 Crypto Portfolio Tracker 💰</h1>
    </div>
    """,
    unsafe_allow_html=True
)

# 🔹 Dividir en tres columnas: una vacía en el medio para más separación
col1, spacer, col2 = st.columns([3, 1, 3])

# 🔹 Columna 1: Formulario y tabla de historial
with col1:
    # Formulario para agregar transacción
    st.header("➕ Agregar Transacción")
    crypto = st.text_input("Criptomoneda (ej: BTC, ETH, USDT)").upper()
    amount = st.number_input("Cantidad", min_value=0.0, format="%.6f")

    if st.button("Agregar"):
        if crypto and amount > 0:
            try:
                response = requests.post(f"{API_URL}/api/transactions/", json={"crypto": crypto, "amount": amount})
                if response.status_code == 200:
                    st.success("✅ Transacción agregada exitosamente")
                    st.rerun()  # Recargar la app para reflejar cambios
                else:
                    st.error(f"❌ Error al agregar la transacción: {response.text}")
            except requests.exceptions.RequestException:
                st.error("🚨 No se pudo conectar con la API. Asegúrate de que está corriendo.")

    # Obtener y mostrar las transacciones (ordenadas por fecha descendente)
    st.header("📋 Historial de Transacciones")
    total_price_at_purchase = 0
    try:
        response = requests.get(f"{API_URL}/api/transactions/")
        if response.status_code == 200:
            transactions = response.json()
            if transactions:
                df = pd.DataFrame(transactions)
                df = df.sort_values(by="date", ascending=False)  # Ordenar por fecha más reciente
                total_price_at_purchase = df["price_at_purchase"].sum()
                st.dataframe(df[["crypto", "amount", "price_at_purchase", "date"]].head(5))  # Mostrar solo 5
            else:
                st.info("ℹ️ No hay transacciones registradas aún.")
        else:
            st.error(f"❌ Error al obtener transacciones: {response.text}")
    except requests.exceptions.RequestException:
        st.error("🚨 No se pudo conectar con la API. Asegúrate de que está corriendo.")

# 🔹 Espaciador vacío (columna del medio)
with spacer:
    st.write("")  # Esto mantiene la separación

# 🔹 Columna 2: Gráfico del portafolio (Torta)
with col2:
    st.header(f"📈 Valor actual del Portafolio - Total Comprado: ${total_price_at_purchase:.2f}")
    try:
        response = requests.get(f"{API_URL}/api/portfolio/")
        if response.status_code == 200:
            portfolio_data = response.json()
            portfolio = portfolio_data.get("portfolio", {})

            if portfolio:
                fig, ax = plt.subplots(figsize=(1, 1))  # Hacer el gráfico más compacto
                cryptos = list(portfolio.keys())
                values = [portfolio[c]["total_value"] for c in cryptos]

                # Crear gráfico de torta con etiquetas y porcentajes más pequeños
                ax.pie(values, 
                        labels=cryptos, 
                        autopct="%1.1f%%", 
                        startangle=140, 
                        colors=plt.cm.Paired.colors,
                        textprops={"fontsize": 4})  # Reducir aún más el tamaño de los textos

                ax.set_title("Distribución del Portafolio", fontsize=6, pad=-10)  # Achicar título y reducir espacio

                st.pyplot(fig)
            else:
                st.info("ℹ️ No hay datos suficientes para mostrar el portafolio.")
        else:
            st.error(f"❌ Error al obtener portafolio: {response.text}")
    except requests.exceptions.RequestException:
        st.error("🚨 No se pudo conectar con la API. Asegúrate de que está corriendo.")