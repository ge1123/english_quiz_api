# 🧠 English Word Quiz API

使用 [FastAPI](https://fastapi.tiangolo.com/) 開發的英文字彙練習系統，結合 [Poetry](https://python-poetry.org/) 管理專案依賴與虛擬環境，具備清晰的模組分層架構，方便維護與擴充。

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

### ✅ 安裝專案依賴

```bash
    poetry install
```

---

### ✅ 進入虛擬環境（每次開發前）

```bash
    poetry shell
```

或（若使用 in-project `.venv`）：

```powershell
.\.venv\Scripts\Activate.ps1
```

---

### ✅ 啟動 FastAPI 應用（使用 `run.py`）

```bash
    python scripts/run.py
```

---

## 🔍 API 測試與文件

- Swagger UI: http://127.0.0.1:8019/docs
- ReDoc: http://127.0.0.1:8019/redoc

---

## 🧹 開發建議工具（格式化 / import 排序）

專案推薦使用以下開發工具：

### ✅ 安裝開發依賴（如尚未安裝）

```bash
    poetry add --dev black isort
```

### ✅ 常用格式化指令

```bash
    poetry run black .
    poetry run isort .
```

### ✅ 推薦 pyproject.toml 設定

```toml
[tool.black]
line-length = 100
target-version = ['py311']

[tool.isort]
profile = "black"
line_length = 100
```

---

## 📁 專案結構（依照 FastAPI 生態圈標準分層）

```
english_word/
├── app/
│   ├── main.py                # FastAPI 啟動點
│   ├── api/                   # 路由模組（包含 routes 與 deps）
│   ├── core/                  # 設定與環境讀取（如 config.py）
│   ├── db/                    # 資料庫 session 設定
│   ├── crud/                  # CRUD 操作（對應資料表）
│   ├── models/                # SQLAlchemy ORM 模型
│   ├── schemas/               # Pydantic schema 定義
│   ├── services/              # 商業邏輯服務層
│   ├── dependencies/          # Depends 注入來源（db, service, crud）
│   └── utils/                 # 工具類函式（如 JWT）
├── scripts/
│   ├── run.py                 # 專案啟動腳本
│   └── create_tables.py       # 建立資料表用
├── test/                      # 測試模組
├── .env                       # 環境變數設定檔
├── .gitignore
├── poetry.lock
├── pyproject.toml
├── README.md
└── requirements.txt
```

---

## 🎁 Bonus：匯出 requirements.txt（for pip 使用）

### ✅ 安裝 export plugin（只需一次）

```bash
    poetry self add poetry-plugin-export
```

### ✅ 匯出 `requirements.txt`

```bash
    poetry export -f requirements.txt --output requirements.txt --without-hashes
```

這可讓部署或 CI/CD 環境使用：

```bash
    pip install -r requirements.txt
```

---

## 📜 授權

MIT License © 2025
