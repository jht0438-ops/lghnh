import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="LG생활건강 2025 손익구조 분석",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================================================
# STYLE
# =========================================================
st.markdown(
    """
    <style>
        .block-container {
            max-width: 1240px;
            padding-top: 2rem;
            padding-bottom: 4rem;
        }
        .title {
            font-size: 2.2rem;
            font-weight: 800;
            letter-spacing: -0.04em;
            margin-bottom: 0.3rem;
        }
        .subtitle {
            color: #6B7280;
            line-height: 1.7;
            margin-bottom: 1.7rem;
        }
        .question-box {
            border: 1px solid #E5E7EB;
            border-radius: 14px;
            padding: 20px 22px;
            background: #FAFAFA;
            margin-bottom: 18px;
        }
        .question-label {
            font-size: 0.78rem;
            color: #6B7280;
            font-weight: 700;
            margin-bottom: 6px;
        }
        .question-text {
            font-size: 1.15rem;
            font-weight: 800;
            line-height: 1.55;
        }
        .insight {
            border-left: 4px solid #111827;
            background: #F7F7F8;
            padding: 18px 20px;
            border-radius: 8px;
            margin-top: 14px;
            margin-bottom: 14px;
            line-height: 1.7;
        }
        .card {
            border: 1px solid #E5E7EB;
            border-radius: 14px;
            padding: 18px;
            background: white;
            min-height: 155px;
        }
        .card-label {
            color: #6B7280;
            font-size: 0.78rem;
            font-weight: 700;
            margin-bottom: 5px;
        }
        .card-title {
            font-size: 1.2rem;
            font-weight: 800;
            margin-bottom: 8px;
        }
        .card-body {
            color: #4B5563;
            font-size: 0.91rem;
            line-height: 1.6;
        }
        .big-number {
            font-size: 1.8rem;
            font-weight: 800;
            letter-spacing: -0.03em;
            margin: 5px 0 8px 0;
        }
        .small-note {
            font-size: 0.83rem;
            color: #6B7280;
            line-height: 1.6;
        }
        .final-box {
            border: 1px solid #D1D5DB;
            border-radius: 14px;
            padding: 22px;
            background: #FCFCFC;
            line-height: 1.75;
        }
        button[data-baseweb="tab"] {
            font-weight: 650;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# =========================================================
# DATA
# =========================================================
# 연결 기준, 단위: 억원
income = pd.DataFrame({
    "구분": ["매출", "매출총이익", "영업이익", "세전손익", "당기순손익"],
    "2023": [68048, 36269, 4870, 2764, 1635],
    "2024": [68119, 35608, 4590, 3166, 2039],
    "2025": [63555, 31446, 1707, -633, -858],
}).set_index("구분")

segment = pd.DataFrame({
    "연도": [2023, 2023, 2023, 2024, 2024, 2024, 2025, 2025, 2025],
    "사업": ["Beauty", "HDB", "Refreshment"] * 3,
    "매출": [28157, 21821, 18070, 28506, 21370, 18243, 23500, 22347, 17707],
    "영업이익": [1465, 1253, 2153, 1582, 1328, 1681, -976, 1263, 1420]
})
segment["영업이익률"] = segment["영업이익"] / segment["매출"] * 100

gross_margin = pd.DataFrame({
    "연도": [2023, 2024, 2025],
    "매출총이익률": [
        36269 / 68048 * 100,
        35608 / 68119 * 100,
        31446 / 63555 * 100,
    ],
    "판관비율": [
        31399 / 68048 * 100,
        31018 / 68119 * 100,
        29739 / 63555 * 100,
    ]
}).set_index("연도")

bridge = pd.DataFrame({
    "항목": [
        "영업이익",
        "금융손익",
        "기타영업외손익",
        "지분법손익",
        "세전손익",
        "법인세",
        "당기순손익"
    ],
    "2025": [
        1707,
        -38,
        -2342,
        40,
        -633,
        -225,
        -858
    ]
}).set_index("항목")

cashflow = pd.DataFrame({
    "연도": [2023, 2024, 2025],
    "영업활동현금흐름": [6591, 5276, 4464]
}).set_index("연도")

impairment = pd.DataFrame({
    "해외 CGU": ["Everlife", "FMG & MISSION", "The Creme Shop", "LG H&H Singapore"],
    "2025 영업권 손상": [429, 170, 741, 84]
}).set_index("해외 CGU")

# =========================================================
# HEADER
# =========================================================
st.markdown('<div class="title">LG생활건강 2025 손익구조 분석</div>', unsafe_allow_html=True)
st.markdown(
    """
    <div class="subtitle">
        공개 재무제표만으로 확인 가능한 범위에서
        <b>2025년 순손실 전환의 원인을 손익구조 → Beauty → 매출총이익률 → 손상 → 현금흐름</b>
        순서로 분석합니다.
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="question-box">
        <div class="question-label">CORE QUESTION</div>
        <div class="question-text">
            LG생활건강은 2025년 왜 순손실로 전환했고,
            그 손실을 어떻게 해석해야 하는가?
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

tabs = st.tabs([
    "개요",
    "손익구조",
    "Beauty 분석",
    "매출총이익률",
    "손상·해외사업",
    "현금흐름",
    "종합진단"
])

# =========================================================
# 1. OVERVIEW
# =========================================================
with tabs[0]:
    st.header("분석 개요")

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(
            """
            <div class="card">
                <div class="card-label">STEP 01</div>
                <div class="card-title">본업 수익성</div>
                <div class="card-body">
                    영업이익이 왜 크게 감소했는지,
                    사업부와 매출총이익 구조에서 확인합니다.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
    with c2:
        st.markdown(
            """
            <div class="card">
                <div class="card-label">STEP 02</div>
                <div class="card-title">순손실 전환</div>
                <div class="card-body">
                    영업이익은 플러스인데 왜 세전손실과 순손실로 내려갔는지
                    영업외손익과 손상차손을 확인합니다.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
    with c3:
        st.markdown(
            """
            <div class="card">
                <div class="card-label">STEP 03</div>
                <div class="card-title">현금창출력</div>
                <div class="card-body">
                    회계상 손실과 실제 영업현금흐름이 동일한 방향인지
                    구분해서 해석합니다.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown(
        """
        <div class="insight">
            <b>분석 원칙</b><br>
            본 프로그램은 공개 재무제표에서 직접 확인 가능한 수치만을 사용합니다.
            제품별 원가, 브랜드별 이익, 제품별 수율처럼 공개되지 않은 내부 데이터는 임의 추정하지 않습니다.
            대신 공개자료만으로도 결론을 낼 수 있는 손익구조와 현금흐름 중심으로 분석합니다.
        </div>
        """,
        unsafe_allow_html=True
    )

# =========================================================
# 2. INCOME STRUCTURE
# =========================================================
with tabs[1]:
    st.header("손익구조: 어디서 크게 꺾였나?")
    st.caption("연결 기준 / 단위: 억원")

    st.dataframe(
        income.style.format("{:,.0f}"),
        use_container_width=True
    )

    st.subheader("2023~2025 손익 주요 항목")
    st.line_chart(income.T)

    sales_24 = income.loc["매출", "2024"]
    sales_25 = income.loc["매출", "2025"]
    gp_24 = income.loc["매출총이익", "2024"]
    gp_25 = income.loc["매출총이익", "2025"]
    op_24 = income.loc["영업이익", "2024"]
    op_25 = income.loc["영업이익", "2025"]

    sales_change = (sales_25 / sales_24 - 1) * 100
    gp_change = (gp_25 / gp_24 - 1) * 100
    op_change = (op_25 / op_24 - 1) * 100

    c1, c2, c3 = st.columns(3)
    c1.metric("매출", f"{sales_25:,.0f}억원", f"{sales_change:.1f}% YoY")
    c2.metric("매출총이익", f"{gp_25:,.0f}억원", f"{gp_change:.1f}% YoY")
    c3.metric("영업이익", f"{op_25:,.0f}억원", f"{op_change:.1f}% YoY")

    st.markdown(
        """
        <div class="insight">
            <b>핵심 해석</b><br>
            2025년에는 매출이 감소했지만 매출총이익은 그보다 더 큰 폭으로 감소했습니다.
            판관비가 급증한 구조가 아니라 <b>매출 단계에서부터 총이익 창출력이 약해진 것</b>이
            영업이익 감소의 핵심 출발점입니다.
        </div>
        """,
        unsafe_allow_html=True
    )

# =========================================================
# 3. BEAUTY
# =========================================================
with tabs[2]:
    st.header("Beauty 분석: 전사 악화의 중심은 어디인가?")
    st.caption("연결 기준 / 단위: 억원")

    sales_pivot = segment.pivot(index="연도", columns="사업", values="매출")
    op_pivot = segment.pivot(index="연도", columns="사업", values="영업이익")

    st.subheader("사업부별 매출")
    st.line_chart(sales_pivot)

    st.subheader("사업부별 영업이익")
    st.bar_chart(op_pivot)

    beauty_24 = segment[(segment["연도"] == 2024) & (segment["사업"] == "Beauty")].iloc[0]
    beauty_25 = segment[(segment["연도"] == 2025) & (segment["사업"] == "Beauty")].iloc[0]

    c1, c2, c3 = st.columns(3)
    c1.metric(
        "Beauty 매출",
        f'{beauty_25["매출"]:,.0f}억원',
        f'{(beauty_25["매출"]/beauty_24["매출"]-1)*100:.1f}% YoY'
    )
    c2.metric(
        "Beauty 영업이익",
        f'{beauty_25["영업이익"]:,.0f}억원',
        f'{beauty_25["영업이익"]-beauty_24["영업이익"]:,.0f}억원 변화'
    )
    c3.metric(
        "Beauty 영업이익률",
        f'{beauty_25["영업이익률"]:.1f}%',
        f'{beauty_25["영업이익률"]-beauty_24["영업이익률"]:.1f}%p'
    )

    st.markdown(
        """
        <div class="insight">
            <b>결론</b><br>
            2025년 전사 영업수익성 악화는 세 사업이 동시에 무너진 결과가 아닙니다.
            <b>Beauty가 영업흑자에서 적자로 전환한 것이 핵심</b>이며,
            HDB와 Refreshment는 여전히 영업흑자를 유지했습니다.
            따라서 전사 회복 여부를 판단할 때 Beauty 사업의 회복 여부가 가장 중요한 관찰 포인트입니다.
        </div>
        """,
        unsafe_allow_html=True
    )

# =========================================================
# 4. GROSS MARGIN
# =========================================================
with tabs[3]:
    st.header("매출총이익률: 단순 매출 감소만의 문제인가?")

    st.subheader("매출총이익률 vs 판관비율")
    st.line_chart(gross_margin)

    gm_24 = gross_margin.loc[2024, "매출총이익률"]
    gm_25 = gross_margin.loc[2025, "매출총이익률"]
    sga_24 = 31018
    sga_25 = 29739

    c1, c2, c3 = st.columns(3)
    c1.metric("2024 매출총이익률", f"{gm_24:.1f}%")
    c2.metric("2025 매출총이익률", f"{gm_25:.1f}%", f"{gm_25-gm_24:.1f}%p")
    c3.metric("2025 판관비", f"{sga_25:,.0f}억원", f"{sga_25-sga_24:,.0f}억원")

    st.markdown(
        """
        <div class="insight">
            <b>핵심 해석</b><br>
            2025년 매출총이익률은 약 49.5%로 2024년 약 52.3%에서 하락했습니다.
            반면 판관비는 오히려 전년보다 감소했습니다.
            따라서 2025년 영업이익 악화를 <b>'비용을 너무 많이 써서 생긴 문제'</b>로 해석하는 것은 적절하지 않습니다.
            공개 재무제표만 놓고 보면 <b>매출 감소 + 매출총이익률 하락</b>이 더 중요한 변화입니다.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.info(
        "매출총이익률 하락의 구체적 원인이 제품 Mix, 할인, 원재료, 채널 변화 중 무엇인지는 공개 재무제표만으로 확정할 수 없습니다."
    )

# =========================================================
# 5. IMPAIRMENT / GLOBAL
# =========================================================
with tabs[4]:
    st.header("손상·해외사업: 영업이익이 남았는데 왜 순손실인가?")

    st.subheader("2025 손익 Bridge")
    st.bar_chart(bridge)

    st.subheader("주요 해외 CGU 영업권 손상")
    st.caption("단위: 억원 / 반올림")
    st.bar_chart(impairment)

    c1, c2, c3 = st.columns(3)
    c1.metric("2025 영업이익", "1,707억원")
    c2.metric("기타영업외비용", "2,799억원")
    c3.metric("무형자산손상차손", "1,798억원")

    st.markdown(
        """
        <div class="insight">
            <b>핵심 해석</b><br>
            2025년에는 영업이익이 플러스였지만 기타영업외비용이 크게 발생했고,
            그 안에서 무형자산 손상차손의 영향이 컸습니다.
            따라서 순손실 전환은 단순히 본업의 영업적자 때문이 아니라
            <b>본업 수익성 약화 + 과거 투자자산 가치 하락</b>이 함께 반영된 결과로 볼 수 있습니다.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="insight">
            <b>Finance 관점</b><br>
            영업권 손상은 당기의 현금유출 자체를 의미하지 않습니다.
            다만 과거 인수·투자 당시 기대했던 미래 현금창출력에 대한 재평가라는 점에서,
            해외사업이 투자 당시 기대한 경제적 성과를 내고 있는지 점검해야 한다는 신호로 볼 수 있습니다.
        </div>
        """,
        unsafe_allow_html=True
    )

# =========================================================
# 6. CASH FLOW
# =========================================================
with tabs[5]:
    st.header("현금흐름: 순손실이면 현금창출력도 무너졌나?")

    st.line_chart(cashflow)

    c1, c2, c3 = st.columns(3)
    c1.metric("2023 영업CF", "6,591억원")
    c2.metric("2024 영업CF", "5,276억원", "-1,315억원")
    c3.metric("2025 영업CF", "4,464억원", "-812억원")

    st.markdown(
        """
        <div class="insight">
            <b>핵심 해석</b><br>
            2025년 당기순손실은 858억원이었지만 영업활동현금흐름은 +4,464억원이었습니다.
            이는 손상차손, 감가상각비 등 비현금성 비용이 손익에는 반영되지만
            당기 현금유출과 동일하지 않기 때문입니다.
            따라서 <b>회계상 손실과 실제 영업현금창출력은 구분해서 해석해야 합니다.</b>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.warning(
        "다만 영업활동현금흐름은 2023 → 2024 → 2025로 2년 연속 감소했습니다. "
        "따라서 '현금은 문제없다'가 아니라, 여전히 양(+)이지만 현금창출력도 약화 추세라는 해석이 적절합니다."
    )

# =========================================================
# 7. FINAL
# =========================================================
with tabs[6]:
    st.header("종합진단")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown(
            """
            <div class="card">
                <div class="card-label">01 · 본업</div>
                <div class="card-title">Beauty 수익성 약화</div>
                <div class="card-body">
                    Beauty가 영업적자로 전환하며 전사 영업이익 감소를 주도했습니다.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c2:
        st.markdown(
            """
            <div class="card">
                <div class="card-label">02 · 영업외</div>
                <div class="card-title">손상차손 부담</div>
                <div class="card-body">
                    해외사업 관련 무형자산 손상 등이 반영되며
                    영업이익이 세전손실·순손실로 내려갔습니다.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c3:
        st.markdown(
            """
            <div class="card">
                <div class="card-label">03 · 현금</div>
                <div class="card-title">현금흐름은 아직 플러스</div>
                <div class="card-body">
                    회계상 순손실에도 영업CF는 양(+)을 유지했지만,
                    절대 규모는 2년 연속 감소했습니다.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown(
        """
        <div class="final-box">
            <b>최종 결론</b><br><br>
            2025년 LG생활건강의 실적 악화는 단순한 비용 증가 문제가 아닙니다.
            Beauty 사업의 매출 감소와 함께 매출총이익률이 하락하면서 본업 수익성이 약화되었고,
            여기에 해외사업 관련 무형자산 손상 등이 더해지며 순손실로 전환되었습니다.
            <br><br>
            다만 영업활동현금흐름은 여전히 양(+)을 유지하고 있어,
            회계상 손실이 곧 현금창출력 상실을 의미하지는 않습니다.
            따라서 향후 회복을 판단할 때는
            <b>① Beauty 매출과 영업이익 회복, ② 매출총이익률 개선,
            ③ 해외사업 수익성 및 추가 손상 여부, ④ 영업현금흐름의 회복</b>
            을 함께 확인할 필요가 있습니다.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("### 재무 담당자라면 이후 무엇을 볼 것인가?")
    st.write(
        """
        - Beauty의 브랜드·채널·지역별 매출 및 이익률
        - 제품 Mix 변화가 매출총이익률에 미친 영향
        - 해외법인 및 CGU별 사업계획 대비 실적
        - 손상검사에 사용된 미래현금흐름 가정의 적정성
        - 영업현금흐름 감소의 운전자본·비현금항목별 원인
        """
    )
