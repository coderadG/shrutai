import mongoose from "mongoose";
import XLSX from "xlsx";
import dotenv from "dotenv";
import Driver from "./models/Driver.js";
import SwapLog from "./models/SwapLog.js";

dotenv.config();

// Helper to read Excel file
const readExcel = (filePath) => {
  const workbook = XLSX.readFile(filePath);
  const sheetName = workbook.SheetNames[0];
  return XLSX.utils.sheet_to_json(workbook.Sheets[sheetName]);
};

const importData = async () => {
  try {
    await mongoose.connect(process.env.MONGO_URI);
    console.log("🌱 Connected to DB...");

    // 1. Load Data
    console.log("Reading Excel files...");
    const driversRaw = readExcel('data/CallRecording.xlsx'); 
    const logsRaw = readExcel('data/BatteryLogs.xlsx');

    // 2. Extract Real Driver IDs
    const realDriverIds = [...new Set(logsRaw.map(l => l.occupant).filter(id => id && id.startsWith('D')))];
    console.log(`Found ${realDriverIds.length} unique driver IDs in logs.`);

    // 3. Import Drivers (WIPE & RELOAD)
    console.log("Importing Drivers...");
    await Driver.deleteMany({}); // <--- This wipes the old data
    
    const driversToInsert = driversRaw.map((row, index) => {
      const assignedId = realDriverIds[index % realDriverIds.length]; 
      
      return {
        // CHANGED: Wrap the single number in an array [ ]
        mobileNumbers: [String(row['Calling No.'])], 
        name: row['Name'],
        driverId: assignedId, 
        recentIssues: [row['Issue type']]
      };
    });

    await Driver.insertMany(driversToInsert);
    console.log(`✅ Imported ${driversToInsert.length} drivers with updated schema.`);

    // 4. Import Swap Logs (WIPE & RELOAD)
    console.log("Importing Swap History...");
    await SwapLog.deleteMany({}); // <--- Wipes old logs to keep it clean

    const usedIds = new Set(driversToInsert.map(d => d.driverId));
    
    const logsToInsert = logsRaw
      .filter(row => usedIds.has(row.occupant))
      .map(row => ({
        driverId: row.occupant,
        batteryId: row.batteryId,
        swapTime: new Date(row.updatedAt), 
        isMisplaced: String(row.isMisplaced).toLowerCase() === 'true'
      }));

    await SwapLog.insertMany(logsToInsert);
    console.log(`✅ Imported ${logsToInsert.length} swap logs.`);

    console.log("🚀 DATABASE UPGRADE COMPLETE!");
    process.exit();
  } catch (error) {
    console.error("❌ Error:", error);
    process.exit(1);
  }
};

importData();