import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="LG생활건강 2025 손익구조 분석",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
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
        /* 왼쪽 내비게이션 */
        section[data-testid="stSidebar"] {
            border-right: 1px solid #E5E7EB;
            background: #FAFAFA;
        }
        section[data-testid="stSidebar"] > div {
            padding-top: 1.4rem;
        }
        .nav-brand {
            font-size: 1.12rem;
            font-weight: 800;
            letter-spacing: -0.03em;
            padding: 0.2rem 0 1rem 0;
            border-bottom: 1px solid #E5E7EB;
            margin-bottom: 1rem;
        }
        .nav-caption {
            font-size: 0.75rem;
            color: #9CA3AF;
            font-weight: 700;
            letter-spacing: 0.04em;
            margin-bottom: 0.3rem;
        }
        section[data-testid="stSidebar"] div[role="radiogroup"] {
            gap: 0.35rem;
        }
        section[data-testid="stSidebar"] label[data-baseweb="radio"] {
            background: transparent;
            border: 1px solid transparent;
            border-radius: 10px;
            padding: 0.6rem 0.7rem;
            transition: all 0.15s ease;
        }
        section[data-testid="stSidebar"] label[data-baseweb="radio"]:hover {
            background: #F3F4F6;
            border-color: #E5E7EB;
        }
        section[data-testid="stSidebar"] label[data-baseweb="radio"]:has(input:checked) {
            background: #FFFFFF;
            border-color: #D1D5DB;
            box-shadow: 0 1px 3px rgba(0,0,0,0.04);
        }
        section[data-testid="stSidebar"] label[data-baseweb="radio"] > div:first-child {
            display: none;
        }
        section[data-testid="stSidebar"] label[data-baseweb="radio"] p {
            font-weight: 650;
            font-size: 0.94rem;
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


# 2026 H1 후속 분석 데이터
h1_compare = pd.DataFrame({
    "항목": ["매출", "매출총이익", "영업이익", "반기순이익"],
    "2025 H1": [33027, 16839, 1972, 1420],
    "2026 H1": [32340, 16750, 2106, 1664]
}).set_index("항목")

h1_segments = pd.DataFrame({
    "사업": ["Beauty", "HDB", "Refreshment"],
    "2025 H1 매출": [16671, 7596, 8760],
    "2026 H1 매출": [15895, 7755, 8690],
    "2025 H1 영업이익": [621, 456, 895],
    "2026 H1 영업이익": [830, 478, 799],
}).set_index("사업")

h1_segments["2025 H1 영업이익률"] = h1_segments["2025 H1 영업이익"] / h1_segments["2025 H1 매출"] * 100
h1_segments["2026 H1 영업이익률"] = h1_segments["2026 H1 영업이익"] / h1_segments["2026 H1 매출"] * 100

h1_working_capital = pd.DataFrame({
    "항목": ["매출채권 및 기타채권", "재고자산"],
    "2025년 말": [5284, 8324],
    "2026년 6월": [6938, 8827]
}).set_index("항목")

# =========================================================
# LEFT NAVIGATION
# =========================================================
with st.sidebar:
    st.markdown('<div class="nav-caption">LG H&H FINANCE ANALYSIS</div>', unsafe_allow_html=True)
    st.markdown('<div class="nav-brand">2025 손익구조 분석</div>', unsafe_allow_html=True)

    page = st.radio(
        "분석 메뉴",
        [
            "종합분석",
            "손익구조",
            "Beauty 분석",
            "매출총이익률",
            "손상·해외사업",
            "현금흐름",
            "2026 H1 · 이후 어떻게 되었나?",
            "종합진단"
        ],
        label_visibility="collapsed"
    )

# =========================================================
# 1. SUMMARY
# =========================================================
if page == "종합분석":
    st.header("종합분석")
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

    with st.expander("왜 이런 분석을 하나요?", expanded=True):
        st.markdown(
            """
            LG생활건강은 2025년 연결 기준 **영업이익 1,707억원을 기록했음에도
            당기순손실 858억원으로 전환**했습니다.

            따라서 단순히 '실적이 나빠졌다'고 보는 것보다,
            **① 본업의 수익성이 어디에서 약화됐는지,
            ② 영업이익이 왜 순손실까지 내려갔는지,
            ③ 회계상 손실이 실제 현금창출력 약화와 같은 의미인지**
            순서대로 구분해 볼 필요가 있다고 판단했습니다.

            이 분석은 공개 재무제표에서 직접 확인할 수 있는 수치를 중심으로
            2025년 손익 악화의 구조를 설명하는 것을 목적으로 합니다.
            """
        )

    with st.expander("어떤 흐름으로 분석하나요?", expanded=False):
        st.markdown("#### ① 손익구조")
        st.write("매출 → 매출총이익 → 영업이익 → 세전손익 → 당기순손익을 따라가며 어느 단계에서 수익성이 크게 훼손됐는지 확인합니다.")

        st.markdown("#### ② Beauty 분석")
        st.write("Beauty·HDB·Refreshment를 비교하여 전사 영업이익 감소를 주도한 사업부를 식별합니다.")

        st.markdown("#### ③ 매출총이익률")
        st.write("매출 감소와 함께 매출총이익률이 어떻게 변했는지 확인하고, 판관비 증가가 주된 원인이었는지도 검토합니다.")

        st.markdown("#### ④ 손상·해외사업")
        st.write("영업이익이 남아 있었는데도 순손실로 전환된 이유를 기타영업외손익과 무형자산 손상차손을 통해 확인합니다.")

        st.markdown("#### ⑤ 현금흐름")
        st.write("당기순손실과 영업활동현금흐름을 비교하여 회계상 손실과 현금창출력을 구분해서 해석합니다.")

    with st.expander("어떤 결론이 도출되나요?", expanded=False):
        st.markdown(
            """
            <div class="insight">
                <b>1. 본업 수익성 악화의 중심은 Beauty입니다.</b><br>
                Beauty가 2024년 영업이익 1,582억원에서
                2025년 영업손실 976억원으로 적자 전환한 영향이 가장 컸습니다.
            </div>

            <div class="insight">
                <b>2. 단순한 판관비 증가 문제는 아닙니다.</b><br>
                2025년 판관비는 전년보다 감소했지만 매출총이익률은 약
                52.3%에서 49.5%로 하락했습니다.
                따라서 매출 감소와 총이익 창출력 약화를 함께 볼 필요가 있습니다.
            </div>

            <div class="insight">
                <b>3. 순손실 전환에는 손상차손의 영향도 컸습니다.</b><br>
                기타영업외비용 가운데 무형자산손상차손이 약 1,798억원으로
                가장 큰 비중을 차지했습니다.
            </div>

            <div class="insight">
                <b>4. 다만 현금창출력이 완전히 사라진 것은 아닙니다.</b><br>
                2025년 당기순손실은 858억원이었지만
                영업활동현금흐름은 +4,464억원을 유지했습니다.
                다만 영업현금흐름 자체는 2년 연속 감소하고 있어 회복 여부를 계속 확인해야 합니다.
            </div>
            """,
            unsafe_allow_html=True
        )

# =========================================================
# 2. INCOME STRUCTURE
# =========================================================
elif page == "손익구조":
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
elif page == "Beauty 분석":
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
elif page == "매출총이익률":
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
elif page == "손상·해외사업":
    st.header("손상·해외사업: 영업이익이 남았는데 왜 순손실인가?")

    st.subheader("2025 손익 Bridge")
    bridge_plot = bridge.reset_index()

    fig_bridge = px.bar(
        bridge_plot,
        x="항목",
        y="2025",
        text="2025",
        labels={"2025": "금액(억원)", "항목": ""},
    )
    fig_bridge.update_traces(
        texttemplate="%{text:,.0f}",
        textposition="outside",
        cliponaxis=False
    )
    fig_bridge.update_xaxes(
        tickangle=0,
        automargin=True
    )
    fig_bridge.update_yaxes(
        zeroline=True,
        zerolinewidth=1,
        title="억원"
    )
    fig_bridge.update_layout(
        showlegend=False,
        height=430,
        margin=dict(l=20, r=20, t=20, b=70)
    )
    st.plotly_chart(fig_bridge, use_container_width=True, config={"displayModeBar": True})

    # 세부내역이 공시된 항목만 클릭해서 확인
    with st.expander("기타영업외손익 세부내역 보기", expanded=False):
        st.markdown(
            """
            2025년 기타영업외손익은 **기타영업외수익 약 457억원 - 기타영업외비용 약 2,799억원
            = 순비용 약 2,342억원**으로 구성됩니다.

            아래는 연결재무제표 주석에서 확인되는 **기타영업외비용 세부내역**입니다.
            """
        )

        other_nonop_detail = pd.DataFrame({
            "세부 항목": [
                "무형자산손상차손",
                "기부금",
                "유형자산손상차손",
                "기타",
                "외환차손",
                "무형자산처분손실",
                "유형자산처분손실",
                "사용권자산손상차손",
                "기타의대손상각비",
                "외화환산손실"
            ],
            "2025 금액(억원)": [
                1798.31,
                520.43,
                125.58,
                114.93,
                121.13,
                19.39,
                46.76,
                32.96,
                11.67,
                7.38
            ]
        })

        st.dataframe(
            other_nonop_detail.style.format({"2025 금액(억원)": "{:,.1f}"}),
            use_container_width=True,
            hide_index=True
        )

        fig_detail = px.bar(
            other_nonop_detail.sort_values("2025 금액(억원)", ascending=True),
            x="2025 금액(억원)",
            y="세부 항목",
            orientation="h",
            text="2025 금액(억원)"
        )
        fig_detail.update_traces(
            texttemplate="%{text:,.0f}",
            textposition="outside",
            cliponaxis=False
        )
        fig_detail.update_layout(
            showlegend=False,
            height=430,
            margin=dict(l=20, r=40, t=10, b=20)
        )
        st.plotly_chart(fig_detail, use_container_width=True)

        st.markdown(
            """
            <div class="insight">
                <b>무엇이 가장 컸나?</b><br>
                기타영업외비용 약 2,799억원 가운데
                <b>무형자산손상차손이 약 1,798억원</b>으로 가장 큰 항목입니다.
                즉 2025년 순손실 전환을 해석할 때 영업수익성 악화뿐 아니라
                해외사업 등을 포함한 무형자산 가치의 재평가 영향을 함께 볼 필요가 있습니다.
            </div>
            """,
            unsafe_allow_html=True
        )

    st.subheader("주요 해외 CGU 영업권 손상")
    st.caption("단위: 억원 / 반올림")

    impairment_plot = impairment.reset_index()
    fig_impairment = px.bar(
        impairment_plot,
        x="해외 CGU",
        y="2025 영업권 손상",
        text="2025 영업권 손상",
        labels={"2025 영업권 손상": "영업권 손상(억원)", "해외 CGU": ""}
    )
    fig_impairment.update_traces(
        texttemplate="%{text:,.0f}",
        textposition="outside",
        cliponaxis=False
    )
    fig_impairment.update_xaxes(tickangle=0, automargin=True)
    fig_impairment.update_layout(
        showlegend=False,
        height=400,
        margin=dict(l=20, r=20, t=20, b=60)
    )
    st.plotly_chart(fig_impairment, use_container_width=True)

    c1, c2, c3 = st.columns(3)
    c1.metric("2025 영업이익", "1,707억원")
    c2.metric("기타영업외비용", "2,799억원")
    c3.metric("무형자산손상차손", "1,798억원")

    st.markdown(
        """
        <div class="insight">
            <b>핵심 해석</b><br>
            2025년에는 영업이익이 플러스였지만 기타영업외비용이 크게 발생했고,
            그 안에서 <b>무형자산손상차손</b>의 영향이 컸습니다.
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
            손상차손은 당기의 현금유출 자체를 의미하지 않습니다.
            다만 과거 인수·투자 당시 기대했던 미래 현금창출력에 대한 재평가라는 점에서,
            해외사업이 투자 당시 기대한 경제적 성과를 내고 있는지 점검해야 한다는 신호로 볼 수 있습니다.
        </div>
        """,
        unsafe_allow_html=True
    )

# =========================================================
# 6. CASH FLOW
# =========================================================
elif page == "현금흐름":
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
# 7. 2026 H1 FOLLOW-UP
# =========================================================
elif page == "2026 H1 · 이후 어떻게 되었나?":
    st.header("2026 H1 · 이후 어떻게 되었나?")
    st.markdown(
        """
        <div class="question-box">
            <div class="question-label">FOLLOW-UP QUESTION</div>
            <div class="question-text">
                2025년 수익성 악화 이후, 2026년 상반기에는 실제 회복 신호가 나타났는가?
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.info(
        "반기 실적은 연간 실적과 직접 비교하지 않고 2025 H1 ↔ 2026 H1 기준으로 비교합니다. "
        "또한 2026년 사업부 재편성에 따라 회사가 2025년 비교기간의 부문정보를 재작성한 수치를 사용합니다."
    )

    st.subheader("1. 매출은 감소했지만 이익은 개선됐습니다")
    c1, c2, c3, c4 = st.columns(4)
    sales_change = (32340 / 33027 - 1) * 100
    gp_change = (16750 / 16839 - 1) * 100
    op_change = (2106 / 1972 - 1) * 100
    ni_change = (1664 / 1420 - 1) * 100
    c1.metric("매출", "3조 2,340억원", f"{sales_change:.1f}% YoY")
    c2.metric("매출총이익", "1조 6,750억원", f"{gp_change:.1f}% YoY")
    c3.metric("영업이익", "2,106억원", f"+{op_change:.1f}% YoY")
    c4.metric("반기순이익", "1,664억원", f"+{ni_change:.1f}% YoY")

    fig_h1 = px.bar(
        h1_compare.reset_index().melt(id_vars="항목", value_vars=["2025 H1", "2026 H1"], var_name="기간", value_name="금액"),
        x="항목", y="금액", color="기간", barmode="group", text_auto=".0f",
        labels={"금액": "억원", "항목": ""}
    )
    fig_h1.update_xaxes(tickangle=0)
    fig_h1.update_layout(height=420, margin=dict(l=20, r=20, t=20, b=50))
    st.plotly_chart(fig_h1, use_container_width=True)

    st.markdown(
        """<div class="insight"><b>해석</b><br>
        2026년 상반기 매출은 전년 동기보다 약 2.1% 감소했지만, 영업이익은 약 6.8%, 반기순이익은 약 17.1% 증가했습니다.
        즉 외형 성장은 아직 회복되지 않았지만 <b>수익성 측면에서는 개선 신호가 나타났습니다.</b>
        </div>""", unsafe_allow_html=True
    )

    st.subheader("2. 2025년 핵심 문제였던 Beauty는 수익성이 회복됐습니다")
    beauty25_sales = h1_segments.loc["Beauty", "2025 H1 매출"]
    beauty26_sales = h1_segments.loc["Beauty", "2026 H1 매출"]
    beauty25_op = h1_segments.loc["Beauty", "2025 H1 영업이익"]
    beauty26_op = h1_segments.loc["Beauty", "2026 H1 영업이익"]
    beauty25_margin = h1_segments.loc["Beauty", "2025 H1 영업이익률"]
    beauty26_margin = h1_segments.loc["Beauty", "2026 H1 영업이익률"]
    c1, c2, c3 = st.columns(3)
    c1.metric("Beauty 매출", f"{beauty26_sales:,.0f}억원", f"{(beauty26_sales/beauty25_sales-1)*100:.1f}% YoY")
    c2.metric("Beauty 영업이익", f"{beauty26_op:,.0f}억원", f"+{(beauty26_op/beauty25_op-1)*100:.1f}% YoY")
    c3.metric("Beauty 영업이익률", f"{beauty26_margin:.1f}%", f"+{beauty26_margin-beauty25_margin:.1f}%p")

    seg_plot = h1_segments[["2025 H1 영업이익", "2026 H1 영업이익"]].reset_index().melt(id_vars="사업", var_name="기간", value_name="영업이익")
    fig_seg = px.bar(seg_plot, x="사업", y="영업이익", color="기간", barmode="group", text_auto=".0f", labels={"영업이익":"억원", "사업":""})
    fig_seg.update_xaxes(tickangle=0)
    fig_seg.update_layout(height=400, margin=dict(l=20, r=20, t=20, b=40))
    st.plotly_chart(fig_seg, use_container_width=True)

    st.markdown(
        """<div class="insight"><b>Beauty의 변화</b><br>
        Beauty 매출은 감소했지만 영업이익은 621억원에서 830억원으로 증가했고, 영업이익률도 약 3.7%에서 5.2%로 개선됐습니다.
        따라서 2025년에 확인됐던 Beauty 수익성 악화에는 <b>2026년 상반기 기준으로 뚜렷한 회복 신호</b>가 나타났다고 볼 수 있습니다.
        다만 매출 자체는 아직 감소하고 있어 '완전한 회복'으로 단정하기는 어렵습니다.
        </div>""", unsafe_allow_html=True
    )

    st.subheader("3. 매출총이익률도 개선됐습니다")
    gm_25h1 = 16839 / 33027 * 100
    gm_26h1 = 16750 / 32340 * 100
    c1, c2, c3 = st.columns(3)
    c1.metric("2025 H1 매출총이익률", f"{gm_25h1:.1f}%")
    c2.metric("2026 H1 매출총이익률", f"{gm_26h1:.1f}%", f"+{gm_26h1-gm_25h1:.1f}%p")
    c3.metric("판관비", "1조 4,644억원", "-223억원 YoY")
    st.markdown(
        """<div class="insight"><b>비용을 무조건 줄여 만든 이익은 아닙니다.</b><br>
        2026년 상반기 광고선전비는 전년 동기보다 증가한 반면 지급수수료는 감소했습니다.
        따라서 마케팅 투자를 유지하면서 다른 비용구조의 효율화를 통해 수익성을 개선했을 가능성을 확인할 수 있습니다.
        다만 지급수수료 감소의 구체적 원인은 공개자료만으로 확정하지 않습니다.
        </div>""", unsafe_allow_html=True
    )

    st.subheader("4. 2025년 순손실을 키웠던 대규모 손상차손은 상반기에 나타나지 않았습니다")
    c1, c2, c3 = st.columns(3)
    c1.metric("2026 H1 영업이익", "2,106억원")
    c2.metric("2026 H1 기타영업외비용", "293억원")
    c3.metric("2026 H1 무형자산손상차손", "0억원")
    st.markdown(
        """<div class="insight"><b>의미</b><br>
        2025년 순손실 전환에는 대규모 무형자산손상차손의 영향이 컸지만, 2026년 상반기에는 해당 손상차손이 발생하지 않았습니다.
        그 결과 영업이익이 세전이익과 반기순이익으로 비교적 자연스럽게 이어졌습니다.
        이는 2025년 순손실이 영업 자체의 구조적 손실만으로 발생한 것은 아니었다는 점을 다시 보여줍니다.
        </div>""", unsafe_allow_html=True
    )

    st.subheader("5. 다만 운전자본은 계속 확인할 필요가 있습니다")
    fig_wc = px.bar(
        h1_working_capital.reset_index().melt(id_vars="항목", value_vars=["2025년 말", "2026년 6월"], var_name="시점", value_name="금액"),
        x="항목", y="금액", color="시점", barmode="group", text_auto=".0f", labels={"금액":"억원", "항목":""}
    )
    fig_wc.update_xaxes(tickangle=0)
    fig_wc.update_layout(height=390, margin=dict(l=20, r=20, t=20, b=40))
    st.plotly_chart(fig_wc, use_container_width=True)
    st.markdown(
        """<div class="insight"><b>남아 있는 과제</b><br>
        2025년 말 대비 2026년 6월 매출채권 및 기타채권과 재고자산이 모두 증가했습니다.
        재고평가손실충당금은 오히려 감소했기 때문에 재고의 질이 악화됐다고 단정할 수는 없지만,
        <b>수익성 개선이 운전자본 효율과 안정적인 현금창출력으로 이어지는지</b>는 계속 확인할 필요가 있습니다.
        </div>""", unsafe_allow_html=True
    )

    st.markdown(
        """<div class="final-box"><b>2026 H1 결론</b><br><br>
        2026년 상반기 LG생활건강은 매출이 소폭 감소했음에도 Beauty의 영업이익과 전사 매출총이익률이 개선되고,
        대규모 무형자산손상차손이 발생하지 않으면서 영업이익과 순이익이 모두 증가했습니다.<br><br>
        따라서 <b>수익성 측면에서는 2025년의 충격에서 회복되는 신호가 나타났다</b>고 볼 수 있습니다.
        다만 Beauty 매출의 외형 회복은 아직 확인되지 않았고 매출채권·재고도 증가했으므로,
        향후에는 <b>Beauty 매출 성장 → 수익성 유지 → 운전자본 효율 → 영업현금흐름 개선</b>이 순차적으로 이어지는지를 확인하는 것이 중요합니다.
        </div>""", unsafe_allow_html=True
    )


# =========================================================
# 8. FINAL
# =========================================================
elif page == "종합진단":
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
            2025년 LG생활건강의 실적 악화는 Beauty 사업의 수익성 약화와
            대규모 무형자산 손상차손이 함께 작용한 결과였습니다.
            <br><br>
            2026년 상반기에는 Beauty 매출이 아직 감소했음에도 영업이익과 영업이익률이 개선되고,
            전사 매출총이익률과 순이익도 회복됐으며 대규모 무형자산손상차손도 발생하지 않았습니다.
            따라서 <b>수익성 측면에서는 회복 신호가 확인된다</b>고 판단할 수 있습니다.
            <br><br>
            다만 Beauty의 외형 성장과 운전자본 효율은 아직 추가 확인이 필요합니다.
            향후에는 <b>① Beauty 매출 성장 여부, ② 수익성 유지,
            ③ 매출채권·재고 관리, ④ 영업현금흐름 개선</b>이 함께 이어지는지를 확인하는 것이 중요합니다.
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
