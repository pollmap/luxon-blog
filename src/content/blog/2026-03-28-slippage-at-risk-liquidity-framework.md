---
title: "Slippage-at-Risk (SaR) — 퍼페츄얼 선물 거래소의 유동성 리스크 프레임워크"
date: 2026-03-28
description: "VaR에서 영감을 받은 전향적(forward-looking) 슬리피지 리스크 지표 SaR/ESaR/TSaR 소개. 현재 오더북 상태에서 청산 스트레스를 정량화하고 자본 요구량에 연결."
heroImage: "https://images.pexels.com/photos/8919551/pexels-photo-8919551.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940"
tags: [crypto, derivatives, liquidity-risk, SaR, perpetual-futures, microstructure, exchange-risk]
---

## "지금 오더북이 청산 스트레스를 버틸 수 있는가?"

크립토 파생상품 거래소에서 **청산 캐스케이드**가 시작되면 오더북이 순식간에 말라버린다. 역사적 슬리피지 평균이나 실현 손실 분포로는 이 순간의 위험을 제대로 측정할 수 없다.

arXiv:2603.09164 (*Slippage-at-Risk (SaR): A Forward-Looking Liquidity Risk Framework for Perpetual Futures Exchanges*)는 이 문제를 해결하기 위해 **현재 오더북 상태**에서 직접 전향적 유동성 리스크를 계산하는 방법을 제시한다.

## SaR 프레임워크의 3계층

금융에서 시장 리스크를 측정하는 VaR(Value-at-Risk)처럼, 유동성 리스크를 측정하는 세 가지 지표를 도입한다:

### 1. SaR(α) — Slippage-at-Risk
**정의**: 전체 포지션/청산 시나리오 분포에서 α 분위수의 슬리피지
```
SaR(α) = Q_α(슬리피지 분포)
```
예: SaR(95%) = "95% 시나리오에서 최대 슬리피지"

### 2. ESaR(α) — Expected Slippage-at-Risk
**정의**: α 꼬리에 속하는 시나리오들의 평균 슬리피지 (CVaR와 유사)
```
ESaR(α) = E[슬리피지 | 슬리피지 > SaR(α)]
```
극단 상황에서의 기대 비용을 측정한다.

### 3. TSaR(α) — Total Slippage-at-Risk
**정의**: 관련 오더북이나 청산 집합 전체의 달러 표시 꼬리 슬리피지 합산
```
TSaR(α) = Σ 포지션별 달러 슬리피지 × I(α 꼬리)
```
시스템 전체의 스트레스 비용을 집계한다.

## 핵심 발견

### 1. 전향적(forward-looking)이어야 한다
과거 실현 슬리피지 분포는 **현재 오더북이 얼마나 취약한지**를 반영하지 않는다. SaR는 **지금 이 순간의 오더북 스냅샷**에서 청산 시나리오를 시뮬레이션한다.

### 2. 꼬리 슬리피지가 중앙값보다 훨씬 중요하다
시스템 실패는 **취약한 소수의 오더북**에서 시작된다. 중앙값 유동성이 좋아도 꼬리가 얇으면 위험하다. 크로스섹션 슬리피지 꼬리 분포가 핵심 모니터링 대상이다.

### 3. 유동성 집중도 페널티
같은 nominal depth라도 **소수의 마켓 메이커가 제공**하는 경우는 다수가 분산 공급하는 경우보다 취약하다. 스트레스 시 동시 철수 가능성이 높기 때문이다.

실용 지표:
```
집중도 페널티 = f(상위 N 메이커의 깊이 비중)
조정 SaR = SaR × (1 + 집중도 페널티)
```

### 4. 자본·보험 펀드 요구량에 직접 연결
SaR/TSaR는 추상적 지표가 아니라 **실제 거래소가 보험 펀드에 얼마를 적립해야 하는지**를 결정하는 데 사용될 수 있다.

### 5. Hyperliquid 2025 청산 캐스케이드 검증
실제 Hyperliquid 거래소의 2025년 청산 이벤트 데이터로 검증. 해당 이벤트 직전 SaR 지표가 높아져 있었음을 확인.

## 퍼프 유동성 스트레스 모니터 구축 제안

```python
# 의사코드
class PerpLiquidityMonitor:
    def compute_sar(self, orderbook_snapshot, alpha=0.95):
        """현재 오더북에서 SaR 계산"""
        scenarios = self.simulate_liquidation_scenarios(orderbook_snapshot)
        slippages = [s.cost for s in scenarios]
        return np.quantile(slippages, alpha)
    
    def compute_concentration_penalty(self, maker_distribution):
        """상위 N 메이커 집중도 페널티"""
        top_n_share = sum(sorted(maker_distribution)[-3:]) / sum(maker_distribution)
        return max(0, top_n_share - 0.5) * 2  # 50% 초과분에 패널티
    
    def risk_dashboard(self, asset="BTC"):
        sar = self.compute_sar(self.get_orderbook(asset))
        esar = self.compute_esar(self.get_orderbook(asset))
        tsar = self.compute_tsar(self.get_orderbook(asset))
        penalty = self.compute_concentration_penalty(self.get_maker_dist(asset))
        
        return {"SaR": sar, "ESaR": esar, "TSaR": tsar, 
                "adjusted_SaR": sar * (1 + penalty)}
```

## 실전 활용 영역

| 활용처 | SaR 연결 방식 |
|--------|------------|
| 거래소 보험 펀드 적립 | TSaR(99%) 기반 최소 적립 목표 |
| ADL(자동 청산) 트리거 | ESaR가 임계값 초과 시 ADL 조기 발동 |
| 리스크 관리 대시보드 | 실시간 SaR 모니터링 + 알림 |
| 레버리지 한도 설정 | SaR 분위 기반 동적 레버리지 상한 |

## 주의사항

- 거래소별 재보정 필수 — Hyperliquid 임계값을 타 거래소에 직접 적용 금지
- 오더북 스냅샷의 한계 — 숨겨진 유동성, 레이턴시, 호가 취소 반사성 미포함
- 집중도 패널티 계수는 파라미터 → 시장 구조에 따라 조정 필요

## 결론

유동성 리스크를 "평균 슬리피지"로 관리하는 시대는 지나갔다. SaR/ESaR/TSaR는 크립토 퍼페츄얼 선물 시장의 꼬리 리스크를 **현재 오더북 상태에서 전향적으로 정량화**하는 실용적 프레임워크다. 특히 유동성 집중도 페널티를 통합한 조정 SaR는 평온기에는 보이지 않지만 스트레스 시에 치명적인 취약점을 사전에 드러낸다.

— Luxon AI 리서치팀

## 📚 출처

- *Slippage-at-Risk (SaR): A Forward-Looking Liquidity Risk Framework for Perpetual Futures Exchanges*. arXiv:2603.09164. [https://arxiv.org/abs/2603.09164](https://arxiv.org/abs/2603.09164)
