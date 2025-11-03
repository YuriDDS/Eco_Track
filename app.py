import streamlit as st
import pandas as pd

# ===== CONFIGURAÇÃO =====
st.set_page_config(page_title="EcoTrack - Consumo Sustentável", layout="wide")
st.title("🌱 EcoTrack - Rastreador de Impacto Ambiental")

# ===== ENTRADAS =====
st.sidebar.header("💸 Registre seus gastos mensais")

mes = st.sidebar.selectbox(
    "Selecione o mês de referência",
    ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", 
     "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]
)

energia = st.sidebar.number_input("Conta de luz (kWh/mês)", min_value=0.0, value=0.0)
transporte_litros = st.sidebar.number_input("Combustível (litros/mês)", min_value=0.0, value=0.0)
alimentacao = st.sidebar.selectbox("Consumo de carne vermelha", ["Baixo", "Médio", "Alto"])

# ===== CÁLCULOS =====
preco_combustivel = 6.00  # valor médio do litro
fator_energia = 0.084  # kg CO2e por kWh
fator_transporte = 2.31  # kg CO2e por litro de gasolina
fator_alimentacao = {"Baixo": 100, "Médio": 250, "Alto": 500}

# Inicializa variáveis como None
total_co2e = None
gasto_combustivel_reais = None

# Botão para calcular
if st.sidebar.button("Calcular impacto"):

    # Calcula valores
    gasto_combustivel_reais = transporte_litros * preco_combustivel
    total_co2e = energia * fator_energia + transporte_litros * fator_transporte + fator_alimentacao[alimentacao]

    km_carro = total_co2e / 0.120  # 120 g CO2/km
    voos_curto = total_co2e / 250  # 250 kg por voo curto
    arvores = total_co2e / 21  # 1 árvore absorve ~21 kg CO2/ano

    # ===== RESULTADOS =====
    st.subheader(f"📊 Resultado de {mes}")
    st.metric("Emissão total estimada", f"{total_co2e:,.2f} kg CO₂e")

    tabela = pd.DataFrame({
        "Indicador": ["🚗 Km equivalentes", "✈️ Voos curtos", "🌳 Árvores necessárias"],
        "Valor": [f"{km_carro:,.0f} km", f"{voos_curto:,.1f} voos", f"{arvores:,.1f} árvores"]
    })
    st.table(tabela)

    # ===== ANÁLISE DE IMPACTO =====
    if total_co2e < 400:
        nivel = "baixo"
        cor = "🟢"
        dica = [
            "Continue assim! Seu impacto está controlado 👏",
            "Mantenha bons hábitos: desligue luzes desnecessárias 💡",
            "Prefira andar a pé ou de bicicleta em trajetos curtos 🚴‍♂️"
        ]
    elif total_co2e < 1001:
        nivel = "médio"
        cor = "🟡"
        dica = [
            "Atenção! Seu consumo está na média ⚠️",
            "Tente reduzir o uso do carro uma vez por semana 🚗➡️🚌",
            "Aposte em refeições com menos carne 🍲"
        ]
    else:
        nivel = "alto"
        cor = "🔴"
        dica = [
            "Alerta! Seu impacto ambiental está alto 🚨",
            "Revise seu consumo de energia e transporte 💡⛽",
            "Considere trocar carne vermelha por proteínas vegetais 🌱",
            "Evite deslocamentos desnecessários e use transporte coletivo 🚌"
        ]

    st.subheader(f"{cor} Nível de impacto: {nivel.upper()}")
    for d in dica:
        st.write(f"• {d}")

    # ===== RESUMO MENSAL =====
    st.markdown("---")
    st.subheader("📅 Resumo Mensal de Gastos")

    df_gastos = pd.DataFrame({
        "Categoria": ["Energia", "Transporte", "Alimentação"],
        "Gasto (R$)": [energia*0.5, gasto_combustivel_reais, fator_alimentacao[alimentacao]*0.2]  # valores ilustrativos
    })
    st.table(df_gastos)

    total_gastos = df_gastos["Gasto (R$)"].sum()
    media_gastos = df_gastos["Gasto (R$)"].mean()

    st.markdown(f"**Total de gastos:** R$ {total_gastos:,.2f}")
    st.markdown(f"**Média por categoria:** R$ {media_gastos:,.2f}")

    st.subheader("💡 Dicas de economia")
    if total_gastos > 1000:
        st.warning("Cuidado! Seus gastos estão altos este mês.")
        st.info("Dica: Reduza gastos em Energia ou Transporte, priorize refeições mais econômicas.")
    elif total_gastos > 500:
        st.info("Seus gastos estão dentro do esperado, mas sempre dá pra economizar!")
    else:
        st.success("Ótimo! Seus gastos estão controlados.")

    st.subheader("📊 Visualização gráfica")
    st.bar_chart(df_gastos.set_index("Categoria"))

# Se ainda não clicou, mostra aviso
if total_co2e is None:
    st.subheader("📊 Resultado de CO₂e")
    st.write("⚠️ Clique no botão 'Calcular impacto' para ver os resultados.")
