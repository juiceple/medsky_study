# 12월 요강 확정본 재비교 절차

지금 앱의 학생부 반영 분류는 경기도교육청 정시모집요강 검색기의 **8~9월 공개본**(2026-10-26 수집) 기준이다. 12월에 대학들이 확정 요강을 올리면 아래 순서로 달라진 대학만 골라 다시 조사한다. 정원·모집군은 앱에 반영하지 않는 원칙이라 요강의 정원 변경은 무시해도 된다.

## 1. 새 요강 수집
```
python3 -I tools/fetch_guides.py <새 작업폴더>      # 예: scratchpad/gy_dec
```
- `<새 작업폴더>/inventory.json`, `pdf/`, `txt/` 가 만들어진다. 10월 수집 폴더(이전 작업폴더)는 보관해 둔다.
- 10월 수집본이 사라졌다면 `docs/research/guides_2027/inventory.json` 에 파일 ID·쪽수·PDF 생성일이 남아 있다(본문 txt는 없으므로 이 경우 파일 ID·쪽수·생성일 변경만 비교 가능).

## 2. 바뀐 대학 골라내기
```
python3 -I tools/guide_diff.py <이전 작업폴더> <새 작업폴더> changed.json
```
- 파일 교체, 쪽수·생성일 변경, 본문이 쪽 단위로 바뀐 대학과 바뀐 쪽 번호를 낸다. `★` 는 이미 앱에 반영한 대학이다.
- 이미지 PDF(전남대 등)는 본문 비교가 안 되므로 파일·생성일이 바뀌었으면 `pdftoppm`으로 변환해 사람이 눈으로 확인한다.
- 정시 학생부 반영과 관련 있는 쪽(전형방법, 반영비율, 학생부·출결, 학교폭력, 모집단위·이월)이 바뀐 대학만 재조사한다. 정원·일정·장학금 쪽만 바뀐 곳은 건너뛴다.

## 3. 재조사 · 반영
- 바뀐 대학의 조사 지침은 `docs/research/verify_2027final/AGENT_SPEC.md`, 독립 검증은 `VERIFY_SPEC.md`를 쓴다.
- 결과 JSON을 `docs/research/verify_2027final/final_<대학>.json` 으로 저장하면(같은 `appUniv`는 통째로 교체됨) `python3 -I tools/hb_spec.py` 가 앱 규칙(HB_DATA)을 다시 만든다.
- 반영 전 앱 파일을 복사해 두고, 반영 후 `scratchpad/pilot/snap.js` 방식으로 단위별 분류를 뽑아 `python3 -I tools/hb_diff.py 이전.json 이후.json` 으로 바뀐 대학·단위를 확인한다. `node tests/smoke.js`도 돌린다.

## 4. 같이 볼 것
- `docs/research/unconfirmed_units_2027.csv`: 요강에 같은 이름이 없어 '미확인'으로 둔 단위. 12월 요강에 새 이름이 올라왔거나 입학처 확인이 되면 분류한다.
- `docs/RECHECK_LIST.md` N 구역(#60~): 근거가 약한 매핑·이월 판단·이미지 PDF로 읽은 범위.
- 아직 요강 조사를 하지 않은 대학(2순위 일반대학, 이미지 PDF 6곳, 전문대)은 `docs/research/verify_2027final/README.md` 의 '보류' 목록을 본다.
