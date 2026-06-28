console.log("JS loaded");


// ---------------- SUMMARY ----------------
document.getElementById("summaryBtn").addEventListener("click", async () => {

    const notes = document.getElementById("notes").value;
    const level = document.getElementById("level").value;

    const res = await fetch("/summary", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ notes, level })
    });

    const data = await res.json();
    document.getElementById("summaryOutput").innerText = data.summary;
});


// ---------------- QUESTIONS ----------------
document.getElementById("questionBtn").addEventListener("click", async () => {

    const notes = document.getElementById("notes").value;

    const res = await fetch("/questions", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ notes })
    });

    const data = await res.json();
    document.getElementById("questionOutput").innerText = data.questions;
});


// ---------------- FLASHCARDS ----------------
document.getElementById("flashBtn").addEventListener("click", async () => {

    const notes = document.getElementById("notes").value;

    const res = await fetch("/flashcards", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ notes })
    });

    const data = await res.json();
    document.getElementById("flashOutput").innerText = data.flashcards;
});


// ---------------- CHAT (WITH HISTORY) ----------------
let chatHistory = JSON.parse(localStorage.getItem("chatHistory")) || [];

renderChat();

document.getElementById("askBtn").addEventListener("click", async () => {

    const notes = document.getElementById("notes").value;
    const question = document.getElementById("userQuestion").value;

    if (!question) return;

    chatHistory.push({ role: "user", text: question });

    const res = await fetch("/ask", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ notes, question })
    });

    const data = await res.json();

    chatHistory.push({ role: "ai", text: data.answer });

    localStorage.setItem("chatHistory", JSON.stringify(chatHistory));

    renderChat();

    document.getElementById("userQuestion").value = "";
});

function renderChat() {

    const box = document.getElementById("answerOutput");

    box.innerHTML = chatHistory.map(msg => {
        return msg.role === "user"
            ? `<div class="user">🧑 You: ${msg.text}</div>`
            : `<div class="ai">🤖 AI: ${msg.text}</div>`;
    }).join("");

    box.scrollTop = box.scrollHeight;
}