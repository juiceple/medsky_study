# -*- coding: utf-8 -*-
"""2027 정시모집요강(경기도교육청 검색기 수록본) 기준 학생부 반영 규칙 생성.

docs/research/verify_2027final/final_*.json 의 각 원소(앱 대학명 appUniv 단위)로 규칙을 만든다.
 - groups[i]: {name, class, summary, details, note, interview, evidence}
 - unit_map[i]: {학과, 군, 구분, group_idx(정수 또는 '미확인'), reason}
 - 앱 구분이 ★(메디컬)인 단위는 UNIV[대학]["med"], 그 외는 UNIV[대학]["rules"]에 넣는다.
 - 이 대학은 기존 규칙(med·rules)을 전부 새 규칙으로 바꾼다.
 - '앱에 없는 전형'(otherTracksNotInApp)은 화면에 표시하지 않으므로 규칙에 넣지 않는다.
"""
import json, pathlib, re, glob

VDIR = pathlib.Path(__file__).resolve().parent.parent / "docs" / "research" / "verify_2027final"
LV = "대학 발행 정시모집요강 원문 확인 · 독립 검증 완료"
BASIS = "2027학년도 정시모집요강(경기도교육청 정시모집요강 검색기 수록본)"

def _esc(s):
    return re.sub(r'([.*+?^${}()|\[\]\\/])', r'\\\1', s)

def build_final(UNIV, SRC, R):
    files = sorted(glob.glob(str(VDIR / "final_*.json")))
    n = 0
    for f in files:
        for j in json.load(open(f, encoding="utf-8")):
            univ = j["appUniv"]
            srcs = j.get("sources", [])
            keys = []
            for i, s in enumerate(srcs[:2]):
                k = "fin_%s_%d" % (univ, i)
                SRC[k] = {"t": (s.get("title") or univ + " 2027학년도 정시모집요강")[:70], "u": s.get("url", ""), "k": s.get("kind") or "대학 발행 요강 원문(경기도교육청 검색기 수록본)"}
                keys.append(k)
            bucket = {}
            for e in j["unit_map"]:
                med = str(e.get("구분", "")) in ("★의대", "★치대", "★한의대", "★약대", "★수의대")
                bucket.setdefault((med, e["group_idx"], e["군"], e.get("구분") if med else None), []).append((e["학과"], e.get("reason", "")))
            rules, med_rules = [], []
            for (med, gi, gun, zone), items in sorted(bucket.items(), key=lambda x: (x[0][0], str(x[0][1]), x[0][2], str(x[0][3]))):
                names = "^(" + "|".join(_esc(nm) for nm, _ in items) + ")$"
                m = {"name": names, "gun": [gun]}
                if zone: m["zone"] = [zone]
                if gi == "미확인":
                    r = R("요강에서 확인 안 되는 모집단위", "미확인", "2027 정시모집요강에서 이 모집단위를 같은 이름으로 확인하지 못했어요.", [], items[0][1][:200], keys, m=m, lvl=LV)
                else:
                    g = j["groups"][int(gi)]
                    note = []
                    iv = (g.get("interview") or "").strip()
                    if iv and not iv.startswith(("없음", "면접 없음", "미실시")): note.append("면접·실기: " + iv)
                    if g.get("note"): note.append(g["note"])
                    r = R(g["name"], g["class"], g["summary"], list(g.get("details", []))[:6], " ".join(note), keys, m=m, lvl=LV)
                (med_rules if med else rules).append(r)
            UNIV[univ] = {"basis": BASIS, "lvl": LV, "rules": rules}
            if med_rules: UNIV[univ]["med"] = med_rules
            n += 1
    return n
