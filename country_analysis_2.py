#[2] 어떤 언어가 전 세계 인구 중 얼마만큼의 비율을 차지하는지 영향력 계산
# 1. 데이터 가져오기
from supabase import create_client, Client

url = "https://uwsijobngxklibfiegzw.supabase.co"
key = "sb_publishable_MPsGCY6VpZsZLDc3f8FRXw_0Xd01YJF"
supabase: Client = create_client(url, key)

import matplotlib.pyplot as plt
import pandas as pd
from supabase import create_client

countries_res = (
    supabase.schema("edu_country").table("countries").select("*").execute()
)
languages_res = (
    supabase.schema("edu_country").table("languages").select("*").execute()
)

df_countries = pd.DataFrame(countries_res.data)
df_languages = pd.DataFrame(languages_res.data)

# 2. 데이터 결합 (국가 코드를 기준으로 조인)
df_merged = pd.merge(
    df_languages, df_countries, on="country_code", how="inner"
)

# 3. 언어별 총 인구수 계산 후 상위 5개 추출
language_pop = (
    df_merged.groupby("language_name")["population"].sum().reset_index()
)
language_pop = language_pop.sort_values(by="population", ascending=False)

# 4. 원그래프(Pie Chart) 시각화
plt.figure(figsize=(7, 7))
plt.pie(
    language_pop["population"],
    labels=language_pop["language_name"],
    autopct="%1.1f%%",  # 비율 표시 방식
    startangle=140,
    colors=["#ff9999", "#66b3ff", "#99ff99", "#ffcc99", "#c2c2f0", "#ffb3e6"],
)

plt.title(
    "Global Population Influence by Language",
    fontsize=14,
    fontweight="bold",
)

# 5. 출력
plt.show()
