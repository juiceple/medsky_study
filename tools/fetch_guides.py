"""경기도교육청 '2027 정시모집요강 검색기'에서 대학별 정시모집요강 PDF를 내려받고 텍스트로 변환한다.
사용: python3 -I tools/fetch_guides.py <작업폴더>
 - 검색기(Apps Script 웹앱) HTML 안의 BOOTSTRAP JSON에서 대학 목록·요강 파일 ID를 읽는다(요강 PDF는 구글 드라이브 공개 링크).
 - <작업폴더>/pdf/<id>.pdf, <작업폴더>/txt/<id>.txt, <작업폴더>/inventory.json 을 만든다. 이미 받은 파일은 건너뛴다.
 - 12월 확정본이 올라오면 같은 명령을 새 폴더에서 다시 돌리고 txt를 이전 것과 비교(diff)하면 바뀐 대학만 골라낼 수 있다.
 - PDF는 크기가 커서(전체 약 900MB) 저장소에 올리지 않는다. 이미지만 있는 PDF(textChars가 작은 것)는 별도로 읽어야 한다."""
import json,os,re,subprocess,sys
from concurrent.futures import ThreadPoolExecutor
URL='https://script.google.com/macros/s/AKfycbyAwrvuIp0Kx8uCEhgp3ZxyFDGvYVkCPMQOMBZdPCE1gHOhuSx5VfXzFHtPzX8R-Xot/exec'
W=sys.argv[1]; os.makedirs(W+'/pdf',exist_ok=True); os.makedirs(W+'/txt',exist_ok=True)
html=subprocess.run(['curl','-sS','-L','-m','60',URL],capture_output=True,text=True).stdout
i=html.index('const BOOTSTRAP = ')+len('const BOOTSTRAP = ');j=html.index(';\n',i)
raw=html[i:j].replace('\\"','"').replace('\\/','/')
raw=re.sub(r'\\u([0-9a-fA-F]{4})',lambda m:chr(int(m.group(1),16)),raw)
D=json.loads(raw)['data']
def fid(u):
    m=re.search(r'id=([^&]+)',u or '') or re.search(r'/d/([^/]+)',u or '');return m.group(1) if m else None
def get(x):
    f=fid(x.get('guideDownloadUrl') or x.get('guideUrl'))
    if not f: return None
    out=f'{W}/pdf/{f}.pdf'
    if not(os.path.exists(out) and os.path.getsize(out)>10000):
        for _ in range(3):
            subprocess.run(['curl','-sS','-L','-m','240','-o',out,f'https://drive.google.com/uc?export=download&id={f}'])
            if open(out,'rb').read(5)==b'%PDF-': break
    if open(out,'rb').read(5)!=b'%PDF-': return {'name':x['name'],'fileId':f,'status':'not-pdf'}
    info=subprocess.run(['pdfinfo',out],capture_output=True,text=True).stdout
    txt=f'{W}/txt/{f}.txt'; subprocess.run(['pdftotext','-layout',out,txt],capture_output=True)
    t=open(txt,encoding='utf-8',errors='ignore').read()
    g=lambda k:(re.search(k+r':\s+(.*)',info) or [0,''])[1].strip()
    return {'name':x['name'],'fileId':f,'status':'ok','pages':int(g('Pages') or 0),'created':g('CreationDate'),'chars':len(t),'has2027':bool(re.search(r'2027\s*학년도',t))}
with ThreadPoolExecutor(5) as ex: res=[r for r in ex.map(get,D) if r]
json.dump(res,open(W+'/inventory.json','w'),ensure_ascii=False,indent=1)
print(len(res),'files')
