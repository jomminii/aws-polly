import streamlit as st

from helper.ai_voice_helper import AIVoiceHelper
from helper.voices_dictionary import voices_dict
voice_dict = voices_dict.copy()

language_list = voice_dict.keys()


st.set_page_config(
    page_title="AI 음성 만들기",
    page_icon="🎤",
)

st.title("AI 음성 만들기")

st.markdown(
    """
    Welcome to my **AI 음성 만들기**.
    
    This is a demo of aws polly.
    
    """
)

selected_language = st.selectbox("언어 선택", language_list)

st.write(selected_language)

selected_engine = st.selectbox("엔진 선택", voice_dict[selected_language].keys())


persona_name_list = [item['이름'] for item in voice_dict[selected_language][selected_engine]]
selected_persona = st.selectbox("목소리 선택", persona_name_list)

st.write(selected_persona)

speed_rate = st.slider("속도 선택", 20, 200, 100)

text = st.text_area(
    label="내용 입력",
    help='음성으로 변환할 내용을 입력해주세요.',
    on_change=print("!!"),
    placeholder='음성으로 변환할 내용을 입력해주세요.',
)

create = st.button(
    label="음성 만들기",
)

if create:
    if selected_persona and text:
        audio_stream = AIVoiceHelper().synthesize_voice(
            text=text,
            # language_code=selected_language_code,
            voice_id=selected_persona,
            rate=speed_rate
        )

        if audio_stream:
            st.download_button(
                label="Download MP3",
                data=audio_stream,
                file_name="ai_voice.mp3",
                mime="audio/mpeg"
            )
    else:
        st.warning("내용을 입력해주세요.")
        print("no")


