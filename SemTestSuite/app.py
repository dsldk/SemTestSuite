import streamlit as st
import pandas as pd
from SemTestSuite.utils import get_lexibot_response, get_models, get_roles, get_role, new_chat, get_image_from_prompt


def chat(model: str) -> None:
    for dialogue in st.session_state.dialogue[1:]:
        st.markdown(body=f"### {dialogue['role']}\n\n{dialogue['content']}")

    send_template = False
    template_input = ""
    chat_container = None
    if st.session_state.template:
        template_container, chat_container = st.tabs(["Templates", "Chat"])
        with template_container:
            with st.form(key="template_form", clear_on_submit=True):
                st.markdown(st.session_state.template)
                col1, col2, col3 = st.columns(3)
                template_input_1 = col1.text_input("a")
                template_input_2 = col2.text_input("b")
                col2.slider(
                    "Temperature",
                    min_value=0.0,
                    max_value=2.0,
                    value=1.0,
                    step=0.1,
                    key="templ_temp_key",
                )
                send_template = st.form_submit_button("Send template")
    if not chat_container:
        chat_container, *rest = st.tabs(
            [
                "Chat",
            ]
        )
    with chat_container:
        with st.form(key="chat_form", clear_on_submit=True):
            user_input = st.text_area("Type something")
            temperature_input = st.slider(
                "~Creativity (the higher the value the more creative -- or unreliable -- the response)",
                min_value=0.0,
                max_value=2.0,
                value=1.0,
                step=0.1,
                key="chat_temp_key",
            )
            send = st.form_submit_button("Send")
    if send or send_template:
        if send_template:
            user_input = st.session_state.template.replace("{b}", template_input_2).replace("{a}", template_input_1)
        with st.spinner("Thinking..."):
            reply, dialogue = get_lexibot_response(
                user_input, model, st.session_state.dialogue, temperature_input
            )
            if not dialogue:
                st.write(reply)
            else:
                st.session_state.dialogue = dialogue
            st.experimental_rerun()


def main() -> None:
    if "dialogue" not in st.session_state:
        st.session_state.dialogue = []
    if "activated" not in st.session_state:
        st.session_state.activated = False
    if "template" not in st.session_state:
        st.session_state.template = ""

    st.title("Lexibot")
    instructions = ""

    with st.sidebar:
        selected_model = st.selectbox("Select a model", get_models()) or ""
        selected_role = st.selectbox("Select a role", get_roles())
        selected_lang = st.selectbox("Select a language", ["en", "da"])

        if selected_role:
            role = get_role(selected_role, lang=selected_lang)
            instructions = st.text_area(
                label="Role instructions",
                value=role.get("instructions", ""),
                height=200,
                key="role_instructions",
            )

            selected_template = st.selectbox(
                "Select a template", role.get("templates", [])
            )
            st.session_state.template = selected_template

        uploaded_file = st.file_uploader("Choose a file")
        if uploaded_file is not None:
            dataframe = pd.read_csv(uploaded_file)
            st.write(dataframe)


        if st.button("New dialogue"):
            st.session_state.activated = True
            st.session_state.dialogue = new_chat(instructions).get("dialogue", [])




        st.divider()

    if st.session_state.activated:
        chat(model=selected_model)

    st.divider()


if __name__ == "__main__":
    main()
