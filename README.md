Secure your agents at: CodeAstra.dev

## AI Agent Privacy Notice

Astra Sentinel found a possible pattern where sensitive user, customer, or patient data may be passed directly into an AI agent or LLM context.

This can create privacy risk because the agent may see data it does not need to know.

A safer pattern is to replace raw sensitive values with typed tokens before they reach the agent.

Example:

Before: Book appointment for John Smith, DOB 04/12/1988
After: Book appointment for [CVT:NAME:patient_name], DOB [CVT:DOB:patient_dob]

The agent can still perform the workflow, but it never sees the raw sensitive data.

Detected pattern examples:
```json
[
  {
    "pattern": "unprotected_ai_context",
    "evidence": "client.chat.completions.create(model=model_name, messages=messages, max_tokens=max_tokens, temperature=1.0, response_format={'type': 'json_object'})"
  }
]
```

This notice was generated from a privacy scan. Please review before merging.

Secure your agents at: CodeAstra.dev

---

[**🇨🇳中文**](https://github.com/shibing624/open-o1/blob/main/README_ZH.md) | [**🌐English**](https://github.com/shibing624/open-o1/blob/main/README.md)

<div align="center">
  <a href="https://github.com/shibing624/open-o1">
    <img src="https://raw.githubusercontent.com/shibing624/open-o1/main/docs/logo.png" height="150" alt="Logo">
  </a>
</div>

-----------------
# open-o1: Using GPT-4o with CoT to Create o1-like Reasoning Chains

This is an early prototype of using prompting strategies to improve the LLM's reasoning capabilities through o1-like reasoning chains. This allows the LLM to "think" and solve logical problems that usually otherwise stump leading models. 
Unlike openai-o1, all the reasoning tokens are shown, and the app uses an open source model.

open-o1 is experimental and being open sourced to help inspire the open source community to develop new strategies to produce o1-like reasoning. 
This experiment helps show the power of prompting reasoning in visualized steps, not a comparison to or full replication of o1, which uses different techniques. 
OpenAI's o1 is instead trained with large-scale reinforcement learning to reason using Chain of Thought, achieving state-of-the-art performance on complex PhD-level problems. 

open-o1 demonstrates the potential of prompting alone to overcome straightforward LLM logic issues like the Strawberry problem, allowing existing open source models to benefit from dynamic reasoning chains and an improved interface for exploring them.

### How it works

open-o1 powered by gpt-4o creates reasoning chains, in principle a dynamic Chain of Thought, that allows the LLM to "think" and solve some logical problems that usually otherwise stump leading models.

At each step, the LLM decides whether to continue or provide a final answer, with titles for clarity. The prompt includes tips such as exploring alternative answers and employing multiple methods to derive the solution.

This approach, combining Chain of Thought reasoning with the exploration of alternatives and self-awareness of limitations, significantly improves accuracy on problems like the Strawberry problem, achieving openai-o1 70% accuracy without additional training (compared to 30% without CoT prompts for gpt-4o).

### Demo

Web Demo: [https://o1.mulanai.com/](https://o1.mulanai.com/)

### Examples

> [!IMPORTANT]
> open-o1 is not perfect, but it can perform significantly better than LLMs out-of-the-box. From initial testing, open-o1 accurately solves simple logic problems 60-80% of the time that usually stump LLMs.

Prompt: How many 'r's are in the word 'strawberry'?

Result:

![Strawberry example](https://github.com/shibing624/open-o1/blob/main/docs/r3.png)
---

Prompt: Which is larger, .9 or .11?

Result:

![0.9 or 0.11 example](https://github.com/shibing624/open-o1/blob/main/docs/0.9.png)


### Quickstart

To use the Streamlit UI, follow these instructions:

```shell
pip3 install -r requirements.txt
export OPENAI_API_KEY=sk...
streamlit run app.py
```

### Prompting Strategy

The prompt is as follows:

```
You are an expert AI assistant that explains your reasoning step by step. For each step, provide a title that describes what you're doing in that step, along with the content. 
Decide if you need another step or if you're ready to give the final answer. Respond in JSON format with 'title', 'content', and 'next_action' (either 'continue' or 'final_answer') keys. USE AS MANY REASONING STEPS AS POSSIBLE. 
AT LEAST 3. BE AWARE OF YOUR LIMITATIONS AS AN LLM AND WHAT YOU CAN AND CANNOT DO. IN YOUR REASONING, INCLUDE EXPLORATION OF ALTERNATIVE ANSWERS. CONSIDER YOU MAY BE WRONG, AND IF YOU ARE WRONG IN YOUR REASONING, WHERE IT WOULD BE. 
FULLY TEST ALL OTHER POSSIBILITIES. YOU CAN BE WRONG. WHEN YOU SAY YOU ARE RE-EXAMINING, ACTUALLY RE-EXAMINE, AND USE ANOTHER APPROACH TO DO SO. DO NOT JUST SAY YOU ARE RE-EXAMINING. USE AT LEAST 3 METHODS TO DERIVE THE ANSWER. USE BEST PRACTICES.

Example of a valid JSON response:
{
    "title": "Identifying Key Information",
    "content": "To begin solving this problem, we need to carefully examine the given information and identify the crucial elements that will guide our solution process. This involves...",
    "next_action": "continue"
}
```

#### Breakdown
1. **Persona**: The assistant role is set as an expert AI.
2. **Step-by-Step Reasoning**: Each step must be titled and detailed, with prompts for possible continuation or finalization.
3. **JSON Formatting**: Responses are structured in JSON format for clarity.
4. **Best Practices**: Emphasized in all-caps for importance, including:
    - Using multiple reasoning steps.
    - Being aware of limitations.
    - Exploring alternative answers.
    - Re-examining and using another approach.
    - Using at least 3 methods to derive the answer.
    - Using best practices.

### Contact

- Issue(建议)
  ：[![GitHub issues](https://img.shields.io/github/issues/shibing624/agentica.svg)](https://github.com/shibing624/agentica/issues)
- 邮件我：xuming: xuming624@qq.com
- 微信我： 加我*微信号：xuming624, 备注：姓名-公司-NLP* 进NLP交流群。

<img src="https://github.com/shibing624/open-o1/blob/main/docs/wechat.jpeg" width="200" />


### Citation

如果你在研究中使用了`open-o1`，请按如下格式引用：

APA:

```
Xu, M. open-o1: Using GPT-4o with CoT to Create O1-like Reasoning Chains (Version 0.0.1) [Computer software]. https://github.com/shibing624/open-o1
```

BibTeX:

```
@misc{Xu_o1,
  title={open-o1: Using GPT-4o with CoT to Create O1-like Reasoning Chains},
  author={Xu Ming},
  year={2024},
  howpublished={\url{https://github.com/shibing624/open-o1}},
}
```

### License

授权协议为 [The Apache License 2.0](/LICENSE)，可免费用做商业用途。请在产品说明中附加`agentica`的链接和授权协议。
### Contribute

项目代码还很粗糙，如果大家对代码有所改进，欢迎提交回本项目，在提交之前，注意以下两点：

- 在`tests`添加相应的单元测试
- 使用`python -m pytest`来运行所有单元测试，确保所有单测都是通过的

之后即可提交PR。

### Acknowledgements 

- [g1](https://github.com/bklieger-groq/g1)
- [openai-o1](https://openai.com/o1/)


Thanks for their great work!

