# 국가별 인구수 비교 
# 1. 데이터 가져오기 
from supabase import create_client,Client

url = "https://uwsijobngxklibfiegzw.supabase.co"
key = "sb_publishable_MPsGCY6VpZsZLDc3f8FRXw_0Xd01YJF"
supabase: Client = create_client(url, key)

import matplotlib.pyplot as plt
import pandas as pd
from supabase import create_client

# countries 테이블 데이터 조회
countries_res = (
    supabase.schema("edu_country")
    .table("countries")
    .select("*")
    .execute()
)

# DataFrame 변환
df_countries = pd.DataFrame(countries_res.data)

# 인구수 기준 내림차순 정렬
df_countries = df_countries.sort_values(
    by="population",
    ascending=False
)

# 그래프 크기 설정
plt.figure(figsize=(12, 6))

# 막대그래프 생성
bars = plt.bar(
    df_countries["country_name"],
    df_countries["population"]
)

# 제목
plt.title(
    "Population by Country",
    fontsize=16,
    fontweight="bold"
)

# x축 / y축 이름
plt.xlabel("Country")
plt.ylabel("Population")

# x축 글자 회전
plt.xticks(rotation=45)

# 막대 위 숫자 표시
for bar in bars:
    yval = bar.get_height()

    plt.text(
        bar.get_x() + bar.get_width() / 2,
        yval,
        f"{int(yval):,}",
        ha='center',
        va='bottom',
        fontsize=8
    )

# 레이아웃 정리
plt.tight_layout()

# 그래프 출력
plt.show()
