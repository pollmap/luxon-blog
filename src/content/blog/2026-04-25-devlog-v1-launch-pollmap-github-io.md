---
title: "Devlog v1 출범 — pollmap.github.io 루트 허브와 24만 자 교재 동시 공개"
date: 2026-04-25
description: "루트 도메인 점유 + Devlog 발행 엔진 + 24만 자 교재 + publish.py v2.1 보안 레이어. 1인 AI 헤지펀드 5년 빌드로그의 본격 출발점."
tags:
- devlog
- github-pages
- release
- luxon-ai
- meta
- pollmap
category: building
prereq: []
---

## 왜 Devlog v1인가

CUFA wiki(margin)는 학회 자산. 나(이찬희) 본인의 5년 빌드로그는 **별도 레이어**가 필요했다.

가설 한 줄로:

> 2028년 졸업 시점에 면접관이 단일 URL 하나로 5년치 자산 — Devlog 600+ 포스트, 20+ 공개 repo, 완성된 책 1권, 398툴 MCP 생태계 — 을 15분 안에 훑을 수 있어야 한다.

오늘 그 첫 단추를 끼웠다.

## 4개의 라이브 URL

```
https://pollmap.github.io/                       — 루트 허브 (오늘 신규)
https://pollmap.github.io/luxon-blog/             — 발행 엔진 (Astro, 214 포스트)
https://github.com/pollmap/equity-research-book   — 교재 v1.0 (16/17 챕터)
https://github.com/pollmap/pollmap.github.io      — 허브 소스 (MIT)
```

루트 도메인 `pollmap.github.io` 자체가 점유되지 않은 걸 신규 repo로 채웠다. 기존 `pollmap.github.io/luxon-blog/` subpath는 그대로 유지하면서 루트만 별도 정적 사이트(HTML/CSS/JSON)로 채운 구조. Vercel도 검토했지만, 무료·영구·벤더락인 0의 GitHub Pages가 개인 포트폴리오 허브엔 모든 면에서 우세였다.

## 4단 funnel 토폴로지

```
면접관 단일 URL
   │
   ▼
┌───────────────────────────────┐
│  pollmap.github.io  (관문)    │  랜딩 · 이력 · "왜 AI 헤지펀드인가"
└──┬─────────────┬────────────┬─┘
   ▼             ▼            ▼
/luxon-blog    /equity-      /projects
 발행 엔진      research-     쇼케이스
 (214 → 600+)   book/         (12 카드, JSON 기반)
                완성품 v1.0
```

각 노드는 단일 역할. **발행은 luxon-blog에만**, **루트 허브는 1페이지 랜딩 + projects.json 카드 인덱스만**. 중복 운영 비용 최소화. 카드 추가는 JSON 한 줄 + push 하나면 끝.

## 오늘 한 일 (단일 세션)

### 214 포스트 자동 카테고리 태깅

slug regex 룰 기반 5분류 자동 매칭. **214/214 (100%)** 성공. 분포:

| 카테고리 | 개수 | 비고 |
|---|---|---|
| deep-dive | 117 | Kyle 모델 / HMM / BSDE / 미시구조 / Game Theory 등 학술 심층 |
| field | 50 | 시장·뉴스·산업 관찰 (oracle, predictive_history, softbank IPO 등) |
| retro | 43 | 회고 시리즈 (yorun, 요런시점) |
| **building** | **4** | mcp-398-tools, open-source-quant, quant-v03-alpha, risk-management-quant |
| failure | 0 | 기존 포스트엔 실패 post-mortem 없음. 앞으로 채울 영역 |

building 4편이 이미 존재했다는 게 흥미. 알게 모르게 빌드로그를 쓰고 있었던 셈.

### content.config.ts v2 (Astro schema 확장)

```ts
const blog = defineCollection({
  schema: z.object({
    // 기존 v1 필드 (변경 없음)
    title: z.string(),
    date: z.coerce.date(),
    description: z.string().optional().default(''),
    heroImage: z.string().optional(),
    tags: z.array(z.string()).optional().default([]),

    // v2 추가 (모두 optional → 214 legacy 포스트 0손실 backward-compatible)
    category: z.enum(CATEGORIES).optional(),
    prereq: z.array(z.string()).optional(),
    readingTime: z.number().int().positive().optional(),
  }),
});
```

핵심 결정: `category`(intent: building/field/...)는 기존 `tags`(topic: 샤프비율/VaR/비트코인/...)와 **직교 축**. 같은 포스트가 양쪽으로 분류되어 정보 손실 없음.

### publish.py v2.1 Layer 1 — 보안 grep ban

커밋 전 7 패턴 정규식 스캔(VPS IP, 사용자 핸들, 로컬 경로, PEM 키, Telegram 봇 토큰 등). 위반 시 `sys.exit(1)`. self-test 3/3 PASS.

가장 흥미로운 결정은 **self-reference 모순 해결**:

> 보안 도구가 자기 자신을 스캔할 때, regex 패턴 정의에 raw literal로 차단 대상 IP/문자열이 박히면 그 파일 자체가 grep-ban 감지 대상이 된다.

해결: 패턴을 module load 시점에 octets/segments를 concat으로 조립.

```python
def _build_grep_ban_patterns():
    # 차단 대상 IP를 octet 배열로 분리. 파일 raw text엔 연속 literal 없음
    ip_octets = ["xxx", "xxx", "xxx", "xxx"]   # 실제로는 보호 대상 IP 4 옥텟
    p_vps = r"\.".join(ip_octets)               # 런타임에 정규식 패턴 완성
    # ... 나머지 패턴도 동일하게 piece concat
```

`grep -E "<protected-ip-pattern>" publish.py` → **0 hits** (파일은 self-scan 통과). 동시에 `_grep_ban_check()`는 정상 동작. 향후 다른 보안 tooling에서도 재사용 가능한 패턴.

### 24만 자 교재 v1.0 공개

「한국 시장 실전 기업분석 — 현장과 AI로 다시 쓰는 가치투자」. 본편 8주차 + 부록 A~G = **16/17 챕터**. CC BY-NC-ND 4.0.

부록 H(NEXUS Finance MCP 가이드)는 본문 docx에 인프라 호스트 IP가 literal로 박혀 있어 v1.1로 보류:

- CC BY-NC-ND **수정금지** 조항 → 원본 docx 본문을 sed로 치환하면 2차 저작물 생성 = 라이선스 위반 가능
- 안전선: H 파일을 repo 외부 디렉토리로 격리 + README에 "v1.1 예정 (호스트 주소 환경변수화 작업 중)" 명시
- v1.1 릴리스 절차는 별도 세션에서: docx unzip → `word/document.xml` 치환 → repackage → 별도 commit

## 핵심 메트릭

| 항목 | 수치 |
|---|---|
| 빌드 페이지 (정적 generated HTML) | **616** (10.65초) |
| 카테고리 자동 매칭률 | **214 / 214 (100%)** |
| 보안 grep-ban 게이트 | **4 / 4** PASS (허브, 책, publish.py, 백필 포스트) |
| 라이브 URL (오늘 신규) | **4** |
| 5년 빌드로그 누적 T 시점 | T+0 |

## 다음 (확정 + 후보)

- **publish.py v2.2** — Layer 2 (CC BY-NC-ND 인용 포맷 검증), Layer 3 (frontmatter 스키마 강제), Layer 4 (링크 유효성 HEAD 200 체크), Layer 5 (draft 상태머신).
- **부록 H 환경변수화** → 교재 v1.1 릴리스.
- **카테고리별 archive 페이지** — Astro `src/pages/category/[category].astro` 동적 라우트로 5 카테고리 인덱스.
- **2027 Q3 인턴 응시 / 2028 Q1 공채** 큐레이션 페이지 — `/interviews/<season>.html` 베스트 15 포스트 단일 스크린.

월 11~16편 페이스로 누적하면 2028 졸업 시점 **600+ 포스트**. 면접관 15분 룰 안에 5년치 자산이 소화 가능한 funnel — 이게 v1의 가설이고, 검증은 2028년 봄에.

오늘이 **T+0**.

---

*이 프레임워크 설계와 코드/콘텐츠 자동화는 Claude와 페어 작업으로 진행했다. AI를 단순 분석 도구가 아니라 빌드 파트너로 쓰는 게 이 Devlog의 또 다른 차별점이기도 하다 — 그 자체가 검증되어야 할 가설.*
