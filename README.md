# Luxon AI Blog

Luxon AI 리서치 블로그 — 퀀트, AI, 금융 분석 인사이트를 공유합니다.

**https://pollmap.github.io/luxon-blog/**

## Stack

- [Astro](https://astro.build/) — Static Site Generator
- GitHub Pages — Hosting
- `publish.py` — 자동 발행 스크립트

## 블로그 발행

```bash
# 환경변수 설정
export PEXELS_API_KEY=your_key_here

# 포스트 발행
python publish.py --title "제목" --slug "my-slug" --content "내용" --tags "AI,퀀트"

# 퀀트 복기 자동 발행 (open-trading-api 연동)
python ../open-trading-api/backtester/scripts/publish_review.py --type weekly
```

## 디렉토리 구조

```
src/content/blog/    # 블로그 포스트 (.md)
publish.py           # 자동 발행 스크립트
.env                 # API 키 (gitignore)
```

## 관련 레포

| 레포 | 설명 |
|------|------|
| [nexus-finance-mcp](https://github.com/pollmap/nexus-finance-mcp) | 398도구 금융 MCP 서버 |
| [cufa-equity-report](https://github.com/pollmap/cufa-equity-report) | AI 기업분석 보고서 |
| [open-trading-api](https://github.com/pollmap/open-trading-api) | AI 퀀트 운용 시스템 |

## License

MIT
