import express from 'express';
import path from 'path';
import { withSupabaseAuth } from './supabaseAuth';

withSupabaseAuth(app); // ✅ This adds Supabase Auth middleware
import { fileURLToPath } from 'url';

import { registerRoutes } from './routes'; // ✅ Use named import

const app = express();

(async () => {
  await registerRoutes(app); // ✅ Correctly call the async route setup
})();

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);


const PORT = process.env.PORT || 3000;

// Serve static files from Vite build output
app.use(express.static(path.join(__dirname, '../client/dist')));

// Mount backend API routes


// Fallback to frontend index.html for SPA routing
app.get('*', (req, res) => {
  res.sendFile(path.join(__dirname, '../client/dist/index.html'));
});

app.listen(PORT, () => {
  console.log(`Server listening on port ${PORT}`);
});