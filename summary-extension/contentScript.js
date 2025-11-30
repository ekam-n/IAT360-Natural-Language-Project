// Listen for messages from the popup
chrome.runtime.onMessage.addListener((msg, sender, sendResponse) => {
  if (msg.type === "GET_SELECTION") {
    const selection = window.getSelection().toString();
    sendResponse({ text: selection });
  }
  // Returning true allows async sendResponse, not needed here
  return false;
});
