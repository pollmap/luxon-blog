---
title: "시계열 인과추론의 함정: Double Machine Learning과 시간 구조의 복원"
date: 2026-03-28
description: "Luxon AI ORACLE/DOGE 리서치팀 분석 — 시계열 인과추론의 함정: Double Machine Learning과 시간 구조의 복원"
heroImage: "https://images.pexels.com/photos/18069697/pexels-photo-18069697.png?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940"
tags: ["AI", "퀀트", "리서치", "LuxonAI"]
---

# 시계열 인과추론의 함정: Double Machine Learning과 시간 구조의 복원

## 서론: 왜 이 연구가 중요한가

금융 시장에서 정책 발표, 스테이블코인 공급 충격, 또는 규제 뉴스가 자산 수익률에 미치는 영향을 정량화하려면 어떻게 해야 할까? 일반적인 머신러닝 모델들은 과거 데이터에서 패턴을 찾는 데 뛰어나지만, **인과관계**를 파악하는 데는 근본적인 약점이 있다. 특히 시계열 데이터에서 이 문제는 더욱 심각하다.

2026년 3월 발표된 "Double Machine Learning for Time Series" 논문은 이 문제의 핵심을 정조한다: **표준적인 머신러닝 교차검증 기법들이 시계열의 순차적 구조를 파괴하면서 인과추론 결과를 무효화할 수 있다**는 것이다. 이는 단순히 통계학적 문제가 아니라, 거시경제 시계열 데이터로 트레이딩 신호나 위험 요인을 추정하는 모든 퀀트 팀에게 실질적인 위협이다.

본 논문이 제시하는 "Reverse Cross-Fitting(RCF)" 방법론과 인과 추론의 핵심 원리들을 살펴보고, 이것이 한국의 자산운용사와 트레이딩 팀에 어떤 실무적 의미를 가지는지 분석해보자.

---

## 1. 시계열 인과추론의 근본적 위기

### 1.1 왜 표준 머신러닝은 시계열에서 실패하는가

현대 머신러닝의 황금 표준은 **cross-validation(교차검증)**이다. 데이터를 무작위로 k개 폴드로 나누어, 각 폴드를 검증 집합으로 남기고 나머지로 학습한 후 성능을 평가한다. 이 방식은 i.i.d(independent and identically distributed) 데이터에서는 완벽하게 작동한다.

그러나 시계열 데이터는 **시간적 의존성(temporal dependence)**을 갖는다. 오늘의 금리는 어제의 금리에 영향을 받고, 내일의 환율은 오늘의 기술적 움직임에 의존한다. 무작위 폴드 분할은 이런 시간적 순서를 무너뜨린다:

```
표준 cross-validation (잘못된 방식):
Fold 1: [2024-01, 2024-05, 2024-09, ...] ← 랜덤하게 분산
Fold 2: [2024-02, 2024-06, 2024-10, ...]
Fold 3: [2024-03, 2024-07, 2024-11, ...]

시간 구조 붕괴 → 미래 정보 누출 가능 → 인과추론 위반
```

더 심각한 것은 **인과 추론(causal inference)**에 미치는 영향이다. 논문의 핵심 설정을 따라가 보자.

### 1.2 부분선형 모형(Partially Linear Model)의 설정

논문이 다루는 기본 인과모형은 다음과 같다:

$$y_t = \theta_0 d_t + g_0(X_t) + \varepsilon_t$$

$$d_t = m_0(X_t) + \xi_t$$

여기서:
- $y_t$: 결과 변수(예: ETF 수익률, 펀딩 레이트)
- $d_t$: 인과 변수, 즉 우리가 영향을 추정하려는 요소(예: 정책 발표 여부, 스테이블코인 공급 변화)
- $X_t$: 고차원 통제 변수들(예: 시장 변동성, 거래량, 다른 자산 수익률)
- $g_0(\cdot)$, $m_0(\cdot)$: 미지의 비모수 함수(머신러닝이 학습할 부분)
- $\varepsilon_t$, $\xi_t$: 오차항

**목표는 $\theta_0$을 일관되게(consistently) 추정하는 것**이다. 이는 $d_t$의 인과 효과이며, 편향(bias)이 없어야 한다.

### 1.3 Double Machine Learning(DML)의 핵심 아이디어

Double Machine Learning은 다음과 같이 작동한다:

**Step 1: 잔차화(Residualization)**

먼저 두 개의 머신러닝 모델을 독립적으로 학습한다:
- 모델 1: $\hat{g}(X_t)$로 $y_t$의 $X_t$ 부분을 예측 → 잔차 $\tilde{y}_t = y_t - \hat{g}(X_t)$
- 모델 2: $\hat{m}(X_t)$로 $d_t$의 $X_t$ 부분을 예측 → 잔차 $\tilde{d}_t = d_t - \hat{m}(X_t)$

**Step 2: 직교화(Orthogonalization)**

이제 원래 비모수 부분이 제거되었으므로:

$$\tilde{y}_t = \theta_0 \tilde{d}_t + (\varepsilon_t + \hat{g}(X_t) - g_0(X_t))$$

머신러닝의 근사 오차가 추가되지만, 정교한 이론 하에서는 큰 샘플에서 **수렴성(consistency)과 점근 정규성(asymptotic normality)을 회복**할 수 있다.

**Step 3: 최종 추정**

$$\hat{\theta}_0 = \frac{\sum_t \tilde{d}_t \tilde{y}_t}{\sum_t \tilde{d}_t^2}$$

이 추정량은 놀랍게도 $\hat{g}$와 $\hat{m}$의 느린 수렴 속도(예: $n^{-1/4}$)에 견딜 수 있다. 이것이 Double Machine Learning의 "이중 강건성(doubly robust)" 특징이다.

---

## 2. 시계열 데이터의 숨겨진 문제들

### 2.1 표준 교차검증이 인과추론을 무효화하는 방식

그런데 $\hat{g}$와 $\hat{m}$을 학습할 때 **표준 무작위 폴드 분할**을 사용하면 무엇이 잘못될까?

시계열에서는 다음이 성립한다:

$$\mathbb{E}[\varepsilon_t | X_t] \neq 0 \quad \text{(일반적으로)}$$

왜냐하면 $X_t$에 미래 정보가 포함될 수 있기 때문이다(폴드 분할이 랜덤하므로). 무작위 fold는 학습-검증 시점을 뒤섞어서, 검증 데이터의 미래 정보가 학습에 사용되는 "정보 누출(information leakage)"이 발생한다.

더 직접적으로: $\hat{m}(X_t)$가 부정확할 때, 잔차 $\tilde{d}_t = d_t - \hat{m}(X_t)$은 근사 오차를 담는다. 시계열의 자기상관(autocorrelation) 때문에 이 오차가 $\varepsilon_t$와 상관될 수 있고, 최종 추정량 $\hat{\theta}_0$이 편향된다.

논문의 표현을 빌리면:

> "Standard randomized cross-fitting in Double Machine Learning is **invalid for dependent macro time series** because it breaks sequential structure."

### 2.2 실제 영향: 소표본과 거시경제 데이터

거시경제 및 금융 시계열의 특징을 생각해 보자:

- **긴 기간 의존성(long-range dependence)**: 금리 충격은 수개월에 걸쳐 영향
- **구조적 변화(structural breaks)**: 정책 레짐 전환, 마켓 구조 변화
- **제한된 샘플**: 고주기 데이터도 연 1-4개 큰 이벤트만 있을 수 있음(예: FOMC 회의)

이런 조건에서 표준 DML은:
1. 폴드 내 자기상관을 무시
2. 작은 표본에서 근사 오차가 상대적으로 커짐
3. 최종 인과 추정이 크게 편향될 가능성

---

## 3. 해결책: Reverse Cross-Fitting(RCF)

### 3.1 시간 구조를 존중하는 폴드 설계

논문이 제안하는 **Reverse Cross-Fitting(RCF)**은 다음과 같이 작동한다:

```
표준 시계열 폴드 (순방향):
Fold 1: Train [2024-01:2024-06], Test [2024-07:2024-12]
Fold 2: Train [2024-01:2024-09], Test [2024-10:2024-12]
...

Reverse Cross-Fitting:
폴드 방향을 뒤집어서 추가로 실행
Fold 1': Train [2024-07:2024-12], Test [2024-01:2024-06]  ← 역방향
Fold 2': Train [2024-10:2024-12], Test [2024-01:2024-09]  ← 역방향
...

최종 추정: 순방향과 역방향 결과의 조화
```

핵심 아이디어:

1. **순방향 폴드**: 시간 순서를 존중하되, 여러 훈련-검증 경계를 만듦
2. **역방향 폴드**: 같은 데이터를 다른 방향으로 처리하여, 시간 구조의 특정 방향에 대한 편향을 상쇄
3. **조화(averaging)**: 두 방향의 결과를 결합하면 시간 순서 위반으로 인한 체계적 편향이 감소

이는 **표본 효율(sample efficiency)**과 **시간 존중(temporal respect)** 사이의 균형을 제공한다.

### 3.2 이웃 드롭(Neighbor-Drop)과의 비교

대안적 접근: "이웃 드롭"은 각 훈련 샘플 주변의 검증 샘플을 제거한다:

```
표준 폴드:
Train: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
Test:  [... 임의 선택 ...]

이웃 드롭:
Train에서 Test 주변 몇 시점 제거
예: Test = [4], Train에서 [2,3,4,5,6] 제거
```

**이웃 드롭의 문제점**:
- 표본 낭비가 심함 (많은 데이터 제거)
- 제거할 "이웃" 범위를 정하기 어려움 (하이퍼파라미터화)
- 여전히 약한 의존성 구조를 놓칠 수 있음

**RCF의 장점**:
- 모든 데이터를 활용
- 추가 하이퍼파라미터 불필요
- 이론적으로 더 정당화됨

---

## 4. 다른 중요한 발견: 예측 성능과 인과성의 괴리

### 4.1 "최고의 예측 모델이 최악의 인과 모델"

논문의 놀라운 발견 중 하나:

> "Predictive RMSE is not a reliable tuning target for nuisance learners in high-dimensional causal time-series settings; the best prediction model can produce a worse causal score."

다시 말해, $\hat{g}(X_t)$와 $\hat{m}(X_t)$를 선택할 때 **예측 오차(RMSE)가 가장 작은 모델**을 선택하면 인과 추정이 더 나빠질 수 있다는 뜻이다.

왜 이런 일이 발생할까?

- **예측 최적화**: RMSE를 최소화하는 모델은 모든 신호(신호+노이즈)를 학습하려고 함
- **인과 최적화**: 인과 추정을 위해서는 $X_t$의 "진정한" 영향만 분리해야 함
- **고차원 문제**: 변수가 많을 때, 과적합되는 노이즈 신호가 인과성을 해친다

구체적으로, $\hat{m}(X_t)$가 과하게 $d_t$의 세부 패턴까지 학습하면, 잔차 $\tilde{d}_t$가 너무 작아지고, 최종 추정의 표준오차가 폭증한다.

### 4.2 "Goldilocks Zone": 폴드 안정성을 기준으로 하는 튜닝

논문이 제안하는 실용적 해결책:

> "The paper's practical calibration idea is a 'Goldilocks zone' of hyperparameters where fold-specific residualization/RMSE is stable."

구체적으로:

1. **각 폴드별로 $\hat{g}^{(k)}$와 $\hat{m}^{(k)}$ 학습** (k번째 폴드)
2. **폴드 간 잔차의 RMSE 변동성 계산**: $\text{Var}_k(\text{RMSE}_k)$
3. **변동성이 최소인 하이퍼파라미터 선택**

이는 다음을 의미한다:
- 너무 단순한 모델(높은 편향): 폴드 간 RMSE 편차 작음 (과소 정규화)
- 너무 복잡한 모델(높은 분산): 폴드 간 RMSE 편차 큼 (과적합)
- **적절한 영역**: 폴드 간 안정성이 최대

이 원리는 저자들이 이론적으로 소표본 편향(small-sample bias)과 연결했다.

---

## 5. 직교화와 장기 분산 추정의 중요성

### 5.1 왜 직교화가 필수인가

DML의 또 다른 핵심 원리는 **직교화(orthogonalization)**다. 잔차화된 모형:

$$\tilde{y}_t = \theta_0 \tilde{d}_t + (\varepsilon_t + \Delta g_t)$$

여기서 $\Delta g_t = \hat{g}(X_t) - g_0(X_t)$는 머신러닝 근사 오차다.

DML의 강건성은 다음에서 나온다:

**Case 1**: $\Delta g_t$가 크지만, $\mathbb{E}[\Delta g_t \cdot \tilde{d}_t] \approx 0$ (직교 조건)
→ 인과 추정이 여전히 일관됨

**Case 2**: $\hat{m}$이 부정확하지만, 동일한 직교성 보장
→ 이중 강건성

이것이 없으면, 근사 오차가 직접 편향이 된다.

### 5.2 시계열의 자기상관과 HAC 추론

그러나 시계열에서는 다음 문제가 발생한다:

$$\text{Var}\left(\sum_t \tilde{d}_t (\varepsilon_t + \Delta g_t)\right) \neq \sum_t \text{Var}(\tilde{d}_t (\varepsilon_t + \Delta g_t))$$

왜냐하면 시점 간 항들이 **자기상관**을 갖기 때문이다.

따라서 표준 추론(단순 t-통계량)이 아닌 **HAC(Heteroskedasticity and Autocorrelation Consistent)** 표준오차를 사용해야 한다:

$$\text{SE}_{\text{HAC}}(\hat{\theta}_0) = \sqrt{\frac{\sum_{j=-M}^{M} w_j \sum_t (\tilde{d}_t - \bar{d})(\tilde{d}_{t-j} - \bar{d})(\varepsilon_t - \bar{\varepsilon})(\varepsilon_{t-j} - \bar{\varepsilon})}{(\sum_t \tilde{d}_t^2)^2}}$$

(간단히 표현한 형태)

여기서 $w_j$는 lag weight, $M$은 대역폭(bandwidth)이다. Newey-West, Andrews, 또는 다른 커널 기반 방법들이 사용된다.

**핵심**: 장기 분산 추정 오차도 편차를 초래할 수 있으므로, 보수적인 접근(더 큰 대역폭)이 권장된다.

---

## 6. 통계적 주의사항과 한계

### 6.1 논문이 명시하는 위험 요소들

논문의 "Statistical or backtest caution" 섹션은 다음을 강조한다:

**1. 정상성(Stationarity) 가정**
- 시계열이 정상이어야 표준 추론이 유효
- 트렌드나 구조적 변화가 있으면 사전 처리 필요
- 금융 데이터(수익률은 대체로 정상, 가격은 비정상)에 따라 다름

**2. 작은 거시 표본의 현실**
- 월별 GDP 성장률: 연 12개 관측치
- 정책 충격 이벤트: 연 1-4개
- 큰 표본 이론이 적용되려면 부족할 수 있음

**3. 구조적 변화(Structural Breaks)**
- 레짐 전환: 금리 인상 사이클 vs 인하 사이클
- 마켓 구조 변화: MiFID II, 암호자산 규제 등
- DML이 사용한 선형성 가정이 깨질 수 있음

**4. 장기 분산 추정 오차**
- HAC 계산 자체가 방법론적 선택에 민감
- 대역폭 선택 오류 → 과소/과대 신뢰구간
- 소표본에서 더욱 심함

### 6.2 "절대 고정된 규칙이 아님" (No Plug-and-Play)

핵심 경고:

> "The transferable lesson is procedural, not plug-and-play. [...] Do not assume predictive CV or shuffled folds are acceptable just because the learner is strong."

즉, **강한 머신러닝 모델이 있다고 해서 자동으로 인과추론이 유효해지지 않는다**. Transformers, XGBoost, 신경망 등이 예측은 잘해도, DML 프레임워크 밖에서 사용하면 인과성이 깨진다.

---

## 7. 실무 적용: ORACLE의 사용 사례

### 7.1 이벤트 기반 인과 추정 파이프라인

논문이 제시하는 Luxon ORACLE의 구체적 응용:

**상황**: ETF 유입/유출이 기초자산 수익률에 미치는 영향 측정

기존 (잘못된) 접근:
```python
# 표준 머신러닝
from sklearn.model_selection import cross_val_score
from sklearn.ensemble import GradientBoosting