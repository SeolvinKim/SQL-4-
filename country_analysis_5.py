import os
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from dotenv import load_dotenv
from supabase import create_client, Client

# 1. .env 파일에 저장된 Supabase API 정보 불러오기
load_dotenv()
url = "https://uwsijobngxklibfiegzw.supabase.co"
key = "sb_publishable_MPsGCY6VpZsZLDc3f8FRXw_0Xd01YJF"
# 2. Supabase 클라이언트 연결
try:
    supabase: Client = create_client(url, key)
    
    # 3. edu_country 스키마의 currencies 테이블에서 데이터 가져오기
    response = (
        supabase.schema("edu_country").table("currencies").select("*").execute()
    )
    
    # 4. 가져온 데이터를 판다스 데이터프레임으로 변환
    df = pd.DataFrame(response.data)
    print("🎉 Supabase 데이터 로드 성공!")
    print(df.head())  # 터미널에 상위 5개 데이터 미리보기 출력

except Exception as e:
    print("❌ 에러 발생: .env 파일의 내용이나 Supabase 연결을 확인하세요.")
    print("상세 에러:", e)
    exit()

# 5. 시각화 세팅 및 그래프 그리기 (Seaborn 사용)
sns.set_theme(style="whitegrid")
plt.figure(figsize=(12, 6))

# 환율(exchange_rate) 기준으로 내림차순 정렬
df_sorted = df.sort_values(by="exchange_rate", ascending=False)

# 막대 그래프 그리기 (통화 코드별 환율)
barplot = sns.barplot(
    x="currency_code",
    y="exchange_rate",
    hue="country_code",
    data=df_sorted,
    palette="viridis",
    legend=False,  # 범례가 복잡해지므로 제외 (색상 구분을 위함)
)

# 6. 그래프 디자인 및 가독성 업그레이드
plt.title(
    "USD Base Exchange Rates by Country", fontsize=16, fontweight="bold", pad=15
)
plt.xlabel("Currency Code", fontsize=12)
plt.ylabel("Exchange Rate", fontsize=12)

# 각 막대 그래프 위에 실제 환율 수치 표시하기
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

# 7. 그래프 화면에 출력
plt.show()
