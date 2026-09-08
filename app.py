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

# 연도별 손익 Bridge 및 해외 CGU 영업권 손상 비교
bridge_by_year = {
    "2023": pd.DataFrame({
        "항목": ["영업이익", "금융손익", "기타영업외손익", "지분법손익", "세전손익", "법인세", "당기순손익"],
        "금액": [4870, 99, -2282, 77, 2764, -1129, 1635]
    }),
    "2024": pd.DataFrame({
        "항목": ["영업이익", "금융손익", "기타영업외손익", "지분법손익", "세전손익", "법인세", "당기순손익"],
        "금액": [4590, 409, -1891, 58, 3166, -1127, 2039]
    }),
    "2025": bridge.reset_index().rename(columns={"2025": "금액"})
}

overseas_goodwill_impairment = {
    "2023": pd.DataFrame({
        "해외 CGU": ["The Avon Company Canada", "Boinca"],
        "영업권 손상": [141, 565]
    }),
    # 2024년 해외 CGU에서 신규 영업권 손상은 확인되지 않음.
    # The Avon Company의 997억원 손상은 무형자산·사용권자산·유형자산 손상으로 영업권 손상이 아님.
    "2024": pd.DataFrame(columns=["해외 CGU", "영업권 손상"]),
    "2025": impairment.reset_index().rename(columns={"2025 영업권 손상": "영업권 손상"})
}


# 기타영업외손익 세부내역: 연결 기준 / 단위 억원
other_nonop_income = {
    "2023": 465.82,
    "2024": 263.95,
    "2025": 456.97,
}

other_nonop_expense = {
    "2023": pd.DataFrame({
        "세부 항목": [
            "무형자산손상차손", "기부금", "기타", "사용권자산손상차손",
            "외환차손", "유형자산처분손실", "유형자산손상차손",
            "무형자산처분손실", "외화환산손실", "투자부동산손상차손",
            "투자부동산처분손실"
        ],
        "금액(억원)": [1122.05, 849.02, 255.10, 160.70, 112.06, 94.06, 65.55, 63.90, 16.76, 8.97, 0.11]
    }),
    "2024": pd.DataFrame({
        "세부 항목": [
            "무형자산손상차손", "기부금", "사용권자산손상차손", "외화환산손실",
            "외환차손", "기타", "유형자산손상차손", "유형자산처분손실",
            "무형자산처분손실", "투자부동산손상차손", "투자부동산처분손실"
        ],
        "금액(억원)": [934.40, 451.94, 220.67, 187.94, 126.90, 77.72, 71.84, 63.97, 13.17, 6.29, 0.00]
    }),
    "2025": pd.DataFrame({
        "세부 항목": [
            "무형자산손상차손", "기부금", "유형자산손상차손", "기타", "외환차손",
            "무형자산처분손실", "유형자산처분손실", "사용권자산손상차손",
            "기타의대손상각비", "외화환산손실"
        ],
        "금액(억원)": [1798.31, 520.43, 125.58, 114.93, 121.13, 19.39, 46.76, 32.96, 11.67, 7.38]
    }),
}


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

# 2025 H2는 FY2025 - H1 2025로 산출한 보조 분석값
half_trend = pd.DataFrame({
    "기간": ["2025 H1", "2025 H2 (산출)", "2026 H1"],
    "매출": [33027, 63555 - 33027, 32340],
    "매출총이익": [16839, 31446 - 16839, 16750],
    "영업이익": [1972, 1707 - 1972, 2106]
})
half_trend["매출총이익률"] = half_trend["매출총이익"] / half_trend["매출"] * 100

profit_quality = pd.DataFrame({
    "연도": [2023, 2024, 2025],
    "영업이익": [4870, 4590, 1707],
    "당기순손익": [1635, 2039, -858],
    "영업활동현금흐름": [6591, 5276, 4464]
})

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
            LG생활건강은 2025년 연결 기준 영업이익 1,707억원을 기록했음에도
            당기순손실 858억원으로 전환했습니다.

            따라서 단순히 '실적이 나빠졌다'고 보는 것보다,
            ① 본업의 수익성이 어디에서 약화됐는지,
            ② 영업이익이 왜 순손실까지 내려갔는지,
            ③ 회계상 손실이 실제 현금창출력 약화와 같은 의미인지
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
    income_plot = income.T.reset_index().rename(columns={"index": "연도"}).melt(
        id_vars="연도", var_name="항목", value_name="금액"
    )
    fig_income = px.line(income_plot, x="연도", y="금액", color="항목", markers=True, labels={"금액": "억원"})
    fig_income.update_xaxes(type="category", tickangle=0, title="")
    fig_income.update_layout(height=430, margin=dict(l=20, r=20, t=20, b=40))
    st.plotly_chart(fig_income, use_container_width=True)

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
    sales_plot = sales_pivot.reset_index().melt(id_vars="연도", var_name="사업", value_name="매출")
    fig_sales = px.line(sales_plot, x="연도", y="매출", color="사업", markers=True, labels={"매출": "억원"})
    fig_sales.update_xaxes(type="category", tickangle=0, title="")
    fig_sales.update_layout(height=410, margin=dict(l=20, r=20, t=20, b=40))
    st.plotly_chart(fig_sales, use_container_width=True)

    st.subheader("사업부별 영업이익")
    op_plot = op_pivot.reset_index().melt(id_vars="연도", var_name="사업", value_name="영업이익")
    fig_op = px.bar(op_plot, x="연도", y="영업이익", color="사업", barmode="group", text_auto=".0f", labels={"영업이익": "억원"})
    fig_op.update_xaxes(type="category", tickangle=0, title="")
    fig_op.update_layout(height=410, margin=dict(l=20, r=20, t=20, b=40))
    st.plotly_chart(fig_op, use_container_width=True)

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
    gm_plot = gross_margin.reset_index().melt(id_vars="연도", var_name="지표", value_name="비율")
    fig_gm = px.line(gm_plot, x="연도", y="비율", color="지표", markers=True, labels={"비율": "%"})
    fig_gm.update_xaxes(type="category", tickangle=0, title="")
    fig_gm.update_layout(height=410, margin=dict(l=20, r=20, t=20, b=40))
    st.plotly_chart(fig_gm, use_container_width=True)

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

    st.subheader("연도별 비교분석")
    st.caption("2023~2025년 손익 Bridge와 주요 해외 CGU 영업권 손상을 같은 기준으로 비교합니다.")

    selected_year = st.radio(
        "비교 연도",
        ["2025", "2024", "2023"],
        horizontal=True,
        format_func=lambda x: f"{x}년 비교분석"
    )

    st.subheader(f"{selected_year} 손익 Bridge")
    year_bridge = bridge_by_year[selected_year].copy()
    fig_bridge = px.bar(
        year_bridge, x="항목", y="금액", text="금액",
        labels={"금액": "금액(억원)", "항목": ""}
    )
    fig_bridge.update_traces(texttemplate="%{text:,.0f}", textposition="outside", cliponaxis=False)
    fig_bridge.update_xaxes(tickangle=0, automargin=True)
    fig_bridge.update_yaxes(zeroline=True, zerolinewidth=1, title="억원")
    fig_bridge.update_layout(showlegend=False, height=430, margin=dict(l=20, r=20, t=20, b=70))
    st.plotly_chart(fig_bridge, use_container_width=True, config={"displayModeBar": True})

    with st.expander("기타영업외손익 세부내역 보기", expanded=False):
        detail_df = other_nonop_expense[selected_year].copy()
        expense_total = detail_df["금액(억원)"].sum()
        income_total = other_nonop_income[selected_year]
        net_nonop = income_total - expense_total

        st.markdown(
            f"""
            {selected_year}년 기타영업외손익은 기타영업외수익 약 {income_total:,.0f}억원에서
            기타영업외비용 약 {expense_total:,.0f}억원을 차감한
            순손익 약 {net_nonop:,.0f}억원입니다.
            아래 표는 연결재무제표 주석에서 확인되는 주요 기타영업외비용 항목입니다.
            """
        )

        st.dataframe(
            detail_df.style.format({"금액(억원)": "{:,.1f}"}),
            use_container_width=True,
            hide_index=True
        )

        fig_detail = px.bar(
            detail_df.sort_values("금액(억원)", ascending=True),
            x="금액(억원)",
            y="세부 항목",
            orientation="h",
            text="금액(억원)"
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

        if selected_year == "2023":
            st.markdown(
                """<div class="insight">
                2023년 기타영업외비용에서는 무형자산손상차손과 기부금의 비중이 컸습니다.
                따라서 영업이익에서 세전이익으로 내려가는 과정에서 비영업 항목의 영향이 상당했음을 확인할 수 있습니다.
                </div>""",
                unsafe_allow_html=True
            )
        elif selected_year == "2024":
            st.markdown(
                """<div class="insight">
                2024년에도 무형자산손상차손이 기타영업외비용의 가장 큰 항목이었습니다.
                다만 2025년과 달리 주요 해외 CGU의 신규 영업권 손상보다는
                The Avon Company의 무형자산·사용권자산·유형자산 손상이 중심이었습니다.
                </div>""",
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                """<div class="insight">
                2025년 기타영업외비용 가운데 무형자산손상차손이 약 1,798억원으로 가장 큰 항목입니다.
                따라서 2025년 순손실 전환은 본업 수익성 악화와 투자자산 가치 재평가를 함께 봐야 합니다.
                </div>""",
                unsafe_allow_html=True
            )

    st.subheader(f"{selected_year} 주요 해외 CGU 영업권 손상")
    st.caption("단위: 억원 / 반올림")
    year_imp = overseas_goodwill_impairment[selected_year].copy()

    if year_imp.empty:
        st.info(
            "2024년에는 주요 해외 CGU에서 신규 영업권 손상이 확인되지 않았습니다. "
            "다만 The Avon Company에서는 무형자산·사용권자산·유형자산에 총 약 997억원의 손상이 인식됐으며, "
            "이는 영업권 손상과 구분해 해석해야 합니다."
        )
    else:
        fig_impairment = px.bar(
            year_imp, x="해외 CGU", y="영업권 손상", text="영업권 손상",
            labels={"영업권 손상": "영업권 손상(억원)", "해외 CGU": ""}
        )
        fig_impairment.update_traces(texttemplate="%{text:,.0f}", textposition="outside", cliponaxis=False)
        fig_impairment.update_xaxes(tickangle=0, automargin=True)
        fig_impairment.update_layout(showlegend=False, height=400, margin=dict(l=20, r=20, t=20, b=60))
        st.plotly_chart(fig_impairment, use_container_width=True)

    if selected_year == "2023":
        st.markdown(
            """<div class="insight"><b>2023년 해석</b><br>
            The Avon Company Canada와 Boinca에서 영업권 손상이 발생했습니다.
            The Avon Company도 추가 손상차손을 인식했지만, 영업권은 이전 기간에 이미 전액 손상돼
            2023년 추가 손상은 영업권 손상으로 분류하지 않았습니다.
            </div>""", unsafe_allow_html=True
        )
    elif selected_year == "2024":
        st.markdown(
            """<div class="insight"><b>2024년 해석</b><br>
            해외 CGU의 신규 영업권 손상은 확인되지 않았지만 The Avon Company의 다른 자산 손상은 계속됐습니다.
            즉 해외사업 리스크가 사라졌다기보다 손상의 대상 자산이 달랐다고 보는 것이 적절합니다.
            </div>""", unsafe_allow_html=True
        )
    else:
        c1, c2, c3 = st.columns(3)
        c1.metric("2025 영업이익", "1,707억원")
        c2.metric("기타영업외비용", "2,799억원")
        c3.metric("무형자산손상차손", "1,798억원")
        st.markdown(
            """<div class="insight"><b>핵심 해석</b><br>
            2025년에는 영업이익이 플러스였지만 기타영업외비용이 크게 발생했고, 그 안에서 무형자산손상차손의 영향이 컸습니다.
            순손실 전환은 본업 수익성 약화와 과거 투자자산 가치 하락이 함께 반영된 결과로 볼 수 있습니다.
            </div>""", unsafe_allow_html=True
        )

    st.markdown(
        """<div class="insight"><b>Finance 관점</b><br>
        손상차손은 당기의 현금유출 자체를 의미하지 않습니다.
        다만 과거 인수·투자 당시 기대했던 미래 현금창출력을 재평가한 결과이므로,
        해외사업의 사업계획 대비 실제 매출·이익·현금흐름을 지속적으로 검증할 필요가 있습니다.
        </div>""", unsafe_allow_html=True
    )

# 6. CASH FLOW
# =========================================================
elif page == "현금흐름":
    st.header("이익의 질·현금흐름: 손익은 실제 현금창출력과 같은가?")

    st.info(
        "영업활동현금흐름은 연결 기준으로 공시되며 Beauty·HDB·Refreshment별 현금흐름은 별도로 공시되지 않습니다. "
        "따라서 공개자료만으로 사업부별 영업활동현금흐름을 임의 배분하지 않고 전사 기준으로 분석합니다."
    )

    st.markdown(
        """<div class="question-box">
            <div class="question-label">QUALITY OF EARNINGS</div>
            <div class="question-text">손익계산서상 이익 변화가 실제 영업현금창출력 변화와 어떻게 다른가?</div>
        </div>""", unsafe_allow_html=True
    )

    pq = profit_quality.melt(id_vars="연도", var_name="지표", value_name="금액")
    fig_pq = px.line(pq, x="연도", y="금액", color="지표", markers=True, labels={"금액": "억원"})
    fig_pq.update_xaxes(type="category", tickangle=0, title="")
    fig_pq.update_layout(height=430, margin=dict(l=20, r=20, t=20, b=40))
    st.plotly_chart(fig_pq, use_container_width=True)

    c1, c2, c3 = st.columns(3)
    c1.metric("2025 영업이익", "1,707억원", "-2,883억원 YoY")
    c2.metric("2025 당기순손익", "-858억원", "적자전환")
    c3.metric("2025 영업활동현금흐름", "4,464억원", "-812억원 YoY")

    st.subheader("2025년: 영업이익 → 순손실 → 영업현금흐름")
    quality_2025 = pd.DataFrame({
        "구분": ["영업이익", "세전손익", "당기순손익", "영업활동현금흐름"],
        "금액": [1707, -633, -858, 4464]
    })
    fig_q25 = px.bar(quality_2025, x="구분", y="금액", text="금액", labels={"금액": "억원", "구분": ""})
    fig_q25.update_traces(texttemplate="%{text:,.0f}", textposition="outside", cliponaxis=False)
    fig_q25.update_xaxes(tickangle=0)
    fig_q25.update_yaxes(zeroline=True, zerolinewidth=1)
    fig_q25.update_layout(showlegend=False, height=400, margin=dict(l=20, r=20, t=20, b=50))
    st.plotly_chart(fig_q25, use_container_width=True)

    st.markdown(
        """<div class="insight"><b>핵심 해석</b><br>
        2025년에는 영업이익 1,707억원을 냈지만 세전손실 633억원, 당기순손실 858억원으로 내려갔습니다.
        반면 영업활동현금흐름은 +4,464억원을 유지했습니다.
        이는 순손실이 본업의 현금유출과 동일한 의미가 아니라는 점을 보여줍니다.
        특히 무형자산손상차손 1,798억원은 이 차이를 설명하는 주요 비현금성 항목 중 하나입니다.
        다만 순이익과 영업현금흐름의 차이는 손상차손 하나만이 아니라 감가상각·상각, 운전자본 변동, 세금 등 여러 항목의 영향을 함께 받습니다.
        </div>""", unsafe_allow_html=True
    )

    st.warning(
        "영업활동현금흐름은 2023년 6,591억원 → 2024년 5,276억원 → 2025년 4,464억원으로 2년 연속 감소했습니다. "
        "따라서 '순손실이지만 현금은 문제없다'가 아니라, 회계상 손실보다 현금창출력은 양호했지만 본업의 현금창출 규모도 약화되고 있다는 해석이 적절합니다."
    )

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
        "회복 여부의 핵심 판단은 계절성을 통제하기 위해 2025 H1 ↔ 2026 H1 전년 동기 기준으로 비교합니다. "
        "다만 변화의 흐름을 놓치지 않기 위해 FY2025에서 H1 실적을 차감한 2025 H2 산출치도 보조적으로 확인합니다. "
        "2025 H2는 별도 공시된 반기 실적이 아니며 연말 결산 과정의 평가·추정 변경 등이 포함될 수 있어, 본 분석에서는 매출·매출총이익·영업이익 등 영업 추세 확인에만 사용합니다."
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
        즉 외형 성장은 아직 회복되지 않았지만 수익성 측면에서는 개선 신호가 나타났습니다.
        </div>""", unsafe_allow_html=True
    )

    st.subheader("1-1. 2025 H2를 포함하면 회복의 흐름이 더 선명해집니다")
    trend_long = half_trend.melt(
        id_vars=["기간", "매출총이익률"],
        value_vars=["매출", "매출총이익", "영업이익"],
        var_name="지표", value_name="금액"
    )
    fig_trend = px.line(trend_long, x="기간", y="금액", color="지표", markers=True, labels={"금액": "억원"})
    fig_trend.update_xaxes(type="category", tickangle=0, title="")
    fig_trend.update_layout(height=420, margin=dict(l=20, r=20, t=20, b=40))
    st.plotly_chart(fig_trend, use_container_width=True)

    st.info(
        "2025 H1 → 2025 H2 → 2026 H1 흐름을 보면 매출과 매출총이익은 2025 H2에 한 차례 더 둔화된 뒤 "
        "2026 H1에 일부 회복되는 모습이 나타납니다. 영업이익 역시 2025 H2에서 크게 약화된 후 "
        "2026 H1에 반등해, 수익성 회복이 2026년 상반기에 본격적으로 나타났음을 확인할 수 있습니다. "
        "다만 2025 H2는 FY2025에서 H1 실적을 차감한 산출치이므로 연말 결산 과정의 평가·추정 변경 등이 "
        "포함될 수 있어 방향성 확인용으로 해석합니다."
    )

    c1, c2, c3 = st.columns(3)
    h2 = half_trend.set_index("기간").loc["2025 H2 (산출)"]
    c1.metric("2025 H2 산출 매출", f"{h2['매출']:,.0f}억원")
    c2.metric("2025 H2 산출 영업이익", f"{h2['영업이익']:,.0f}억원")
    c3.metric("2025 H2 산출 매출총이익률", f"{h2['매출총이익률']:.1f}%")

    st.caption(
        "2025 H2 = FY2025 - H1 2025 산출값입니다. 별도 공시 반기 실적이 아니므로 순이익·세전손익 비교에는 사용하지 않고, 영업 추세를 보조적으로 확인하는 용도로만 활용합니다."
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

    st.subheader("4. 손상차손은 상반기만으로 회복 여부를 판단할 수 없습니다")
    impairment_timing = pd.DataFrame({
        "시점": ["2025 Q1", "2025 H1", "2025 Q3", "2025 FY", "2026 H1"],
        "무형자산손상차손": [0, 0, 0, 1798, 0]
    })
    fig_imp_timing = px.bar(
        impairment_timing, x="시점", y="무형자산손상차손", text="무형자산손상차손",
        labels={"무형자산손상차손": "억원", "시점": ""}
    )
    fig_imp_timing.update_traces(texttemplate="%{text:,.0f}", textposition="outside", cliponaxis=False)
    fig_imp_timing.update_xaxes(tickangle=0)
    fig_imp_timing.update_layout(showlegend=False, height=380, margin=dict(l=20, r=20, t=20, b=40))
    st.plotly_chart(fig_imp_timing, use_container_width=True)

    st.markdown(
        """<div class="insight"><b>해석</b><br>
        2025년에도 Q1·H1·Q3까지 무형자산손상차손이 없었고, 대규모 손상은 연말 결산에서 인식됐습니다.
        따라서 2026 H1의 손상차손 0원만으로 해외 투자자산 가치가 회복됐다고 판단할 수 없습니다.
        손상 여부는 2026년 연말 정기 손상검사와 향후 사업 전망을 추가 확인해야 합니다.
        2026 H1의 실제 회복 근거는 손상차손 부재가 아니라 Beauty 영업이익·영업이익률과 전사 매출총이익률 개선입니다.
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
        2026년 상반기 LG생활건강은 매출이 소폭 감소했음에도 Beauty의 영업이익과 전사 매출총이익률이 개선되며
        본업 수익성 측면에서 회복 신호가 나타났습니다.<br><br>
        다만 손상차손은 2025년에도 연말에 집중 인식됐으므로, 2026 H1의 손상차손 0원만으로 해외 투자자산 리스크가 해소됐다고 판단할 수는 없습니다.
        다만 Beauty 매출의 외형 회복은 아직 확인되지 않았고 매출채권·재고도 증가했으므로,
        향후에는 <b>Beauty 매출 성장 → 수익성 유지 → 운전자본 효율 → 영업현금흐름 개선</b>이 순차적으로 이어지는지를 확인하는 것이 중요합니다.
        </div>""", unsafe_allow_html=True
    )


# =========================================================
# 8. FINAL
# =========================================================
elif page == "종합진단":
    st.header("종합진단")

    st.markdown(
        """
        <div class="question-box">
            <div class="question-label">FINAL QUESTION</div>
            <div class="question-text">
                2025년의 수익성 악화와 2026년 상반기의 회복 신호를 바탕으로,
                LG생활건강은 앞으로 무엇을 관리해야 하는가?
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.subheader("분석을 통해 확인한 핵심 진단")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown(
            """
            <div class="card">
                <div class="card-label">01 · 본업</div>
                <div class="card-title">Beauty가 핵심</div>
                <div class="card-body">
                    2025년 전사 수익성 악화의 중심은 Beauty였습니다.
                    다만 2026년 상반기에는 Beauty 매출이 감소했음에도
                    영업이익과 영업이익률이 개선되며 수익성 회복 신호가 나타났습니다.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c2:
        st.markdown(
            """
            <div class="card">
                <div class="card-label">02 · 투자자산</div>
                <div class="card-title">해외사업 가치 재평가</div>
                <div class="card-body">
                    2025년 연말 손상검사에서 일부 해외 CGU의 회수가능액이
                    장부금액을 하회하면서 대규모 손상차손이 발생했습니다.
                    향후에는 투자 이후의 실제 현금창출력을 더 엄격하게 검증할 필요가 있습니다.
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
                <div class="card-title">이익 이후의 현금까지</div>
                <div class="card-body">
                    회계상 손실에도 영업현금흐름은 양(+)을 유지했지만,
                    2026년 상반기에는 매출채권과 재고가 증가했습니다.
                    수익성 개선이 실제 현금창출력으로 이어지는지 확인해야 합니다.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("---")
    st.subheader("LG생활건강이 앞으로 해야 할 네 가지")

    with st.expander(
        "첫째, Beauty는 단순한 매출 회복보다 '수익성 있는 성장'에 집중해야 합니다.",
        expanded=True
    ):
        st.markdown(
            """
            2025년에는 Beauty 사업이 전사 영업이익 감소를 주도했습니다.
            반면 2026년 상반기에는 Beauty 매출이 전년 동기보다 감소했음에도
            영업이익은 621억원 → 830억원, 영업이익률은 약 3.7% → 5.2%로 개선됐습니다.

            따라서 향후 핵심은 단순히 Beauty 매출 규모를 다시 키우는 것이 아니라,
            어떤 매출이 실제 이익을 만드는지를 구분하면서 성장하는 것입니다.

            재무 관점에서는 브랜드·제품·채널·지역별로 매출액뿐 아니라
            매출총이익률과 영업이익률을 함께 관리할 필요가 있습니다.
            예를 들어 매출은 증가하지만 할인·프로모션·유통수수료 부담으로 이익률이 낮아지는 채널이라면
            외형 확대가 반드시 기업가치 개선으로 이어지지는 않습니다.

            따라서 수익성이 높은 핵심 브랜드와 채널에는 마케팅·상품개발·유통 자원을 집중하고,
            매출 규모에 비해 이익 기여도가 낮은 영역은 가격정책, 프로모션 방식,
            유통구조 및 제품 Mix를 다시 점검하는 방향이 필요합니다.
            """
        )

        st.markdown(
            """
            <div class="insight">
                <b>재무 담당자가 확인할 지표</b><br>
                브랜드·제품·채널·지역별 매출 / 매출총이익률 / 영업이익률 /
                할인·프로모션율 / 판매수수료 / 마케팅비 대비 이익 개선효과
            </div>
            """,
            unsafe_allow_html=True
        )

    with st.expander(
        "둘째, 해외사업은 외형 확대보다 기존 투자자산의 수익성을 먼저 검증해야 합니다.",
        expanded=True
    ):
        st.markdown(
            """
            2025년 연말 손상검사에서는 Everlife, FMG&MISSION, The Creme Shop,
            LG H&H Singapore, 중국 상해법인 등 일부 현금창출단위의 회수가능액이
            장부금액보다 낮아지면서 손상차손이 인식됐습니다.

            이는 손상차손 자체가 현금유출이라는 의미는 아니지만,
            과거 인수·투자 당시 기대했던 미래 현금창출력을 현재 시점에서
            충분히 인정하기 어려워졌다는 회계적 신호입니다.

            따라서 해외사업의 성과를 단순 매출 성장률이나 시장 진출 여부로 평가하기보다
            사업계획 대비 실제 매출·영업이익·현금흐름이 얼마나 달성되고 있는지
            정기적으로 검증할 필요가 있습니다.

            특히 추가 투자나 지분 확대를 결정하기 전에는
            해당 법인의 실제 현금창출력, 투자금 회수기간, 자본비용을 함께 검토해야 합니다.
            계획 대비 성과가 지속적으로 미달하는 사업은 무조건 추가 투자를 이어가기보다
            투자규모 조정, 브랜드·채널 전략 변경, 구조조정 또는 자원 재배분까지 검토하는 것이 합리적입니다.

            또한 2025년에는 1~3분기까지 대규모 무형자산손상차손이 없었고
            연말 손상검사에서 손상이 집중적으로 인식됐습니다.
            따라서 2026년 상반기 손상차손이 0이라는 사실만으로
            해외 투자자산의 가치가 회복됐다고 판단해서는 안 됩니다.
            실제 판단은 2026년 연말 손상검사와 각 CGU의 사업실적을 함께 확인해야 합니다.
            """
        )

        st.markdown(
            """
            <div class="insight">
                <b>재무 담당자가 확인할 지표</b><br>
                해외법인·CGU별 사업계획 대비 매출·영업이익·현금흐름 /
                투자자본수익률 / 투자금 회수기간 / 손상검사 주요 가정 /
                할인율·영구성장률 변화 / 추가 투자 필요성
            </div>
            """,
            unsafe_allow_html=True
        )

    with st.expander(
        "셋째, 브랜드 포트폴리오는 성장성과 수익성을 기준으로 더 선별적으로 운영해야 합니다.",
        expanded=True
    ):
        st.markdown(
            """
            2025년 손상검사에서는 해외 CGU뿐 아니라
            국내 화장품사업부문에서 단종 브랜드와 관련된 손상차손도 인식됐습니다.
            이는 모든 브랜드를 동일한 방식으로 유지하기보다,
            각 브랜드가 실제로 만들어내는 경제적 성과를 기준으로
            포트폴리오를 재정비할 필요가 있음을 보여줍니다.

            신규 브랜드 육성 자체를 줄여야 한다는 의미는 아닙니다.
            중요한 것은 한정된 마케팅비·R&D비·유통자원을
            장기 성장성과 수익성이 높은 브랜드에 우선 배분하는 것입니다.

            이를 위해 브랜드별 매출 증가율뿐 아니라
            매출총이익, 마케팅비 투입 후 영업기여도, 재고회전,
            해외 확장 가능성 등을 함께 비교해야 합니다.
            성장성이 낮고 반복적으로 계획을 미달하는 브랜드는
            리포지셔닝·채널 축소·SKU 정리·단종 등을 검토하고,
            반대로 수익성과 성장성이 동시에 확인되는 브랜드에는
            글로벌 유통과 마케팅 투자를 집중하는 방식이 필요합니다.

            이런 방식은 단순한 비용절감이 아니라
            한정된 자원을 더 높은 수익을 만드는 브랜드로 이동시키는 자원배분의 문제입니다.
            """
        )

        st.markdown(
            """
            <div class="insight">
                <b>재무 담당자가 확인할 지표</b><br>
                브랜드별 매출 성장률 / 매출총이익 / 마케팅비 /
                마케팅비 대비 이익 기여도 / SKU별 재고회전 /
                사업계획 달성률 / 브랜드별 투자자본수익률
            </div>
            """,
            unsafe_allow_html=True
        )

    with st.expander(
        "넷째, 손익 개선이 실제 영업현금흐름 회복으로 이어지는지 관리해야 합니다.",
        expanded=True
    ):
        st.markdown(
            """
            2025년에는 당기순손실이 발생했지만 영업활동현금흐름은 여전히 양(+)을 유지했습니다.
            이는 손상차손처럼 현금유출을 직접 수반하지 않는 비용이 손익에 반영됐기 때문입니다.

            다만 영업활동현금흐름은 2023년 약 6,591억원 → 2024년 5,276억원
            → 2025년 4,464억원으로 감소했습니다.
            따라서 회계상 적자와 현금창출력을 구분하는 것과 별개로,
            본업에서 만들어내는 현금의 규모가 약해지고 있었는지는 계속 확인해야 합니다.

            또한 2026년 상반기에는 수익성이 개선됐지만
            2025년 말 대비 매출채권 및 기타채권과 재고자산이 증가했습니다.
            매출채권 회수가 느려지거나 판매보다 재고 증가가 빠르면
            손익계산서상 이익이 개선돼도 실제 현금은 운전자본에 묶일 수 있습니다.

            따라서 향후에는 Beauty 수익성 회복을 최종 성과로 보지 않고,
            그 이익이 매출채권 회수와 재고 판매를 거쳐
            실제 영업현금흐름으로 전환되는지까지 관리할 필요가 있습니다.
            """
        )

        st.markdown(
            """
            <div class="insight">
                <b>재무 담당자가 확인할 지표</b><br>
                영업활동현금흐름 / 매출채권 회전일수 /
                SKU별 재고일수·재고연령 / Sell-through /
                재고평가손실 / 운전자본 증감 / 이익의 현금전환율
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("---")
    st.subheader("종합적으로 보면")

    st.markdown(
        """
        <div class="final-box">
            2025년의 문제는 단순히 '매출이 줄었다'거나 '비용이 늘었다'는 한 가지 원인으로 설명되지 않습니다.
            Beauty의 수익성 약화와 일부 해외 투자자산의 가치 하락이 동시에 나타났고,
            그 결과 영업이익 감소와 대규모 손상차손이 함께 반영됐습니다.
            <br><br>
            2026년 상반기에는 Beauty 영업이익률과 전사 수익성이 개선되면서
            <b>본업 측면에서는 회복 신호가 나타났습니다.</b>
            그러나 Beauty 매출 자체의 외형 회복은 아직 확인되지 않았고,
            해외 투자자산의 가치는 연말 손상검사를 다시 확인해야 하며,
            매출채권·재고 증가가 현금흐름에 미칠 영향도 남아 있습니다.
            <br><br>
            따라서 앞으로의 핵심은
            <b>① 수익성 있는 Beauty 성장,
            ② 해외 투자자산의 수익성 검증,
            ③ 브랜드 포트폴리오의 선택과 집중,
            ④ 이익을 현금흐름으로 전환하는 운전자본 관리</b>입니다.
        </div>
        """,
        unsafe_allow_html=True
    )
