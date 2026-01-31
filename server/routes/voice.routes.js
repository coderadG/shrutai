import { Router } from "express";
import multer from "multer";
import fs from "fs";
import { transcribeAudio, getAIReply } from "../services/aiService.js";
import Driver from "../models/Driver.js";
import SwapLog from "../models/SwapLog.js";

const router = Router();
const upload = multer({ dest: "uploads/" }); // Temp folder for audio

router.post("/talk", upload.single("audio"), async (req, res) => {
  try {
    const audioPath = req.file ? req.file.path : null;
    let userText = "";

    // 1. STT: Transcribe Audio
    if (audioPath) {
      userText = await transcribeAudio(audioPath);
      fs.unlinkSync(audioPath); // Clean up
    } else {
      userText = req.body.text || ""; // Fallback for text-only testing
    }

    // Get the caller's number (or default to UNKNOWN for testing)
    const currentMobile = req.body.mobileNumber || "UNKNOWN";
    console.log(`📞 Call from: ${currentMobile} | Said: "${userText}"`);

    // 2. IDENTITY CHECK LEVEL 1: Search by Mobile Number
    // We look for a driver where the 'mobileNumbers' array contains this caller's number
    let driver = await Driver.findOne({ mobileNumbers: currentMobile });

    // 3. IDENTITY CHECK LEVEL 2: Search by Spoken Driver ID (Self-Healing)
    // If we didn't find them by number, check if they said their ID (e.g., "Main D121604 hoon")
    if (!driver) {
      // Regex looks for 'D' followed by 4-7 digits (e.g., D121604)
      const idMatch = userText.match(/\b[Dd]\d{4,7}\b/);
      
      if (idMatch) {
        const spokenId = idMatch[0].toUpperCase();
        console.log(`🕵️ Detected Driver ID in speech: ${spokenId}`);
        
        // Find the driver by their official ID
        driver = await Driver.findOne({ driverId: spokenId });

        if (driver) {
          // AUTO-LINK: Add this new phone number to their profile!
          // We only add it if it's a real number (not "UNKNOWN")
          if (currentMobile !== "UNKNOWN" && !driver.mobileNumbers.includes(currentMobile)) {
            driver.mobileNumbers.push(currentMobile);
            await driver.save();
            console.log(`🔗 SUCCESS: Linked new number ${currentMobile} to driver ${driver.name}`);
          }
        }
      }
    }

    // 4. BUILD CONTEXT FOR AI
    let contextString = "";
    
    if (driver) {
      // We found them (either by phone or by spoken ID)
      const lastSwap = await SwapLog.findOne({ driverId: driver.driverId }).sort({ swapTime: -1 });
      
      contextString = `
        User Name: ${driver.name}
        Driver ID: ${driver.driverId}
        Subscription Status: ${driver.subscription?.status || "Unknown"}
        Last Swap: ${lastSwap ? lastSwap.swapTime.toDateString() : "No record"}
        Recent Issue: ${driver.recentIssues[0] || "None"}
      `;
    } else {
      // Stranger / New User
      contextString = `
        User Identity: Unknown
        Current Mobile: ${currentMobile}
        INSTRUCTION: I do not recognize this phone number.
        - Politely ask the user if they are a registered driver.
        - Ask them to say their "Driver ID" (starting with D, like D12345) so I can find their account.
        - If they are new, tell them to visit the nearest station to register.
      `;
    }

    // 5. GENERATE REPLY
    const aiResult = await getAIReply(userText, [{ role: "system", content: `Context:\n${contextString}` }]);

    res.json({ 
      success: true, 
      transcript: userText,
      reply: aiResult.reply,
      handoffTriggered: aiResult.handoffTriggered,
      driverName: driver ? driver.name : "Guest"
    });

  } catch (error) {
    console.error("❌ Error:", error);
    res.status(500).json({ success: false, error: error.message });
  }
});

export default router;