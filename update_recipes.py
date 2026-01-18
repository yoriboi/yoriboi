import os, json, requests

# 깃허브 금고(Secrets)에서 정보 가져오기
NOTION_TOKEN = os.environ.get('NOTION_TOKEN')
DATABASE_ID = os.environ.get('NOTION_DATABASE_ID')

headers = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

def get_recipes():
    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
    try:
        response = requests.post(url, headers=headers)
        data = response.json()
        
        if response.status_code != 200:
            print(f"❌ 노션 연결 에러: {data.get('message')}")
            return

        recipes = []
        for row in data.get("results", []):
            try:
                # 사진 4번의 '레시피명' 칸을 정확히 읽습니다.
                props = row.get("properties", {})
                name_list = props.get("레시피명", {}).get("title", [])
                
                if name_list:
                    name = name_list[0]["text"]["content"]
                    link = row.get("url", "#") # 노션 페이지 주소 자동 연결
                    recipes.append({"name": name, "link": link})
            except Exception as e:
                print(f"⚠️ 항목 읽기 건너뜀: {e}")
                continue
        
        # 데이터 저장
        with open("recipes.json", "w", encoding="utf-8") as f:
            json.dump(recipes, f, ensure_ascii=False, indent=4)
        print(f"✅ {len(recipes)}개의 레시피를 성공적으로 가져왔습니다!")

    except Exception as e:
        print(f"❌ 시스템 오류: {e}")

if __name__ == "__main__":
    get_recipes()
