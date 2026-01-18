import os, json, requests

# 깃허브 금고에서 열쇠 꺼내기
NOTION_TOKEN = os.environ['NOTION_TOKEN']
DATABASE_ID = os.environ['NOTION_DATABASE_ID']

headers = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

def get_recipes():
    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
    response = requests.post(url, headers=headers)
    data = response.json()
    
    recipes = []
    # 노션 표의 각 줄을 자동으로 읽어옵니다
    for row in data.get("results", []):
        try:
            # 사용자님의 표 설정인 '레시피명' 칸을 읽습니다
            name = row["properties"]["레시피명"]["title"][0]["text"]["content"]
            
            # 노션 페이지 자체 주소를 링크로 사용합니다
            link = row.get("url", "#")
            
            recipes.append({"name": name, "link": link})
        except Exception as e:
            print(f"오류 발생 항목 건너뜀: {e}")
            
    # 결과를 recipes.json으로 저장합니다
    with open("recipes.json", "w", encoding="utf-8") as f:
        json.dump(recipes, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    get_recipes()
