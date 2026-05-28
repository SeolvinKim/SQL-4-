

from getpass import getpass
from supabase import create_client

url = "https://uwsijobngxklibfiegzw.supabase.co"
key = "sb_publishable_MPsGCY6VpZsZLDc3f8FRXw_0Xd01YJF"

SUPABASE_URL = input("Supabase URL: ").strip()
SUPABASE_ANON_KEY = getpass("Supabase anon key: ").strip()

supabase = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)

print("Supabase 연결 완료")


import random

# 도시 데이터
cities = [
    ("Seoul", "KR"),
    ("New York", "US"),
    ("Los Angeles", "US"),
    ("Chicago", "US"),
    ("Paris", "FR"),
    ("Tokyo", "JP"),
    ("Ottawa", "CA"),
    ("Toronto", "CA"),
    ("Vancouver", "CA"),
    ("Beijing", "CN"),
    ("Singapore", "SG"),
    ("Manila", "PH"),
    ("Berlin", "DE"),
    ("London", "UK"),
    ("Manchester", "UK"),
    ("Birmingham", "UK")
]

# 국가 코드 → 국가명
country_names = {
    "KR": "South Korea",
    "US": "United States",
    "FR": "France",
    "JP": "Japan",
    "CA": "Canada",
    "CN": "China",
    "SG": "Singapore",
    "PH": "Philippines",
    "DE": "Germany",
    "UK": "United Kingdom"
}


def start_game():
    # 정답 도시 1개 랜덤 선택
    correct_city = random.choice(cities)
    correct_city_name = correct_city[0]
    correct_country_code = correct_city[1]

    # 같은 나라 도시 후보들 찾기
    correct_candidates = [
        city for city in cities
        if city[1] == correct_country_code
    ]

    # 정답 도시 선택
    answer = random.choice(correct_candidates)

    # 오답 도시 선택
    wrong_choices = [
        city for city in cities
        if city[1] != correct_country_code
    ]

    wrong_answers = random.sample(wrong_choices, 3)

    # 보기 섞기
    options = wrong_answers + [answer]
    random.shuffle(options)

    # 문제 출력
    print("\n===== 도시 퀴즈 게임 =====")
    print(f"\n다음 중 {country_names[correct_country_code]}의 도시는 무엇일까요?\n")

    for idx, option in enumerate(options, start=1):
        print(f"{idx}. {option[0]}")

    # 사용자 입력
    user_input = int(input("\n번호를 선택하세요: "))

    selected_city = options[user_input - 1]

    # 정답 판별
    if selected_city[1] == correct_country_code:
        print("\n정답입니다!")
    else:
        print("\n오답입니다!")

    print(f"정답 도시: {answer[0]}")
    print(f"국가: {country_names[correct_country_code]}")


# 게임 실행
start_game()
