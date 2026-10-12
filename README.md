# VoiceStudio Telegram Bot 🤖🎙️

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Telegram Bot](https://img.shields.io/badge/Telegram-Bot-blue?logo=telegram)](https://t.me/your_bot?start=github)
[![VoiceStudio](https://img.shields.io/badge/Powered_by-VoiceStudio-764ABC)](https://github.com/debpalash/VoiceStudio)

---

## 🇨🇳 中文

### 为什么有这个项目

[VoiceStudio](https://github.com/debpalash/VoiceStudio) 是目前最强大的本地语音克隆与合成开源项目，但它的交互方式主要通过桌面应用或 API。本项目将 VoiceStudio 的能力带入 Telegram，让你在手机上轻松克隆声音、生成语音，而无需安装任何客户端。

> 这是一个 **生态附属项目**，所有核心语音能力均来自 VoiceStudio，本仓库仅提供 Telegram 机器人封装。请务必遵守主项目的 [AGPL-3.0 许可](https://github.com/debpalash/VoiceStudio/blob/main/LICENSE)。

### ✨ 特性

- 📲 **直接在 Telegram 中使用**：无需复杂设置，添加机器人即可使用
- 🎙️ **文本转语音**：发送文字，立即获得 VoiceStudio 合成的高质量语音
- 🧬 **声音克隆**：发送一段参考音频，机器人会帮您生成该音色的 TTS
- 🔌 **依赖本地 VoiceStudio 服务**：你需要有一个运行中的 VoiceStudio 实例（本地或服务器）
- ⚙️ **灵活配置**：支持自定义 API 地址、默认引擎等
- 🔒 **私密安全**：所有音频处理在你的机器上完成，不上传第三方

### 📦 安装

1. 克隆本仓库：
   ```bash
   git clone https://github.com/your-username/voicestudio-telegram-bot.git
   cd voicestudio-telegram-bot
   ```

2. 安装依赖（推荐使用虚拟环境）：
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Linux/macOS
   # .venv\Scripts\activate   # Windows
   pip install -e .
   ```

3. 配置环境变量（创建 `.env` 文件或直接设置）：
   ```dotenv
   TELEGRAM_TOKEN=your_telegram_bot_token
   VOICESTUDIO_API=http://localhost:5000/api   # VoiceStudio API 地址
   ```

4. 启动机器人：
   ```bash
   python -m voicestudio_telegram_bot.bot
   ```

### 🚀 快速上手

与机器人开始对话：
- 发送任意文字 → 获得合成的语音音频
- 发送 `.wav` / `.mp3` 语音消息 → 机器人将提取音色，并用该声音朗读后续文字
- 支持 `/start`, `/help` 等基本命令

代码示例（最小化调用 VoiceStudio API）：
```python
import requests
API = "http://localhost:5000/api"
text = "你好，世界！"
resp = requests.post(f"{API}/tts", json={"text": text})
with open("output.wav", "wb") as f:
    f.write(resp.content)
```

### 📁 项目结构

```
voicestudio-telegram-bot/
├── src/voicestudio_telegram_bot/
│   ├── __init__.py
│   └── bot.py          # 机器人主入口
├── pyproject.toml
├── LICENSE
└── README.md
```

### 🔗 与 VoiceStudio 的关系

- 本机器人 **完全依赖** VoiceStudio 的后端能力，需要您预先启动 VoiceStudio 服务（请参考[官方文档](https://github.com/debpalash/VoiceStudio#get-started)）。
- 机器人本身不含任何语音模型，仅转发请求与格式化响应。
- 由于 VoiceStudio 使用 AGPL-3.0 许可证，若您分发或修改本机器人，请遵守开源协议义务。
- 欢迎到主项目点星 🙏 [VoiceStudio](https://github.com/debpalash/VoiceStudio)

### 🗺️ Roadmap

- [ ] 支持多语言自动检测
- [ ] 管理多个 VoiceStudio 实例负载均衡
- [ ] 用户音色收藏与切换
- [ ] 支持更多音频格式
- [ ] 提供 Docker 一键部署

### 📄 License

本项目采用 [MIT License](LICENSE)。使用时请同时遵守 VoiceStudio 的 AGPL-3.0 协议。

---

## 🇬🇧 English

### Why this project

[VoiceStudio](https://github.com/debpalash/VoiceStudio) is the most powerful open-source voice cloning & synthesis system that runs fully locally. Its primary interface is a desktop app or an API. This project wraps VoiceStudio into a Telegram bot — clone voices and generate speech right from your chat app, no extra client needed.

> **This is an ecosystem companion repo.** All voice intelligence is powered by VoiceStudio. This repository only provides the Telegram integration. Please respect the [AGPL-3.0 license](https://github.com/debpalash/VoiceStudio/blob/main/LICENSE) of the upstream project.

### ✨ Features

- 📲 **Direct Telegram usage** – no complex setup, just talk to the bot
- 🎙️ **Text-to-Speech** – send text, get high-quality VoiceStudio audio
- 🧬 **Voice Cloning** – send a voice sample and the bot will clone the timbre
- 🔌 **Requires a running VoiceStudio server** – local or remote
- ⚙️ **Configurable** – custom API endpoint, default engine, etc.
- 🔒 **Private & secure** – audio stays on your own machine

### 📦 Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/voicestudio-telegram-bot.git
   cd voicestudio-telegram-bot
   ```

2. Install with pip (use a virtual environment):
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -e .
   ```

3. Set environment variables (create a `.env` file):
   ```dotenv
   TELEGRAM_TOKEN=your_telegram_bot_token
   VOICESTUDIO_API=http://localhost:5000/api
   ```

4. Run the bot:
   ```bash
   python -m voicestudio_telegram_bot.bot
   ```

### 🚀 Quick Start

Start chatting with the bot:
- Send any text → get a speech audio message back
- Send a `.wav` / `.mp3` voice message → the bot will extract the voice and use it for subsequent text
- Commands: `/start`, `/help`

Minimal code example calling VoiceStudio in Python:
```python
import requests
API = "http://localhost:5000/api"
text = "Hello, world!"
resp = requests.post(f"{API}/tts", json={"text": text})
with open("output.wav", "wb") as f:
    f.write(resp.content)
```

### 📁 Project structure

```
voicestudio-telegram-bot/
├── src/voicestudio_telegram_bot/
│   ├── __init__.py
│   └── bot.py
├── pyproject.toml
├── LICENSE
└── README.md
```

### 🔗 Relationship to VoiceStudio

- This bot **entirely depends** on a running VoiceStudio backend. Set it up first following the [official guide](https://github.com/debpalash/VoiceStudio#get-started).
- The bot contains no speech models; it merely forwards requests and formats responses.
- Because VoiceStudio is AGPL-3.0, distributing or modifying this bot may impose certain obligations. Please read its license.
- ⭐ If you like this, please give a star to the amazing [VoiceStudio](https://github.com/debpalash/VoiceStudio) project!

### 🗺️ Roadmap

- [ ] Automatic language detection
- [ ] Load balancing across multiple VoiceStudio instances
- [ ] Voice presets and favourites
- [ ] Support additional audio formats
- [ ] Docker Compose deployment

### 📄 License

This project is licensed under the [MIT License](LICENSE). When using it, you must also comply with VoiceStudio’s AGPL-3.0 license.
