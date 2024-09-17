# -*- coding: utf-8 -*-
"""
@description:
"""

import os
import json
import time
from openai import OpenAI
from loguru import logger
from dotenv import load_dotenv

load_dotenv()
api_key: str = os.getenv("OPENAI_API_KEY")
base_url: str = os.getenv("OPENAI_BASE_URL")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o-mini")
client = OpenAI(api_key=api_key, base_url=base_url)


def make_api_call(messages, max_tokens, is_final_answer=False):
    """
    Make an API call to the OpenAI API.
    :param messages:
    :param max_tokens:
    :param is_final_answer:
    :return:
    """
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
            max_tokens=max_tokens,
            temperature=1.0,
            response_format={"type": "json_object"}
        )
        r = response.choices[0].message.content

        try:
            return json.loads(r)
        except json.JSONDecodeError:
            # If parsing fails, return the content as is
            return {
                "title": "Raw Response",
                "content": r,
                "next_action": "final_answer" if is_final_answer else "continue"
            }
    except Exception as e:
        error_message = f"Failed to generate {'final answer' if is_final_answer else 'step'}. Error: {str(e)}"
        return {"title": "Error", "content": error_message, "next_action": "final_answer"}


def cot_response_stream(prompt):
    """
    Generate reasoning steps for a given prompt using the CoT method. stream mode.
    :param prompt: str, query
    :return: steps, total_thinking_time
    """
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
        steps.append((f"Step {step_count}: {step_data['title']}", step_data.get('content', ''), thinking_time))
        messages.append({"role": "assistant", "content": json.dumps(step_data, ensure_ascii=False)})

        if step_data['next_action'] == 'final_answer' or step_count >= 15:
            break
        step_count += 1
        yield steps, total_thinking_time

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


def cot_response(prompt):
    """COT response. no stream mode."""
    return list(cot_response_stream(prompt))[-1]


if __name__ == '__main__':
    prompt = "一句话介绍林黛玉"
    # If you want to stream the response:
    response_generator = cot_response_stream(prompt)
    for steps, total_thinking_time in response_generator:
        for i, (title, content, thinking_time) in enumerate(steps):
            if title.startswith("Final Answer"):
                print(f"### {title}")
                print(content)
            else:
                print(f"{title}:")
                print(content)
        print(f"**Total thinking time so far: {total_thinking_time:.2f} seconds**")

    # Or, if you want to get the final answer only:
    steps, total_thinking_time = cot_response(prompt)
    for step in steps:
        print(step)
    print("Total thinking time:", total_thinking_time)
