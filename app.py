# -*- coding: utf-8 -*-
"""
@author:XuMing(xuming624@qq.com)
@description: 
"""

import os
import json
import time
import streamlit as st
from openai import OpenAI
from loguru import logger
from dotenv import load_dotenv

load_dotenv()
api_key: str = os.getenv("OPENAI_API_KEY")
base_url: str = os.getenv("OPENAI_BASE_URL")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o-mini")
client = OpenAI(api_key=api_key, base_url=base_url)


def make_api_call(messages, max_tokens, is_final_answer=False):
    r = ""
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
            max_tokens=max_tokens,
            temperature=1.0,
            response_format={"type": "json_object"}
        )
        r = response.choices[0].message.content
        return json.loads(r)
    except json.JSONDecodeError as e1:
        if is_final_answer:
            return {"title": "Process", "content": f"{r}"}
        else:
            return {"title": "Process", "content": f"{r}", "next_action": "final_answer"}
    except Exception as e:
        if is_final_answer:
            return {"title": "Error",
                    "content": f"Failed to generate final answer: {str(e)}"}
        else:
            return {"title": "Error", "content": f"Failed to generate step. Error: {str(e)}",
                    "next_action": "final_answer"}


def generate_response(prompt):
    messages = [
        {"role": "system", "content": """You are an expert AI assistant that explains your reasoning step by step. For each step, provide a title that describes what you're doing in that step, along with the content. Decide if you need another step or if you're ready to give the final answer. Respond in JSON format with 'title', 'content', and 'next_action' (either 'continue' or 'final_answer') keys. 
USE AS MANY REASONING STEPS AS POSSIBLE. AT LEAST 3. BE AWARE OF YOUR LIMITATIONS AS AN LLM AND WHAT YOU CAN AND CANNOT DO. IN YOUR REASONING, INCLUDE EXPLORATION OF ALTERNATIVE ANSWERS. CONSIDER YOU MAY BE WRONG, AND IF YOU ARE WRONG IN YOUR REASONING, WHERE IT WOULD BE. FULLY TEST ALL OTHER POSSIBILITIES. YOU CAN BE WRONG. WHEN YOU SAY YOU ARE RE-EXAMINING, ACTUALLY RE-EXAMINE, AND USE ANOTHER APPROACH TO DO SO. 
DO NOT JUST SAY YOU ARE RE-EXAMINING. USE AT LEAST 3 METHODS TO DERIVE THE ANSWER. USE BEST PRACTICES.
Answer using the language same as the question. If the question uses Chinese, the answer should be in Chinese.

Example of a valid JSON response:
```json
{
    "title": "Identifying Key Information",
    "content": "To begin solving this problem, we need to carefully examine the given information and identify the crucial elements that will guide our solution process. This involves...",
    "next_action": "continue"
}```
"""},
        {"role": "user", "content": prompt},
        {"role": "assistant",
         "content": "Thank you! I will now think step by step following my instructions, starting at the beginning after decomposing the problem."}
    ]

    steps = []
    step_count = 1
    total_thinking_time = 0

    while True:
        start_time = time.time()
        step_data = make_api_call(messages, 800)
        logger.debug(f"Step {step_count}, step_data: {step_data}")
        end_time = time.time()
        thinking_time = end_time - start_time
        total_thinking_time += thinking_time

        steps.append((f"Step {step_count}: {step_data['title']}", step_data['content'], thinking_time))

        messages.append({"role": "assistant", "content": json.dumps(step_data, ensure_ascii=False)})

        if step_data['next_action'] == 'final_answer':
            break

        step_count += 1

        # Yield after each step for Streamlit to update
        yield steps, None  # We're not yielding the total time until the end

    # Generate final answer
    messages.append({"role": "user", "content": "Please provide the final answer based on your reasoning above."})

    start_time = time.time()
    final_data = make_api_call(messages, 1000, is_final_answer=True)
    logger.debug(f"final_data: {final_data}")
    end_time = time.time()
    thinking_time = end_time - start_time
    total_thinking_time += thinking_time

    steps.append(("Final Answer", final_data.get('content', ''), thinking_time))

    yield steps, total_thinking_time


def main():
    st.set_page_config(page_title="o1 prototype", page_icon="🧠", layout="wide")

    st.title("o1: Using GPT-4o with CoT to Create O1-like Reasoning Chains")

    st.markdown("""
    This is an early prototype of using prompting to create o1-like reasoning chains to improve output accuracy. It is not perfect and accuracy has yet to be formally evaluated.

    Github [shibing624/o1](https://github.com/shibing624/o1)
    """)

    # Text input for user query
    user_query = st.text_area(label="Enter your query:", placeholder="e.g., How many 'R's are in the word strawberry?",
                              height=3)

    if user_query:
        st.write("Generating response...")

        # Create empty elements to hold the generated text and total time
        response_container = st.empty()
        time_container = st.empty()

        # Generate and display the response
        for steps, total_thinking_time in generate_response(user_query):
            with response_container.container():
                for i, (title, content, thinking_time) in enumerate(steps):
                    if title.startswith("Final Answer"):
                        st.markdown(f"### {title}")
                        # st.markdown(content.replace('\n', '<br>'), unsafe_allow_html=True)
                        st.markdown(content, unsafe_allow_html=True)
                    else:
                        with st.expander(title, expanded=True):
                            # st.markdown(content.replace('\n', '<br>'), unsafe_allow_html=True)
                            st.markdown(content, unsafe_allow_html=True)

            # Only show total time when it's available at the end
            if total_thinking_time is not None:
                time_container.markdown(f"**Total thinking time: {total_thinking_time:.2f} seconds**")


if __name__ == "__main__":
    main()
