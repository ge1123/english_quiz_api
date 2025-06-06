# 🧠 English Word Quiz API

使用 [FastAPI](https://fastapi.tiangolo.com/) 建立的英文字彙練習 API，並透過 [Poetry](https://python-poetry.org/) 管理專案依賴與虛擬環境。

---

## 📦 環境建置與啟動方式

### ✅ 安裝 Poetry（如果尚未安裝）

建議使用 [`pipx`](https://pypa.github.io/pipx/)：

```bash
    pipx install poetry
```

或使用官方安裝方式（PowerShell）：

```powershell
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -
```

---

### ✅ 安裝 `poetry shell` 插件（只需一次）

```bash
    poetry self add poetry-plugin-shell
```

---

### ✅ 初始化專案（已有 `pyproject.toml` 可略過）

```bash
    poetry init
```

---

### ✅ 安裝專案依賴

```bash
    poetry install
```

---

### ✅ 進入虛擬環境（每次開發前）

```bash
    poetry shell
```

或使用傳統方式（若有手動建立 `.venv`）：

```powershell
.\venv\Scripts\Activate.ps1
```

---

## 🚀 執行 FastAPI 開發伺服器

```bash
    uvicorn main:app --reload
```

---

## 🔍 API 測試與文件

- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

---

## 🧹 開發建議工具（自動格式化 / Import 排序）

專案推薦使用以下工具搭配開發：

### ✅ 安裝開發依賴（若尚未安裝）

```bash
    poetry add --dev black isort
```

### ✅ 常用格式化指令

```bash
    poetry run black .
    poetry run isort .
```

### ✅ 推薦的 `pyproject.toml` 設定

```toml
[tool.black]
line-length = 100
target-version = ['py311']

[tool.isort]
profile = "black"
line_length = 100
```

你也可以在 PyCharm 中透過 File Watcher 設定儲存時自動格式化。

## 🎁 Bonus：匯出 requirements.txt（for pip 使用）

### ✅ 安裝 `poetry-plugin-export`（只需一次）

```bash
    poetry self add poetry-plugin-export
```

---

### ✅ 匯出 `requirements.txt`

```bash
    poetry export -f requirements.txt --output requirements.txt --without-hashes
```

這會將目前 `pyproject.toml` 中定義的套件（不含 hash）匯出成 `requirements.txt`，可供部署或在非 Poetry 環境中使用：

```bash
    pip install -r requirements.txt
```

---

📌 建議在 CI/CD 或部署腳本中自動執行 `poetry export`，確保 pip 環境能正確對應 Poetry 專案。
---

## 📁 專案結構建議

```
english_word/
├── app/
│   ├── main.py              # FastAPI 入口
│   ├── models/              # Pydantic 資料模型
│   └── services/            # 商業邏輯處理
├── .venv/                   # Poetry 虛擬環境（若使用 in-project 模式）
├── pyproject.toml           # Poetry 設定檔
├── README.md
└── requirements.txt         # 可選：相容 pip 環境
```

---

## 📜 授權

MIT License © 2025 
