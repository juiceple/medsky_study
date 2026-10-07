# -*- coding: utf-8 -*-
"""지거국(비메디컬)·교대 학생부 반영 규칙 생성 (hb_b2_spec.py 와 같은 방식).

- 검증된 조사 JSON(docs/research/verify_b3/vB3_*.json)의 그룹 요약을 쓰고,
  "앱의 어느 모집단위에 어느 그룹을 적용할지"만 MAP 에서 지정한다.
- MAP 항목: (매칭, 그룹번호, 옵션)  옵션: cls name sum extra f(검증 파일명; 기본은 DEFAULT_FILE)
- PREPEND: 이미 규칙이 있는 대학(이화 등)의 앞쪽에 끼워 넣는 규칙
"""
import json, pathlib

VDIR = pathlib.Path(__file__).resolve().parent.parent / "docs" / "research" / "verify_b3"
FILES = ["vB3_1", "vB3_2", "vB3_3", "vB3_4"]

# 요강 모집단위표에 이름이 없는 수시이월 단위 → 이월 모집 여부 불명이라 미확인
def NOTFOUND(msg):
    return {"cls": "미확인", "name": "요강에 없는 모집단위",
            "sum": "2027 정시모집요강의 모집단위표에서 이 모집단위를 찾지 못했어요. 수시 이월 모집 여부를 확인하지 못했어요.",
            "extra": msg}

NF = "앱의 단위명과 요강의 단위명이 달라(명칭 개편 가능성) 확인이 필요해요. 이 대학의 정시 일반 규정은 수능 100%(학폭 감점만)예요."

MAP = {
 "경북대학교": [
   ({"gun": ["수시이월"], "name": r"^(응용화학과|화학공학과|컴퓨터학부\(글로벌소프트웨어융합\)|컴퓨터학부\(플랫폼SW데이터과학\))$"}, 0, NOTFOUND(NF)),
   ({"name": r"^디자인학과$"}, 1, {}),
   ({"name": r"^간호학과$"}, 0, {"extra": "정시 '지역인재 기초생활수급자등대상자전형'(수시 미충원 시, 학생부 교과 80% + 서류 20%)은 의예·치의예·간호·약학 대상이지만 앱의 간호학과(가, 일반)와는 별개 전형이에요."}),
   (None, 0, {"extra": "컴퓨터학부·IT대학자율학부 등 일부 앱 단위명이 요강과 달라 명칭 개편 가능성이 있어요(일반학생전형 방식으로 분류)."}),
 ],
 "부산대학교": [
   ({"gun": ["수시이월"], "name": r"^(광메카트로닉스공학과|나노메카트로닉스공학과|나노에너지공학과|동물생명자원과학과|식물생명과학과|첨단융합학부\(공학\)|첨단융합학부\(정보의생명공학\))$"}, 0, NOTFOUND(NF)),
   ({"name": r"^체육교육과$", "gun": ["수시이월"]}, 0, {"extra": "체육교육과는 이월된 경우 인문·사회계열 선발방법(수능 100%)을 적용해요."}),
   (None, 0, {}),
 ],
 "경상국립대학교": [
   ({"name": r"^(인문사회자율전공|자연과학자율전공)$"}, 1, {"cls": "미확인", "name": "요강에 없는 모집단위",
        "sum": "2027 정시모집요강에서 이 자율전공 단위를 찾지 못했어요.", "extra": "요강에는 자율전공학부(광역, 나군 30명 직접 모집)만 있어요. 분류는 수능 100% 규정을 따를 가능성이 높지만 확인이 필요해요."}),
   ({"name": r"^자율전공학부$"}, 1, {"extra": "앱에는 '수시이월'로 표기돼 있지만 요강상 나군 30명 직접 모집이에요."}),
   (None, 0, {}),
 ],
 "전남대학교": [(None, 0, {})],
 "전북대학교": [({"gun": ["수시이월"]}, 1, {}), (None, 0, {})],
 "충남대학교": [({"gun": ["수시이월"]}, 1, {}), (None, 0, {})],
 "충북대학교": [({"name": r"^소프트웨어학부$"}, 1, {}), ({"gun": ["수시이월"]}, 2, {}), (None, 0, {})],
 "강원대학교": [({"name": r"^스마트팜융합바이오시스템공학과$"}, 1, {}), (None, 0, {})],
 "제주대학교": [({"name": r"^초등교육과$"}, 0, {"f": "vB3_4"}), ({"name": r"^자유전공$"}, 1, {}), (None, 0, {})],
 # 교대
 "서울교육대학교": [(None, 0, {})],
 "경인교육대학교": [(None, 0, {})],
 "춘천교육대학교": [({"name": r"\[지역\]"}, 1, {}), (None, 0, {})],
 "청주교육대학교": [(None, 0, {})],
 "공주교육대학교": [(None, 0, {})],
 "대구교육대학교": [({"name": r"\[만학\]"}, 1, {"extra": "앱의 [만학]이 1차(학생부종합, 정성)인지 2차(수능위주, 정량)인지 확정하지 못했어요. 정시 일정과 방식이 같은 2차로 봤고, 1차 전형(서류 700 + 면접 300)은 정성이에요."}), (None, 0, {})],
 "부산교육대학교": [(None, 0, {})],
 "전주교육대학교": [(None, 0, {})],
 "광주교육대학교": [({"name": r"\[만학\]"}, 1, {}), (None, 0, {})],
 "진주교육대학교": [(None, 0, {})],
 "한국교원대학교": [({"name": r"^초등교육과$"}, 0, {}), (None, 0, {"cls": "미확인", "name": "교대 외 모집단위", "sum": "이 모집단위는 이번 조사 범위(초등교육과)가 아니에요.", "extra": ""})],
}
DEFAULT_FILE = {"경북대학교": "vB3_1", "부산대학교": "vB3_1", "경상국립대학교": "vB3_1",
                "전남대학교": "vB3_2", "전북대학교": "vB3_2", "제주대학교": "vB3_2",
                "충남대학교": "vB3_3", "충북대학교": "vB3_3", "강원대학교": "vB3_3"}
PREPEND = {"이화여자대학교": [({"name": r"^초등교육과$"}, 0, {"f": "vB3_4"})]}

def _src_list(srcs, univ):
    out = []
    for s in srcs:
        u = s.get("url", "")
        if u.startswith("http"):
            out.append({"t": (s.get("title") or univ)[:70], "u": u, "k": (s.get("kind") or "")[:40]})
    return out[:2]

def build_b3(UNIV, SRC, LV_COPY, R):
    data = {}
    for f in FILES:
        for u in json.load(open(VDIR / (f + ".json"), encoding="utf-8")):
            data[(f, u["univ"])] = u
    def get(univ, f=None):
        if f:
            return data.get((f, univ))
        f = DEFAULT_FILE.get(univ, "vB3_4")
        return data.get((f, univ))
    def mk(univ, rules):
        out = []
        for m, gi, opt in rules:
            j = get(univ, opt.get("f"))
            if not j:
                return None
            g = j["groups"][gi]
            lst = _src_list(j.get("sources", []), univ) or [{"t": univ + " 2027학년도 정시모집요강", "u": "", "k": "입학처 원문 PDF (링크 미확보)"}]
            keys = []
            for i, s in enumerate(lst):
                k = "b3_%s_%s_%d" % (univ, opt.get("f") or "m", i); SRC[k] = s; keys.append(k)
            note = []
            iv = (g.get("interview") or "").strip()
            if iv and not iv.startswith("없음") and not iv.startswith("면접 없음") and not iv.startswith("미실시"):
                note.append("면접: " + iv)
            if g.get("note"): note.append(g["note"])
            if opt.get("extra"): note.append(opt["extra"])
            out.append(R(opt.get("name", g["name"]), opt.get("cls", g["class"]), opt.get("sum", g["summary"]),
                         list(g.get("details", []))[:6], " ".join(note), keys, m=m, lvl=LV_COPY))
        return out
    missing = []
    for univ, rules in MAP.items():
        out = mk(univ, rules)
        if out is None:
            missing.append(univ); continue
        d = UNIV.setdefault(univ, {"basis": "2027학년도 정시모집요강", "lvl": LV_COPY, "rules": []})
        d["rules"] = out
        if "med" not in d:
            d["basis"] = "2027학년도 정시모집요강"
    for univ, rules in PREPEND.items():
        out = mk(univ, rules)
        if out is None:
            missing.append(univ); continue
        UNIV[univ]["rules"] = out + UNIV[univ]["rules"]
    return missing
