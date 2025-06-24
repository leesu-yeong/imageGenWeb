import streamlit as st
from openai import OpenAI


st.title("🖼️ AI 이미지 생성기")
st.write("텍스트를 입력하면, 해당 내용을 바탕으로 이미지를 생성합니다.")

# 사이드바: API 키 입력
st.sidebar.title("🔑 설정")
openai_api_key = st.sidebar.text_input("OpenAI API 키를 입력", type="password")

if not openai_api_key:
    st.sidebar.warning("OpenAI API 키를 입력하세요.")
    st.stop()

# OpenAI 클라이언트 설정
client = OpenAI(api_key=openai_api_key)

# 사용자 입력
prompt = st.text_input("📝 이미지 설명을 입력하세요:", 
                       value="")

# 스타일 버튼 클릭 시 상태 저장을 위해 session_state 사용
if 'style_option' not in st.session_state:
    st.session_state['style_option'] = '기본'

col1, col2, col3 = st.columns(3)
with col1:
    if st.button("만화 스타일"):
        st.session_state['style_option'] = "만화 스타일"
with col2:
    if st.button("유화 스타일"):
        st.session_state['style_option'] = "유화 스타일"
with col3:
    if st.button("기본"):
        st.session_state['style_option'] = "기본"

style_option = st.session_state['style_option']

# ✅ 선택된 스타일을 프롬프트에 반영
if style_option == "만화 스타일":
    full_prompt = f"{prompt}, in cartoon style"
elif style_option == "유화 스타일":
    full_prompt = f"{prompt}, in oil painting style"
else:
    full_prompt = prompt

# ✅ 이미지 크기 선택 옵션 추가
image_size = st.selectbox(
    "🖼️ 이미지 크기를 선택하세요:",
    ["256x256", "512x512", "1024x1024"],
    index=2  # 기본값: 1024x1024
)

# 전송 버튼
if st.button("이미지 생성하기"):
    with st.spinner("이미지를 생성 중입니다..."):
        try:
            response1 = client.images.generate(
                prompt=full_prompt,
                model="dall-e-3",
                n=1, # 또는 "dall-e-2"
                size="1024x1024"
            )
            response2 = client.images.generate(
                prompt=full_prompt,
                model="dall-e-3",
                n=1,  # 또는 "dall-e-2"
                size="1024x1024"
             )
            image_url = response1.data[0].url
            image_ur2 = response2.data[0].url
            st.image(image_url, caption="생성된 이미지1", use_column_width=True)
            st.image(image_ur2, caption="생성된 이미지2", use_column_width=True)
        except Exception as e:
            st.error(f"이미지 생성 중 오류가 발생했습니다: {e}")