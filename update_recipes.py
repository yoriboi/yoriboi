import os, json, requests

def update_notion_recipes():
    # 1. 환경변수 가져오기
    token = os.environ.get('NOTION_TOKEN')
    database_id = os.environ.get('NOTION_DATABASE_ID')

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }

    print("🚀 노션 데이터 가져오기 시작...")
    
    url = f"https://api.notion.com/v1/databases/{database_id}/query"
    payload = { "page_size": 100 }

    try:
        response = requests.post(url, headers=headers, json=payload)
        data = response.json()

        # 연결 실패 체크
        if response.status_code != 200:
            print(f"❌ 노션 연결 실패! (ID/토큰 확인 필요): {data}")
            return

        results = []
        rows = data.get("results", [])
        print(f"🧐 노션에서 총 {len(rows)}개의 줄을 발견했습니다.")

        for i, page in enumerate(rows):
            try:
                props = page.get("properties", {})
                
                # --- [1] 이름 찾기 (Name, 이름, 제목, Page) ---
                title = "제목 없음"
                # 가능한 모든 이름 컬럼을 뒤져봄
                name_candidates = ["이름", "Name", "제목", "Title", "Page"]
                for key in name_candidates:
                    if key in props:
                        t_list = props[key].get("title", [])
                        if t_list:
                            title = t_list[0]["text"]["content"]
                            break
                
                # --- [2] 링크 찾기 (URL, url, Link, link, 링크) ---
                link = "#"
                # 가능한 모든 링크 컬럼을 뒤져봄
                url_candidates = ["URL", "url", "Url", "Link", "link", "링크", "주소"]
                for key in url_candidates:
                    if key in props:
                        link = props[key].get("url", "#")
                        if link: break
                
                # --- [3] 이미지 찾기 (이미지, Image, 사진, file) ---
                image = "https://ui-avatars.com/api/?name=No+Img"
                img_candidates = ["이미지", "Image", "image", "사진", "File", "file"]
                for key in img_candidates:
                    if key in props:
                        files = props[key].get("files", [])
                        if files:
                            f = files[0]
                            image = f.get('file', {}).get('url') or f.get('external', {}).get('url')
                            break

                # 링크가 없으면 저장하지 않음
                if link and link != "#":
                    print(f"  ✅ [{i+1}] 저장 성공: {title}")
                    results.append({
                        "title": title,
                        "link": link,
                        "image": image
                    })
                else:
                    print(f"  ⚠️ [{i+1}] 건너뜀 (링크 없음): {title}")
                    # 디버깅을 위해 노션에 어떤 칸들이 있는지 출력
                    print(f"     👉 발견된 칸 이름들: {list(props.keys())}")

            except Exception as e:
                print(f"❌ 데이터 처리 중 에러 ({title}): {e}")
                continue

        # 파일 저장
        with open("links.json", "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=4)
        
        print(f"🎉 최종 완료: 총 {len(results)}개의 버튼을 생성했습니다.")

    except Exception as e:
        print(f"❌ 시스템 에러: {e}")

if __name__ == "__main__":
    update_notion_recipes()
