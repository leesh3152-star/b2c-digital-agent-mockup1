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
# 2. 스타일(CSS) 및 세션 상태 정의
# -----------------------------------------------------------------------------
st.markdown("""
<style>
    /* 전체 폰트 및 기본 스타일 */
    .stApp {
        background-color: #ffffff;
    }
    
    /* 채팅 메시지 스타일 */
    .stChatMessage {
        background-color: #f7f9fc;
        border-radius: 12px;
        padding: 12px;
        border: 1px solid #e1e4e8;
    }

    /* 커스텀 헤더 스타일 (아이콘 + 텍스트) */
    .custom-header {
        display: flex;
        align-items: center;
        margin-bottom: 15px;
        padding-bottom: 10px;
        border-bottom: 2px solid #f0f2f6;
    }
    .custom-header .icon {
        font-size: 1.8rem;
        margin-right: 12px;
        background-color: #e8f0fe;
        padding: 8px;
        border-radius: 10px;
        line-height: 1;
    }
    .custom-header .title {
        font-size: 1.5rem;
        font-weight: 700;
        color: #1f2937;
        margin: 0;
    }
    
    /* 질문 예시 박스 스타일 (New!) */
    .question-box {
        background-color: #f8f9fa;
        border: 1px solid #e9ecef;
        border-radius: 8px;
        padding: 15px;
        margin-bottom: 10px;
        cursor: pointer;
        transition: all 0.2s;
    }
    .question-box:hover {
        background-color: #e8f0fe;
        border-color: #4285F4;
    }
    .question-box h5 {
        margin: 0 0 5px 0;
        color: #1a73e8;
        font-size: 1.0rem;
        font-weight: 600;
    }
    .question-box p {
        margin: 0;
        color: #495057;
        font-size: 0.95rem;
    }
    
    /* 메트릭 카드 스타일 */
    .metric-card {
        background: linear-gradient(to right, #f8f9fa, #ffffff);
        border-left: 5px solid #4285F4;
        padding: 20px;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        margin-bottom: 25px;
    }
    .metric-card h4 {
        margin: 0 0 8px 0;
        color: #1a73e8;
        font-size: 1.1rem;
        font-weight: 600;
    }
    .metric-card p {
        margin: 0;
        color: #4b5563;
        font-size: 0.95rem;
        line-height: 1.5;
    }
</style>
""", unsafe_allow_html=True)

# 초기 세션 상태 설정
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "좋은 아침입니다! ☀️\n현재 **'S25 사전예약 캠페인(Day 4)'** 모니터링 중입니다. 특이사항이 감지되었으니 오른쪽 대시보드를 확인해주세요."}
    ]

# 현재 분석 모드 상태 관리
if "analysis_mode" not in st.session_state:
    st.session_state.analysis_mode = None 

# -----------------------------------------------------------------------------
# 3. 레이아웃 분할
# -----------------------------------------------------------------------------
col_chat, col_board = st.columns([3.5, 6.5], gap="medium")

# =============================================================================
# [Left Panel] Chat & Control
# =============================================================================
with col_chat:
    st.markdown("""
    <div class="custom-header">
        <span class="icon">💬</span>
        <h3 class="title">Chat & Control</h3>
    </div>
    """, unsafe_allow_html=True)
    
    st.caption("AI에게 캠페인 현황, 성과 원인, 예산 최적화 등을 물어보세요.")
    
    # 채팅 기록 표시
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    # (MTA 모드일 때만) 예산 시뮬레이터 표시
    if st.session_state.analysis_mode == 'mta':
        st.divider()
        st.markdown("#### ⚙️ 예산 시뮬레이터")
        st.info("AI 분석 결과에 따라 예산을 조정해보세요.")
        
        insta_budget = st.slider("인스타그램 예산 증액 (%)", 0, 50, 20)
        kakao_budget = st.slider("카카오톡 예산 증액 (%)", 0, 50, 10)
        
        if st.button("🚀 예산 재배치 실행", use_container_width=True):
            st.toast(f"✅ 인스타 +{insta_budget}%, 카톡 +{kakao_budget}% 적용 완료!", icon="🎉")
            time.sleep(1)

# =============================================================================
# [Right Panel] Intelligence Board
# =============================================================================
with col_board:
    st.markdown("""
    <div class="custom-header">
        <span class="icon">🧠</span>
        <h3 class="title">Intelligence Board</h3>
    </div>
    """, unsafe_allow_html=True)

    # ---------------------------------------------------------
    # [Case 0] 초기 상태: S25 Campaign Dashboard (Default)
    # ---------------------------------------------------------
    if st.session_state.analysis_mode is None:
        st.markdown("### 🚀 Campaign: Galaxy S25 사전예약 (Day 4)")
        st.caption("2026.01.20 09:00 기준 실시간 현황")
        
        # 1. 핵심 캠페인 지표 (KPIs)
        kpi1, kpi2, kpi3 = st.columns(3)
        with kpi1:
            st.metric(label="누적 사전 예약자", value="142,500명", delta="목표 대비 115% 🚀")
        with kpi2:
            st.metric(label="전환율 (CVR)", value="4.8%", delta="▲ 1.2% (전일 대비)")
        with kpi3:
            st.metric(label="마케팅 예산 소진", value="₩4.5억 / 10억", delta="45% 소진")
        
        st.divider()

        # 2. 일별 예약 추이 그래프
        dates = ['D-3', 'D-2', 'D-1', 'Day 1', 'Day 2', 'Day 3', 'Day 4 (Today)']
        target = [10000, 25000, 45000, 70000, 90000, 110000, 125000]
        actual = [12000, 28000, 48000, 75000, 105000, 138000, 142500]

        fig_main = go.Figure()
        fig_main.add_trace(go.Scatter(
            x=dates, y=target, mode='lines', name='목표 (Target)',
            line=dict(color='gray', dash='dot')
        ))
        fig_main.add_trace(go.Scatter(
            x=dates, y=actual, mode='lines+markers', name='실적 (Actual)',
            fill='tonexty', fillcolor='rgba(66, 133, 244, 0.2)',
            line=dict(color='#4285F4', width=3)
        ))
        fig_main.update_layout(
            title="일별 사전예약 달성 추이", height=320, margin=dict(l=20, r=20, t=40, b=20), hovermode="x unified"
        )
        st.plotly_chart(fig_main, use_container_width=True)

        # 3. AI Insight Hook (디자인 개선됨!)
        st.success("""
        **🤖 AI Insight 발견**
        * **Event:** 'Day 2'부터 예약자가 폭발적으로 급증했습니다. (+35% Jump)
        * **Analysis:** 주말에 적용한 **'AI 타겟팅 모델 v2'**의 효과로 추정됩니다.
        """)
        
        st.markdown("#### 👇 상세 원인이 궁금하다면?")
        
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("""
            <div class="question-box">
                <h5>이게 진짜 AI 덕분일까?</h5>
                <p>"S25 성과 검증해줘" (Causal)</p>
            </div>
            """, unsafe_allow_html=True)
        with c2:
            st.markdown("""
            <div class="question-box">
                <h5>어떤 채널이 효자였을까?</h5>
                <p>"매체 기여도 분석해줘" (MTA)</p>
            </div>
            """, unsafe_allow_html=True)

    # ---------------------------------------------------------
    # [Case 1] MTA 분석 모드 (Multi-Touch Attribution)
    # ---------------------------------------------------------
    elif st.session_state.analysis_mode == 'mta':
        st.markdown("### 🔍 분석 결과: Multi-Touch Attribution (기여도 분석)")
        
        st.markdown("""
        <div class="metric-card">
            <h4>📄 숨겨진 효자 채널 발견!</h4>
            <p>인스타/카카오톡의 <b>'인지 기여(어시스트)'</b>가 전체 성과의 70% 차지.<br>
            단순 마지막 클릭 기준으로는 보이지 않던 성과입니다.</p>
        </div>
        """, unsafe_allow_html=True)

        fig_mta = go.Figure()
        fig_mta.add_trace(go.Bar(
            name='Last Click (기존)', x=['Google', 'Instagram', 'Kakao'], y=[90, 5, 5],
            marker_color=['#b0c4de', '#b0c4de', '#b0c4de']
        ))
        fig_mta.add_trace(go.Bar(
            name='Multi-Touch Attribution', x=['Google', 'Instagram', 'Kakao'], y=[30, 40, 30],
            marker_color=['#4285F4', '#E1306C', '#FEE500']
        ))
        fig_mta.update_layout(title="기여도 모델 비교 (Last Click vs MTA)", barmode='group', height=400)
        st.plotly_chart(fig_mta, use_container_width=True)

        c1, c2 = st.columns(2)
        with c1:
            st.info("⚽ **Insight:** 인스타/카카오톡은 '킬러 패스', 구글은 '슈팅' 역할입니다.")
        with c2:
            st.button("💰 저성과 매체 감액 및 예산 이동", type="primary", use_container_width=True)
        
        if st.button("🔙 메인 대시보드로 돌아가기"):
            st.session_state.analysis_mode = None
            st.rerun()

    # ---------------------------------------------------------
    # [Case 2] Causal Analysis 모드 (인과추론)
    # ---------------------------------------------------------
    elif st.session_state.analysis_mode == 'causal':
        st.markdown("### 📈 분석 결과: Causal Analysis (S25 성과 검증)")
        
        st.markdown("""
        <div class="metric-card">
            <h4>🚀 순수 AI 효과 (Incremental Lift): +1.8배</h4>
            <p>신제품 출시 효과(Base Lift) 및 계절성 요인을 제거하고<br>
            <b>인과추론(Causal Inference)</b>을 통해 검증한 순수 성과입니다.</p>
        </div>
        """, unsafe_allow_html=True)

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
        fig_did.add_trace(go.Scatter(
            x=dates_did, y=y_treatment, fill='tonexty', fillcolor='rgba(66, 133, 244, 0.1)',
            mode='none', name='Causal Effect (+80%)'
        ))
        fig_did.update_layout(
            title="인과 효과 분석 (Causal Analysis)", height=400,
            annotations=[dict(x='W5', y=7.5, xref="x", yref="y", text="+1.8x Lift", showarrow=True, arrowhead=1)]
        )
        st.plotly_chart(fig_did, use_container_width=True)

        c1, c2 = st.columns(2)
        with c1:
            st.success("💡 **Insight:** 고구매 확률 'Prime 고객' 집중 공략 성공.")
        with c2:
            st.button("✅ 전사 확대 적용 결재 요청", type="primary", use_container_width=True)

        if st.button("🔙 메인 대시보드로 돌아가기"):
            st.session_state.analysis_mode = None
            st.rerun()

# -----------------------------------------------------------------------------
# 4. 사용자 입력 처리 (Routing Logic) - 하단 고정
# -----------------------------------------------------------------------------
if prompt := st.chat_input("질문을 입력하세요..."):
    
    st.session_state.messages.append({"role": "user", "content": prompt})

    # [A] 인과추론(Causal Analysis) 요청
    if any(word in prompt for word in ["S25", "타겟팅", "효과", "검증", "신제품", "인과", "Causal", "진짜"]):
        st.session_state.analysis_mode = 'causal'
        response_text = "외부 요인을 제거하고 정확한 효과를 측정하기 위해 **인과추론(Causal Analysis)**을 수행합니다... (🔄 데이터 스캔 중...)\n\n**검증 완료.** 순수 AI 기여도는 **+1.8배**입니다. 오른쪽 결과를 확인해주세요. 👉"

    # [B] 멀티 터치 어트리뷰션(MTA) 요청
    # 👉 (수정됨) "효자", "채널", "어떤" 키워드 추가로 질문 인식률 향상
    elif any(word in prompt for word in ["기여도", "성과", "매체", "인스타", "어트리뷰션", "분석", "Multi", "MTA", "효자", "채널", "어떤"]):
        st.session_state.analysis_mode = 'mta'
        response_text = "단순 클릭만으로는 진짜 효자를 찾기 어렵습니다. 전체 여정을 분석하는 **Multi-Touch Attribution** 분석 결과입니다.\n\n**분석 완료.** 인스타와 카톡이 숨겨진 효자였습니다! 👉"
    
    # [C] 메인 복귀
    elif any(word in prompt for word in ["메인", "처음", "홈", "돌아가"]):
        st.session_state.analysis_mode = None
        response_text = "메인 대시보드로 복귀합니다."

    else:
        response_text = "죄송합니다. **'S25 성과 검증'** 또는 **'매체 기여도 분석'**에 대해 질문해주시면 정확히 답변드릴 수 있습니다. 😅"

    st.session_state.messages.append({"role": "assistant", "content": response_text})
    st.rerun()
