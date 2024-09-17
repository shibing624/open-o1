[**🇨🇳中文**](https://github.com/shibing624/open-o1/blob/main/README_ZH.md) | [**🌐English**](https://github.com/shibing624/open-o1/blob/main/README.md)

<div align="center">
  <a href="https://github.com/shibing624/open-o1">
    <img src="https://raw.githubusercontent.com/shibing624/open-o1/main/docs/logo.png" height="150" alt="Logo">
  </a>
</div>

-----------------
# open-o1: Using GPT-4o with CoT to Create o1-like Reasoning Chains

这是一个早期的原型，旨在通过提示策略提高 LLM 的推理能力，创建类似 openai-o1 的推理链。这使得 LLM 可以“思考”和解决更复杂的逻辑推理问题。与 OpenAI 的 o1 不同，所有的推理过程都是公开，并且代码开源。

open-o1 仍处于实验阶段，并被开源出来，以激发开源社区开发新的策略来生成类 o1 的推理。这项实验展示了通过可视化步骤提示推理的力量，而不是对 o1 的比较或完全复制，后者使用了不同的技术。
OpenAI 的 o1 是通过大规模强化学习训练来使用思维链进行推理，能够在复杂的博士级问题上实现最先进的性能。

open-o1 展示了仅通过提示就能克服诸如草莓问题等简单逻辑问题的潜力，使现有开源模型能够从动态推理链和改进的探索界面中受益。

### 工作原理

使用 GPT-4o 的 open-o1 创建了推理链，本质上是一个动态的思维链，使 LLM 可以“思考”并解决复杂的逻辑问题。

在每一步，LLM 决定是继续下一步还是提供最终答案，并且每步都有清晰的标题。提示还包括一些建议，例如探索替代答案和使用多种方法来推导解决方案。

这种方法将思维链推理与探讨替代方案和自我意识结合起来，显著提高了诸如草莓问题等问题的准确性，在无需额外训练的情况下达到了约 70% 的准确率（相比之下，不提示的情况下 GPT-4 的准确率仅为 30%）。

### 示例

> [!重要]
> open-o1 并不完美，但它能比现成的 LLM 表现显著更好。从初步测试来看，open-o1 在通常让 LLM 难倒的简单逻辑问题上准确解决了 60-80% 的问题。

##### 草莓中有多少个 R？
提示：草莓中有多少个 R？

结果：

![草莓示例](https://github.com/shibing624/open-o1/blob/main/docs/r3.png)
---

提示：0.9 和 0.11 哪个更大？

结果：

![0.9 或 0.11 示例](https://github.com/shibing624/open-o1/blob/main/docs/0.9.png)


### 快速入门

要使用 Streamlit UI，请按照以下指示操作：

```shell
pip3 install -r requirements.txt
export OPENAI_API_KEY=sk...
streamlit run app.py
```

### 提示策略

提示如下：

```
你是一个专家 AI 助手，按步骤解释你的推理过程。每一步提供一个描述你在该步骤中所做内容的标题以及具体内容。决定是否需要进一步的步骤或给出最终答案。
以 JSON 格式回复，包含 'title'（标题）、'content'（内容）和 'next_action'（继续或最终答案）键。尽可能使用尽多的推理步骤，至少 3 步。
要意识到你作为 LLM 的局限性以及你能做和不能做的事情。在你的推理中，包含对替代答案的探索。考虑到你可能是错的，如果你的推理中出错，错在哪里。
全面测试所有其他可能性。你可以是错的。当你说在重新审视时，实际上要重新审视，并使用另一种方法来进行。不要仅仅说你在重新审视。使用至少 3 种方法来推导答案。遵循最佳实践。

有效的 JSON 回复示例：
{
    "title": "识别关键信息",
    "content": "为了开始解决这个问题，我们需要仔细检查给定的信息，并识别出将指导我们解决过程的关键要素。这涉及...",
    "next_action": "继续"
}
```

#### 细目说明

1. **角色设定**：将助手角色设定为专家 AI。
2. **逐步推理**：每一步都必须有标题和详细内容，并且有提示是否继续或提供最终答案。
3. **JSON 格式**：为清晰起见，回复以 JSON 格式结构化。
4. **最佳实践**：以全大写强调其重要性，包括：
    - 使用多个推理步骤。
    - 了解自身局限。
    - 探索替代答案。
    - 重新审视并使用另一种方法。
    - 使用至少 3 种方法来推导答案。
    - 遵循最佳实践。


### Contact

- Issue(建议)
  ：[![GitHub issues](https://img.shields.io/github/issues/shibing624/agentica.svg)](https://github.com/shibing624/agentica/issues)
- 邮件我：xuming: xuming624@qq.com
- 微信我： 加我*微信号：xuming624, 备注：姓名-公司-NLP* 进NLP交流群。

<img src="https://github.com/shibing624/open-o1/blob/main/docs/wechat.jpeg" width="200" />

<img src="https://github.com/shibing624/open-o1/blob/main/docs/wechat_group.jpg" width="200" />


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

