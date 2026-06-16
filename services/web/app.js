const API = "";

async function loadTasks() {
  const res = await fetch(`${API}/task/`);
  const data = await res.json();
  const list = document.getElementById("task-list");
  list.innerHTML = (data.tasks || []).map(t => `
    <div class="task ${t.status === 'done' ? 'done' : ''}">
      <span class="task-text">${t.content}</span>
      <span class="task-status">${t.status === 'done' ? '✅' : '⬜'}</span>
    </div>
  `).join("");
}

async function addTask() {
  const input = document.getElementById("task-input");
  await fetch(`${API}/task/`, { method: "POST", headers: {"Content-Type":"application/x-www-form-urlencoded"}, body: `content=${encodeURIComponent(input.value)}` });
  input.value = "";
  loadTasks();
}

async function searchMemory() {
  const query = document.getElementById("mem-input").value;
  const res = await fetch(`${API}/memory/?query=${encodeURIComponent(query)}`);
  const data = await res.json();
  document.getElementById("mem-results").innerHTML = (data.memories || []).map(m => `
    <div class="mem-item">${m.content}</div>
  `).join("");
}

async function sendChat() {
  const text = document.getElementById("quick-input").value;
  const res = await fetch(`${API}/task/intent`, {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({text})
  });
  const data = await res.json();
  document.getElementById("chat-result").innerText = `🧠 ${data.intent}: ${data.content.slice(0,80)}`;
}

loadTasks();
