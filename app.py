import streamlit as st

st.set_page_config(
    page_title="LG생활건강 사업부별 수익성 및 운영효율 분석",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
.block-container {max-width:1250px;padding-top:2.2rem;padding-bottom:4rem;}
.main-title {font-size:2.15rem;font-weight:800;letter-spacing:-0.04em;margin-bottom:.3rem;}
.main-subtitle {font-size:1rem;color:#6B7280;margin-bottom:1.8rem;}
.section-title {font-size:1.35rem;font-weight:750;letter-spacing:-0.03em;margin:.3rem 0 .4rem;}
.section-desc {color:#6B7280;font-size:.95rem;line-height:1.65;margin-bottom:1rem;}
.business-card,.diagnosis-card {border:1px solid #E5E7EB;border-radius:14px;padding:20px;background:white;}
.business-card {min-height:170px;}
.business-label,.diagnosis-number {font-size:.8rem;color:#6B7280;font-weight:700;margin-bottom:6px;}
.business-name {font-size:1.22rem;font-weight:750;margin-bottom:8px;}
.business-share {font-size:2rem;font-weight:800;letter-spacing:-.04em;margin-bottom:10px;}
.business-text,.diagnosis-text {font-size:.9rem;line-height:1.65;color:#4B5563;}
.flow-card {border:1px solid #E5E7EB;border-radius:12px;padding:16px;min-height:145px;background:#FAFAFA;}
.flow-step {font-size:.78rem;font-weight:700;color:#6B7280;margin-bottom:6px;}
.flow-title {font-size:1rem;font-weight:750;margin-bottom:8px;}
.flow-question {font-size:.85rem;line-height:1.55;color:#4B5563;}
.insight-box {border-left:4px solid #111827;background:#F7F7F8;padding:18px 20px;border-radius:8px;margin:12px 0;}
.insight-title {font-weight:750;margin-bottom:5px;}
.insight-text {line-height:1.65;color:#374151;font-size:.93rem;}
.notice-box {border:1px solid #E5E7EB;border-radius:12px;padding:18px 20px;background:#FCFCFC;margin-top:20px;}
.notice-title {font-weight:750;font-size:.95rem;margin-bottom:6px;}
.notice-text {color:#6B7280;font-size:.88rem;line-height:1.65;}
.diagnosis-card {min-height:225px;}
.diagnosis-title {font-size:1.08rem;font-weight:800;margin-bottom:10px;}
div[data-testid="stExpander"] {border:1px solid #E5E7EB;border-radius:14px;overflow:hidden;margin-bottom:12px;}
div[data-testid="stExpander"] details summary p {font-size:1rem;font-weight:700;}
button[data-baseweb="tab"] {font-weight:650;}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="main-title">LG생활건강 사업부별 수익성 및 운영효율 분석</div>
<div class="main-subtitle">
공개된 사업·재무 데이터를 활용하여 수익성 변화에서 출발해
생산·원가·재고·비용 및 현금흐름의 변화를 살펴봅니다.
</div>
""", unsafe_allow_html=True)

tabs = st.tabs([
    "개요", "사업부별 수익성", "생산·원가 분석", "재고 분석",
    "판관비 분석", "현금흐름·Global Risk", "종합진단"
])

with tabs[0]:
    with st.expander("LG생활건강은 어떤 사업구조인가요?", expanded=True):
        st.markdown("""
        <div class="section-title">Beauty · HDB · Refreshment, 서로 다른 특성을 가진 세 사업</div>
        <div class="section-desc">
        LG생활건강은 화장품, 생활용품, 음료를 중심으로 사업을 영위하고 있습니다.
        2025년 기준 매출 비중은 Beauty 37%, HDB 35%, Refreshment 28%로,
        세 사업이 비교적 균형 있게 구성되어 있습니다.
        </div>
        """, unsafe_allow_html=True)

        c1, c2, c3 = st.columns(3)
        cards = [
            ("Beauty · 화장품","Beauty","37%","더후·숨37° 등을 중심으로 한 화장품 사업입니다. 제품 효능뿐 아니라 브랜드, 디자인, 사용경험 등 무형의 가치가 함께 중요한 고부가가치 소비재 사업입니다."),
            ("Home Care & Daily Beauty","HDB","35%","엘라스틴·페리오·샤프란 등 홈케어와 퍼스널케어 제품을 중심으로 구성된 사업입니다. 일상생활에 필요한 소비재 수요를 기반으로 사업을 운영합니다."),
            ("Refreshment · 음료","Refreshment","28%","코카콜라·스프라이트·몬스터 에너지 등 탄산·비탄산 음료를 제조·판매하는 사업입니다. 생산과 유통망을 기반으로 사업을 운영합니다.")
        ]
        for col, (label, name, share, text) in zip((c1,c2,c3), cards):
            with col:
                st.markdown(f"""
                <div class="business-card">
                    <div class="business-label">{label}</div>
                    <div class="business-name">{name}</div>
                    <div class="business-share">{share}</div>
                    <div class="business-text">{text}</div>
                </div>""", unsafe_allow_html=True)

        st.markdown("""
        <div class="insight-box">
          <div class="insight-title">왜 사업부별로 나누어 분석하나요?</div>
          <div class="insight-text">
          세 사업은 수요 특성, 원재료, 생산방식, 판매채널 및 수익구조가 서로 다릅니다.
          따라서 연결재무제표의 전체 실적만 보는 것보다 <b>사업부별 실적을 먼저 확인한 뒤
          각 사업의 운영지표와 연결하여 보는 것이 수익성 변화의 원인을 파악하는 데 적합하다고 판단했습니다.</b>
          </div>
        </div>
        """, unsafe_allow_html=True)
        st.caption("자료 기준: LG생활건강 2026년 반기보고서 · 2025년 기준 사업부문별 매출 비중")

    with st.expander("어떤 흐름으로 프로그램이 구성되어 있나요?", expanded=False):
        st.markdown("""
        <div class="section-title">결과를 확인하고 → 원인을 세분화하고 → 운영지표로 검토합니다</div>
        <div class="section-desc">
        단순 재무비율 계산에 그치지 않고, 사업부별 수익성 변화에서 출발하여
        생산·원가·재고·비용 및 현금흐름 데이터를 순차적으로 확인하도록 구성했습니다.
        </div>
        """, unsafe_allow_html=True)

        steps = [
            ("STEP 01","사업부별 수익성","어느 사업부에서 매출과 영업이익의 주요 변화가 발생했는가?"),
            ("STEP 02","생산·원가","생산능력·생산실적·가동률 및 주요 원재료 가격은 어떻게 변했는가?"),
            ("STEP 03","재고","판매 변화와 함께 재고가 효율적으로 관리되고 있는가?"),
            ("STEP 04","판관비","광고선전비·지급수수료 등 비용구조는 어떻게 변화했는가?"),
            ("STEP 05","현금흐름 · Global Risk","손익 변화가 현금창출로 이어지는가? 해외사업 자산에는 어떤 위험이 있는가?"),
            ("STEP 06","종합진단","공개자료에서 확인한 원인 후보와 추가로 필요한 내부 데이터를 정리합니다.")
        ]
        for start in (0,3):
            cols = st.columns(3)
            for col, (step,title,q) in zip(cols, steps[start:start+3]):
                with col:
                    st.markdown(f"""
                    <div class="flow-card">
                      <div class="flow-step">{step}</div>
                      <div class="flow-title">{title}</div>
                      <div class="flow-question">{q}</div>
                    </div>""", unsafe_allow_html=True)
            st.write("")

        st.markdown("""
        <div class="notice-box">
          <div class="notice-title">분석 범위 안내</div>
          <div class="notice-text">
          본 프로그램은 LG생활건강이 공개한 사업보고서 및 반기보고서를 기반으로 제작했습니다.
          공개되지 않은 제품별 표준원가, 실제원가, 원재료 투입량 등은 임의로 추정하지 않습니다.<br><br>
          공개자료를 통해 확인할 수 있는 변화와 원인 후보를 파악한 뒤,
          <b>실제 재무 담당자라면 어떤 내부 데이터를 추가로 확인해야 하는지 제시하는 것</b>을 목적으로 합니다.
          </div>
        </div>
        """, unsafe_allow_html=True)

placeholders = {
    1: ("사업부별 수익성","Beauty · HDB · Refreshment의 매출, 영업이익, 영업이익률 변화를 분석할 예정입니다."),
    2: ("생산·원가 분석","생산능력, 생산실적, 가동률 및 사업부별 주요 원재료 가격 변화를 연결해 분석할 예정입니다."),
    3: ("재고 분석","사업부별 재고자산, 재고자산회전율 및 재고자산평가손실을 분석할 예정입니다."),
    4: ("판관비 분석","광고선전비, 지급수수료, 운반비 등 주요 판매비와관리비의 변화를 살펴볼 예정입니다."),
    5: ("현금흐름 · Global Risk","영업활동현금흐름과 해외 현금창출단위의 영업권·무형자산 손상 등을 분석할 예정입니다.")
}
for idx, (title, desc) in placeholders.items():
    with tabs[idx]:
        st.markdown(f"### {title}")
        st.info(desc)

with tabs[6]:
    st.markdown("""
    <div class="section-title">분석이 최종적으로 향하는 질문</div>
    <div class="section-desc">
    단순히 실적이 좋아졌는지 나빠졌는지를 판단하는 것이 아니라,
    수익성 변화가 어디에서 발생했고 그 원인을 어떤 데이터로 검증할 것인지 정리합니다.
    </div>
    """, unsafe_allow_html=True)

    d1, d2, d3 = st.columns(3)
    diagnoses = [
        ("01 · WHAT HAPPENED?","어디에서 수익성 변화가 발생했는가",
         "사업부별 매출과 영업이익을 구분하여 전사 실적 변화의 핵심 사업부를 먼저 식별합니다.<br><br>현재 공개자료에서는 2025년 Beauty 사업의 영업적자 전환이 전사 수익성 저하의 주요 요인으로 확인됩니다."),
        ("02 · WHAT SHOULD WE WATCH?","무엇을 함께 관리해야 하는가",
         "매출 회복 여부만 보는 것이 아니라 생산·원가·재고·비용의 변화가 함께 효율적으로 관리되고 있는지 살펴봅니다.<br><br>성장 자체보다 그 성장이 실제 수익성 개선으로 연결되는지가 중요합니다."),
        ("03 · WHAT WOULD FINANCE DO?","실제 재무 담당자라면 무엇을 확인할 것인가",
         "제품·채널별 매출, 표준원가와 실제원가, 제품별 생산량과 수율, SKU별 재고, 브랜드·지역별 마케팅 비용 등 내부 데이터를 추가로 확인합니다.<br><br>이를 통해 원인을 검증하고 다음 계획과 자원배분에 반영합니다.")
    ]
    for col, (num,title,text) in zip((d1,d2,d3), diagnoses):
        with col:
            st.markdown(f"""
            <div class="diagnosis-card">
              <div class="diagnosis-number">{num}</div>
              <div class="diagnosis-title">{title}</div>
              <div class="diagnosis-text">{text}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("""
    <div class="insight-box">
      <div class="insight-title">프로젝트의 최종 방향</div>
      <div class="insight-text">
      <b>성장을 매출이 아니라 수익성으로 검증합니다.</b><br><br>
      Beauty 사업의 회복 과정에서 매출 증가만을 목표로 보기보다 생산·원가·재고·비용 데이터를 함께 관리하여,
      매출 회복이 실질적인 이익과 현금창출력 개선으로 연결되는지 확인하는 것을 최종적인 분석 방향으로 설정했습니다.
      </div>
    </div>
    """, unsafe_allow_html=True)
