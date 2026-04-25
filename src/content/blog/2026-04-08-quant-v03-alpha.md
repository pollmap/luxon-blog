---
title: Luxon Quant v0.3α — Walk-Forward 검증, Capital Ladder, 듀얼 거래소
date: 2026-04-08
description: '1인 AI 퀀트 운용 시스템 v0.3α 업데이트: OOS 검증, 점진적 자본 배포, 업비트 클라이언트'
tags:
- 퀀트
- AI
- Luxon
- 투자
- 업데이트
category: building
---

## 1인 AI 헤지펀드, 실전 배포 직전까지

Luxon Quant System이 v0.3α에 도달했습니다. 286개 테스트에서 378개로 (+92), 회귀 0건.

## 이번 업데이트 핵심

### Walk-Forward OOS 검증

과최적화는 퀀트 전략의 가장 큰 적입니다. N-fold 롤링 윈도우로 In-Sample에서 학습하고 Out-of-Sample에서 검증합니다.

- 5-fold 롤링/확장 윈도우 IS→OOS 분석
- IS→OOS Sharpe degradation 추적 (50%+ 이면 과최적화 경고)
- 멀티 종목 포트폴리오 검증 지원

### Capital Ladder (점진적 자본 배포)

Ed Thorp의 교훈: "살아남는 것이 수익보다 중요하다."

5단계로 자본을 점진적으로 배포합니다:

1. PAPER (0%) — 모의투자로 전략 검증
2. SEED (10%) — 소액 실전 진입
3. GROWTH (30%) — 검증된 전략 확대
4. SCALE (60%) — 본격 운용
5. FULL (100%) — 전액 배포

각 단계에서 Sharpe/MDD/운용 기간 조건을 충족해야 승격. MDD 초과 시 자동 강등.

### 업비트 클라이언트

KIS(한국 주식) + Upbit(크립토) 듀얼 거래소 지원:

- REST API: 시세, 호가, 캔들, 계좌, 주문 (JWT 인증)
- WebSocket: ticker/trade/orderbook 실시간 스트리밍
- pyupbit(Apache 2.0) 참고, httpx/websockets 기반 자체 구현

### 자동화 인프라

- Windows Task Scheduler 자동 등록 (매일 16:00 복기)
- ReviewScheduler + Capital Ladder 연동
- 복기 → 블로그 자동 발행 파이프라인

## 전체 파이프라인

```
분석(CUFA) → 시그널(MCP 398도구)
  → 최적화(BL/HRP)
    → 검증(Walk-Forward)
      → 배포(Capital Ladder)
        → 실행(KIS/Upbit)
          → 모니터링(WebSocket)
            → 복기(Vault+Blog)
```

## 숫자로 보는 현황

| 항목 | 값 |
|------|-----|
| 테스트 | 378 passed, 0 failed |
| MCP 도구 | 398개 / 64서버 |
| 전략 프리셋 | 6종 (멀티팩터, 페어트레이딩, 글로벌매크로 등) |
| 리스크 체크 | 7개 사전체크 + Kill Switch |
| 거래소 | KIS + Upbit (듀얼) |

## 다음 단계

1. 페이퍼 트레이딩 첫 실행 (`--dry-run --ladder`)
2. 모의투자 4주 → 소액 실전 50만원 → 검증 후 증액
3. 리스크 관리 > 알파 추구

---

GitHub: [pollmap/open-trading-api](https://github.com/pollmap/open-trading-api)
MCP: [pollmap/nexus-finance-mcp](https://github.com/pollmap/nexus-finance-mcp)

*본 글은 Luxon AI 퀀트 파이프라인의 자동 발행 시스템에서 생성되었습니다.*
