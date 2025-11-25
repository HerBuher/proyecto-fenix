import streamlit as st
import yfinance as yf
import pandas as pd

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="FÉNIX AI", layout="wide", page_icon="🦅")

# --- TÍTULO Y ESTILO ---
st.title("🦅 PROYECTO FÉNIX: Inteligencia Financiera")
st.markdown("### Algoritmo de Protección Patrimonial & Escasez")

# --- BARRA LATERAL (CONTROLES) ---
st.sidebar.header("Panel de Control")
activo = st.sidebar.text_input("Símbolo del Activo", value="BTC-USD")
dias_analisis = st.sidebar.slider("Días de Análisis Histórico", 200, 2000, 365)

# --- FUNCIÓN DE CEREBRO ---
def analizar_mercado(symbol, days):
    try:
        ticker = yf.Ticker(symbol)
        datos = ticker.history(period=f"{days}d")
        
        # Calcular media móvil (La línea de la verdad)
        datos['Media_200'] = datos['Close'].rolling(window=200).mean()
        return datos
    except:
        return None

# --- EJECUCIÓN VISUAL ---
st.write(f"Conectando con mercados globales para: *{activo}*...")
data = analizar_mercado(activo, dias_analisis)

if data is not None and not data.empty:
    # Obtener precios actuales
    precio_actual = data['Close'].iloc[-1]
    precio_ayer = data['Close'].iloc[-2]
    promedio_200 = data['Media_200'].iloc[-1]
    cambio = precio_actual - precio_ayer
    
    # MOSTRAR MÉTRICAS GRANDES
    col1, col2, col3 = st.columns(3)
    col1.metric("Precio Actual", f"USD {precio_actual:,.2f}", f"{cambio:,.2f}")
    col2.metric("Promedio Histórico (200d)", f"USD {promedio_200:,.2f}")
    
    # EL VEREDICTO
    diferencia_pct = ((precio_actual - promedio_200) / promedio_200) * 100
    
    if precio_actual > promedio_200:
        col3.success(f"TENDENCIA ALCISTA (+{diferencia_pct:.2f}%)")
        st.balloons() # ¡Festejo si hay ganancia!
        mensaje = "✅ *SEMAFORO VERDE:* El activo está fuerte. El Smart Contract autoriza compras."
        color_mensaje = "success"
    else:
        col3.error(f"TENDENCIA BAJISTA ({diferencia_pct:.2f}%)")
        mensaje = "🛡 *MODO PROTECCIÓN ACTIVADO:* El precio está bajo la media histórica. No arriesgar capital."
        color_mensaje = "error"
        
    # MOSTRAR EL MENSAJE DE LA IA
    if color_mensaje == "success":
        st.success(mensaje)
    else:
        st.error(mensaje)

    # GRÁFICO INTERACTIVO
    st.markdown("### 📈 Gráfico de Tendencia vs. Historia")
    st.line_chart(data[['Close', 'Media_200']])

else:
    st.error("No se pudo conectar con el activo. Verifica el símbolo.")

st.markdown("---")
st.caption("Sistema Fénix v5.0 - Desarrollado bajo Arquitectura de Escasez y Ciclos Históricos.")