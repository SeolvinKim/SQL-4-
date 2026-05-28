#[3] 국가별 랜드마크 보유 현황과 역사성 분석
# 1. 데이터 가져오기
from supabase import create_client, Client

url = "https://uwsijobngxklibfiegzw.supabase.co"
key = "sb_publishable_MPsGCY6VpZsZLDc3f8FRXw_0Xd01YJF"
supabase: Client = create_client(url, key)

import matplotlib.pyplot as plt
import pandas as pd
from supabase import create_client

landmarks_res = (
    supabase.schema("edu_country").table("landmarks").select("*").execute()
)
df_landmarks = pd.DataFrame(landmarks_res.data)

# 2. 건립 연도순으로 정렬 (오래된 순)
df_landmarks = df_landmarks.sort_values(by="established_year")

# 3. 수평 막대그래프(Horizontal Bar Chart) 시각화
plt.figure(figsize=(10, 6))

# 4. 연도가 오래될수록 막대가 길어지도록 연도 데이터를 그래프로 표현
bars = plt.barh(
    df_landmarks["landmark_name"],
    df_landmarks["established_year"],
    color="peru",
    edgecolor="black",
)

plt.title("Landmarks by Established Year", fontsize=14, fontweight="bold")
plt.xlabel("Established Year (A.D.)", fontsize=12)
plt.ylabel("Landmark Name", fontsize=12)
plt.grid(axis="x", linestyle="--", alpha=0.5)

# 5. 막대 끝에 정확한 연도 텍스트 표시하기
for bar in bars:
    xval = bar.get_width()
    plt.text(
        xval + 20,  # 텍스트 위치 살짝 오른쪽으로
        bar.get_y() + bar.get_height() / 2,
        f"{int(xval)}",
        ha="left",
        va="center",
        fontsize=10,
    )

# 6. 출력
plt.show()
