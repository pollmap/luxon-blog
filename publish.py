#!/usr/bin/env python3
"""
publish.py — Luxon AI 블로그 자동 발행
사용법: python publish.py --title "제목" --slug "slug" --content "내용" [--tags "AI,퀀트"]
"""
import os, sys, re, subprocess, argparse, requests
from datetime import datetime
from pathlib import Path

PEXELS_KEY = os.environ.get("PEXELS_API_KEY", "")
BLOG_DIR = Path(__file__).parent / "src/content/blog"
BLOG_DIR.mkdir(parents=True, exist_ok=True)


def get_pexels_image(query: str) -> str:
    """키워드로 Pexels 이미지 검색"""
    try:
        r = requests.get(
            f"https://api.pexels.com/v1/search?query={query}&per_page=3&orientation=landscape",
            headers={"Authorization": PEXELS_KEY},
            timeout=10
        )
        photos = r.json().get("photos", [])
        if photos:
            return photos[0]["src"]["large2x"]
    except Exception as e:
        print(f"Pexels 오류: {e}")
    return ""



def preprocess_markdown(text):
    """** 볼드 마크다운을 HTML strong으로 변환 (Astro 파서 호환성 문제 방지)"""
    import re
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong></strong>', text, flags=re.DOTALL)
    text = re.sub(r'\*\*', '', text)  # 닫히지 않은 ** 제거
    return text

def publish(title: str, slug: str, content: str, tags: list = None, image_query: str = None):
    today = datetime.now().strftime("%Y-%m-%d")
    tags = tags or ["AI", "Luxon"]
    
    # 이미지 검색
    query = image_query or title.split()[:2][0]
    hero_image = get_pexels_image(query)
    if hero_image:
        print(f"이미지: {hero_image[:60]}...")
    
    # 마크다운 파일 생성
    tags_str = "[" + ", ".join(tags) + "]"
    blog_url = f"https://pollmap.github.io/luxon-blog/blog/{today}-{slug}/"
    frontmatter = f"""---
title: "{title}"
date: {today}
description: "{title}"
{"heroImage: " + chr(34) + hero_image + chr(34) if hero_image else ""}
tags: {tags_str}
---

"""
    # 출처 섹션 자동 추가
    if '📺 원본' not in content and '📊 출처' not in content and '출처' not in content[-500:]:
        content += f"""

---

**📊 출처:** Luxon AI HERMES 리서치팀
**발행:** [{blog_url}]({blog_url})
*본 글은 Luxon AI 에이전트가 분석·작성한 콘텐츠입니다.*
"""
    filepath = BLOG_DIR / f"{today}-{slug}.md"
    filepath.write_text(frontmatter + preprocess_markdown(content), encoding="utf-8")
    print(f"파일 생성: {filepath}")
    
    # git push
    os.chdir(Path(__file__).parent)
    subprocess.run(["git", "add", "-A"], check=True)
    subprocess.run(["git", "commit", "-m", f"post: {title}"], check=True)
    result = subprocess.run(["git", "push", "origin", "main"], capture_output=True, text=True)
    if result.returncode == 0:
        print(f"✅ 발행 완료: https://pollmap.github.io/luxon-blog/blog/{today}-{slug}/")
    else:
        print(f"❌ Push 오류: {result.stderr}")
    
    return f"https://pollmap.github.io/luxon-blog/blog/{today}-{slug}/"


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--title", required=True)
    parser.add_argument("--slug", required=True)
    parser.add_argument("--content", default="")
    parser.add_argument("--tags", default="AI,Luxon")
    parser.add_argument("--image", default="")
    args = parser.parse_args()
    
    content = args.content or sys.stdin.read()
    tags = [t.strip() for t in args.tags.split(",")]
    publish(args.title, args.slug, content, tags, args.image or None)
