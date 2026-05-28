import os
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from dotenv import load_dotenv
from supabase import create_client, Client


load_dotenv()
url = "https://uwsijobngxklibfiegzw.supabase.co"
key = "sb_publishable_MPsGCY6VpZsZLDc3f8FRXw_0Xd01YJF"

try:
    supabase: Client = create_client(url, key)
    

    response = (
        supabase.schema("edu_country").table("currencies").select("*").execute()
    )
    
  
    df = pd.DataFrame(response.data)
    print("🎉 Supabase 데이터 로드 성공!")
    print(df.head())  

except Exception as e:
    print("❌ 에러 발생: .env 파일의 내용이나 Supabase 연결을 확인하세요.")
    print("상세 에러:", e)
    exit()

sns.set_theme(style="whitegrid")
plt.figure(figsize=(12, 6))


df_sorted = df.sort_values(by="exchange_rate", ascending=False)


barplot = sns.barplot(
    x="currency_code",
    y="exchange_rate",
    hue="country_code",
    data=df_sorted,
    palette="viridis",
    legend=False,  
)


plt.title(
    "USD Base Exchange Rates by Country", fontsize=16, fontweight="bold", pad=15
)
plt.xlabel("Currency Code", fontsize=12)
plt.ylabel("Exchange Rate", fontsize=12)


for p in barplot.patches:
    if p.get_height() > 0:
        barplot.annotate(
            f"{p.get_height():.2f}",
            (p.get_x() + p.get_width() / 2.0, p.get_height()),
            ha="center",
            va="center",
            xytext=(0, 8),
            textcoords="offset points",
            fontsize=10,
            fontweight="bold",
            
        )

plt.tight_layout()

plt.show()
