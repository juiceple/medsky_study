# 테스트

`smoke.js`는 앱을 실제 브라우저(Playwright 크로미움)로 열어 핵심 동작을 점검하는 스모크 테스트입니다.

```
NODE_PATH=$(npm root -g) node tests/smoke.js            # 저장소의 jeongsi_tool.html
NODE_PATH=$(npm root -g) node tests/smoke.js 경로.html   # 다른 파일
```

크로미움 경로는 기본 `/opt/pw-browsers/chromium`이고, 다르면 `CHROMIUM_PATH` 환경변수로 지정합니다.

점검 항목: 로딩·오류, 숫자 서식, 보고서 어투 변환, 탭 렌더링, 정밀 매칭 기본값, 환산 불리/유리 배지, 추천 대학, 입력 경고, 열 설정, 보고서(어투·펑크 근거 제외·PDF), 지원희망 화면(요약 띠·군별 구역·최종 지정).
화면을 바꾸거나 데이터 규칙을 고친 뒤에는 이 테스트를 먼저 돌리세요.
