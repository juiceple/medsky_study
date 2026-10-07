# -*- coding: utf-8 -*-
"""서울과기대·경기권 주요대학 학생부 반영 규칙 생성.

검증 JSON(docs/research/verify_b4/vB4_*.json)의 groups 와 unit_map 으로
(대학, 그룹번호, 군)별 규칙을 만든다. unit_map 에서 group_idx 가 '미확인'인 단위는
미확인 규칙, '제외'는 메디컬 단위(기존 med 규칙)라 건너뛴다.
"""
import json, pathlib, re

VDIR = pathlib.Path(__file__).resolve().parent.parent / "docs" / "research" / "verify_b4"
FILES = ["vB4_1", "vB4_2", "vB4_3"]

def _esc(s):
    return re.sub(r'([.*+?^${}()|\[\]\\/])', r'\\\1', s)

def _src_list(srcs, univ):
    out = []
    for s in srcs:
        u = s.get("url", "")
        if u.startswith("http"):
            out.append({"t": (s.get("title") or univ)[:70], "u": u, "k": (s.get("kind") or "")[:40]})
    return out[:2]

def build_b4(UNIV, SRC, LV_COPY, R):
    missing = []
    for f in FILES:
        p = VDIR / (f + ".json")
        if not p.exists():
            missing.append(f); continue
        for j in json.load(open(p, encoding="utf-8")):
            univ = j["univ"]
            lst = _src_list(j.get("sources", []), univ) or [{"t": univ + " 2027학년도 정시모집요강", "u": "", "k": "입학처 원문 PDF (링크 미확보)"}]
            keys = []
            for i, s in enumerate(lst):
                k = "b4_%s_%d" % (univ, i); SRC[k] = s; keys.append(k)
            # (group_idx, gun) -> [names]
            bucket = {}
            for e in j["unit_map"]:
                gi = e["group_idx"]
                if gi == "제외":
                    continue
                bucket.setdefault((gi, e["군"]), []).append((e["학과"], e.get("reason", "")))
            rules = []
            for (gi, gun), items in sorted(bucket.items(), key=lambda x: (str(x[0][0]), x[0][1])):
                names = "^(" + "|".join(_esc(n) for n, _ in items) + ")$"
                m = {"name": names, "gun": [gun]}
                if gi == "미확인":
                    why = items[0][1]
                    rules.append(R("요강에서 확인 안 되는 모집단위", "미확인",
                                   "2027 정시모집요강에서 이 모집단위를 같은 이름으로 확인하지 못했어요.",
                                   [], why[:200], keys, m=m, lvl=LV_COPY))
                    continue
                g = j["groups"][int(gi)]
                note = []
                iv = (g.get("interview") or "").strip()
                if iv and not iv.startswith(("없음", "면접 없음", "미실시")):
                    note.append("면접: " + iv)
                if g.get("note"):
                    note.append(g["note"])
                rules.append(R(g["name"], g["class"], g["summary"], list(g.get("details", []))[:6],
                               " ".join(note), keys, m=m, lvl=LV_COPY))
            d = UNIV.setdefault(univ, {"basis": "2027학년도 정시모집요강", "lvl": LV_COPY, "rules": []})
            d["rules"] = rules
    return missing
