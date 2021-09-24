import uvicorn
from fastapi import FastAPI
import pandas as pd
import matplotlib.pyplot as plt
import json
import seaborn as sns
from src.responses import TrendItem
from src.service import *
from src.tokens import CONSUMER_SECRET, CONSUMER_KEY, ACCESS_TOKEN_SECRET, ACCESS_TOKEN
from src.constants import *
from src.analyze_feeling import *


app = FastAPI()


@app.get("/trends", response_model=List[TrendItem])
def get_trends_route():
    return get_trends()


if __name__ == "__main__":
    trends = get_trends()

    if not trends:
        save_trends()

    uvicorn.run(app, host="0.0.0.0", port=8000)

# "Direcionando" o token de acesso
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

brazil_trends = api.trends_place(BRAZIL_WOE_ID)

trends = json.loads(json.dumps(brazil_trends, indent=1))

for trend in trends[0]["trends"]:
    print(trend["name"].strip("#"), trend["tweet_volume"])

ttrends = []
for item in trends:
    trends = item["trends"]

df = pd.DataFrame(trends)

df_trends = df.rename(
    columns={
        "name": "Em Ascensão",
        "url": "URI",
        "promoted_content": "Patrocinado",
        "query": "Hashtag",
        "tweet_volume": "Volume"
    })

df_trends["Volume"].fillna(0, inplace=True)

df_trends.groupby("Em Ascensão")["Volume"].mean()

plt.style.use("ggplot")
gc = df_trends[df_trends["Volume"] > 0].sort_values("Volume")
gc.plot("Em Ascensão", ["Volume"], kind="bar", figsize=(10, 5))
plt.title("Em Alta no Twitter")

gc = df_trends[df_trends["Volume"] > 0].sort_values("Volume")
gc.plot("Em Ascensão", ["Volume"], kind='line', figsize=(15, 9))
plt.title("Em Alta no Twitter")

gc = df_trends[df_trends["Volume"] > 0].sort_values("Volume")
gc.plot("Em Ascensão", ["Volume"], kind='barh', figsize=(10, 5))
plt.title("Em Alta no Twitter")

gc = df_trends[df_trends["Volume"] > 0].sort_values("Volume")
gc.plot("Em Ascensão", ["Volume"], kind='area', figsize=(15, 9))
plt.title("Em Alta no Twitter")

# Analise de Sentimentos
df_trends["Subjetividade"] = df_trends['Em Ascensão'].apply(get_pola)
df_trends["Polaridade"] = df_trends["Em Ascensão"].apply(get_subj)

# Mostra um novo dataframe com as colunas subjetividade e polaridade
df_trends.head()

df_trends["Analise"] = df_trends["Polaridade"].apply(analyze)

# Printando apenas os tweets positivos
print("Tweets Positivos :\n")

# Ordenando os tweets
j = 1
sortedDF = df_trends.sort_values(by=["Polaridade"])
for i in range(0, sortedDF.shape[0]):
    if sortedDF["Analise"][i] == "Positivo":

        print(str(j) + ") " + sortedDF["Em Ascensão"][i])
        print()
        j = j+1

# Printando apenas os tweets negativos
print("Tweets Negativos: \n")

j = 1
sortedDF = df_trends.sort_values(by=['Polaridade'], ascending=False)
for i in range(0, sortedDF.shape[0]):
    if sortedDF["Analise"][i] == "Negativo":
        print(str(j) + ") "+sortedDF["Em Ascensão"][i])
        print()
        j = j+1

plt.figure(figsize=(8, 6))
for i in range(0, df_trends.shape[0]):
    plt.scatter(df_trends["Polaridade"][i], df_trends["Subjetividade"][i], color="darkblue")
plt.title("Análise de sentimento")
plt.xlabel("Polaridade")
plt.ylabel("Subjetividade")
plt.show()

# Porcentagem de tweets positivos
positive = df_trends[df_trends.Analise == "Positivo"]
positive = positive["Em Ascensão"]

print("A Porcentagem de Trendings Positivas é de:")
round((positive.shape[0] / df_trends.shape[0]) * 100, 1)

# Porcentagem de tweets negativos
negative = df_trends[df_trends.Analise == "Negativo"]
negative = negative["Em Ascensão"]

print("A porcentagem de Trendings Negativas é de: ")
round((negative.shape[0] / df_trends.shape[0]) * 100, 1)

# Porcentagem de tweets neutros
neutro = df_trends[df_trends.Analise == "Neutro"]
neutro = neutro["Em Ascensão"]

print("A porcentagem de Trendings Neutras é de: ")
round((neutro.shape[0] / df_trends.shape[0]) * 100, 1)

df = pd.DataFrame(df_trends["Analise"].value_counts())

plt.figure()
ax = sns.barplot(x=df["Analise"], y=df.index, data=df_trends)
ax.set_xlabel("Volume")
ax.set_ylabel("Sentimento")

ax = sns.barplot(x=df.index, y=df["Analise"], data=df_trends, label="Volume")
ax.set_ylabel("Volume")
ax.set_xlabel("Sentimento")
