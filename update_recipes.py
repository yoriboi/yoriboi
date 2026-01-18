import os, json, requests

# 환경변수 가져오기
token = os.environ.get('NOTION_TOKEN')
database_id = os.environ.get('NOTION_DATABASE_ID')

headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

def get_data():
    url = f"https://api.notion.com/v1/databases/{database_id}/query"
    payload = { "page_size": 100 }

    try:
        response = requests.post(url, headers=headers, json=payload)
        data = response.json()

        # 연결 실패 시 에러 출력
        if response.status_code != 200:
            print(f"❌ 노션 연결 실패! (ID나 토큰 확인): {data}")
            return

        results = []
        for page in data.get("results", []):
            try:
                props = page.get("properties", {})
                
                # 1. 제목 (이름)
                # '이름', 'Name', '제목' 중 하나라도 있으면 가져옴
                title_prop = props.get("이름") or props.get("Name") or props.get("제목")
                title = "제목 없음"
                if title_prop and title_prop['title']:
                    title = title_prop['title'][0]['text']['content']

                # 2. 링크 (URL)
                # 대소문자 상관없이 'URL', 'url', 'Link' 다 찾아봄
                url_prop = props.get("URL") or props.get("url") or props.get("Link")
                link = "#"
                if url_prop and url_prop['url']:
                    link = url_prop['url']
                
                # 3. 이미지
                files_prop = props.get("이미지") or props.get("Image") or props.get("사진")
                image = "https://ui-avatars.com/api/?name=No+Image"
                if files_prop and files_prop['files']:
                    f = files_prop['files'][0]
                    image = f.get('file', {}).get('url') or f.get('external', {}).get('url')

                # 데이터 담기 (링크가 있는 것만!)
                if link != "#": 
                    results.append({"title": title, "link": link, "image": image})
                    print(f"✅ 가져옴: {title}")
                else:
                    print(f"⚠️ 건너뜀 (링크 없음): {title}")

            except Exception as e:
                print(f"❌ 데이터 처리 중 에러: {e}")
                continue

        # 파일 저장 (links.json)
        with open("links.json", "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=4)
        
        print(f"🎉 총 {len(results)}개의 데이터를 links.json으로 저장했습니다.")

    except Exception as e:
        print(f"❌ 시스템 에러: {e}")

if __name__ == "__main__":
    get_data()
