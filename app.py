import streamlit as st
import pandas as pd

st.set_page_config(page_title="LG생활건강 사업부별 수익성 및 운영효율 분석", page_icon="📊", layout="wide")
st.markdown('''<style>
.block-container{max-width:1250px;padding-top:2rem}.title{font-size:2.1rem;font-weight:800}
.sub{color:#6b7280;margin:.4rem 0 1.5rem}.box{border:1px solid #e5e7eb;border-radius:14px;padding:18px;min-height:150px}
.insight{border-left:4px solid #111827;background:#f7f7f8;padding:18px;border-radius:8px;margin:16px 0}
</style>''',unsafe_allow_html=True)
st.markdown('<div class="title">LG생활건강 사업부별 수익성 및 운영효율 분석</div><div class="sub">공개 사업·재무 데이터로 수익성 변화의 위치를 찾고 운영지표를 통해 원인 후보를 검토합니다.</div>',unsafe_allow_html=True)

profit=pd.DataFrame({
"연도":[2023]*3+[2024]*3+[2025]*3,
"사업":["Beauty","HDB","Refreshment"]*3,
"매출":[28157,21821,18070,28506,21370,18243,23500,22347,17707],
"영업이익":[1465,1253,2153,1582,1328,1681,-976,1263,1420]})
profit["영업이익률"]=profit["영업이익"]/profit["매출"]*100

tabs=st.tabs(["개요","사업부별 수익성","생산·원가","재고","판관비","현금흐름·Global Risk","종합진단"])

with tabs[0]:
    with st.expander("LG생활건강은 어떤 사업구조인가요?",expanded=True):
        st.markdown("### Beauty · HDB · Refreshment")
        cs=st.columns(3)
        data=[("Beauty","37%","럭셔리·프리미엄 화장품 중심"),("HDB","35%","홈케어·오랄케어·헤어·바디케어 중심"),("Refreshment","28%","탄산·비탄산 음료 중심")]
        for c,(n,s,d) in zip(cs,data):
            c.markdown(f'<div class="box"><b>{n}</b><h2>{s}</h2>{d}</div>',unsafe_allow_html=True)
        st.markdown('<div class="insight"><b>분석 관점</b><br>세 사업의 수익구조가 다르므로 사업부별 수익성 변화를 먼저 식별한 뒤 운영지표로 원인 후보를 좁힙니다.</div>',unsafe_allow_html=True)
    with st.expander("어떤 흐름으로 프로그램이 구성되어 있나요?"):
        st.write("**사업부별 수익성 → 생산·원가 → 재고 → 판관비 → 현금흐름·Global Risk → 종합진단**")
        st.info("공개되지 않은 제품별 표준원가·실제원가·투입량은 임의 추정하지 않습니다.")

with tabs[1]:
    st.header("사업부별 수익성")
    st.caption("단위: 억원 / 연결 기준")
    y=st.selectbox("기준 연도",[2025,2024,2023])
    d=profit[profit.연도==y].set_index("사업")
    cs=st.columns(3)
    for c,b in zip(cs,["Beauty","HDB","Refreshment"]):
        c.metric(b,f'{d.loc[b,"매출"]:,.0f}억원',f'영업이익 {d.loc[b,"영업이익"]:,.0f}억원')
        c.caption(f'영업이익률 {d.loc[b,"영업이익률"]:.1f}%')
    st.subheader("매출 추이")
    st.line_chart(profit.pivot(index="연도",columns="사업",values="매출"))
    st.subheader("영업이익 추이")
    st.bar_chart(profit.pivot(index="연도",columns="사업",values="영업이익"))
    b24=dummy=profit[(profit.연도==2024)&(profit.사업=="Beauty")].iloc[0]
    b25=profit[(profit.연도==2025)&(profit.사업=="Beauty")].iloc[0]
    decline=(b25["매출"]/b24["매출"]-1)*100
    st.markdown(f'<div class="insight"><b>핵심 해석</b><br>Beauty 매출은 2024년 {b24["매출"]:,.0f}억원에서 2025년 {b25["매출"]:,.0f}억원으로 {decline:.1f}% 감소했고, 영업이익은 {b24["영업이익"]:,.0f}억원에서 {b25["영업이익"]:,.0f}억원으로 적자 전환했습니다. 반면 HDB와 Refreshment는 흑자를 유지했습니다.<br><br><b>따라서 이후 분석은 Beauty 수익성 악화와 동시에 생산·재고·비용에서 어떤 변화가 나타났는지를 추적합니다.</b></div>',unsafe_allow_html=True)

with tabs[2]:
    st.header("생산·원가")
    p=pd.DataFrame({"연도":[2023,2024,2025],"생산능력":[24620,25522,18623],"생산실적":[19954,20562,15058]}).set_index("연도")
    st.subheader("Beauty 생산능력·생산실적")
    st.caption("단위: 억원")
    st.bar_chart(p)
    ratio=(15058/18623)*100
    st.markdown(f'<div class="insight"><b>해석</b><br>2025년 Beauty 생산능력과 생산실적은 함께 감소했습니다. 생산실적/생산능력은 약 {ratio:.1f}%로, 공개자료만으로 단순한 저가동에 따른 고정비 부담 증가를 결론내리기는 어렵습니다. 실제 업무에서는 생산능력 조정 배경, 제품 Mix, 품목별 생산량·수율을 추가 확인해야 합니다.</div>',unsafe_allow_html=True)
    raw=pd.DataFrame({"품목":["Macadamia Oil","Cetyl Alcohol","Stearyl Alcohol","Palm Stearin Oil","Palm Kernel Oil","원액","당분류","오렌지과즙","포도과즙"],"사업":["Beauty"]*3+["HDB"]*2+["Refreshment"]*4,"2024":[7892,9499,10161,1155,1930,475699,848,9248,3206],"2025":[7200,9466,14594,1034,1808,478383,802,9763,3211],"2026H1":[7798,9066,10701,1102,1978,467083,668,9392,3446]})
    biz=st.selectbox("원재료 사업 선택",["Beauty","HDB","Refreshment"])
    st.dataframe(raw[raw.사업==biz].drop(columns="사업"),use_container_width=True,hide_index=True)
    st.markdown('<div class="insight"><b>원가 관점</b><br>원재료 가격은 방향성을 보여주지만 실제 투입량이 공개되지 않아 이익 변동 원인으로 직접 환산할 수 없습니다. 내부적으로 구매가격·투입수량·표준가격·수율·폐기량·제품 Mix를 연결해 검증해야 합니다.</div>',unsafe_allow_html=True)

with tabs[3]:
    st.header("재고")
    cs=st.columns(3); cs[0].metric("2024년 말","9,224억원"); cs[1].metric("2025년 말","8,324억원","-900억원"); cs[2].metric("2026년 6월","8,827억원","+503억원 vs 2025말")
    inv=pd.DataFrame({"사업":["Beauty","HDB","Refreshment"],"2025년 말":[3104,3607,1613],"2026년 6월":[4228,2904,1695]}).set_index("사업")
    st.subheader("사업부별 재고 변화")
    st.bar_chart(inv)
    st.markdown('<div class="insight"><b>핵심 관찰</b><br>2026년 상반기 Beauty 재고는 2025년 말 약 3,104억원에서 약 4,228억원으로 증가한 반면 HDB는 감소했습니다. 재고 증가는 선제적 확보일 수도 있으므로 악화로 단정하지 않고, Beauty 매출 회복 속도와 함께 모니터링해야 합니다. 내부적으로 SKU별 재고일수·재고연령·Sell-through를 확인합니다.</div>',unsafe_allow_html=True)

with tabs[4]:
    st.header("판관비")
    sg=pd.DataFrame({"항목":["광고선전비","지급수수료","운반비"],"2024":[5000,11648,2776],"2025":[5058,9871,2783]}).set_index("항목")
    st.caption("단위: 억원 / 반올림")
    st.bar_chart(sg); st.dataframe(sg,use_container_width=True)
    st.markdown('<div class="insight"><b>핵심 해석</b><br>2025년 광고선전비는 약 5,058억원으로 전년과 유사한 반면 지급수수료는 감소했습니다. 회사가 Beauty 재정비와 해외 중점 브랜드 마케팅 확대를 추진한 만큼 단순 비용절감보다 브랜드·지역·채널별 투입이 매출·이익 개선으로 연결되는지를 검증하는 것이 중요합니다.</div>',unsafe_allow_html=True)

with tabs[5]:
    st.header("현금흐름 · Global Risk")
    cf=pd.DataFrame({"연도":[2023,2024,2025],"영업활동현금흐름":[6591,5276,4464]}).set_index("연도")
    st.subheader("영업활동현금흐름"); st.caption("단위: 억원 / 반올림"); st.line_chart(cf)
    st.markdown('<div class="insight"><b>현금흐름</b><br>영업활동현금흐름은 2023년 약 6,591억원에서 2025년 약 4,464억원으로 감소했지만 양(+)을 유지했습니다. 손익 악화와 현금창출력 변화를 구분해 볼 필요가 있습니다.</div>',unsafe_allow_html=True)
    imp=pd.DataFrame({"CGU":["Everlife","FMG & MISSION","The Creme Shop","LG H&H Singapore"],"영업권 손상":[429,170,741,84]}).set_index("CGU")
    st.subheader("2025 해외 CGU 영업권 손상"); st.caption("단위: 억원 / 반올림"); st.bar_chart(imp)
    st.markdown('<div class="insight"><b>Global Risk</b><br>일부 해외 현금창출단위에서 영업권 손상이 인식됐습니다. 이는 즉시 현금유출을 뜻하기보다 과거 인수·투자 당시 기대했던 미래 현금창출력에 대한 재평가 신호이므로 해외사업 수익성과 자산가치를 함께 점검할 필요가 있습니다.</div>',unsafe_allow_html=True)

with tabs[6]:
    st.header("종합진단")
    cs=st.columns(3)
    cards=[("WHAT HAPPENED?","Beauty가 핵심","2025년 Beauty가 영업적자로 전환하며 전사 수익성 하락을 주도했습니다."),
           ("WHAT SHOULD WE WATCH?","회복의 질","매출 회복과 함께 생산·재고·마케팅 비용 효율이 실제 이익으로 연결되는지 봅니다."),
           ("WHAT WOULD FINANCE DO?","내부 데이터로 검증","제품·채널별 매출, 표준/실제원가, 수율, SKU 재고일수, 브랜드·지역별 마케팅비를 연결합니다.")]
    for c,(k,t,x) in zip(cs,cards): c.markdown(f'<div class="box"><small>{k}</small><h3>{t}</h3>{x}</div>',unsafe_allow_html=True)
    st.markdown('<div class="insight"><b>최종 결론 — 성장을 매출이 아니라 수익성으로 검증한다</b><br><br>공개자료 기준 최근 전사 수익성 저하의 중심은 Beauty입니다. 향후 회복을 판단할 때는 매출 증가뿐 아니라 생산·원가·재고·비용 효율이 함께 개선되고 그 결과가 영업이익과 현금창출력으로 연결되는지 확인해야 합니다.<br><br><b>한계:</b> 공개자료만으로 특정 비용이 손익 악화를 얼마만큼 발생시켰는지 인과관계를 확정하지 않습니다. 원인 후보를 좁히고 실제 재무 담당자가 확인할 내부 데이터를 구체화하는 데 목적이 있습니다.</div>',unsafe_allow_html=True)
