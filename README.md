# PSRL MVP — Personal Secretary Runtime Layer

> 可 docker 一鍵啟動的私人秘書系統：記憶 + 任務 + 事件日誌

## 一鍵啟動

```bash
git clone https://github.com/leebaron/psrl-mvp
cd psrl-mvp
TELEGRAM_TOKEN=your_token docker compose up --build
```

三秒後：
- **API**: http://localhost:8000
- **Bot**: Telegram (task / remember / /tasks)

## API

| Method | Endpoint | 功能 |
|--------|----------|------|
| POST | `/task` | 建立任務 |
| GET | `/tasks` | 列出任務 |
| POST | `/task/{id}/done` | 完成任務 |
| POST | `/memory` | 儲存記憶 |
| GET | `/memory` | 查詢記憶 |
| GET | `/events` | 事件日誌 |
| GET | `/health` | 健康檢查 |

## 系統分層

```
Telegram Bot
  ↓
FastAPI (PSRL Core)
  ↓
SQLite (tasks + memory) + JSONL (events)
  ↓
Worker (background jobs)
```

## 產品邊界

✅ Telegram 操作 (task / remember)
✅ 任務 CRUD (SQLite)
✅ 記憶查詢 (SQLite)
✅ 事件日誌 (JSONL append-only)
✅ Docker 一鍵啟動

❌ CBLD (獨立工程層)
❌ Causal graph
❌ Policy optimizer
❌ AST scanning
