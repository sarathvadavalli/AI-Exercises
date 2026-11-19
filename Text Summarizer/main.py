import streamlit as st

from langchain_helper import summarize_text


st.set_page_config(
    page_title="Text Summarizer",
    page_icon=":material/article:",
    layout="wide",
)

st.title("Text summarizer", icon=":material/article:")
st.caption("Turn long passages into a clear topic, concise summary, and key takeaways.")

left, right = st.columns([0.42, 0.58], gap="large")

with left:
    with st.container(border=True):
        st.subheader("Source text", icon=":material/edit_note:")
        st.caption("Paste an article, essay, report, or meeting notes.")

        with st.form("summarizer_form", border=False):
            text = st.text_area(
                "Text to summarize",
                height=280,
                placeholder="Paste or type your text here...",
            )

            st.caption("Summary length")
            target_size = st.segmented_control(
                "Summary size",
                ["Small", "Medium", "Detailed"],
                default="Medium",
                width="stretch",
                label_visibility="collapsed",
            )

            submitted = st.form_submit_button(
                "Summarize text",
                icon=":material/auto_awesome:",
                width="stretch",
                type="primary",
            )

            if submitted:
                if not text.strip():
                    st.error("Enter some text before summarizing.")
                else:
                    try:
                        with st.spinner("Summarizing your text..."):
                            st.session_state["summary_result"] = summarize_text(
                                text=text,
                                target_size=target_size,
                            )
                    except Exception as exc:
                        st.error(f"Could not summarize the text: {exc}")

with right:
    result = st.session_state.get("summary_result")

    if result:
        with st.container(border=True):
            st.subheader("Extracted topic", icon=":material/category:")
            st.markdown(f"### {result.topic}")

        with st.container(border=True):
            st.subheader("Summary", icon=":material/summarize:")
            st.write(result.summary)

        with st.container(border=True):
            st.subheader("Key points", icon=":material/list_alt:")
            for index, point in enumerate(result.key_points, start=1):
                st.markdown(
                    f":blue-badge[{index}]  {point}",
                )
    else:
        with st.container(border=True):
            st.subheader("Your summary", icon=":material/notes:")
            st.caption("Results will appear here after you summarize your text.")