import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import time

# -----------------------------------------------------------------------------
# 1. 페이지 설정 및 디자인 시스템 (Design System) 적용
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Galaxy S25 AI Marketing Agent",
    layout="wide",
    initial_sidebar_state="expanded"
)

# UI/UX 디자이너 모드: 폰트, 여백, 카드 스타일 정밀 조정
st.markdown("""
<style>
    /* Google Fonts (Pretendard/Roboto 계열) 적용 느낌 */
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Noto Sans KR', sans-serif;
        font-size: 18px; /* 기본 폰트 사이즈 Up */
    }

    /* 헤더 스타일 강화 */
    h1, h2, h3 {
        font-weight: 700 !important;
        letter-spacing: -0.5px;
    }
    h3 {
        font-size: 1.6rem !important; /* 소제목 크기 확대 */
        margin-bottom: 1rem !important;
    }
    
    /* 카드 디자인 (Shadow & Rounded) */
    .metric-card {
        background-color: #ffffff;
        border: 1px solid #e0e0e0;
        border-radius: 12px;
        padding: 24px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        margin-bottom: 24px;
        transition: transform 0.2s;
    }
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(0,0,0,0.1);
    }
    .metric-card h4 {
        margin: 0 0 12px 0;
        color: #1a73e8; /* Google Blue */
        font-size: 1.2rem;
        font-weight: 600;
    }
    .metric-card p {
        margin: 0;
        color: #424242;
        font-size: 1.05rem;
        line-height: 1.6;
    }
    
    /* 채팅 메시지 가독성 개선 */
    .stChatMessage {
        font-size: 1.05rem;
        line-height: 1.6;
        border-radius: 16px;
    }

    /* 커스텀 헤더 (아이콘 + 텍스트) */
    .custom-header {
        display: flex;
        align-items: center;
        margin-bottom: 20px;
        padding-bottom: 12px;
        border-bottom: 3px solid #f1f3f4;
    }
    .custom-header .icon {
        font-size: 2.2rem;
        margin-right: 16px;
        background-color: #e8f0fe;
        padding: 12px;
        border-radius: 16px;
        line-height: 1;
    }
    .custom-header .title {
        font-size: 1.8rem;
        font-weight: 800;
        color: #202124;
        margin: 0;
    }

    /* 질문 예시 버튼 스타일 */
    .question-box {
        background-color: #f8f9fa;
        border: 1px solid #dadce0;
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 12px;
        cursor: pointer;
    }
    .question-box h5 {
        margin: 0 0 4px 0;
        color: #1a73e8;
        font-size: 1.1rem;
        font-weight: 600;
    }
    
    /* 로딩 애니메이션 컨테이너 */
    .loading-container {
        text-align: center;
        padding: 50px;
        color: #5f6368;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. 세션 상태 및 로직 관리 (State Machine)
# -----------------------------------------------------------------------------

# 초기 세션 설정
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "좋은 아침입니다! ☀️\n현재 **'S25 사전예약 캠페인(Day 4)'** 모니터링 중입니다. 특이사항이 감지되었습니다."}
    ]
if "analysis_mode" not in st.session_state:
    st.session_state.analysis_mode = None 

# [NEW] 로딩 상태 관리 (True면 로딩 화면을 보여줌)
if "is_processing" not in st.session_state:
    st.session_state.is_processing = False
if "next_mode" not in st.session_state:
    st.session_state.next_mode = None
if "processing_text" not in st.session_state:
    st.session_state.processing_text = ""

# -----------------------------------------------------------------------------
# 3. 레이아웃 (Layout)
# -----------------------------------------------------------------------------
col_chat, col_board = st.columns([3.5, 6.5], gap="large")

# =============================================================================
# [Left Panel] Chat & Control
# =============================================================================
with col_chat:
    st.markdown("""
    <div class="custom-header">
        <span class="icon">💬</span>
        <h3 class="title">Chat</h3>
    </div>
    """, unsafe_allow_html=True)
    
    st.caption("AI에게 캠페인 현황, 성과 원인, 예산 최적화 등을 물어보세요.")
    
    # 채팅 기록 표시
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    # (MTA 모드일 때만) 예산 시뮬레이터 표시
    if st.session_state.analysis_mode == 'mta' and not st.session_state.is_processing:
        st.divider()
        st.markdown("#### ⚙️ 예산 시뮬레이터")
        st.info("AI 분석 결과에 따라 예산을 조정해보세요.")
        
        insta_budget = st.slider("인스타그램 예산 증액 (%)", 0, 50, 20)
        kakao_budget = st.slider("카카오톡 예산 증액 (%)", 0, 50, 10)
        
        if st.button("🚀 예산 재배치 실행", use_container_width=True):
            st.toast(f"✅ 인스타 +{insta_budget}%, 카톡 +{kakao_budget}% 적용 완료!", icon="🎉")

# =============================================================================
# [Right Panel] Intelligence Board (여기가 핵심!)
# =============================================================================
with col_board:
    st.markdown("""
    <div class="custom-header">
        <span class="icon">🧠</span>
        <h3 class="title">Board</h3>
    </div>
    """, unsafe_allow_html=True)

    # ---------------------------------------------------------
    # [상태 A] 로딩 중 (Processing State) - 연출 강화
    # ---------------------------------------------------------
    if st.session_state.is_processing:
        # 로딩 화면 렌더링
        with st.container():
            st.markdown(f"""
            <div class="loading-container">
                <h3>🔄 {st.session_state.processing_text}</h3>
                <p>대용량 로그 데이터를 스캔하고 있습니다. 잠시만 기다려주세요...</p>
            </div>
            """, unsafe_allow_html=True)
            
            # 프로그레스 바 연출
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # [UX Trick] 강제 지연 (2초) 동안 진행률 올라가는 연출
            for percent_complete in range(0, 101, 20):
                time.sleep(0.3) # 0.3초 * 5회 = 1.5초 지연
                progress_bar.progress(percent_complete)
                status_text.text(f"데이터 처리 중... {percent_complete}%")
            
            # 로딩 완료 후 상태 변경
            st.session_state.analysis_mode = st.session_state.next_mode
            st.session_state.is_processing = False
            st.rerun() # 화면 새로고침 (결과 화면으로 이동)

    # ---------------------------------------------------------
    # [상태 B] 결과 화면 (Normal State)
    # ---------------------------------------------------------
    else:
        # [Case 0] 초기 대시보드
        if st.session_state.analysis_mode is None:
            st.markdown("### 🚀 Campaign: Galaxy S25 사전예약 (Day 4)")
            st.caption("2026.01.20 09:00 기준 실시간 현황")
            
            kpi1, kpi2, kpi3 = st.columns(3)
            with kpi1:
                st.metric(label="누적 사전 예약자", value="142,500명", delta="115% 🚀")
            with kpi2:
                st.metric(label="전환율 (CVR)", value="4.8%", delta="1.2%")
            with kpi3:
                st.metric(label="예산 소진율", value="45%", delta="₩4.5억")
            
            st.divider()

            # 차트 영역
            dates = ['D-3', 'D-2', 'D-1', 'Day 1', 'Day 2', 'Day 3', 'Day 4']
            target = [10000, 25000, 45000, 70000, 90000, 110000, 125000]
            actual = [12000, 28000, 48000, 75000, 105000, 138000, 142500]

            fig_main = go.Figure()
            fig_main.add_trace(go.Scatter(x=dates, y=target, mode='lines', name='목표', line=dict(color='gray', dash='dot')))
            fig_main.add_trace(go.Scatter(x=dates, y=actual, mode='lines+markers', name='실적', fill='tonexty', fillcolor='rgba(66, 133, 244, 0.1)', line=dict(color='#4285F4', width=3)))
            fig_main.update_layout(title="일별 사전예약 달성 추이", height=350, margin=dict(l=20, r=20, t=40, b=20), hovermode="x unified")
            st.plotly_chart(fig_main, use_container_width=True)

            # AI Insight Hook
            st.success("**🤖 AI Insight:** 'Day 2'부터 예약자가 폭발적으로 급증했습니다. (+35% Jump)")
            
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

        # [Case 1] MTA 분석 결과
        elif st.session_state.analysis_mode == 'mta':
            st.markdown("### 🔍 Multi-Touch Attribution (기여도 분석)")
            
            st.markdown("""
            <div class="metric-card">
                <h4>📄 숨겨진 효자 채널 발견!</h4>
                <p>인스타/카카오톡의 <b>'인지 기여(어시스트)'</b>가 전체 성과의 70%를 차지하고 있습니다.<br>
                단순 마지막 클릭(Last Click) 기준으로는 보이지 않던 성과입니다.</p>
            </div>
            """, unsafe_allow_html=True)

            fig_mta = go.Figure()
            fig_mta.add_trace(go.Bar(name='Last Click', x=['Google', 'Instagram', 'Kakao'], y=[90, 5, 5], marker_color=['#b0c4de', '#b0c4de', '#b0c4de']))
            fig_mta.add_trace(go.Bar(name='MTA Model', x=['Google', 'Instagram', 'Kakao'], y=[30, 40, 30], marker_color=['#4285F4', '#E1306C', '#FEE500']))
            fig_mta.update_layout(title="기여도 모델 비교", barmode='group', height=400)
            st.plotly_chart(fig_mta, use_container_width=True)

            st.button("🔙 메인 대시보드로 돌아가기", use_container_width=True)

        # [Case 2] Causal Analysis 결과
        elif st.session_state.analysis_mode == 'causal':
            st.markdown("### 📈 Causal Analysis (S25 성과 검증)")
            
            st.markdown("""
            <div class="metric-card">
                <h4>🚀 순수 AI 효과 (Incremental Lift): +1.8배</h4>
                <p>신제품 출시 효과(Base Lift) 및 계절성 요인을 <b>인과추론</b> 알고리즘으로 제거했습니다.<br>
                이를 통해 검증된 순수한 AI 타겟팅 성과입니다.</p>
            </div>
            """, unsafe_allow_html=True)

            dates_did = ['W1', 'W2', 'W3 (AI적용)', 'W4', 'W5']
            y_control = [2.0, 2.2, 2.5, 2.8, 3.0]
            y_treatment = [2.0, 2.3, 4.5, 6.0, 7.5]

            fig_did = go.Figure()
            fig_did.add_trace(go.Scatter(x=dates_did, y=y_control, mode='lines+markers', name='Control (랜덤)', line=dict(color='gray', dash='dot')))
            fig_did.add_trace(go.Scatter(x=dates_did, y=y_treatment, mode='lines+markers', name='Treatment (AI타겟)', line=dict(color='#4285F4', width=3)))
            fig_did.add_trace(go.Scatter(x=dates_did, y=y_treatment, fill='tonexty', fillcolor='rgba(66, 133, 244, 0.1)', mode='none', name='Pure Lift'))
            fig_did.update_layout(title="인과 효과 분석 (Lift Chart)", height=400)
            st.plotly_chart(fig_did, use_container_width=True)

            st.button("🔙 메인 대시보드로 돌아가기", use_container_width=True)

# -----------------------------------------------------------------------------
# 4. 사용자 입력 처리 (Logic Flow)
# -----------------------------------------------------------------------------
if prompt := st.chat_input("질문을 입력하세요..."):
    
    # 1. 사용자 메시지 즉시 표시
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # 2. 다음 상태 결정 (Logic Routing)
    next_mode = None
    processing_msg = "분석 중..."
    response_text = ""

    # [Logic A] 인과추론
    if any(word in prompt for word in ["S25", "타겟팅", "효과", "검증", "신제품", "인과", "Causal", "진짜"]):
        next_mode = 'causal'
        processing_msg = "인과추론(Causal Inference) 수행 중..."
        response_text = "외부 요인을 제거하고 정확한 효과를 측정했습니다. 오른쪽 결과를 확인해주세요. 👉"

    # [Logic B] MTA
    elif any(word in prompt for word in ["기여도", "성과", "매체", "인스타", "어트리뷰션", "분석", "Multi", "MTA", "효자", "채널", "어떤"]):
        next_mode = 'mta'
        processing_msg = "고객 여정(Journey) 데이터 매핑 중..."
        response_text = "단순 클릭이 아닌, 전체 여정을 분석한 결과입니다. 인스타와 카톡이 효자였네요! 👉"
    
    # [Logic C] 메인 복귀
    elif any(word in prompt for word in ["메인", "처음", "홈", "돌아가"]):
        next_mode = None
        response_text = "메인 대시보드로 복귀합니다."
    
    else:
        response_text = "죄송합니다. **'S25 성과 검증'** 또는 **'매체 기여도 분석'**에 대해 질문해주세요. 😅"

    # 3. 로딩 상태 설정 (핵심!)
    if next_mode is not None:
        st.session_state.is_processing = True # 로딩 화면 트리거
        st.session_state.next_mode = next_mode
        st.session_state.processing_text = processing_msg
    else:
        st.session_state.analysis_mode = None # 메인 복귀 등 즉시 처리

    # 4. 에이전트 답변 저장 및 리런
    st.session_state.messages.append({"role": "assistant", "content": response_text})
    st.rerun() # 여기서 리런하면 -> 위쪽 'is_processing' 블록이 실행됨
