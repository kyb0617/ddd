import json
import random


input_file = "광주_전라권_관광지.json"

output_file = "stamps.json"



# 원본 JSON 읽기
with open(input_file, "r", encoding="utf-8") as f:
    data = json.load(f)



# =========================
# 점수 기준
# =========================

condition_list = {
    100: 1,
    50: 2,
    30: 3
}


weather_list = {
    "맑음": 1,
    "흐림": 2,
    "비": 3,
    "눈": 4
}


time_list = {
    "상시": 1,
    "랜덤 달": 2,
    "랜덤 시간": 3
}



# =========================
# 희귀도 계산
# =========================

def calculate_rarity(distance, weather, time):

    score = 0

    score += condition_list[distance]

    score += weather_list[weather]

    score += time_list[time]


    if score <= 5:

        return {
            "name": "일반",
            "weight": 10
        }


    elif score <= 7:

        return {
            "name": "고급",
            "weight": 30
        }


    elif score <= 9:

        return {
            "name": "희귀",
            "weight": 50
        }


    else:

        return {
            "name": "전설",
            "weight": 80
        }



# =========================
# 장소 랜덤 10개
# =========================

places = data["items"]

random_places = random.sample(places, 10)



stamps = []



# =========================
# 도장 생성
# =========================

for i, place in enumerate(random_places):


    # 랜덤 조건

    distance = random.choice(
        [100,50,30]
    )


    weather = random.choice(
        list(weather_list.keys())
    )


    time = random.choice(
        list(time_list.keys())
    )



    rarity = calculate_rarity(
        distance,
        weather,
        time
    )



    stamp = {


        "id": f"STAMP{i+1:03}",


        "place": place.get("title",""),


        "address": place.get("addr1",""),


        "lat": place.get("mapy",""),


        "lng": place.get("mapx",""),


        "image": place.get("firstimage",""),



        "rarity": rarity["name"],


        "weight": rarity["weight"],



        "condition": {

            "distance": distance

        },



        "special": {

            "weather": weather,

            "time": time

        }


    }


    stamps.append(stamp)



# =========================
# 저장
# =========================

with open(output_file, "w", encoding="utf-8") as f:

    json.dump(
        stamps,
        f,
        ensure_ascii=False,
        indent=2
    )


print("stamps.json 생성 완료!")