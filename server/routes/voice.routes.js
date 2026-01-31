import { Router } from "express";
import { getAIReply } from "../services/aiService.js"; // Import the function, not 'groq'

const router = Router();

router.post("/talk", async (req, res) => {
  try {
    const { text } = req.body; // Postman uses "text" in your screenshot
    
    // Use the imported function
    const aiResponse = await getAIReply(text);

    res.json({ 
      success: true, 
      reply: aiResponse 
    });
  } catch (error) {
    // This is where your "groq is not defined" error was being caught
    res.status(500).json({ success: false, error: error.message });
  }
});

export default router;