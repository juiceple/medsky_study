# -*- coding: utf-8 -*-
"""건동홍숙·국숭세단성·광명상가·한서삼·기타 여대(비메디컬) 학생부 반영 규칙 생성.

- 검증된 조사 JSON(docs/research/verify_b2/vB2_*.json)의 그룹 요약을 그대로 쓰고,
  "앱의 어느 모집단위에 어느 그룹을 적용할지"만 MAP 에서 지정한다. (hb_med_spec.py 와 같은 방식)
- MAP 항목: (매칭, 그룹번호, 옵션) / 옵션: cls name sum extra
- 한 대학에 메디컬 규칙(med)이 이미 있으면 그대로 두고 비메디컬 규칙(rules)만 채운다.
"""
import json, pathlib

VDIR = pathlib.Path(__file__).resolve().parent.parent / "docs" / "research" / "verify_b2"
FILES = ["vB2_1", "vB2_2", "vB2_2b", "vB2_3", "vB2_4"]

# 검증 JSON 의 univ 이름 → 앱 대학명
ALIAS = {"명지대학교(인문)": "명지대학교", "가톨릭대학교(비메디컬)": "가톨릭대학교"}

CONTRACT_NOTE = "계약학과 채용조건형·재직자 등 정원외 특별전형은 이 앱의 모집단위가 아니라 제외했어요."

# 앱 대학명 → [(매칭, 그룹번호, 옵션)]
MAP = {
 "건국대학교": [({"gun": ["수시이월"]}, 2, {}), (None, 0, {})],
 "동국대학교": [({"gun": ["다"], "name": r"^(교육학과|국어교육과|역사교육과|지리교육과|수학교육과|가정교육과)$"}, 2, {"cls": "정량"}),
                ({"gun": ["다"]}, 1, {"cls": "정량"}), (None, 0, {})],
 "홍익대학교": [({"zone": ["홍익대예"]}, 1, {}), (None, 0, {})],
 "숙명여자대학교": [({"gun": ["나"]}, 1, {}), (None, 0, {})],
 "국민대학교": [({"name": r"^(공간디자인학과|영상디자인학과)$"}, 1, {}), ({"name": r"^스포츠건강재활학과$"}, 2, {}), (None, 0, {})],
 "숭실대학교": [(None, 0, {})],
 "세종대학교": [(None, 0, {})],
 "단국대학교": [(None, 0, {})],
 "성신여자대학교": [(None, 0, {})],
 "광운대학교": [(None, 0, {})],
 "명지대학교": [(None, 0, {})],
 "명지대학교(자연)": [(None, 0, {})],
 "상명대학교": [(None, 0, {})],
 "가톨릭대학교": [(None, 0, {})],
 "한성대학교": [(None, 0, {})],
 "서경대학교": [(None, 0, {"extra": "헤어디자인학과·코스메틱뷰티매니지먼트학과는 계약학과 채용조건형(정원외, 학생부 교과 200점 + 산업체매칭 800점, 정량)이 따로 있어요. " + CONTRACT_NOTE})],
 "삼육대학교": [(None, 0, {"extra": "경영학과는 특성화고졸재직자전형(정원외, 학생부 교과 100%, 정량)이 따로 있어요. " + CONTRACT_NOTE})],
 "동덕여자대학교": [(None, 0, {})],
 "서울여자대학교": [(None, 0, {})],
 "덕성여자대학교": [({"name": r"^자유전공학부$"}, 1, {}), (None, 0, {"extra": "정원외 재직자 학생부종합 전형은 이 앱의 모집단위가 아니라 제외했어요."})],
}

def _src_list(srcs, univ):
    out = []
    for s in srcs:
        u = s.get("url", "")
        if not u.startswith("http"):
            continue
        out.append({"t": (s.get("title") or univ)[:70], "u": u, "k": (s.get("kind") or "")[:40]})
    return out[:2]

def build_b2(UNIV, SRC, LV_COPY, R):
    data = {}
    for f in FILES:
        p = VDIR / (f + ".json")
        if not p.exists():
            continue
        for u in json.load(open(p, encoding="utf-8")):
            data[ALIAS.get(u["univ"], u["univ"])] = u
    missing = []
    for univ, rules in MAP.items():
        j = data.get(univ)
        if not j:
            missing.append(univ); continue
        lst = _src_list(j.get("sources", []), univ) or [{"t": univ + " 2027학년도 정시모집요강", "u": "", "k": "입학처 원문 PDF (링크 미확보)"}]
        keys = []
        for i, s in enumerate(lst):
            k = "b2_%s_%d" % (univ, i); SRC[k] = s; keys.append(k)
        out = []
        for m, gi, opt in rules:
            g = j["groups"][gi]
            note_parts = []
            iv = (g.get("interview") or "").strip()
            if iv and not iv.startswith("없음") and not iv.startswith("면접 없음"):
                note_parts.append("면접: " + iv)
            if g.get("note"):
                note_parts.append(g["note"])
            if opt.get("extra"):
                note_parts.append(opt["extra"])
            out.append(R(opt.get("name", g["name"]), opt.get("cls", g["class"]), opt.get("sum", g["summary"]),
                         list(g.get("details", []))[:6], " ".join(note_parts), keys, m=m, lvl=LV_COPY))
        d = UNIV.setdefault(univ, {"basis": "2027학년도 정시모집요강", "lvl": LV_COPY, "rules": []})
        d["rules"] = out
        d["basis"] = "2027학년도 정시모집요강" if "med" not in d else d["basis"]
    return missing
