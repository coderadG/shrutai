import 'dotenv/config'; // This shorthand works perfectly for ES Modules
import app from "./app.js";

const PORT = 5000;

app.listen(PORT, () => {
  console.log(`🚀 Voicebot running on port ${PORT}`);
});