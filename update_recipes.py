import os, json, requests

NOTION_TOKEN = os.environ['NOTION_TOKEN']
DATABASE_ID = os.environ['NOTION_DATABASE_ID']

headers = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

def get_recipes():
    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
    
    # ✅ 정렬 옵션 추가: 만든 날짜(created_time) 기준 내림차순(descending)
    # 이렇게 하면 가장 최근에 만든 레시피가 맨 위로 옵니다!
    query_payload = {
        "sorts": [
            {
                "timestamp": "created_time",
                "direction": "descending"
            }
        ]
    }
    
    response = requests.post(url, headers=headers, json=query_payload)
    data = response.json()
    
    recipes = []
    for row in data.get("results", []):
        try:
            name = row["properties"]["이름"]["title"][0]["text"]["content"]
            link = row["properties"].get("URL", {}).get("url", "#")
            recipes.append({"name": name, "link": link})
        except Exception as e:
            print(f"항목 건너뜀: {e}")
            
    with open("recipes.json", "w", encoding="utf-8") as f:
        json.dump(recipes, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    get_recipes()
