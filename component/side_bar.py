import streamlit as st


def aws_credentials_sidebar():
    access_key_in_session = st.session_state.get("access_key")
    secret_access_key_in_session = st.session_state.get("secret_access_key")

    with st.sidebar:
        if not access_key_in_session:
            access_key = st.text_input(
                "Write down an AWS ACCESS KEY",
                placeholder="AWS ACCESS KEY",
            )
        else:
            access_key = access_key_in_session

        if not secret_access_key_in_session:
            secret_access_key = st.text_input(
                "Write down an AWS SECRET ACCESS KEY",
                placeholder="AWS SECRET ACCESS KEY",
            )
        else:
            secret_access_key = secret_access_key_in_session

        if not (access_key_in_session and secret_access_key_in_session):
            st.button(
                label="Save Key",
                on_click=lambda: st.session_state.update(
                    {"access_key": access_key, "secret_access_key": secret_access_key}
                )
            )

        if access_key_in_session and secret_access_key_in_session:
            st.button(
                label="Clear Key",
                on_click=lambda: st.session_state.clear()
            )

        return access_key_in_session, secret_access_key_in_session
