# Luxon Blog 폰트 가이드

## 규칙
- 본문: Pretendard Variable (CDN: jsdelivr)
- 코드: JetBrains Mono (Google Fonts)
- 로고: Space Mono (Google Fonts)
- fallback: -apple-system, Noto Sans KR, sans-serif

## 폰트 로드 위치
BaseLayout.astro `<head>` 에서만 로드. 개별 페이지/컴포넌트에서 중복 로드 금지.

> ⚠️ 단, 현재 index.astro / blog/index.astro / category/[tag].astro / blog/[...slug].astro 는
> BaseLayout을 상속하지 않는 standalone 페이지이므로 각자 `<head>`에 폰트 링크를 포함.
> 향후 BaseLayout으로 리팩토링 시 제거할 것.

## 사용법
- 일반 텍스트: font-family 명시 불필요 (global.css body에서 상속)
- 코드블록: `font-family: 'JetBrains Mono', monospace`
- 로고/브랜드: `font-family: 'Space Mono', monospace`

## CDN URLs
```
# Pretendard (본문)
https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable-dynamic-subset.min.css

# JetBrains Mono + Space Mono (코드 + 로고)
https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;700&family=Space+Mono:wght@400;700&display=swap
```

## font-family 선언 표준
```css
/* 본문 */
font-family: 'Pretendard Variable', Pretendard, -apple-system, BlinkMacSystemFont, 'Noto Sans KR', sans-serif;

/* 코드 */
font-family: 'JetBrains Mono', 'Fira Code', monospace;

/* 로고/브랜드 */
font-family: 'Space Mono', monospace;
```
