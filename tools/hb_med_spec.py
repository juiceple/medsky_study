# -*- coding: utf-8 -*-
"""메디컬(의·치·한의·약·수의) 학생부 반영 규칙 생성.

- 검증된 조사 JSON(docs/research/verify_med/v*.json)의 그룹 요약을 그대로 사용하고,
  "앱의 어떤 모집단위에 어느 그룹을 적용할지"만 아래 MAP 에서 지정한다.
- MAP 항목: (매칭, 그룹번호, 옵션)   매칭 None = 나머지 전부(마지막에 둘 것)
  옵션: cls(분류 덮어쓰기), name(그룹명 덮어쓰기), sum(요약 덮어쓰기), extra(특이사항 추가)
- 호출: hb_spec.py 가 build_med() 로 UNIV[대학]["med"] 와 SRC 를 채운다.
"""
import json, pathlib

VDIR = pathlib.Path(__file__).resolve().parent.parent / "docs" / "research" / "verify_med"
FILES = ["vAB", "vC", "vD1", "vD2", "vE", "vF"]

# 앱의 대학명 → 검증 JSON 의 univ 이름(다를 때만)
ALIAS = {
    "건국대학교": "건국대학교", "동국대학교": "동국대학교", "연세대학교": "연세대학교",
    "고려대학교": "고려대학교", "한양대학교": "한양대학교",
}

JI = {"name": r"\[지역\]"}                     # 지역인재 단위
JI_OR_ISI = {"name": r"\[지역\]"}
LIST_OFFICIAL = {"서울대학교", "연세대학교", "고려대학교", "경희대학교"}  # 입학처 원문을 직접 확인한 대학

# 대학 → [(매칭, 그룹번호, 옵션)]
MAP = {
 "서울대학교": [(JI, 1, {}), (None, 0, {})],
 "연세대학교": [({"name": r"^의예과$"}, 0, {}), (None, 1, {})],
 "연세대학교(미래)": [(JI, 1, {}), (None, 0, {})],
 "고려대학교": [({"name": r"\[교과\]"}, 1, {}), (None, 0, {})],
 "성균관대학교": [(None, 0, {})],
 "경희대학교": [(None, 0, {})],
 "중앙대학교": [(None, 0, {})],
 "한양대학교": [(None, 0, {})],
 "이화여자대학교": [(None, 0, {})],
 "가톨릭대학교": [({"name": r"^의예과$"}, 0, {}), (None, 1, {})],
 "아주대학교": [({"name": r"^의예과$"}, 0, {}), (None, 1, {})],
 "인하대학교": [(None, 0, {})],
 "가천대학교": [(None, 0, {})],
 "건국대학교": [(None, 0, {})],
 "건국대학교(글로컬)": [(JI, 1, {}), (None, 0, {})],
 "단국대학교(천안)": [(JI, 1, {"cls": "미확인", "name": "[지역] 모집단위 확인 불가",
        "sum": "이 모집단위에 대응하는 2027학년도 정시 전형을 정시모집요강에서 찾지 못했어요. (지역의료인재는 수시 이월 시에만 선발하며 수능 100%)",
        "extra": "앱의 [지역] 모집단위와 요강이 맞지 않아 분류하지 않았어요."}), (None, 0, {})],
 "동국대학교": [(None, 0, {})],
 "동국대학교(WISE)": [({"name": r"\[지역\]"}, 1, {}), ({"gun": ["수시이월"]}, 1, {}), (None, 0, {})],
 "삼육대학교": [(None, 0, {})],
 "숙명여자대학교": [(None, 0, {})],
 "덕성여자대학교": [(None, 0, {})],
 "동덕여자대학교": [(None, 0, {})],
 "한양대학교(ERICA)": [(None, 0, {})],
 "차의과학대학교": [(None, 0, {})],
 "경북대학교": [({"name": r"^의예과"}, 0, {"extra": "정시 '지역인재 기초생활수급자등대상자전형'(수시 미충원 시 모집)은 학생부 교과 80% + 서류평가 20%를 반영하지만 이 앱에는 없는 전형이에요."}),
                ({"name": r"^(치의예과|약학과)$"}, 1, {}), (None, 2, {})],
 "부산대학교": [({"name": r"^(의예과|치의예과)"}, 0, {}), ({"name": r"^한의학전문대학원"}, 2, {}), (None, 1, {})],
 "경상국립대학교": [(JI, 1, {}), (None, 0, {})],
 "계명대학교": [(JI, 1, {}), (None, 0, {})],
 "영남대학교": [(JI, 1, {}), (None, 0, {})],
 "대구가톨릭대학교": [(JI, 2, {}), ({"name": r"^의예과$"}, 0, {}), (None, 1, {})],
 "동아대학교": [(JI, 1, {}), (None, 0, {})],
 "경성대학교": [(None, 0, {})],
 "고신대학교": [(JI, 1, {}), (None, 0, {})],
 "인제대학교": [({"name": r"^의예과"}, 0, {}), (None, 1, {})],
 "동의대학교": [(None, 0, {})],
 "대구한의대학교": [(None, 0, {})],
 "전남대학교": [(JI, 1, {}), (None, 0, {})],
 "전북대학교": [(JI, 1, {}), (None, 0, {})],
 "조선대학교": [(JI, 1, {}), (None, 0, {})],
 "원광대학교": [(None, 0, {})],
 "제주대학교": [(JI, 1, {}), (None, 0, {})],
 "목포대학교": [(JI, 1, {"extra": "요강에 '수능 성적이 없는 경우 학생부 교과성적 환산(최대 200점)' 규정이 있으나, 약학과는 수학(미적분/기하)·과탐 응시자만 지원할 수 있어 통상 적용되지 않아요. 입학처 확인을 권장해요."}),
                 (None, 0, {"extra": "요강에 '수능 성적이 없는 경우 학생부 교과성적 환산(최대 200점)' 규정이 있으나, 약학과는 수학(미적분/기하)·과탐 응시자만 지원할 수 있어 통상 적용되지 않아요. 입학처 확인을 권장해요."})],
 "순천대학교": [(JI, 1, {}), (None, 0, {})],
 "동신대학교": [(None, 0, {})],
 "우석대학교": [(None, 0, {})],
 "대전대학교": [(JI, 1, {}), (None, 0, {})],
 "건양대학교": [(JI, 1, {}), (None, 0, {})],
 "충남대학교": [(JI, 1, {}), (None, 0, {})],
 "충북대학교": [(JI, 1, {}), (None, 0, {})],
 "강원대학교": [({"name": r"^수의예과\[지역\]$"}, 2, {"cls": "미확인", "name": "수의예과[지역] 확인 불가",
        "sum": "2027학년도 정시요강에는 수의예과 대상 지역인재 전형이 없어, 이 모집단위에 대응하는 전형을 확인하지 못했어요.",
        "extra": "수의학과(6년제)는 일반 수능 전형만 확인돼요. 모집요강 확정 후 확인이 필요해요."}),
                 (JI, 1, {}), (None, 0, {})],
 "강원대학교(강릉)": [(None, 0, {"extra": "강릉원주대 2027 시행계획 기준이에요. 강원대 명의의 정시모집요강은 아직 확인하지 못했어요."})],
 "가톨릭관동대학교": [(None, 0, {})],
 "한림대학교": [(None, 0, {})],
 "상지대학교": [(None, 0, {"extra": "출결 감점이 한의예과 수능전형에 실제 적용되는지 문구가 엇갈려(시행계획 '정시모집' 적용 / 일부 표는 '학생부교과·실기'만 표기) 입학처 확인이 필요해요. 미적용이면 '미반영'이에요."})],
 "세명대학교": [(None, 0, {})],
 "순천향대학교": [(JI, 1, {}), (None, 0, {})],
 "을지대학교": [(None, 0, {})],
 "울산대학교": [(None, 0, {})],
 "고려대학교(세종)": [(None, 0, {})],
}

# 근거 문서 기준(기본은 정시모집요강). 다르면 여기에 적는다.
BASIS = {
 "동국대학교(WISE)": "2027학년도 시행계획(안, 2025.3) — 정시모집요강 미확인",
 "강원대학교(강릉)": "2027학년도 대학입학전형 시행계획 — 정시모집요강 미확인",
 "경북대학교": "2027학년도 정시모집요강(안)",
}

def _src_list(srcs, univ):
    out = []
    for s in srcs:
        u = s.get("url", "")
        if not u.startswith("http"):
            continue
        t = s.get("title") or s.get("kind") or univ
        out.append({"t": t[:70], "u": u, "k": (s.get("kind") or "")[:40]})
    return out[:2]

def build_med(UNIV, SRC, LV_OFFICIAL, LV_COPY, R):
    data = {}
    for f in FILES:
        for u in json.load(open(VDIR / (f + ".json"), encoding="utf-8")):
            data[u["univ"]] = u
    missing = []
    for univ, rules in MAP.items():
        j = data.get(univ)
        if not j:
            missing.append(univ); continue
        keys = []
        lst = _src_list(j.get("sources", []), univ)
        if not lst:
            lst = [{"t": univ + " 2027학년도 정시모집요강", "u": "", "k": "입학처 원문 PDF (링크 미확보)"}]
        for i, s in enumerate(lst):
            k = "med_%s_%d" % (univ, i)
            SRC[k] = s; keys.append(k)
        out = []
        for m, gi, opt in rules:
            g = j["groups"][gi]
            cls = opt.get("cls", g["class"])
            summ = opt.get("sum", g["summary"])
            note_parts = []
            iv = (g.get("interview") or "").strip()
            if iv and not iv.startswith("없음") and not iv.startswith("면접 없음"):
                note_parts.append("면접: " + iv)
            if g.get("note"):
                note_parts.append(g["note"])
            if opt.get("extra"):
                note_parts.append(opt["extra"])
            r = R(opt.get("name", g["name"]), cls, summ, list(g.get("details", []))[:6], " ".join(note_parts), keys, m=m,
                  lvl=LV_OFFICIAL if univ in LIST_OFFICIAL else LV_COPY)
            out.append(r)
        d = UNIV.setdefault(univ, {"basis": BASIS.get(univ, "2027학년도 정시모집요강"),
                                   "lvl": LV_OFFICIAL if univ in LIST_OFFICIAL else LV_COPY, "rules": []})
        d["med"] = out
        if univ in BASIS:
            d["basis"] = BASIS[univ]
    return missing
