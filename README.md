# LangChain Practice

个人 LangChain 学习练习，按章节保存示例代码，每日进度见 [LEARNING_LOG.md](LEARNING_LOG.md)。

## 当前练习

- `dm01_LangChain_Version.py`：输出当前安装的 LangChain 版本。
- `chapter_2/dm01_model_init_online .py`：加载 `.env`，初始化 `ChatDeepSeek` 并调用模型。
- `requirements.txt`：现有学习环境依赖清单，包含后续练习可能使用的组件。

## 本地运行

在已安装 Python 的环境中执行以下 PowerShell 命令：

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
Copy-Item .env.example .env
```

如果已有 `.env`，跳过复制步骤，保留原配置。将 `.env` 中的占位值替换为自己的 API Key；使用自定义服务时，按服务要求配置连接地址。`.env` 已加入 Git 忽略规则。

```powershell
.\.venv\Scripts\python.exe dm01_LangChain_Version.py
.\.venv\Scripts\python.exe "chapter_2/dm01_model_init_online .py"
```

在线调用需要可用的 API Key 和网络，可能产生服务费用。当前代码使用 `deepseek-flash`，运行前请确认自己的服务支持该模型名称；尚未在本次整理中验证在线调用。
