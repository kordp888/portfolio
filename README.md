# Derrick Hwang · Forward Deployed Engineer

고객 업무를 이해하고 Python·LLM/API·Next.js로 직접 구현·검증합니다. 광고 사업 창업과 고객관리·데이터분석 경험을 바탕으로 요구사항을 정리합니다.

[포트폴리오](https://kordp888.github.io/portfolio/) · [검증 범위](VERIFICATION.md)

## 경력

골드문파트너스 Founder & CEO (2024.06–2025.07)로 광고 사업을 창업·운영하며 고객 유입·상담·전환 흐름을 관리했습니다. 이전에는 코네의 팀장·데이터분석 (2021.03–2022.04), JW투자진흥원의 팀장·고객관리 및 데이터분석 (2020.03–2021.03), 채움의 팀장·광고기획 (2019.03–2020.03)을 맡았습니다. FDE는 현재 목표 직무이며 과거 직책을 바꾼 것이 아닙니다.

## 대표 사례

| 고객·운영 문제 | 구현한 것 | 확인 결과와 공개 자료 |
|---|---|---|
| 반복되는 콘텐츠 제작과 원본 대조 | Python으로 수집·LLM 초안·음성·영상·검증·비공개 업로드 연결, 개인 구현·운영 | 2026.09.09 정리한 과거 운영 집계에서 정시 파이프라인 업로드 게이트 도달 225건 중 37건 차단. [사례](projects/content-automation/). 정확도·오류 탐지율·효율 개선률이 아니며 원시 로그를 이번에 재집계하지 않았습니다. |
| WESOP의 업무 흐름과 AI Agent 적용 범위 | SeSAC 기업 연계 프로젝트에서 프로토타입·MVP·데이터/API 접근 범위 협의 | 프로토타입·연동 요구사항 설계. [교육용 화면](https://wesop-shopsol-prototype.vercel.app/). 합성 데이터이며 상용 연동 완료·실데이터 접근·매출 효과를 뜻하지 않습니다. |
| 경험과 직무를 연결하는 AI 해석의 확인 | Career Insight Coach, Next.js·TypeScript 웹 프로토타입 Vercel 배포 | 사용자가 AI 해석을 확인·수정하는 화면. [초대 코드가 필요한 베타 웹](https://career-insight-coach.vercel.app/). 저장·가져오기·내보내기·오류 상황은 확인·개선 중입니다. |

ZENITH, 다시ON5060, 린온, ONDA는 [보조 사례](https://kordp888.github.io/portfolio/#archive)에서 개인 역할·팀 결과·진행 상태를 구분해 설명합니다. 린온은 5인 팀 해커톤입니다.

## English

I am pursuing Forward Deployed Engineer roles. I define requirements using experience in founding an advertising business, customer operations and data analysis, then build and verify Python, LLM/API workflows and Next.js web prototypes.

The YouTube multichannel workflow connects collection, drafts, voice, video, source comparison and private upload. Historical figures compiled on 2026.09.09 report 37 blocked attempts out of 225 scheduled pipeline attempts reaching the upload gate. Raw logs were not recounted in this update. This is not accuracy, an error detection rate or an efficiency gain. Public release is a human decision.

WESOP is a SeSAC industry collaboration prototype and integration requirements exercise, not employment or completed commercial integration. Career Insight Coach is a deployed Next.js/TypeScript web prototype that currently requires an invitation code; save, import, export and error states remain under review and improvement.

## 운영

정적 HTML/CSS/JavaScript와 기존 GitHub Pages main 루트 배포를 유지합니다. 한국어 기본, 영어 전환, 모바일 메뉴와 인쇄를 제공합니다. 이력서는 연락 후 개별 전달하며 웹에서 다운로드를 제공하지 않습니다. 회사별 제출용 문서와 비공개 편집 메모는 이 저장소에 포함하지 않습니다.

`analytics.js`의 기존 분석 설정과 이벤트 목적을 유지합니다. ID가 비어 있으면 외부 분석 요청이 없습니다. 이벤트에는 연락처, 입력값, URL 쿼리, 원문 링크 텍스트를 넣지 않습니다.

```sh
python3 evidence/run_checks.py
python3 -m http.server 8765
```

화면은 웹에서 확인한 실제 산출물과 보존된 공개 화면을 사용합니다. 제품의 내부 규칙·프롬프트·원본 운영 자료는 추가하지 않습니다.
