import { getAIReply } from "./aiService.js";

export async function generateReply(userText) {
  if (!userText) {
    return "No text received.";
  }

  const text = userText.toLowerCase();

  // Fast rule-based replies (cheap + instant)
  if (text.includes("hello")) {
    return "Hello! I'm ShrutAI 👋";
  }

  if (text.includes("how are you")) {
    return "I'm doing great! How can I help you today?";
  }

  if (text.includes("bye")) {
    return "Goodbye! Talk to you soon 😊";
  }

  // Everything else → Groq AI
  return await getAIReply(userText);
}
