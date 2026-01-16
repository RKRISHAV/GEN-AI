let DOC_ID = null;
const API_BASE = "http://127.0.0.1:8000";

function addMessage(type, text) {
  const chat = document.getElementById("chat");
  const div = document.createElement("div");
  div.className = `message ${type}`;
  div.innerText = text;
  chat.appendChild(div);
  chat.scrollTop = chat.scrollHeight;
}

async function uploadPDF() {
  const fileInput = document.getElementById("pdfFile");
  const status = document.getElementById("uploadStatus");

  if (!fileInput.files.length) {
    alert("Please select a PDF");
    return;
  }

  const formData = new FormData();
  formData.append("file", fileInput.files[0]);

  status.innerText = "Uploading...";

  const res = await fetch(`${API_BASE}/upload`, {
    method: "POST",
    body: formData
  });

  const data = await res.json();
  DOC_ID = data.doc_id;

  status.innerText = "Uploaded successfully!";
  addMessage("system", "PDF uploaded. Ask me anything about it.");
}

async function askQuestion() {
  const input = document.getElementById("question");
  const question = input.value.trim();

  if (!question) return;
  if (!DOC_ID) {
    alert("Upload a PDF first!");
    return;
  }

  addMessage("user", question);
  input.value = "";

  addMessage("system", "Thinking...");

  const res = await fetch(`${API_BASE}/ask?doc_id=${DOC_ID}&question=${encodeURIComponent(question)}`, {
    method: "POST"
  });

  const data = await res.json();

  const systemMsgs = document.querySelectorAll(".system");
  systemMsgs[systemMsgs.length - 1].remove();

  addMessage("bot", data.answer);
}
