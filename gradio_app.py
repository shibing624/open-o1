# -*- coding: utf-8 -*-
"""
@author:XuMing(xuming624@qq.com)
@description: 
"""
import gradio as gr
from o1 import cot_response


def format_steps(steps, total_time):
    html_content = ""
    for title, content, thinking_time in steps:
        if title == "Final Answer":
            html_content += "<h3>{}</h3>".format(title)
            html_content += "<p>{}</p>".format(content.replace('\n', '<br>'))
        else:
            html_content += """
            <details>
                <summary><strong>{}</strong></summary>
                <p>{}</p>
                <p><em>Thinking time for this step: {:.2f} seconds</em></p>
            </details>
            <br>
            """.format(title, content.replace('\n', '<br>'), thinking_time)
    html_content += "<strong>Total thinking time: {:.2f} seconds</strong>".format(total_time)
    return html_content


def main(user_query):
    if not user_query:
        return "Please enter a query to get started.", ""

    try:
        steps, total_time = cot_response(user_query)
        formatted_steps = format_steps(steps, total_time)
    except Exception as e:
        return f"An error occurred during processing. Error: {str(e)}", ""

    return formatted_steps, ""


# Define the Gradio interface
with gr.Blocks() as demo:
    gr.Markdown("# 🤔 open-o1: Using GPT-4o with CoT to Create o1-like Reasoning Chains")

    gr.Markdown("""
    open-o1: Using prompting to create o1-like reasoning chains to improve output accuracy. 

    Github [shibing624/open-o1](https://github.com/shibing624/open-o1)
    """)

    with gr.Row():
        with gr.Column():
            user_input = gr.Textbox(
                label="Enter your query:",
                placeholder="e.g., How many 'R's are in the word strawberry?",
                lines=3
            )
            submit_btn = gr.Button('Submit')

    with gr.Row():
        with gr.Column():
            output_html = gr.HTML()

    submit_btn.click(fn=main, inputs=[user_input], outputs=output_html)

# Launch the Gradio app
if __name__ == "__main__":
    demo.launch()
