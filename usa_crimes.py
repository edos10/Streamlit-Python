import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px

st.title(":bar_chart:Crimes USA Dashboard:fire:")
st.write("Привет! В этом дашборде ты можешь посмотреть немного информации о населении и преступлениях в США, а также на основе некоторых графиков посравнивать информацию и сделать выводы.")
st.write("P.S. мой замысел был в том, чтобы на основе несккольких графиков человек мог выбирать нужные параметры и пытаться искать какие-то выводы, исходя из информации, как о населении, так и о преступлениях.")
df = pd.read_csv("crimedata.csv")
df = df[df.columns].fillna(value=0)
crimes = ["rapes", "robberies", "assaults", "burglaries", "assaults", "rapes", "larcenies", "autoTheft", "murders", "arsons"]
df["crimes"] = df["rapes"] + df["robberies"] + df["assaults"] + df["burglaries"] + df["assaults"] + df["rapes"] + df["larcenies"] + df["autoTheft"] + df["murders"] + df["arsons"]
df["agePct29t65"] = 100 - df["agePct65up"] - df["agePct12t29"]
df["agePct21t29"] = df["agePct12t29"] - df["agePct12t21"]

####################################

first_filter = st.selectbox("Выберите критерий распределения, по которому будет анализироваться этот и следующий графики:", ["Возраст", "Расы"])
if first_filter == "Возраст":
    df1 = df.groupby("state").agg({"agePct12t21": "mean", "agePct21t29":"mean", "agePct29t65":"mean", "agePct65up":"mean"}).reset_index()
    plt.figure(figsize=(25, 25))
    fig1 = px.bar(df1, x="state", y=["agePct12t21", "agePct21t29", "agePct29t65", "agePct65up"], title='Распределение населения по возрасту по штатам')
    st.write(fig1)
else:
    df['racePctOthers'] = 100 - df['racePctWhite'] - df['racePctAsian'] - df['racepctblack']
    df1 = df.groupby("state").agg({"racepctblack": "mean", "racePctWhite": "mean", "racePctAsian": "mean", "racePctOthers": "mean"}).reset_index()
    plt.figure(figsize=(25, 25))
    fig1 = px.bar(df1, x="state", y=["racepctblack", "racePctWhite", "racePctAsian", "racePctOthers"],
                  title='Распределение населения по расам по штатам')
    st.write(fig1)

####################################

second_filter = st.selectbox("Выберите вид преступления, по которому будет анализироваться этот и предыдущий графики:", crimes)
df2 = df.groupby("state").agg({f'{second_filter}': "sum", "crimes":"sum"}).reset_index()
df2[f"procent of {second_filter} in state"] = df2[f"{second_filter}"] / df2["crimes"]
plt.figure(figsize=(25, 25))
fig2 = px.bar(df2, y=f"procent of {second_filter} in state", x="state", title='Процент данного вида преступления от всех в штате')
st.write(fig2)

####################################

third_filter = st.selectbox("Выберите интересующее население муниципальных образований, которые вам нужны:", ["0 - 50 000", "50 000 - 100 000", "100 000 - 200 000", "200 000 - 500 000", "500 000 - 1 000 000", "1 000 000 - 20 000 000"])
third_filter = third_filter.replace(" ", "").split("-")
df3 = df[df['population'] <= int(third_filter[1])]
df3 = df3[df3['population'] >= int(third_filter[0])]
df3 = df3.groupby('state').agg({'crimes': "sum"}).reset_index()
df3 = df3.sort_values(by="crimes", ascending=True)
fig3 = px.bar(df3, x="crimes", y="state", title='Суммарное число преступлений по штатам')
st.write(fig3)

###################################

fourth_filter = st.selectbox("Выберите критерий обеспеченности жителей штатов:", ["Размер домохозяйства", "Доходы"])
if fourth_filter == "Размер домохозяйства":
    df4 = df.groupby('state').agg({'householdsize': "mean"}).reset_index()
    df4 = df4.sort_values(by="householdsize", ascending=True)
    fig4 = px.bar(df4, x="householdsize", y="state", title='Средний размер домохозяйства в штате')
    st.write(fig4)
else:
    df4 = df.groupby('state').agg({'medIncome': "mean"}).reset_index()
    df4 = df4.sort_values(by="medIncome", ascending=True)
    fig4 = px.bar(df4, x="medIncome", y="state", title='Средний доход по штатам')
    st.write(fig4)

###################################
#здесь сделаем изначально датасет с крупными городами
x = st.slider('Выберите, от скольки тысяч население города вы бы хотели посмотреть:', min_value=400000, max_value=int(df['population'].max()), step=50000)
df5 = df[df['population'] > x]
crimes_per_pop = ["murdPerPop", "rapesPerPop", "robbbPerPop", "assaultPerPop", "burglPerPop", "larcPerPop", "autoTheftPerPop", "arsonsPerPop"]
for i in crimes_per_pop:
    fig5 = px.bar(df5, y=i, x='communityName', text_auto='.2s', title='Среднее число данного вида преступления по муниципальным образованиям/городам')
    fig5.update_xaxes(tickangle=45)
    st.write(fig5)
