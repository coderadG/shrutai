import mongoose from "mongoose";

const DriverSchema = new mongoose.Schema({
  // CHANGED: Now an array of strings to support multiple numbers
  mobileNumbers: [{ type: String, index: true }], 
  
  driverId: { type: String, required: true, unique: true },
  name: String,
  language: { type: String, default: "Hinglish" },
  
  subscription: {
    status: { type: String, enum: ["Active", "Expired", "Grace Period"] },
    expiryDate: Date,
    planType: String 
  },

  lastSwap: {
    stationName: String,
    date: Date,
    batterySOC: Number,
    energyConsumed: Number
  }
});

export default mongoose.model("Driver", DriverSchema);