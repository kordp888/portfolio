# Evidence Pack

채용 문서의 숫자와 제품 주장을 검토할 수 있도록 만든 공개 검증 묶음입니다.
프로덕션 소스, 운영 원장, 개인정보는 포함하지 않습니다.

## 재현 가능한 상세 검증

현재 합성 입력과 테스트 명령까지 공개한 사례는 3건입니다.

| 사례 | 공개하는 것 | 공개하지 않는 것 |
|---|---|---|
| [콘텐츠 자동화](./content_automation/) | 합성 입력, 7개 대표 범주, 차단·통과 추적 | 원문, 채널 식별자, 운영 로그 |
| [LLM Wiki](./llm_wiki/) | 가산 전용 동기화 계약과 삭제 방지 테스트 | 위키 내용, 옛 미러 구현 |
| [ONDA](./onda/) | 고정 센서 시각 실패와 속도 계산 복구 | 실제 위치, 차량·기기 식별자 |

## 전체 포트폴리오 공개 범위

상세 검증 사례가 없다고 제품이 빠진 것은 아닙니다. 공개 가능한 근거의 형태가
제품마다 다릅니다.

| 제품 | 현재 공개 근거 | 비공개로 유지하는 것 |
|---|---|---|
| LLM Content Pipeline | [합성 차단 상태 전이](./content_automation/), [공개 품질 게이트 모듈](https://github.com/kordp888/llm-quality-gates) | 프로덕션 소스, 운영 원장, 채널 식별자 |
| LLM Wiki | [아키텍처 문서](https://github.com/kordp888/llm-wiki), [가산 전용 동기화 검증](./llm_wiki/) | 운영 위키 내용, 구현 원본, 비공개 테스트 스위트 |
| ONDA | [공개 쇼케이스](https://github.com/kordp888/ONDA-for-Tesla-showcase), [GPS 폴백 검증](./onda/) | 앱 구현 원본, 실제 위치, 기기 식별자, 음성 자산 |
| Signal Crew | [공개 제품 저장소](https://github.com/kordp888/signal-crew) | 비공개 개발 원본과 운영 데이터 |
| 다시ON5060 | [공개 쇼케이스](https://github.com/kordp888/dasi-on5060), [Live MVP](https://dasion-app.vercel.app) | 앱 구현 원본과 사용자 데이터 |
| 세이프체크 | [제품 설명](https://kordp888.github.io/portfolio/#projects) | 팀 작업물, 사용자 테스트 녹취, 구현 원본 |
| 린온 | [Live demo](https://lean-on-goodquestion.vercel.app) | 구현 원본과 사용자 데이터 |

## 공개 도구

| 도구 | 공개 근거 |
|---|---|
| [LLM Quality Gates](https://github.com/kordp888/llm-quality-gates) | 공개 모듈 테스트 78건 통과, 선택 통합 테스트 1건 제외 |
| [AI Tell Removal](https://github.com/kordp888/ai-tell-removal) | 문서에서 반복되는 기계적 표현 패턴을 검사하는 공개 CLI |

공개 문구의 정본은 [claims.json](./claims.json)입니다. 각 항목에 측정 시점, 범위,
제외 조건, 만료일을 함께 저장합니다. 테스트 수처럼 자주 바뀌는 값은 히어로에서
사용하지 않고 프로젝트 검증 기록에만 둡니다.

## 로컬 검증

```bash
python3 evidence/run_checks.py
```

이 명령은 claims registry, 공개 제거 규칙, 합성 하네스 3개를 한 번에 검사합니다.
공개 하네스가 통과해도 비공개 프로덕션 전체를 재현했다는 뜻은 아닙니다.
