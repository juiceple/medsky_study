"""조사 결과 JSON 형식·완전성 검사.
사용: python3 -I tools/final_check.py <결과.json> <units.json> <요강.txt>
 - 모든 앱 단위가 unit_map에 정확히 한 번씩 있는지, group_idx·class가 유효한지
 - evidence 쪽 번호가 존재하고 인용 조각이 그 쪽에 있는지(표 병합으로 글자가 다르면 경고만)
 - 학생부 점수 반영을 시사하는 키워드가 있는 쪽 중 evidence로 인용되지 않은 쪽을 알려 준다(누락 점검용)"""
import json,re,sys
res=json.load(open(sys.argv[1],encoding='utf-8'));units=json.load(open(sys.argv[2],encoding='utf-8'))
P=open(sys.argv[3],encoding='utf-8',errors='ignore').read().split('\f')
norm=lambda s:re.sub(r'[\s| ]+','',s)
PN=[norm(p) for p in P]
err=[];warn=[]
if isinstance(res,dict): res=[res]
key=lambda u:(u['학과'],u['군'],u.get('구분'))
for r in res:
    app=r.get('appUniv','?')
    gs=r['groups']
    for i,g in enumerate(gs):
        if g['class'] not in('미반영','정량','정성'): err.append(f'{app} group{i} class={g["class"]}')
        for k in('summary','name'):
            if not g.get(k): err.append(f'{app} group{i} {k} 없음')
    seen={}
    for e in r['unit_map']:
        seen.setdefault(key(e),[]).append(e)
        gi=e['group_idx']
        if gi!='미확인' and not(isinstance(gi,int) and 0<=gi<len(gs)): err.append(f'{app} {e["학과"]} group_idx={gi}')
    # 앱 단위: 같은 대학명 단위 목록은 units.json 하나(캠퍼스 분리 시 appUniv별로 파일을 따로 검사)
    need={key(u) for u in units}
    miss=need-set(seen);extra=set(seen)-need;dup=[k for k,v in seen.items() if len(v)>1]
    if miss: err.append(f'{app} 미분류 단위 {len(miss)}: {sorted(miss)[:5]}')
    if dup: err.append(f'{app} 중복 단위 {len(dup)}: {dup[:3]}')
    if extra: warn.append(f'{app} 앱에 없는 단위 {len(extra)}: {sorted(extra)[:3]}')
    cited=set();bad=0;tot=0
    for g in gs:
        for ev in g.get('evidence',[]):
            m=re.search(r'p\.?\s*(\d+)',ev.get('where',''))
            if not m: err.append(f'{app} 근거 쪽 번호 없음: {ev.get("quote","")[:30]}');continue
            pg=int(m.group(1))
            if not 1<=pg<=len(P): err.append(f'{app} 쪽 번호 범위 밖 {pg}');continue
            cited.add(pg);tot+=1
            parts=[x for x in re.split(r'\.\.\.|…|\|',ev['quote']) if len(norm(x))>8]
            if parts and not all(norm(x) in PN[pg-1] for x in parts): bad+=1
    if tot and bad: warn.append(f'{app} 인용 {bad}/{tot}건이 해당 쪽에서 글자 그대로 찾아지지 않음(표 병합일 수 있음)')
    cnt={}
    for e in r['unit_map']:
        gi=e['group_idx'];c=gs[gi]['class'] if isinstance(gi,int) else '미확인';cnt[c]=cnt.get(c,0)+1
    print(app,'단위',len(r['unit_map']),cnt)
rx=re.compile(r'학생부\s*\(?교과\)?\s*[0-9]+\s*%|학생부교과|교과\s*(성적|점수)\s*반영|서류평가|출결\s*(점수|반영|감점)|비교과|학교생활기록부\s*(반영|평가)')
risk=[i+1 for i,p in enumerate(P) if rx.search(p)]
unc=[p for p in risk if p not in cited]
if unc: warn.append(f'학생부 반영 키워드가 있는데 인용되지 않은 쪽: {unc[:25]}')
for w in warn: print('경고:',w)
for e in err: print('오류:',e)
sys.exit(1 if err else 0)
