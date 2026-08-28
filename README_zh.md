<p align="center"><a href="README.md">English</a> | <b>简体中文</b></p>

<h1 align="center">ScriptProof</h1>

<p align="center">
  <b>开拍之前，先把事实查清楚。</b><br>
  剧本研究 · 证据账本 · 连续性检查 · 制片交接
</p>

<p align="center">
  <a href="#产品能力">产品能力</a> ·
  <a href="#工作流程">工作流程</a> ·
  <a href="#本地运行">本地运行</a> ·
  <a href="docs/COMPETITION_RULES.md">比赛约束</a>
</p>

---

![ScriptProof 界面](docs/assets/scriptproof-home.png)

## 产品能力

ScriptProof 把剧本草稿转化为一份带出处、可以直接交给编剧和制片团队的研究报告。它不是普通聊天机器人，也不会默认重写故事。

- 找出会影响年代准确性、安全、法律可信度、地点真实性和技术细节的关键事实。
- 通过 Parallel 实时搜索并保留可复核的来源链接。
- 标记得到支持、与资料矛盾、证据不足或需要更多上下文的陈述。
- 对照不同场景，发现人物知识、道具、时间和出入口等连续性问题。
- 为编剧、道具、服装、场景、声音、法律和安全部门生成具体修改动作。

![ScriptProof 报告](docs/assets/scriptproof-report.png)

## 工作流程

```text
剧本文本 + 制作背景
        ↓
剧本分析 Agent：提取待核查事实和连续性候选
        ↓
证据研究 Agent：调用 Parallel 搜索并生成引用
        ↓
故事编辑 Agent：输出结构化修改与制片交接报告
```

三个 Agent 由 Google ADK 编排，模型使用 Gemini 3.5 Flash。Parallel 官方 `parallel-google-adk` 包提供搜索、网页提取和调用追踪。

## 本地运行

需要 Python 3.12、已启用 Vertex AI 的 Google Cloud 项目，以及 Parallel API Key。

```bash
cp .env.example .env
uv sync --extra dev
gcloud auth application-default login
uv run flask --app main run --port 8080
```

测试：

```bash
uv run ruff check .
uv run pytest --cov=scriptproof --cov-report=term-missing -q
```

## 比赛

ScriptProof 是为 [Agentic Cinema](https://agentic-cinema.devpost.com/) 的 Parallel 赛道新建的独立项目。AI 与 Agent 能力只使用 Google Cloud，Parallel Search 在生产流程中被真实调用。

## License

MIT License，详见 [LICENSE](LICENSE)。

**作者：** Simon 林 · X [@linsizhen](https://x.com/linsizhen) · 邮箱：[simonlin0423@gmail.com](mailto:simonlin0423@gmail.com)

## 赞赏

<p align="center">
  <a href="https://buymeacoffee.com/simonlin1212"><img src="./assets/bmc-qr.png" width="180" alt="Buy Me a Coffee"></a>
</p>
