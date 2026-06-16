"""services/web/ui.py — Web UI server (FastAPI route serving static HTML)."""

from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
def index():
    return HTMLResponse(INDEX_HTML)


@router.get("/app.js", response_class=HTMLResponse)
def app_js():
    with open("services/web/app.js") as f:
        return HTMLResponse(f.read())


@router.get("/style.css", response_class=HTMLResponse)
def style_css():
    with open("services/web/style.css") as f:
        return HTMLResponse(f.read())


INDEX_HTML = """<!DOCTYPE html>
<html lang="zh-TW">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>PSRL 私人秘書</title>
  <link rel="stylesheet" href="/style.css">
</head>
<body>
  <div id="app">
    <header>
      <h1>🧠 PSRL 私人秘書</h1>
      <p class="subtitle">今天要做的事</p>
    </header>

    <div class="card">
      <h2>📋 任務</h2>
      <div id="task-input-row">
        <input id="task-input" placeholder="新增任務…" onkeydown="if(event.key==='Enter')addTask()">
        <button onclick="addTask()">＋</button>
      </div>
      <div id="task-list"></div>
    </div>

    <div class="card">
      <h2>🧠 記憶</h2>
      <input id="mem-input" placeholder="搜尋記憶…" onkeydown="if(event.key==='Enter')searchMemory()">
      <div id="mem-results"></div>
    </div>

    <div class="card">
      <h2>💬 快速輸入</h2>
      <textarea id="quick-input" placeholder="說點什麼… (會自動分類)"></textarea>
      <button onclick="sendChat()" style="margin-top:8px">送出</button>
      <div id="chat-result"></div>
    </div>
  </div>
  <script src="/app.js"></script>
</body>
</html>"""
