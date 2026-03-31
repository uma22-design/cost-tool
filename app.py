import streamlit as st
import pandas as pd
import plotly.express as px
from openai import OpenAI

st.title("🚀 CMA Cost Analysis Tool - Accenture CFM Demo")

uploaded_file = st.file_uploader("📁 Upload CSV", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    df['Total_Variable'] = df['Variable_Cost_Per_Unit'] * df['Units']
    df['Total_Cost'] = df['Fixed_Cost'] + df['Total_Variable']
    df['Cost_Per_Unit'] = df['Total_Cost'] / df['Units']
    
    st.subheader("📊 Cost Breakdown")
    st.dataframe(df)
    
    fig = px.bar(df, x='Category', y='Cost_Per_Unit', title="Cost Per Unit")
    st.plotly_chart(fig)
    
    api_key = st.text_input("🔑 OpenAI Key", type="password")
    if api_key and st.button("🤖 AI Savings Tips"):
        client = OpenAI(api_key=api_key)
        prompt = f"3 cost optimization tips: {df.to_string()}"
        response = client.chat.completions.create(model="gpt-4o-mini", messages=[{"role": "user", "content": prompt}])
        st.success(response.choices[0].message.content)