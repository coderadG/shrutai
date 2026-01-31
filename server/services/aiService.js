import Groq from "groq-sdk";
import fs from "fs";

const groq = new Groq({
  apiKey: process.env.GROQ_API_KEY,
});

/**
 * Converts audio file to text using Whisper Large v3 [cite: 80]
 */
export async function transcribeAudio(filePath) {
  const transcription = await groq.audio.transcriptions.create({
    file: fs.createReadStream(filePath),
    model: "whisper-large-v3", 
    language: "hi", // Still use 'hi' as base to capture diverse Indian accents [cite: 80, 82]
    response_format: "json",
  });
  return transcription.text;
}

/**
 * Generates AI response with dynamic language matching 
 */
export async function getAIReply(userText, history = []) {
  const completion = await groq.chat.completions.create({
    model: "llama-3.3-70b-versatile",
    messages: [
      { 
        role: "system", 
        content: `You are ShrutAI, a multilingual voice assistant for drivers. [cite: 27]
        - LANGUAGE RULE: Match the user's language exactly. If they speak proper Hindi, reply in Hindi. If they speak proper English, reply in English. If they use Hinglish, reply in Hinglish. 
        - Resolve queries related to payments, battery swaps, and subscriptions. [cite: 31, 35]
        - Identify intents like checking swap history or nearest stations. [cite: 31, 32]
        - WARM HANDOFF: If the user sounds angry, frustrated, or you are confused, trigger a handoff. [cite: 38, 39, 107]
        - Always provide concise, natural responses safe for someone driving. [cite: 57, 63]`
      },
      ...history, // Maintains conversation context [cite: 44, 98]
      { role: "user", content: userText },
    ],
    temperature: 0.7, 
  });

  const aiMessage = completion.choices[0].message.content;

  // Handoff logic based on plan requirements [cite: 51, 73]
  const handoffTriggered = 
    aiMessage.toLowerCase().includes("human agent") || 
    aiMessage.toLowerCase().includes("connecting you") ||
    aiMessage.toLowerCase().includes("transferring") ||
    aiMessage.toLowerCase().includes("agent se connect");

  return {
    reply: aiMessage,
    handoffTriggered: handoffTriggered
  };
}