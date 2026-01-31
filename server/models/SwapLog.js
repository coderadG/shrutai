import mongoose from "mongoose";

const SwapLogSchema = new mongoose.Schema({
  driverId: { type: String, required: true, index: true }, // The link to Driver
  batteryId: String,
  swapTime: Date,
  isMisplaced: Boolean
});

export default mongoose.model("SwapLog", SwapLogSchema);