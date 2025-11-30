const btn = document.getElementById("summarizeBtn");
const statusEl = document.getElementById("status");
const summaryEl = document.getElementById("summary");

btn.addEventListener("click", async () => {
  statusEl.textContent = "Getting selection";
  summaryEl.textContent = "";

  // Get active tab
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });

  // Ask content script for selected text
  const selection = await chrome.tabs.sendMessage(tab.id, { type: "GET_SELECTION" });
  const text = selection?.text?.trim();

  if (!text) {
    statusEl.textContent = "No text selected. Highlight some text first.";
    return;
  }

  statusEl.textContent = "Summarizing";

  try {
    const res = await fetch("http://localhost:8000/summarize", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text })
    });

    if (!res.ok) {
      throw new Error("API error " + res.status);
    }

    const data = await res.json();
    summaryEl.textContent = data.summary;
    statusEl.textContent = "Done";
  } catch (err) {
    console.error(err);
    statusEl.textContent = "Error talking to API";
  }
});
