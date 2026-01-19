import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import time

# -----------------------------------------------------------------------------
# 1. 페이지 기본 설정 (와이드 모드)
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="B2C AI Marketing Agent",
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
    /* 채팅창이 하단에 고정되므로 왼쪽 패널과 어우러지게 조정 */
</style>
""", unsafe_allow_html=True)

# 초기 세션 상태 설정
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "user", "content": "인스타랑 카톡에 돈 많이 썼는데 성과는 구글만 높아. 이거 예산 줄여야 돼?"},
        {"role": "assistant", "content": "마지막 클릭(Last Click)만 보면 위험합니다. 전체 고객 여정을 분석하는 **AI 기여도 모델링(MTA)**이 필요해 보입니다. 궁금한 점을 물어봐주세요!"}
    ]

if "analysis_done" not in st.session_state:
    st.session_state.analysis_done = False

# -----------------------------------------------------------------------------
# 3. 레이아웃 분할 (Left: Chat & Control / Right: Intelligence Board)
# -----------------------------------------------------------------------------
col_chat, col_board = st.columns([3.5, 6.5], gap="medium")

# =============================================================================
# [Left Panel] Chat & Control
# =============================================================================
with col_chat:
    st.subheader("💬 Chat & Control")
    st.caption("AI 에이전트에게 '성과 분석', '기여도', '왜' 등을 물어보세요.")
    st.divider()

    # 1. 채팅 기록 표시 (왼쪽 컬럼 안에 쌓임)
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    # 2. (분석 완료 후) 컨트롤 패널 표시
    if st.session_state.analysis_done:
        st.divider()
        st.markdown("#### ⚙️ 예산 시뮬레이터")
        st.info("AI 분석 결과에 따라 예산을 조정해보세요.")
        
        insta_budget = st.slider("인스타그램 예산 증액 (%)", 0, 50, 20)
        kakao_budget = st.slider("카카오톡 예산 증액 (%)", 0, 50, 10)
        
        if st.button("🚀 예산 재배치 제안 실행", use_container_width=True):
            st.toast(f"✅ 인스타 +{insta_budget}%, 카톡 +{kakao_budget}% 예산안이 적용되었습니다!", icon="🎉")

# =============================================================================
# [Right Panel] Intelligence Board
# =============================================================================
with col_board:
    st.subheader("📊 Intelligence Board")
    st.divider()

    if not st.session_state.analysis_done:
        # [State A] 분석 전: Last Click 차트 (문제 상황)
        st.info("현재 'Last Click' 기준 분석 데이터를 보고 계십니다.")
        
        fig_before = go.Figure(data=[
            go.Bar(name='Google', x=['매체별 성과'], y=[90], marker_color='#4285F4'),
            go.Bar(name='Instagram', x=['매체별 성과'], y=[5], marker_color='#E1306C'),
            go.Bar(name='KakaoTalk', x=['매체별 성과'], y=[5], marker_color='#FEE500')
        ])
        fig_before.update_layout(
            title="기존 분석 (Last Click)", 
            barmode='group', 
            height=400,
            yaxis_title="전환 기여도(%)"
        )
        st.plotly_chart(fig_before, use_container_width=True)

    else:
        # [State B] 분석 후: MTA 결과 (Before vs After)
        st.success("💡 **숨겨진 영웅 발견:** 인스타/카카오톡의 **'인지 기여(어시스트)'**가 전체 성과의 70%를 차지합니다.")

        # Plotly로 Before vs After 비교 차트
        fig_compare = go.Figure()
        
        # Before (Last Click)
        fig_compare.add_trace(go.Bar(
            name='Last Click (기존)', 
            x=['Google', 'Instagram', 'Kakao'], 
            y=[90, 5, 5],
            marker_color=['#b0c4de', '#b0c4de', '#b0c4de'] # 회색톤 처리
        ))

        # After (AI MTA)
        fig_compare.add_trace(go.Bar(
            name='AI Attribution (재평가)', 
            x=['Google', 'Instagram', 'Kakao'], 
            y=[30, 40, 30],
            marker_color=['#4285F4', '#E1306C', '#FEE500'] # 브랜드 컬러
        ))

        fig_compare.update_layout(
            title="기여도 모델 비교 (Last Click vs MTA)",
            barmode='group',
            height=450,
            yaxis_title="기여도(%)"
        )
        st.plotly_chart(fig_compare, use_container_width=True)

        # Insight & Action Section
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("""
            #### ⚽ Insight
            * **인스타/카톡**: '킬러 패스(어시스트)' 역할
            * **구글**: '골(슈팅)' 역할
            """)
        with c2:
            st.markdown("#### ⚡ Actions")
            st.button("📄 상세 보고서 다운로드 (PDF)", use_container_width=True)
            st.button("💰 저성과 매체 감액 및 예산 이동", type="primary", use_container_width=True)

# -----------------------------------------------------------------------------
# 4. 사용자 입력 처리 (Chat Input) - 하단 고정
# -----------------------------------------------------------------------------
if prompt := st.chat_input("질문을 입력하세요 (예: 왜 구글만 성과가 높아? 분석해줘)"):
    
    # 1. 사용자 메시지 추가 및 표시
    st.session_state.messages.append({"role": "user", "content": prompt})
    # (참고: 입력 즉시 UI 갱신을 위해 rerun이 일어나므로 위쪽 for 루프에서 메시지가 그려짐)

    # 2. 에이전트 응답 로직 (키워드 매칭)
    trigger_words = ["분석", "성과", "이유", "왜", "어트리뷰션", "기여도", "다시"]
    
    if any(word in prompt for word in trigger_words):
        # 분석 요청으로 간주
        response_content = "네, 전체 고객 여정 데이터를 기반으로 **MTA(멀티 터치 어트리뷰션)** 분석을 수행했습니다. 오른쪽 결과를 확인해주세요! 👉"
        st.session_state.analysis_done = True
    else:
        # 엉뚱한 질문 방어
        response_content = "죄송합니다. 저는 마케팅 성과 분석 에이전트입니다. **'성과 분석'**이나 **'기여도'**에 대해 물어봐주세요. 😅"

    # 3. 에이전트 메시지 저장
    st.session_state.messages.append({"role": "assistant", "content": response_content})
    
    # 4. 화면 갱신 (오른쪽 패널 업데이트를 위해)
    st.rerun()
