const state = {
  token: localStorage.getItem("ls_token"),
  user: JSON.parse(localStorage.getItem("ls_user") || "null"),
  view: "overview",
  subjects: [],
  chat: {
    conversationId: null,
    conversations: [],
    isSending: false
  }
};

const apiBase = window.LEARNSPHERE_API_BASE
  || (window.location.hostname.endsWith("github.io") ? "" : "/api");

const $ = (selector) => document.querySelector(selector);
const $$ = (selector) => Array.from(document.querySelectorAll(selector));
const esc = (value) => String(value ?? "").replace(/[&<>"]/g, (char) => ({
  "&": "&amp;",
  "<": "&lt;",
  ">": "&gt;",
  '"': "&quot;"
}[char]));

function detailButton(id, content) {
  return `<button class="note-row detail-trigger" type="button" data-detail-id="${id}">${content}</button>`;
}

function bindDetailButtons(records, describe) {
  $$('[data-detail-id]').forEach((button) => {
    button.onclick = () => {
      const record = records.find((item) => String(item.id) === button.dataset.detailId);
      if (record) showDetail(describe(record));
    };
  });
}

function showDetail({title, fields}) {
  const existing = $("#detail-modal");
  if (existing) existing.remove();
  const modal = document.createElement("div");
  modal.id = "detail-modal";
  modal.className = "detail-modal";
  modal.innerHTML = `<section class="detail-card" role="dialog" aria-modal="true" aria-label="${esc(title)}"><div class="detail-heading"><h2>${esc(title)}</h2><button class="text-button" type="button" data-close-detail>Close</button></div><dl>${fields.map(([label, value]) => `<div><dt>${esc(label)}</dt><dd>${esc(value || "Not provided")}</dd></div>`).join("")}</dl></section>`;
  modal.onclick = (event) => { if (event.target === modal) modal.remove(); };
  document.body.appendChild(modal);
  modal.querySelector("[data-close-detail]").onclick = () => modal.remove();
}

function taskDetails(task) {
  return {title: task.title, fields: [["Subject", task.subject_name || "General"], ["Target date", task.due_date || "No date"], ["Focus time", `${task.planned_minutes} minutes`], ["Status", task.status], ["Description", task.description], ["Created", task.created_at]]};
}

const navItems = [
  ["overview", "Overview"],
  ["planner", "Study planner"],
  ["knowledge", "Knowledge base"],
  ["syllabus", "Syllabus"],
  ["pyq", "Previous questions"],
  ["timetable", "Timetable"],
  ["practice", "Practice lab"],
  ["insights", "Learning insights"],
  ["diary", "Daily diary"]
];

const titles = {
  overview: "Welcome,",
  planner: "Study planner",
  knowledge: "Knowledge base",
  syllabus: "Syllabus",
  pyq: "Previous-year questions",
  timetable: "Timetable",
  practice: "Practice lab",
  insights: "Learning insights",
  diary: "Daily diary",
  integrations: "AI connections"
};

function toast(message) {
  const el = $("#toast");
  el.textContent = message;
  el.classList.add("show");
  window.setTimeout(() => el.classList.remove("show"), 2800);
}

async function api(path, options = {}) {
  if (!apiBase) {
    throw new Error("Sign-in needs the LearnSphere API deployment. Use the local app until the production backend URL is configured.");
  }
  const headers = options.body instanceof FormData ? {} : {"Content-Type": "application/json"};
  if (state.token) headers.Authorization = `Bearer ${state.token}`;
  let res;
  try {
    res = await fetch(`${apiBase}${path}`, {...options, headers: {...headers, ...(options.headers || {})}});
  } catch {
    throw new Error("The LearnSphere API is not online yet. Deploy the Render service, then try again.");
  }
  const data = await res.json().catch(() => ({}));
  if (!res.ok) {
    if (res.status === 401 && state.token) logout();
    if (res.status === 405 && path.includes("study-coach")) {
      const methodErr = new Error("The Study Coach request method is not supported. Please reload the page and try again.");
      methodErr.retryable = false;
      throw methodErr;
    }
      const errMsg = data.error || data.message || "Something went wrong.";
      const err = new Error(errMsg);
      err.retryable = Boolean(data.retryable);
      err.code = data.code || data.error_code || null;
      throw err;
  }
  return data;
}

async function publicApi(path, options = {}) {
  const data = await api(path, options);
  return data.data ?? data;
}

function setAuth(mode = "login") {
  $("#auth-form").reset();
  $("#auth").classList.remove("hidden");
  $("#name-field").style.display = mode === "register" ? "grid" : "none";
  $("#auth-title").textContent = mode === "register" ? "Build your study workspace." : "Welcome back.";
  $("#auth-copy").textContent = mode === "register"
    ? "Start with sample subjects and a calm academic dashboard."
    : "Continue your study rhythm.";
  $("#auth-form").dataset.mode = mode;
  $("#auth-toggle").textContent = mode === "register" ? "Already have an account? Sign in" : "New here? Create an account";
}

function logout() {
  localStorage.removeItem("ls_token");
  localStorage.removeItem("ls_user");
  state.token = null;
  state.user = null;
  $("#app").classList.add("hidden");
  $("#landing").classList.remove("hidden");
}

function buildNavigation() {
  const nav = $("#side-nav");
  nav.innerHTML = navItems.map(([view, label]) => (
    `<button data-view="${view}" class="${state.view === view ? "active" : ""}">${label}</button>`
  )).join("");
  $$("[data-view]").forEach((button) => {
    button.onclick = () => {
      state.view = button.dataset.view;
      $$("[data-view]").forEach((item) => item.classList.toggle("active", item.dataset.view === state.view));
      render();
    };
  });
}

async function start() {
  if (!state.token) return;
  $("#landing").classList.add("hidden");
  $("#app").classList.remove("hidden");
  buildNavigation();
  try {
    state.user = await api("/me");
    localStorage.setItem("ls_user", JSON.stringify(state.user));
    $("#profile-btn").textContent = state.user.name.slice(0, 1).toUpperCase();
    $("#today").textContent = new Date().toLocaleDateString(undefined, {
      weekday: "long",
      month: "long",
      day: "numeric"
    });
    await render();
  } catch (error) {
    toast(error.message);
  }
}

function setHeader() {
  const title = titles[state.view] || "Workspace";
  $("#view-title").innerHTML = state.view === "overview"
    ? `${title} ${esc((state.user?.name || "Student").split(" ")[0])}.`
    : esc(title);
}

async function render() {
  setHeader();
  const view = $("#view");
  view.innerHTML = '<div class="empty">Loading your workspace...</div>';
  try {
    const renderer = {
      overview,
      planner,
      knowledge,
      syllabus,
      pyq,
      timetable,
      practice,
      insights,
      diary,
      integrations
    }[state.view];
    await renderer(view);
  } catch (error) {
    view.innerHTML = `<section class="card"><h2>We could not load this view</h2><p class="empty">${esc(error.message)}</p></section>`;
  }
}

async function overview(view) {
  const d = await api("/dashboard");
  await loadStudyCoachConversations();
  const conversationOptions = state.chat.conversations.length
    ? [`<option value="">New conversation</option>`, ...state.chat.conversations.map((conversation) => (`<option value="${conversation.id}">${esc(conversation.title)}</option>`))].join("")
    : '<option value="">New conversation</option>';

  view.innerHTML = `
    <div class="metrics">
      <div class="metric"><label>Subjects</label><b>${d.metrics.subjects}</b><small>Active learning map</small></div>
      <div class="metric"><label>Focus this week</label><b>${d.metrics.focus_minutes}<small> min</small></b><small>Recorded work</small></div>
      <div class="metric"><label>Consistency</label><b>${d.metrics.consistency}<small>%</small></b><small>Against planned load</small></div>
      <div class="metric"><label>Completed</label><b>${d.metrics.tasks_completed}</b><small>Finished tasks</small></div>
    </div>
    <div class="dashboard-grid">
      <section class="card">
        <h2>Next actions</h2>
        ${d.tasks.length ? d.tasks.map(taskRow).join("") : '<p class="empty">Your planner is clear. Add one focused task.</p>'}
      </section>
      <section class="card">
        <h2>Subjects in motion</h2>
        ${d.subjects.map((s) => `<div class="subject-pill"><span class="dot" style="background:${esc(s.color || "#2563eb")};display:inline-block;margin-right:8px"></span>${esc(s.name)} <small style="float:right">${s.task_count} open</small></div>`).join("")}
        <button class="text-button" data-go="planner">Add a subject</button>
      </section>
    </div>
    <div class="dashboard-grid">
      <section class="card">
        <h2>Study coach</h2>
        <div class="chat-toolbar"><select id="chat-conversation-select">${conversationOptions}</select><button id="chat-new-conversation" class="text-button">New</button><button id="chat-delete-conversation" class="text-button danger" type="button">Delete</button></div>
        <div id="chat-log" class="chat-log"></div>
        <form id="chat-form" class="chat-form"><textarea name="message" rows="2" placeholder="Ask your study coach..."></textarea><button class="button primary">Send</button></form>
      </section>
      <section class="card">
        <h2>Today reflection</h2>
        <p class="empty">Close the loop with a short diary entry after one meaningful study block.</p>
        <button class="button primary" data-go="diary">Open diary</button>
      </section>
    </div>`;
  bindDoneButtons();
  bindTaskDetails(d.tasks);
  bindGoButtons();
  $("#chat-form").onsubmit = chatSubmit;
  $("#chat-form").message.onkeydown = chatKeyDown;
  $("#chat-conversation-select").onchange = (event) => loadStudyCoachConversation(event.target.value ? Number(event.target.value) : null);
  $("#chat-new-conversation").onclick = () => loadStudyCoachConversation(null);
  $("#chat-delete-conversation").onclick = deleteStudyCoachConversation;
  loadStudyCoachConversation(state.chat.conversationId);
}

function taskRow(t) {
  return `<div class="task-row">
    <span class="dot" style="background:${esc(t.color || "#2563eb")}"></span>
    <button class="row-grow task-detail-trigger" type="button" data-detail-id="${t.id}"><b>${esc(t.title)}</b><small>${esc(t.subject_name || "General")} / ${esc(t.planned_minutes)} min / ${esc(t.due_date || "No date")}</small></button>
    <button class="done" data-done="${t.id}" title="Mark done">Done</button>
  </div>`;
}

function bindDoneButtons() {
  $$("[data-done]").forEach((button) => {
    button.onclick = async () => {
      await api("/tasks", {method: "PATCH", body: JSON.stringify({id: button.dataset.done, status: "done"})});
      toast("Task completed");
      render();
    };
  });
}

function bindTaskDetails(tasks) {
  bindDetailButtons(tasks, taskDetails);
}

function bindGoButtons() {
  $$('[data-go]').forEach((button) => {
    button.onclick = () => {
      state.view = button.dataset.go;
      buildNavigation();
      render();
    };
  });
}

function renderChatLog(messages) {
  const log = $("#chat-log");
  if (!log) return;
  log.innerHTML = messages.length
    ? messages.map((item) => `<div class="bubble ${item.role === "assistant" ? "coach" : "student"}">${esc(item.content)}</div>`).join("")
    : `<div class="bubble coach">Ask for a revision plan, a concept breakdown, or a better next study move.</div>`;
  bindRetryButtons();
  log.scrollTop = log.scrollHeight;
}

function setChatLoading(isLoading) {
  const form = $("#chat-form");
  if (!form) return;
  const button = form.querySelector("button");
  const input = form.querySelector("textarea");
  if (button) button.disabled = isLoading;
  if (input) input.disabled = isLoading;
  if (button) button.textContent = isLoading ? "Thinking..." : "Send";
}

function chatKeyDown(event) {
  if (event.key === "Enter" && !event.shiftKey) {
    event.preventDefault();
    event.currentTarget.form.requestSubmit();
  }
}

async function loadStudyCoachConversations() {
  try {
    const d = await api("/study-coach/conversations");
    state.chat.conversations = d.conversations || [];
  } catch {
    state.chat.conversations = [];
  }
}

function renderConversationOptions() {
  const select = $("#chat-conversation-select");
  if (!select) return;
  select.innerHTML = state.chat.conversations.length
    ? [`<option value="">New conversation</option>`, ...state.chat.conversations.map((conversation) => (`<option value="${conversation.id}" ${conversation.id === state.chat.conversationId ? "selected" : ""}>${esc(conversation.title)}</option>`))].join("")
    : '<option value="">New conversation</option>';
}

async function loadStudyCoachConversation(conversationId) {
  if (!conversationId) {
    state.chat.conversationId = null;
    renderChatLog([]);
    renderConversationOptions();
    return;
  }
  try {
    const d = await api(`/study-coach/conversations/${conversationId}`);
    state.chat.conversationId = conversationId;
    renderChatLog(d.messages || []);
    renderConversationOptions();
  } catch (error) {
    toast(error.message);
    renderChatLog([]);
  }
}

async function deleteStudyCoachConversation() {
  if (!state.chat.conversationId || state.chat.isSending) return;
  try {
    await api(`/study-coach/conversations/${state.chat.conversationId}`, {method: "DELETE"});
    state.chat.conversationId = null;
    await loadStudyCoachConversations();
    renderConversationOptions();
    renderChatLog([]);
    toast("Conversation deleted");
  } catch (error) {
    toast(error.message);
  }
}

function bindRetryButtons() {
  $$("[data-retry-message]").forEach((button) => {
    button.onclick = () => sendChatMessage(button.dataset.retryMessage);
  });
}

async function chatSubmit(event) {
  event.preventDefault();
  const input = event.currentTarget.message;
  const message = input.value.trim();
  if (!message) return;
  input.value = "";
  await sendChatMessage(message);
}

async function sendChatMessage(message) {
  if (state.chat.isSending) return;
  if (!message) return;
  const log = $("#chat-log");
  state.chat.isSending = true;
  setChatLoading(true);
  log.insertAdjacentHTML("beforeend", `<div class="bubble student">${esc(message)}</div>`);
  const pending = document.createElement("div");
  pending.className = "bubble coach loading";
  pending.textContent = "Thinking...";
  log.appendChild(pending);
  log.scrollTop = log.scrollHeight;
  try {
    const d = await api("/study-coach/chat", {method: "POST", body: JSON.stringify({message, conversation_id: state.chat.conversationId})});
    state.chat.conversationId = d.conversation_id || state.chat.conversationId;
    if (pending.parentNode) pending.remove();
    log.insertAdjacentHTML("beforeend", `<div class="bubble coach">${esc(d.message.content)}</div>`);
    log.scrollTop = log.scrollHeight;
    await loadStudyCoachConversations();
    renderConversationOptions();
  } catch (error) {
    if (pending.parentNode) pending.remove();
    // If the backend marked this as retryable (transient provider error),
    // attempt one automatic retry after a short delay.
      if (error && error.code === "RESOURCE_EXHAUSTED") {
        const quotaMsg = "Study Coach: Gemini's project quota is exhausted. Wait for the quota reset or update quota/billing in Google AI Studio.";
        log.insertAdjacentHTML("beforeend", `<div class="bubble coach error">${esc(quotaMsg)} <button class="text-button" data-retry-message="${esc(message)}">Retry</button></div>`);
        bindRetryButtons();
        log.scrollTop = log.scrollHeight;
        toast(quotaMsg);
        return;
      } else if (error && error.retryable) {
      await new Promise((r) => setTimeout(r, 1500));
      try {
        const d = await api("/study-coach/chat", {method: "POST", body: JSON.stringify({message, conversation_id: state.chat.conversationId})});
        state.chat.conversationId = d.conversation_id || state.chat.conversationId;
        log.insertAdjacentHTML("beforeend", `<div class="bubble coach">${esc(d.message.content)}</div>`);
        await loadStudyCoachConversations();
        renderConversationOptions();
        log.scrollTop = log.scrollHeight;
        bindRetryButtons();
        return;
      } catch (err2) {
        // fall through to show a friendly retry UI
      }
    }

    const friendly = (error && error.retryable)
      ? "AI service is temporarily busy. Please try again in a few moments."
      : `Gemini could not answer: ${esc(error.message)}`;
    log.insertAdjacentHTML("beforeend", `<div class="bubble coach error">${esc(friendly)} <button class="text-button" data-retry-message="${esc(message)}">Retry</button></div>`);
    bindRetryButtons();
    log.scrollTop = log.scrollHeight;
    toast(friendly);
  } finally {
    state.chat.isSending = false;
    setChatLoading(false);
  }
}

async function planner(view) {
  state.subjects = await api("/subjects");
  const tasks = await api("/tasks");
  const opts = subjectOptions();
  view.innerHTML = `
    ${viewHead("Make the next move obvious", "Plan focused work.")}
    <div class="split">
      <section class="card"><h2>Add a study task</h2>
        <form id="task-form" class="form-grid">
          <label class="full">Task title<input name="title" required placeholder="Practice linked-list questions"></label>
          <label class="full">Description<textarea name="description" rows="3" placeholder="What should you complete or revise?"></textarea></label>
          <label>Subject<select name="subject_id"><option value="">General</option>${opts}</select></label>
          <label>Focus minutes<input name="planned_minutes" type="number" min="5" max="600" value="45"></label>
          <label class="full">Target date<input name="due_date" type="date"></label>
          <button class="button primary full">Add to planner</button>
        </form>
      </section>
      <section class="card"><h2>Add a subject</h2>
        <form id="subject-form" class="form-grid">
          <label class="full">Subject name<input name="name" required placeholder="Operating Systems"></label>
          <label class="full">Purpose<input name="description" placeholder="What are you working toward?"></label>
          <button class="button primary full">Create subject</button>
        </form>
      </section>
    </div>
    <section class="card" style="margin-top:16px"><h2>Planned work</h2>${tasks.filter((t) => t.status !== "done").map(taskRow).join("") || '<p class="empty">No upcoming tasks yet.</p>'}</section>`;
  $("#task-form").onsubmit = async (event) => submitJson(event, "/tasks", "Task added");
  $("#subject-form").onsubmit = async (event) => submitJson(event, "/subjects", "Subject created");
  bindDoneButtons();
  bindTaskDetails(tasks);
}

function subjectOptions() {
  return state.subjects.map((s) => `<option value="${s.id}">${esc(s.name)}</option>`).join("");
}

async function submitJson(event, path, message) {
  event.preventDefault();
  await api(path, {method: "POST", body: JSON.stringify(Object.fromEntries(new FormData(event.currentTarget)))});
  toast(message);
  render();
}

function viewHead(kicker, title) {
  return `<div class="view-head"><div><p class="eyebrow">${esc(kicker)}</p><h2>${esc(title)}</h2></div></div>`;
}

async function knowledge(view) {
  const notes = await publicApi("/notes");
  view.innerHTML = `
    ${viewHead("Study material library", "Capture what matters.")}
    <div class="split">
      <section class="card"><h2>New note</h2>
        <form id="note-form" class="form-grid">
          <label class="full">Title<input name="title" required placeholder="Gradient descent"></label>
          <label>Subject<input name="subject" placeholder="Machine Learning"></label>
          <label>Topic<input name="topic" placeholder="Optimisation"></label>
          <label>Semester<input name="semester" type="number" min="1" max="12" value="6"></label>
          <label class="full">Description<input name="description" placeholder="Short summary"></label>
          <label class="full">Content<textarea name="content" rows="5" placeholder="Key concepts, questions, or next steps"></textarea></label>
          <button class="button primary full">Save note</button>
        </form>
      </section>
      <section class="card"><h2>Saved notes</h2>${notes.map((n) => `${detailButton(n.id, `<div class="row-grow"><b>${esc(n.title)}</b><small>${esc(n.subject || "General")} / Semester ${esc(n.semester || 1)} / ${esc(n.topic || "General")}</small></div>`) }`).join("") || '<p class="empty">Your saved notes will appear here.</p>'}</section>
    </div>`;
  $("#note-form").onsubmit = async (event) => {
    event.preventDefault();
    await publicApi("/notes", {method: "POST", body: JSON.stringify(Object.fromEntries(new FormData(event.currentTarget)))});
    toast("Note saved");
    render();
  };
  bindDetailButtons(notes, (n) => ({title: n.title, fields: [["Subject", n.subject], ["Topic", n.topic], ["Semester", n.semester], ["Description", n.description], ["Full content", n.content || n.body]]}));
}

async function syllabus(view) {
  const records = await publicApi("/syllabus");
  view.innerHTML = `
    ${viewHead("Course outline", "Know what to study.")}
    <div class="split">
      <section class="card"><h2>Add syllabus unit</h2>
        <form id="syllabus-form" class="form-grid">
          <label>Subject code<input name="subject_code" required placeholder="ML601"></label>
          <label>Subject name<input name="subject_name" required placeholder="Machine Learning"></label>
          <label>Semester<input name="semester" type="number" min="1" max="12" value="6"></label>
          <label>Unit<input name="unit" required placeholder="1"></label>
          <label class="full">Unit title<input name="unit_title" required placeholder="Introduction"></label>
          <label class="full">Topics<textarea name="topics" required rows="4" placeholder="Key topics in this unit"></textarea></label>
          <button class="button primary full">Save syllabus unit</button>
        </form>
      </section>
      <section class="card"><h2>Saved syllabus</h2>${records.map((x) => `${detailButton(x.id, `<div class="row-grow"><b>${esc(x.subject_name)} / Unit ${esc(x.unit)}: ${esc(x.unit_title)}</b><small>Semester ${esc(x.semester)} / ${esc(x.topics)}</small></div>`) }`).join("") || '<p class="empty">Add your first syllabus unit.</p>'}</section>
    </div>`;
  $("#syllabus-form").onsubmit = async (event) => submitPublic(event, "/syllabus", "Syllabus unit saved");
  bindDetailButtons(records, (x) => ({title: `${x.subject_name} ? Unit ${x.unit}`, fields: [["Subject code", x.subject_code], ["Semester", x.semester], ["Unit title", x.unit_title], ["Topics and subtopics", x.topics], ["Description", x.description]]}));
}

async function pyq(view) {
  const records = await publicApi("/pyq");
  view.innerHTML = `
    ${viewHead("Exam practice", "Previous-year questions.")}
    <div class="split">
      <section class="card"><h2>Add question</h2>
        <form id="pyq-form" class="form-grid">
          <label>Subject<input name="subject" required placeholder="Machine Learning"></label>
          <label>Code<input name="subject_code" required placeholder="ML601"></label>
          <label>Semester<input name="semester" type="number" min="1" max="12" value="6"></label>
          <label>Exam year<input name="exam_year" type="number" value="2025"></label>
          <label class="full">Exam type<input name="exam_type" required placeholder="Final exam"></label>
          <label class="full">Question<textarea name="question" rows="4" placeholder="Write the question"></textarea></label>
          <button class="button primary full">Save question</button>
        </form>
      </section>
      <section class="card"><h2>Question bank</h2>${records.map((x) => `${detailButton(x.id, `<div class="row-grow"><b>${esc(x.subject)} / ${esc(x.exam_year)}</b><small>${esc(x.exam_type)} / ${esc(x.question || "PDF question paper attached")}</small></div>`) }`).join("") || '<p class="empty">Add a previous-year question to begin.</p>'}</section>
    </div>`;
  $("#pyq-form").onsubmit = async (event) => submitPublic(event, "/pyq", "Question saved");
  bindDetailButtons(records, (x) => ({title: `${x.subject} ? ${x.exam_year}`, fields: [["Subject code", x.subject_code], ["Semester", x.semester], ["Exam type", x.exam_type], ["Unit", x.unit], ["Marks", x.marks], ["Complete question", x.question], ["Attached file", x.file_url]]}));
}

async function timetable(view) {
  const records = await publicApi("/timetable");
  view.innerHTML = `
    ${viewHead("Weekly study map", "Timetable.")}
    <div class="split">
      <section class="card"><h2>Add class</h2>
        <form id="timetable-form" class="form-grid">
          <label>Day<select name="day">${["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"].map((d) => `<option>${d}</option>`).join("")}</select></label>
          <label>Semester<input name="semester" type="number" min="1" max="12" value="6"></label>
          <label>Subject<input name="subject" required placeholder="Machine Learning"></label>
          <label>Code<input name="subject_code" required placeholder="ML601"></label>
          <label>Start time<input name="start_time" type="time" required></label>
          <label>End time<input name="end_time" type="time" required></label>
          <label>Room<input name="room" placeholder="Lab 2"></label>
          <label>Faculty<input name="faculty" placeholder="Faculty name"></label>
          <button class="button primary full">Save class</button>
        </form>
      </section>
      <section class="card"><h2>Weekly timetable</h2>${records.map((x) => `${detailButton(x.id, `<div class="row-grow"><b>${esc(x.day)} / ${esc(x.subject)}</b><small>${esc(x.start_time)}-${esc(x.end_time)} / ${esc(x.room || "Room TBA")}</small></div>`) }`).join("") || '<p class="empty">Add your first timetable entry.</p>'}</section>
    </div>`;
  $("#timetable-form").onsubmit = async (event) => submitPublic(event, "/timetable", "Timetable entry saved");
  bindDetailButtons(records, (x) => ({title: `${x.day} ? ${x.subject}`, fields: [["Subject code", x.subject_code], ["Semester", x.semester], ["Start time", x.start_time], ["End time", x.end_time], ["Room", x.room], ["Faculty", x.faculty]]}));
}

async function submitPublic(event, path, message) {
  event.preventDefault();
  await publicApi(path, {method: "POST", body: JSON.stringify(Object.fromEntries(new FormData(event.currentTarget)))});
  toast(message);
  render();
}

async function practice(view) {
  const quizzes = await api("/quizzes");
  view.innerHTML = `
    ${viewHead("Active recall", "Practice until it feels clear.")}
    <div class="split">
      <section class="card"><h2>Generate a quick check</h2>
        <form id="quiz-form"><label>Topic<input name="topic" required placeholder="Binary search"></label><button class="button primary">Create 3-question quiz</button></form>
        <div id="quiz-area"></div>
      </section>
      <section class="card"><h2>Saved practice results</h2>${quizzes.map((q) => detailButton(q.id, `<div class="row-grow"><b>${esc(q.topic)}</b><small>${esc(q.score)} / ${esc(q.total)} correct</small></div>`)).join("") || '<p class="empty">Complete a quiz to build your saved practice record.</p>'}</section>
    </div>`;
  bindDetailButtons(quizzes, (q) => ({title: `${q.topic} practice result`, fields: [["Score", `${q.score} / ${q.total}`], ["Accuracy", `${Math.round((q.score / Math.max(q.total, 1)) * 100)}%`], ["Completed", q.created_at]]}));
  $("#quiz-form").onsubmit = async (event) => {
    event.preventDefault();
    const d = await api("/quizzes/generate", {method: "POST", body: JSON.stringify(Object.fromEntries(new FormData(event.currentTarget)))});
    $("#quiz-area").innerHTML = `<form id="answer-form">${d.questions.map((q, i) => `<div class="quiz-q"><p>${i + 1}. ${esc(q.question)}</p>${q.options.map((o, j) => `<label><input type="radio" required name="q${i}" value="${j}">${esc(o)}</label>`).join("")}</div>`).join("")}<button class="button primary">Save result</button></form>`;
    $("#answer-form").onsubmit = async (answerEvent) => {
      answerEvent.preventDefault();
      const form = new FormData(answerEvent.currentTarget);
      const score = d.questions.reduce((n, q, i) => n + (Number(form.get(`q${i}`)) === q.answer ? 1 : 0), 0);
      const result = await api("/quizzes/submit", {method: "POST", body: JSON.stringify({topic: d.topic, score, total: d.questions.length})});
      toast(`${score}/${d.questions.length} saved. ${result.feedback}`);
      render();
    };
  };
}
async function insights(view) {
  const [d, sessions, quizzes] = await Promise.all([api("/insights"), api("/study-sessions"), api("/quizzes")]);
  const totalMinutes = sessions.reduce((sum, item) => sum + Number(item.minutes || 0), 0);
  view.innerHTML = `
    ${viewHead("Patterns, not pressure", "Make the next week smarter.")}
    <div class="split">
      <button id="insight-consistency" class="card detail-trigger" type="button"><h2>Consistency signal</h2><div class="insight-score">${d.consistency}<small>%</small></div><p class="empty">Recorded focus time relative to planned workload.</p></button>
      <button id="insight-mark" class="card detail-trigger" type="button"><h2>Indicative mark scenario</h2><div class="insight-score">${d.predicted_mark}<small>%</small></div><p class="empty">${esc(d.disclaimer)}</p></button>
    </div>
    <section class="card" style="margin-top:16px"><h2>Saved learning activity</h2><p class="empty">${totalMinutes} recorded focus minutes across ${sessions.length} sessions and ${quizzes.length} saved practice results.</p></section>
    <section class="card" style="margin-top:16px"><h2>Recommended next actions</h2><ol class="rec-list">${d.recommendations.map((item) => `<li>${esc(item)}</li>`).join("")}</ol></section>`;
  $("#insight-consistency").onclick = () => showDetail({title: "Consistency signal", fields: [["Consistency", `${d.consistency}%`], ["Recorded focus minutes", totalMinutes], ["Focus sessions", sessions.length], ["Calculation", "Saved focus time relative to your saved planned workload."]]});
  $("#insight-mark").onclick = () => showDetail({title: "Indicative mark scenario", fields: [["Scenario", `${d.predicted_mark}%`], ["Saved quiz results used", quizzes.length], ["Confidence", d.confidence], ["Important", d.disclaimer]]});
}
async function diary(view) {
  const entries = await api("/diary");
  view.innerHTML = `
    ${viewHead("Close the loop", "Daily diary.")}
    <div class="split">
      <section class="card"><h2>Today reflection</h2>
        <form id="diary-form">
          <label>Mood<select name="mood"><option>Focused</option><option>Productive</option><option>Stuck</option><option>Tired</option></select></label>
          <label>What did you learn? What changes tomorrow?<textarea name="body" rows="7" required placeholder="Keep it honest and specific."></textarea></label>
          <button class="button primary">Save reflection</button>
        </form>
      </section>
      <section class="card"><h2>Recent entries</h2>${entries.map((x) => `${detailButton(x.id, `<div class="row-grow"><b>${esc(x.entry_date)} / ${esc(x.mood)}</b><small>${esc(x.body)}</small></div>`) }`).join("") || '<p class="empty">Your reflections will become a useful learning record.</p>'}</section>
    </div>`;
  $("#diary-form").onsubmit = async (event) => submitJson(event, "/diary", "Reflection saved");
  bindDetailButtons(entries, (x) => ({title: `${x.entry_date} reflection`, fields: [["Mood", x.mood], ["Full entry", x.body], ["Saved", x.created_at]]}));
}

async function integrations(view) {
  const d = await api("/integrations");
  view.innerHTML = `
    ${viewHead("Safe provider design", "AI connections.")}
    <section class="card"><h2>Provider roadmap</h2>
      <p class="empty">AI services must be connected through administrator-managed API keys or approved OAuth. Students should never enter third-party account passwords into LearnSphere AI.</p>
      ${d.providers.map((p) => `<div class="note-row"><div class="row-grow"><b>${esc(p.name)}</b><small>${esc(p.purpose)}</small></div><small>${esc(p.status)}</small></div>`).join("")}
    </section>
    <section class="card" style="margin-top:16px"><h2>Integration policy</h2><ul class="rec-list"><li>Use server-side secret storage and least-privilege scopes.</li><li>Show students what data is sent to any provider.</li><li>Offer a non-AI fallback and data deletion path before public release.</li></ul></section>`;
}

$$("[data-open-auth]").forEach((button) => {
  button.onclick = () => setAuth(button.dataset.openAuth);
});
$("[data-close-auth]").onclick = () => $("#auth").classList.add("hidden");
$("#auth-toggle").onclick = () => setAuth($("#auth-form").dataset.mode === "login" ? "register" : "login");
$("#auth-form").onsubmit = async (event) => {
  event.preventDefault();
  const form = new FormData(event.currentTarget);
  const mode = event.currentTarget.dataset.mode || "login";
  const body = Object.fromEntries(form);
  if (mode === "login") delete body.name;
  try {
    const data = await api(`/auth/${mode}`, {method: "POST", body: JSON.stringify(body)});
    state.token = data.token;
    state.user = data.user;
    localStorage.setItem("ls_token", data.token);
    localStorage.setItem("ls_user", JSON.stringify(data.user));
    $("#auth").classList.add("hidden");
    toast("Your study workspace is ready");
    start();
  } catch (error) {
    toast(error.message);
  }
};

$("#logout").onclick = logout;
$("#focus-btn").onclick = async () => {
  try {
    await api("/study-sessions", {method: "POST", body: JSON.stringify({minutes: 25})});
    toast("25 focus minutes recorded");
    render();
  } catch (error) {
    toast(error.message);
  }
};
$("#mobile-menu").onclick = () => toast("Use a wider screen for the full sidebar navigation in this demo.");
if (state.token) start();
