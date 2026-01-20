import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import time

# -----------------------------------------------------------------------------
# 1. 페이지 기본 설정 (와이드 모드)
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Galaxy S25 AI Marketing Agent",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------------------------------------------------
# 2. 스타일 및 세션 상태 정의
# -----------------------------------------------------------------------------
st.markdown("""
<style>
    .stChatMessage {
        background-color: #f0f2f6;
        border-radius: 10px;
        padding: 10px;
    }
    /* 메트릭 카드 스타일 */
    .metric-card {
        background-color: #e8f0fe;
        border-left: 5px solid #4285F4;
        padding: 15px;
        border-radius: 5px;
        margin-bottom: 20px;
        color: #333;
    }
    .metric-card h4 {
        margin: 0 0 10px 0;
        color: #1a73e8;
    }
</style>
""", unsafe_allow_html=True)

# 초기 세션 상태 설정
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "좋은 아침입니다! ☀️\n현재 **'S25 사전예약 캠페인(Day 4)'** 모니터링 중입니다. 특이사항이 감지되었으니 오른쪽 대시보드를 확인해주세요."}
    ]

# 현재 분석 모드 상태 관리 (None: 대시보드, 'mta': 기여도분석, 'did': 성과검증)
if "analysis_mode" not in st.session_state:
    st.session_state.analysis_mode = None 

# -----------------------------------------------------------------------------
# 3. 레이아웃 분할 (Left: Chat & Control / Right: Intelligence Board)
# -----------------------------------------------------------------------------
col_chat, col_board = st.columns([3.5, 6.5], gap="medium")

# =============================================================================
# [Left Panel] Chat & Control
# =============================================================================
with col_chat:
    st.subheader("💬 Chat & Control")
    st.caption("AI에게 캠페인 현황, 성과 원인, 예산 최적화 등을 물어보세요.")
    st.divider()

    # 1. 채팅 기록 표시
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    # 2. (MTA 모드일 때만) 예산 시뮬레이터 표시
    if st.session_state.analysis_mode == 'mta':
        st.divider()
        st.markdown("#### ⚙️ 예산 시뮬레이터")
        st.info("AI 분석 결과에 따라 예산을 조정해보세요.")
        
        insta_budget = st.slider("인스타그램 예산 증액 (%)", 0, 50, 20)
        kakao_budget = st.slider("카카오톡 예산 증액 (%)", 0, 50, 10)
        
        if st.button("🚀 예산 재배치 실행", use_container_width=True):
            st.toast(f" 인스타 +{insta_budget}%, 카톡 +{kakao_budget}% 적용 완료!", icon="🎉")
            time.sleep(1)

# =============================================================================
# [Right Panel] Intelligence Board (동적 렌더링)
# =============================================================================
with col_board:
    st.subheader("Simply U+ Intelligence Board")
    st.divider()

    # ---------------------------------------------------------
    # [Case 0] 초기 상태: S25 Campaign Dashboard (Default)
    # ---------------------------------------------------------
    if st.session_state.analysis_mode is None:
        st.markdown("### Campaign: Galaxy S25 사전예약 (Day 4)")
        st.caption("2026.01.20 09:00 기준 실시간 현황")
        
        # 1. 핵심 캠페인 지표 (KPIs)
        kpi1, kpi2, kpi3 = st.columns(3)
        with kpi1:
            st.metric(label="누적 사전 예약자", value="142,500명", delta="목표 대비 115% ")
        with kpi2:
            st.metric(label="전환율 (CVR)", value="4.8%", delta="▲ 1.2% (전일 대비)")
        with kpi3:
            st.metric(label="마케팅 예산 소진", value="₩4.5억 / 10억", delta="45% 소진")
        
        st.divider()

        # 2. 일별 예약 추이 그래프 (Target vs Actual)
        dates = ['D-3', 'D-2', 'D-1', 'Day 1', 'Day 2', 'Day 3', 'Day 4 (Today)']
        target = [10000, 25000, 45000, 70000, 90000, 110000, 125000] # 목표치
        actual = [12000, 28000, 48000, 75000, 105000, 138000, 142500] # 실적치 (Day 2부터 급등)

        fig_main = go.Figure()
        # 목표 선
        fig_main.add_trace(go.Scatter(
            x=dates, y=target, mode='lines', name='목표 (Target)',
            line=dict(color='gray', dash='dot')
        ))
        # 실적 선
        fig_main.add_trace(go.Scatter(
            x=dates, y=actual, mode='lines+markers', name='실적 (Actual)',
            fill='tonexty', fillcolor='rgba(66, 133, 244, 0.2)',
            line=dict(color='#4285F4', width=3)
        ))
        fig_main.update_layout(
            title="일별 사전예약 달성 추이",
            height=320,
            margin=dict(l=20, r=20, t=40, b=20),
            hovermode="x unified"
        )
        st.plotly_chart(fig_main, use_container_width=True)

        # 3. AI Insight Hook
        st.success("""
        **🤖 AI Insight 발견**
        * **Event:** 'Day 2'부터 예약자가 폭발적으로 급증했습니다. (+35% Jump)
        * **Analysis:** 주말에 적용한 **'AI 타겟팅 모델 v2'**의 효과로 추정됩니다.
        """)
        
        st.markdown(" **상세 원인이 궁금하다면? (아래 질문을 입력해보세요)**")
        c1, c2 = st.columns(2)
        with c1:
            st.info("**이게 진짜 AI 덕분일까?**")
            st.code("S25 성과 검증해줘 (DiD)", language="text")
        with c2:
            st.info("**어떤 채널이 효자였을까?**")
            st.code("매체 기여도 분석해줘 (MTA)", language="text")

    # ---------------------------------------------------------
    # [Case 1] MTA 분석 모드 (기여도 분석)
    # ---------------------------------------------------------
    elif st.session_state.analysis_mode == 'mta':
        st.markdown("### 🔍 분석 결과: 매체별 AI 기여도 분석 (MTA)")
        
        st.markdown("""
        <div class="metric-card">
            <h4>📄 숨겨진 영웅 발견</h4>
            <p>인스타/카카오톡의 <b>'인지 기여(어시스트)'</b>가 전체 성과의 70% 차지.<br>
            단순 마지막 클릭 기준으로는 보이지 않던 성과입니다.</p>
        </div>
        """, unsafe_allow_html=True)

        # Plotly 비교 차트
        fig_mta = go.Figure()
        fig_mta.add_trace(go.Bar(
            name='Last Click (기존)', x=['Google', 'Instagram', 'Kakao'], y=[90, 5, 5],
            marker_color=['#b0c4de', '#b0c4de', '#b0c4de']
        ))
        fig_mta.add_trace(go.Bar(
            name='AI Attribution (재평가)', x=['Google', 'Instagram', 'Kakao'], y=[30, 40, 30],
            marker_color=['#4285F4', '#E1306C', '#FEE500']
        ))
        fig_mta.update_layout(title="기여도 모델 비교 (Last Click vs MTA)", barmode='group', height=400)
        st.plotly_chart(fig_mta, use_container_width=True)

        c1, c2 = st.columns(2)
        with c1:
            st.info("⚽ **Insight:** 인스타/카톡은 '킬러 패스', 구글은 '슈팅' 역할입니다.")
        with c2:
            st.button("💰 저성과 매체 감액 및 예산 이동", type="primary", use_container_width=True)
        
        if st.button("🔙 메인 대시보드로 돌아가기"):
            st.session_state.analysis_mode = None
            st.rerun()

    # ---------------------------------------------------------
    # [Case 2] DiD 분석 모드 (성과 검증)
    # ---------------------------------------------------------
    elif st.session_state.analysis_mode == 'did':
        st.markdown("### 📈 분석 결과: S25 사전예약 성과 검증 (DiD)")
        
        st.markdown("""
        <div class="metric-card">
            <h4>🚀 AI 타겟팅 순수 증분 효과 (Incremental Lift): +1.8배</h4>
            <p>전환율 기준. 신제품 출시 효과(Base Lift) 및 계절성 요인을 제외한 순수 성과입니다.</p>
        </div>
        """, unsafe_allow_html=True)

        # Plotly 라인 차트
        dates_did = ['W1', 'W2', 'W3 (AI적용)', 'W4', 'W5']
        y_control = [2.0, 2.2, 2.5, 2.8, 3.0]
        y_treatment = [2.0, 2.3, 4.5, 6.0, 7.5]

        fig_did = go.Figure()
        fig_did.add_trace(go.Scatter(
            x=dates_did, y=y_control, mode='lines+markers', name='랜덤 노출군 (Control)',
            line=dict(color='gray', dash='dot')
        ))
        fig_did.add_trace(go.Scatter(
            x=dates_did, y=y_treatment, mode='lines+markers', name='AI 타겟군 (Treatment)',
            line=dict(color='#4285F4', width=3)
        ))
        # 빗금 영역
        fig_did.add_trace(go.Scatter(
            x=dates_did, y=y_treatment, fill='tonexty', fillcolor='rgba(66, 133, 244, 0.1)',
            mode='none', name='순수 AI 효과 (+80%)'
        ))
        fig_did.update_layout(
            title="전환율 비교 (DiD Analysis)", height=400,
            annotations=[dict(x='W5', y=7.5, xref="x", yref="y", text="+1.8x Lift", showarrow=True, arrowhead=1)]
        )
        st.plotly_chart(fig_did, use_container_width=True)

        c1, c2 = st.columns(2)
        with c1:
            st.success("💡 **Insight:** 고가망 구매 확률 'Prime 고객' 집중 공략 성공.")
        with c2:
            st.button("✅ 전사 확대 적용 결재 요청", type="primary", use_container_width=True)

        if st.button("🔙 메인 대시보드로 돌아가기"):
            st.session_state.analysis_mode = None
            st.rerun()

# -----------------------------------------------------------------------------
# 4. 사용자 입력 처리 (Routing Logic) - 하단 고정
# -----------------------------------------------------------------------------
if prompt := st.chat_input("질문을 입력하세요..."):
    
    # 사용자 메시지 저장
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 의도 파악 및 라우팅
    # [A] DiD 분석 요청
    if any(word in prompt for word in ["S25", "타겟팅", "효과", "검증", "신제품", "DiD", "진짜"]):
        st.session_state.analysis_mode = 'did'
        response_text = "외부 요인 제거를 위해 인과추론 분석을 시작합니다... (🔄 고객 데이터 스캔 중...)\n\n**검증 완료.** 순수 AI 기여도는 **+1.8배**입니다. 오른쪽 결과를 확인해주세요. 👉"

    # [B] MTA 분석 요청
    elif any(word in prompt for word in ["기여도", "성과", "매체", "인스타", "어트리뷰션", "분석", "왜"]):
        st.session_state.analysis_mode = 'mta'
        response_text = "마지막 클릭(Last Click)만 보면 위험합니다. 전체 고객 여정을 분석하는 **AI 기여도 모델링(MTA)**을 수행했습니다.\n\n**분석 완료.** 인스타와 카톡이 '어시스트'에 결정적 역할을 했습니다. 👉"
    
    # [C] 메인으로 가고 싶을 때
    elif any(word in prompt for word in ["메인", "처음", "홈", "돌아가"]):
        st.session_state.analysis_mode = None
        response_text = "메인 대시보드로 복귀합니다."

    # [D] 예외 처리
    else:
        response_text = "죄송합니다. **'S25 성과 검증'** 또는 **'매체 기여도 분석'**에 대해 질문해주시면 정확히 답변드릴 수 있습니다. 😅"

    # 응답 저장 및 화면 갱신
    st.session_state.messages.append({"role": "assistant", "content": response_text})
    st.rerun()
