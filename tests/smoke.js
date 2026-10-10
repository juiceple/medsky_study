/* 정시 합격 분석 도구 스모크 테스트
   사용: NODE_PATH=$(npm root -g) node tests/smoke.js [html 경로]
   Playwright(크로미움)가 필요하다. 수정할 때마다 돌려서 화면 오류·핵심 동작이 깨지지 않았는지 확인한다. */
const {chromium}=require('playwright');
const path=require('path');
const FILE=process.argv[2]||path.resolve(__dirname,'..','jeongsi_tool.html');
const EXE=process.env.CHROMIUM_PATH||'/opt/pw-browsers/chromium';
let fail=0;
const ok=(c,m)=>{console.log((c?'  ✓ ':'  ✗ ')+m);if(!c)fail++};
(async()=>{
  const b=await chromium.launch({executablePath:EXE});
  const p=await (await b.newContext({viewport:{width:1440,height:900}})).newPage();
  const errs=[];p.on('pageerror',e=>errs.push(e.message));
  await p.goto('file://'+FILE);await p.waitForSelector('.ucard',{timeout:60000});
  console.log('1. 기본 로딩');ok(errs.length===0,'페이지 오류 없음');
  ok(await p.evaluate(()=>U.length)>6000,'모집단위 6천 개 이상 로드');

  console.log('2. 숫자 서식(fmt)');
  const f=await p.evaluate(()=>[fmt(370,0),fmt(300,0),fmt(0.2,2),fmt(12.50,1),fmt(null),pct(2.063),pct(25.74)]);
  ok(f[0]==='370'&&f[1]==='300','정수 끝의 0이 지워지지 않음');ok(f[2]==='0.2'&&f[3]==='12.5'&&f[4]==='–','소수 끝 0 정리');ok(f[5]==='2.06'&&f[6]==='25.7','누백 표기 2.06 / 25.7');

  console.log('3. 보고서 어투 변환');
  const c=await p.evaluate(()=>['선발해요','누백이에요','참고 지표예요','있어요','나와요','확인하세요','거예요','필요','중요한'].map(fmText));
  ok(c.join('|')==='선발합니다|누백입니다|참고 지표입니다|있습니다|나옵니다|확인하십시오|것입니다|필요|중요한','~요 → ~습니다 변환');

  console.log('4. 탭 렌더링');
  for(const t of ['student','browse','chart','match','wish','report','data']){await p.click(`[data-tab=${t}]`);await p.waitForTimeout(400)}
  ok(errs.length===0,'모든 탭 오류 없음');

  console.log('5. 정밀 매칭 기본값');
  await p.click('[data-tab=match]');await p.waitForSelector('#mt tbody tr');
  const m=await p.evaluate(()=>({noPro:MF.noPro,key:TM.sortKey,first:B[basis][TM.last[0]][0],pro:TM.last.some(i=>isPro(U[i]))}));
  ok(m.noPro&&!m.pro,'전문대 제외가 기본');ok(m.key==='judge'&&m.first===4,'판정 순 정렬, 첫 행은 적정');

  console.log('6. 환산 불리/유리 배지');
  const pf=await p.evaluate(()=>{const o={};for(const bs of ['all','sci','hum']){basis=bs;POS_CLEAR();let n=0;U.forEach((u,i)=>{if(posFlag(i))n++});o[bs]=n}basis='all';POS_CLEAR();return {o,track:studentTrack()}});
  ok(pf.o.all>0,'전체 기준에서 배지 표시');ok(pf.track==='sci'?pf.o.hum===0:pf.o.sci===0,'계열이 다른 응시자 기준에서는 숨김');

  console.log('7. 추천 대학');
  const rec=await p.evaluate(()=>{const P=chProfile();return P.tiers.map(([l,list])=>[l,list.slice(0,12).map(x=>x.n)])});
  ok(!rec.some(([l,a])=>l==='적정 추천'&&a.includes('신한대학교')),'신한대는 적정 추천에 없음');

  console.log('8. 입력 경고');
  await p.click('[data-tab=student]');await p.fill('[data-k="kor.s"]','150');await p.dispatchEvent('[data-k="kor.s"]','change');await p.waitForTimeout(1500);
  ok(await p.locator('.notice.warn').count()===1,'범위 밖 표준점수 경고');
  await p.fill('[data-k="kor.s"]','134');await p.dispatchEvent('[data-k="kor.s"]','change');await p.waitForTimeout(1500);
  ok(await p.locator('.notice.warn').count()===0,'값을 고치면 경고 해제');

  console.log('9. 열 설정 저장');
  await p.click('[data-tab=match]');await p.waitForSelector('#mt tbody tr');
  const heads=(await p.locator('#mt thead th').allInnerTexts()).join('|');
  ok(heads.includes('과거 합격권 누백')&&['25','24','23','22','21'].every(y=>heads.includes(y)),'과거 5개년 합격권 누백 열이 기본으로 보임');
  const before=(await p.locator('#mt thead th').allInnerTexts()).length;
  await p.click('#mCols');await p.check('.colmenu [data-cm=region]');await p.waitForTimeout(300);
  ok((await p.locator('#mt thead th').allInnerTexts()).length===before+1,'열 추가');
  await p.evaluate(()=>{const T=TM;saveHide('match',COL_DEFAULT_HIDE)});

  console.log('10. 보고서');
  await p.evaluate(()=>{const f=(n,g)=>U.findIndex(u=>u[0]===n&&gunOf(u)===g);const a=f('중앙대학교','가'),b2=f('경희대학교','나'),c2=f('한국외국어대학교','다');[a,b2,c2].forEach(i=>{if(S.picks[keyOf(i)]==null)togglePick(i)});S.finals={가:keyOf(a),나:keyOf(b2),다:keyOf(c2)}});
  await p.click('[data-tab=report]');await p.waitForSelector('.rp-doc');
  const txt=await p.evaluate(()=>document.querySelector('#rpDoc').innerText);
  ok(!/[가-힣]+요(?![가-힣])/.test(txt.replace(/필요|중요|주요|수요|소요|개요/g,'')),'보고서에 ~요체 문장이 남지 않음');
  ok(!txt.includes('펑크 근거'),'보고서에 펑크 근거 없음');
  await p.emulateMedia({media:'print'});const pdf=await p.pdf({format:'A4',printBackground:true});
  ok(pdf.length>20000,'PDF 생성');

  console.log('11. 지원희망 화면');
  await p.click('[data-tab=wish]');await p.waitForTimeout(400);
  const w=await p.evaluate(()=>({sums:document.querySelectorAll('.wsum').length,secs:document.querySelectorAll('.wgun').length,fin:document.querySelectorAll('.wt tr.fin').length,hdr:[...document.querySelectorAll('.wt thead')][0]?.innerText.includes('과거 합격권 누백')}));
  ok(w.sums===3&&w.secs>=3,'군별 요약 띠(3칸)와 군별 구역');ok(w.fin===Object.keys(await p.evaluate(()=>S.finals)).length,'최종 지원 행이 강조됨');ok(w.hdr,'지원희망 표에 과거 5개년 합격권 누백 표시');
  const k0=await p.evaluate(()=>Object.keys(S.finals).length);await p.locator('[data-fin]').filter({hasText:'최종으로'}).first().click();await p.waitForTimeout(300);
  ok(await p.evaluate(()=>Object.keys(S.finals).length)>=k0,'최종으로 버튼 동작');

  console.log('\n오류:',errs.length?errs:'없음');
  await b.close();
  if(fail||errs.length){console.log(`\n실패 ${fail}건`);process.exit(1)}
  console.log('\n모든 테스트 통과');
})();
