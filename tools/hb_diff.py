"""두 스냅샷(JSON: [[대학,학과,군,분류],...])을 비교해 대학별 분류 변화 표를 출력한다.
스냅샷은 앱을 열어 U 전체에 haksaengOf(u).cls 를 뽑아 저장한 것이다(tests나 playwright로 생성)."""
import json,sys,collections
a=json.load(open(sys.argv[1]));b=json.load(open(sys.argv[2]))
ch=collections.defaultdict(collections.Counter)
for x,y in zip(a,b):
    if x[3]!=y[3]: ch[x[0]][f'{x[3]}→{y[3]}']+=1
tot=collections.Counter()
for u,c in sorted(ch.items()):
    print(u,dict(c));tot.update(c)
print('합계',dict(tot),'대학',len(ch))
