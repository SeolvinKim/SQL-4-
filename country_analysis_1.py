# [1] 대륙별 총 인구수 및 국가 수 비교
# 1. 데이터 가져오기
from supabase import create_client, Client

url = "https://uwsijobngxklibfiegzw.supabase.co"
key = "sb_publishable_MPsGCY6VpZsZLDc3f8FRXw_0Xd01YJF"
supabase: Client = create_client(url, key)

import matplotlib.pyplot as plt
import pandas as pd
from supabase import create_client

response = (
    supabase.schema("edu_country").table("countries").select("*").execute()
)
df = pd.DataFrame(response.data)

# 2. 데이터 분석 (대륙별 인구 합계 구하기)
continent_pop = (
    df.groupby("continent")["population"].sum().reset_index()
)

# 3. VS Code에서 시각화하기
plt.figure(figsize=(8, 5))
plt.bar(
    continent_pop["continent"],
    continent_pop["population"] / 100000000,
    color="skyblue",
)
plt.title("Population by Continent (Unit: 100 Million)")
plt.xlabel("Continent")
plt.ylabel("Population")
plt.grid(axis="y", linestyle="--", alpha=0.7)

# 그래프 출력
plt.show()
