# 콘텐츠 자동화: 원본 수치 불일치 차단

프로덕션에서 쓰는 비공개 검증 로직을 복사하지 않고, 공개 가능한 합성 입력으로
같은 운영 계약을 보여 주는 최소 하네스입니다.

## 관측된 위험

시장 원본은 `2.5%`인데 생성물이 `5.2%`라고 쓰면 사실과 다른 콘텐츠가 됩니다.
[차단 입력](./input.blocked.json)은 이 불일치를 의도적으로 넣었습니다.
[통과 입력](./input.approved.json)은 원본과 생성물의 주체, 수치, 방향, 기준일,
출처를 맞췄습니다.

## 판정

```text
T+000ms input=SYN-MARKET-001
T+012ms category=number_grounding expected=2.5 observed=5.2
T+013ms decision=BLOCK
T+014ms next_stage=NONE
```

통과 입력은 `PRIVATE_UPLOAD`까지만 이동합니다. 공개 전 사람 승인을 생략하는
경로는 이 하네스에 없습니다.

대표 검증 범주는 주체, 수치, 방향, 출처, 기준일, 투자권유, 표현 길이의 일곱
가지입니다. 앞의 여섯 범주는 하드페일이고 표현 길이는 경고입니다. 사람 승인은
별도 상태 전이 조건입니다.

## 검증

```bash
python3 -m unittest evidence.content_automation.test_validator
```

이 결과는 합성 하네스의 상태 전이를 증명합니다. 비공개 프로덕션 전체, 운영 이력
319건, 전체 게이트 수를 재현하거나 증명하지 않습니다.
