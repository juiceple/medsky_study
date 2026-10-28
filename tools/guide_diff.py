"""12월 요강 재수집 후, 10월에 받은 요강과 달라진 대학만 골라낸다.
사용: python3 -I tools/guide_diff.py <이전 작업폴더> <새 작업폴더> [결과.json]
 - 두 폴더는 tools/fetch_guides.py 가 만든 폴더(inventory.json, txt/)
 - 대학별로 파일 ID·쪽수·PDF 생성일이 바뀌었는지, 본문(txt)이 쪽 단위로 얼마나 바뀌었는지 비교한다
 - 이미지 PDF(본문 없음)는 파일 ID·쪽수·생성일만 비교한다(바뀌었으면 사람이 이미지로 확인해야 한다)
 - 결과: 바뀐 대학 목록(바뀐 쪽 번호 포함)을 쪽 수 많은 순으로 출력. '재조사 대상'은 이미 앱에 반영한 대학(docs/research/verify_2027final/final_*.json) 중 바뀐 곳"""
import difflib,glob,json,os,re,sys
old,new=sys.argv[1],sys.argv[2]
out=sys.argv[3] if len(sys.argv)>3 else None
def inv(w):
    return {(x['name'],x.get('campus','')):x for x in json.load(open(w+'/inventory.json',encoding='utf-8'))}
def pages(w,x):
    p=f"{w}/txt/{x['guideFileId']}.txt"
    if not os.path.exists(p): return []
    return open(p,encoding='utf-8',errors='ignore').read().split('\f')
norm=lambda s:re.sub(r'\s+','',s)
here=os.path.dirname(os.path.abspath(__file__))
vdir=os.path.join(here,'..','docs','research','verify_2027final')
verified=set()
for f in glob.glob(vdir+'/final_*.json'):
    for j in json.load(open(f,encoding='utf-8')): verified.add(j['appUniv'])
nm=json.load(open(os.path.join(here,'..','docs','research','guides_2027','name_map.json'),encoding='utf-8'))
ver_keys={(v['name'],v['campus']) for k,v in nm.items() if k in verified}
A,B=inv(old),inv(new)
res=[]
for k,b in B.items():
    a=A.get(k)
    row={'대학':k[0],'캠퍼스':k[1],'재조사대상':k in ver_keys}
    if not a:
        row.update(변경='새로 등록'); res.append(row); continue
    why=[]
    if a['guideFileId']!=b['guideFileId']: why.append('파일 교체')
    if a['pages']!=b['pages']: why.append('쪽수 %s→%s'%(a['pages'],b['pages']))
    if a.get('pdfCreated')!=b.get('pdfCreated'): why.append('PDF 생성일 변경')
    pa,pb=pages(old,a),pages(new,b)
    changed=[]
    img=sum(len(t.strip()) for t in pa)<500 and sum(len(t.strip()) for t in pb)<500
    if pa and pb and not img:
        for i in range(max(len(pa),len(pb))):
            x=norm(pa[i]) if i<len(pa) else ''
            y=norm(pb[i]) if i<len(pb) else ''
            if x!=y and difflib.SequenceMatcher(None,x,y,autojunk=False).quick_ratio()<0.999: changed.append(i+1)
    elif img and why: why.append('이미지 PDF: 사람이 직접 확인')
    if changed: why.append('바뀐 쪽 %d개'%len(changed))
    if why:
        row.update(변경=', '.join(why),바뀐쪽=changed); res.append(row)
for k in A:
    if k not in B: res.append({'대학':k[0],'캠퍼스':k[1],'재조사대상':k in ver_keys,'변경':'새 목록에서 사라짐'})
res.sort(key=lambda r:(-len(r.get('바뀐쪽',[])),r['대학']))
for r in res: print(('★' if r['재조사대상'] else ' '),r['대학'],r['캠퍼스'],'|',r['변경'],('| 쪽 '+','.join(map(str,r['바뀐쪽'][:15]))) if r.get('바뀐쪽') else '')
print('바뀐 대학 %d곳 중 재조사 대상(★) %d곳'%(len(res),sum(r['재조사대상'] for r in res)))
if out: json.dump(res,open(out,'w',encoding='utf-8'),ensure_ascii=False,indent=1)
