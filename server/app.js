import express from "express";
import voiceRoutes from "./routes/voice.routes.js";

const app = express();

app.use(express.json());

app.use("/api/voice", voiceRoutes);

export default app;
