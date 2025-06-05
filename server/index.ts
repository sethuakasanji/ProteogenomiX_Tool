import express from 'express';
import path from 'path';
import { withSupabaseAuth } from './supabaseAuth';
import { fileURLToPath } from 'url';
import { registerRoutes } from './routes';

const app = express(); // ✅ use "app" consistently

withSupabaseAuth(app); // ✅ apply Supabase auth

(async () => {
  await registerRoutes(app); // ✅ register routes
})();

const __filename = fileURLToPath(import.meta.url);
const dirname = path.dirname(filename);

const PORT = process.env.PORT || 3000;

// ✅ Serve static files
app.use(express.static(path.join(__dirname, '../client/dist')));

// ✅ Fallback for SPA routing
app.get('*', (req, res) => {
  res.sendFile(path.join(__dirname, '../client/dist/index.html'));
});

// ✅ Start server
app.listen(PORT, () => {
  console.log(`Server listening on port ${PORT}`);
});