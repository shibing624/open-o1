# -*- coding: utf-8 -*-
"""
@author:XuMing(xuming624@qq.com)
@description: streamlit app

usage: streamlit run app.py
"""
import streamlit as st
from o1 import cot_response_stream


def main():
    st.set_page_config(page_title="open-o1", page_icon="🤔", layout="wide")

    st.title("open-o1: Using GPT-4o with CoT to Create o1-like Reasoning Chains")

    st.markdown("""
    open-o1: Using prompting to create o1-like reasoning chains to improve output accuracy. 

    Github [shibing624/open-o1](https://github.com/shibing624/open-o1)
    """)

    # Examples
    examples = [
        "How many 'R's are in the word strawberry?",
        "Solve the equation 2x + 3 = 7. What is x?",
        "Amy 有 5 个苹果，她又买了 3 个苹果。然后她给了她的朋友 2 个苹果。最后，她还剩下多少个苹果？",
    ]

    # Display examples as clickable buttons
    example_query = None
    for example in examples:
        if st.button(example):
            example_query = example  # Set the example query if the button is clicked

    # If an example is clicked, use it as the default query
    if example_query:
        st.session_state['user_query'] = example_query

    # Text input for user query
    user_query = st.text_area(
        label="Enter your query:",
        value=st.session_state.get('user_query', ''),
        placeholder="e.g., How many 'R's are in the word strawberry?",
        height=3
    )

    if user_query:
        st.session_state['user_query'] = user_query
        st.write("Generating response...")

        # Create empty elements to hold the generated text and total time
        response_container = st.empty()
        time_container = st.empty()

        # Generate and display the response
        response_generator = cot_response_stream(user_query)
        for steps, total_thinking_time in response_generator:
            with response_container.container():
                for i, (title, content, thinking_time) in enumerate(steps):
                    if title.startswith("Final Answer"):
                        st.markdown(f"### {title}")
                        st.markdown(content, unsafe_allow_html=True)
                    else:
                        with st.expander(title, expanded=True):
                            st.markdown(content, unsafe_allow_html=True)

            # Only show total time when it's available at the end
            if total_thinking_time is not None:
                time_container.markdown(f"**Total thinking time: {total_thinking_time:.2f} seconds**")


if __name__ == "__main__":
    main()
