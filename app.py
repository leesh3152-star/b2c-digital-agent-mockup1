import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import time

# -----------------------------------------------------------------------------
# 1. 페이지 설정 및 디자인 시스템 (Design System)
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Galaxy S25 AI Marketing Agent",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    /* 1. 폰트 시스템 (채팅 폰트 대폭 확대) */
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Noto Sans KR', sans-serif;
    }

    /* 채팅 메시지 스타일 (가독성 최우선) */
    .stChatMessage p {
        font-size: 1.25rem !important; /* 20px */
        line-height: 1.6 !important;
        font-weight: 500;
    }

    /* 2. 메트릭 카드 디자인 */
    .metric-card {
        background-color: #ffffff;
        border: 1px solid #e0e0e0;
        border-radius: 12px;
        padding: 24px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        margin-bottom: 24px;
    }
    .metric-card h4 {
        margin: 0 0 12px 0;
        color: #1a73e8;
        font-size: 1.2rem;
        font-weight: 700;
    }
    .metric-card p {
        font-size: 1.1rem;
        color: #424242;
    }
    
    /* 3. 질문 가이드 박스 */
    .question-box {
        background-color: #f1f3f4;
        border: 1px solid #dadce0;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 15px;
        cursor: pointer;
        transition: all 0.2s;
    }
    .question-box:hover {
        background-color: #e8f0fe;
        border-color: #4285F4;
        transform: translateY(-2px);
    }
    .question-box h5 {
        margin: 0 0 8px 0;
        color: #1a73e8;
        font-size: 1.1rem;
        font-weight: 700;
    }
    .question-box p {
        margin: 0;
        font-size: 1rem;
        color: #5f6368;
    }

    /* 4. 헤더 스타일 */
    .custom-header {
        display: flex;
        align-items: center;
        margin-bottom: 25px;
        padding-bottom: 15px;
        border-bottom: 3px solid #f1f3f4;
    }
    .custom-header .icon {
        font-size: 2.2rem;
        margin-right: 15px;
    }
    .custom-header .title {
        font-size: 1.8rem;
        font-weight: 800;
        color: #202124;
        margin: 0;
    }

    /* 5. 로딩 컨테이너 */
    .loading-container {
        text-align: center;
        padding: 60px;
    }
    .loading-container h3 {
        font-size: 1.8rem;
        color: #1a73e8;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. 상태 관리 (State Management)
# -----------------------------------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "좋은 아침입니다! ☀️\n현재 **'S25 사전예약 캠페인(Day 4)'** 모니터링 중입니다. 특이사항이 감지되었습니다."}
    ]
if "analysis_mode" not in st.session_state:
    st.session_state.analysis_mode = None 

# 로딩 상태
if "is_processing" not in st.session_state:
    st.session_state.is_processing = False
if "next_mode" not in st.session_state:
    st.session_state.next_mode = None
if "processing_text" not in st.session_state:
    st.session_state.processing_text = ""

# -----------------------------------------------------------------------------
# 3. 레이아웃
# -----------------------------------------------------------------------------
col_chat, col_board = st.columns([4, 6], gap="large")

# =============================================================================
# [Left Panel] Chat
# =============================================================================
with col_chat:
    st.markdown("""
    <div class="custom-header">
        <span class="icon">💬</span>
        <h3 class="title">Chat</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # 채팅 기록 표시
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # (MTA 모드일 때만) 예산 시뮬레이터
    if st.session_state.analysis_mode == 'mta' and not st.session_state.is_processing:
        st.divider()
        st.markdown("#### ⚙️ 예산 시뮬레이터")
        st.info("AI 제안: 인스타 효율이 좋으므로 예산을 늘려보세요.")
        
        insta_budget = st.slider("인스타그램 예산 증액 (%)", 0, 50, 20)
        kakao_budget = st.slider("카카오톡 예산 증액 (%)", 0, 50, 10)
        
        if st.button("🚀 예산 재배치 실행", use_container_width=True):
            st.toast(f"✅ 인스타 +{insta_budget}%, 카톡 +{kakao_budget}% 적용 완료!", icon="🎉")

# =============================================================================
# [Right Panel] Board
# =============================================================================
with col_board:
    st.markdown("""
    <div class="custom-header">
        <span class="icon">🧠</span>
        <h3 class="title">Intelligence Board</h3>
    </div>
    """, unsafe_allow_html=True)

    # ---------------------------------------------------------
    # [A] 로딩 화면 (10초 리얼 타임)
    # ---------------------------------------------------------
    if st.session_state.is_processing:
        with st.container():
            st.markdown(f"""
            <div class="loading-container">
                <h3>🔄 {st.session_state.processing_text}</h3>
                <p>대용량 로그 데이터(500만 건)를 정밀 분석 중입니다...</p>
            </div>
            """, unsafe_allow_html=True)
            
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # 10초 로딩 연출
            steps = 100
            for i in range(steps + 1):
                time.sleep(0.1) 
                progress_bar.progress(i)
                
                if i < 30:
                    status_text.text(f"데이터 수집 중... {i}%")
                elif i < 60:
                    status_text.text(f"노이즈 제거 및 인과관계 추론 중... {i}%")
                else:
                    status_text.text(f"시각화 리포트 생성 중... {i}%")
            
            # 상태 변경 및 리런
            st.session_state.analysis_mode = st.session_state.next_mode
            st.session_state.is_processing = False
            st.rerun()

    # ---------------------------------------------------------
    # [B] 결과 화면
    # ---------------------------------------------------------
    else:
        # [Case 0] 메인 대시보드
        if st.session_state.analysis_mode is None:
            st.markdown("### 🚀 Campaign: Galaxy S25 사전예약 (Day 4)")
            st.caption("2026.01.20 14:00 기준 실시간 현황")
            
            kpi1, kpi2, kpi3 = st.columns(3)
            with kpi1:
                st.metric("누적 사전 예약", "142,500명", "115% 🚀")
            with kpi2:
                st.metric("전환율 (CVR)", "4.8%", "1.2%")
            with kpi3:
                st.metric("예산 소진", "45%", "₩4.5억")
            
            st.divider()

            # 그래프
            dates = ['D-3', 'D-2', 'D-1', 'Day 1', 'Day 2', 'Day 3', 'Day 4']
            target = [10000, 25000, 45000, 70000, 90000, 110000, 125000]
            actual = [12000, 28000, 48000, 75000, 105000, 138000, 142500]

            fig = go.Figure()
            fig.add_trace(go.Scatter(x=dates, y=target, mode='lines', name='Target', line=dict(color='gray', dash='dot')))
            fig.add_trace(go.Scatter(x=dates, y=actual, mode='lines+markers', name='Actual', fill='tonexty', fillcolor='rgba(66, 133, 244, 0.1)', line=dict(color='#4285F4', width=3)))
            fig.update_layout(title="일별 예약 추이 (Day 2 급등 감지)", height=320, margin=dict(t=30, l=10, r=10, b=10))
            st.plotly_chart(fig, use_container_width=True)

            st.success("📢 **AI 알림:** 'Day 2'부터 예약자가 목표치를 크게 상회하고 있습니다. (+35% Jump)")
            
            # 질문 가이드 박스
            st.markdown("#### 👇 무엇을 분석해 드릴까요?")
            c1, c2 = st.columns(2)
            with c1:
                st.markdown("""
                <div class="question-box">
                    <h5>🤔 이게 진짜 AI 덕분일까?</h5>
                    <p>"S25 성과 검증해줘" (Causal)</p>
                </div>
                """, unsafe_allow_html=True)
            with c2:
                st.markdown("""
                <div class="question-box">
                    <h5>🏆 어떤 채널이 효자였을까?</h5>
                    <p>"매체 기여도 분석해줘" (MTA)</p>
                </div>
                """, unsafe_allow_html=True)

        # [Case 1] MTA (기여도 분석)
        elif st.session_state.analysis_mode == 'mta':
            st.markdown("### 🔍 Multi-Touch Attribution")
            st.markdown("""
            <div class="metric-card">
                <h4>📄 숨겨진 효자 채널 발견!</h4>
                <p>인스타/카카오톡의 <b>'어시스트(인지 기여)'</b> 비중이 70%입니다.<br>
                Last Click 기준으로는 보이지 않던 성과입니다.</p>
            </div>
            """, unsafe_allow_html=True)

            fig = go.Figure()
            fig.add_trace(go.Bar(name='Last Click', x=['Google', 'Insta', 'Kakao'], y=[90, 5, 5], marker_color='#b0c4de'))
            fig.add_trace(go.Bar(name='MTA Model', x=['Google', 'Insta', 'Kakao'], y=[30, 40, 30], marker_color=['#4285F4', '#E1306C', '#FEE500']))
            fig.update_layout(title="기여도 모델 비교", barmode='group', height=400)
            st.plotly_chart(fig, use_container_width=True)

            if st.button("🔙 메인 대시보드로 돌아가기"):
                st.session_state.analysis_mode = None
                st.rerun()

        # [Case 2] Causal Analysis (성과 검증)
        elif st.session_state.analysis_mode == 'causal':
            st.markdown("### 📈 Causal Analysis (인과추론)")
            st.markdown("""
            <div class="metric-card">
                <h4>🚀 순수 AI 효과: +1.8배</h4>
                <p>신제품 출시 효과(Hype)를 제거하고 검증한 수치입니다.<br>
                AI 타겟팅 그룹이 랜덤 그룹보다 <b>80% 높은 전환율</b>을 보였습니다.</p>
            </div>
            """, unsafe_allow_html=True)

            fig = go.Figure()
            fig.add_trace(go.Scatter(y=[2, 2.2, 2.5, 2.8, 3], name='Control', line=dict(color='gray', dash='dot')))
            fig.add_trace(go.Scatter(y=[2, 2.3, 4.5, 6, 7.5], name='Treatment', line=dict(color='#4285F4', width=3)))
            fig.add_trace(go.Scatter(y=[2, 2.3, 4.5, 6, 7.5], fill='tonexty', name='Lift', fillcolor='rgba(66,133,244,0.1)', mode='none'))
            fig.update_layout(title="인과 효과 분석 (Lift Chart)", height=400)
            st.plotly_chart(fig, use_container_width=True)

            if st.button("🔙 메인 대시보드로 돌아가기"):
                st.session_state.analysis_mode = None
                st.rerun()

# -----------------------------------------------------------------------------
# 4. 사용자 입력 처리 (Logic Routing)
# -----------------------------------------------------------------------------
if prompt := st.chat_input("질문을 입력하세요..."):
    
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    next_mode = None
    processing_msg = ""
    response_text = ""

    # [Logic 1] 특이사항/원인 질문
    if any(word in prompt for word in ["특이", "감지", "알림", "성과", "높아", "이유", "원인"]) and not any(word in prompt for word in ["검증", "기여", "MTA", "인과"]):
        response_text = "네, 맞습니다! **Day 4 기준 성과가 급등**했는데, 이는 Day 2부터 적용된 AI 모델 덕분으로 보입니다. \n\n정확한 **검증(Causal)**이나 **매체별 기여도(MTA)**를 확인해 보시겠습니까?"
        next_mode = None 

    # [Logic 2] 인과추론 요청
    elif any(word in prompt for word in ["검증", "인과", "Causal", "진짜", "효과"]):
        next_mode = 'causal'
        processing_msg = "인과추론(Causal Inference) 수행 중..."
        response_text = "외부 요인을 제거하고 정확한 AI 효과를 검증했습니다. 오른쪽 결과를 확인해주세요. 👉"

    # [Logic 3] MTA 요청
    elif any(word in prompt for word in ["기여", "MTA", "매체", "채널", "효자", "어떤", "누구"]):
        next_mode = 'mta'
        processing_msg = "고객 여정(Customer Journey) 매핑 중..."
        response_text = "단순 클릭이 아닌, 전체 여정을 분석해 숨겨진 효자 채널을 찾았습니다! 👉"
    
    # [Logic 4] 메인 복귀
    elif any(word in prompt for word in ["메인", "처음", "홈"]):
        next_mode = None
        st.session_state.analysis_mode = None 
        response_text = "메인 대시보드로 돌아왔습니다."
        
    else:
        response_text = "죄송합니다. **'성과 검증'** 또는 **'기여도 분석'**에 대해 물어봐주세요."

    # 로딩 트리거
    if next_mode is not None:
        st.session_state.is_processing = True
        st.session_state.next_mode = next_mode
        st.session_state.processing_text = processing_msg

    st.session_state.messages.append({"role": "assistant", "content": response_text})
    st.rerun()
