"""요강 텍스트(pdftotext 결과)를 쪽 번호와 함께 검색·출력한다. 쪽 번호는 PDF 쪽(1부터)이다.
  python3 -I tools/guide_grep.py <txt> grep <정규식> [앞뒤줄수=1]   # 일치하는 줄을 '쪽:줄' 번호와 함께 출력
  python3 -I tools/guide_grep.py <txt> page <시작쪽> [끝쪽]          # 해당 쪽 전체 출력
  python3 -I tools/guide_grep.py <txt> pages                          # 쪽별 글자 수(이미지 전용 쪽 찾기)"""
import re,sys
f,cmd=sys.argv[1],sys.argv[2]
P=open(f,encoding='utf-8',errors='ignore').read().split('\f')
if cmd=='grep':
    rx=re.compile(sys.argv[3]);c=int(sys.argv[4]) if len(sys.argv)>4 else 1
    for pi,p in enumerate(P,1):
        L=p.split('\n')
        for li,l in enumerate(L):
            if rx.search(l):
                print(f'--- p.{pi}:{li+1}')
                print('\n'.join(x.rstrip() for x in L[max(0,li-c):li+c+1]))
elif cmd=='page':
    a=int(sys.argv[3]);b=int(sys.argv[4]) if len(sys.argv)>4 else a
    for pi in range(a,b+1): print(f'===== PDF p.{pi} =====');print(P[pi-1])
elif cmd=='pages':
    print(' '.join(f'{i}:{len(p.strip())}' for i,p in enumerate(P,1)))
