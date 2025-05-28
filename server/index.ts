import express from 'express';
import path from 'path';
import { fileURLToPath } from 'url';

import * as routes from './routes'; // Ensure routes.ts exports an express.Router

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const app = express();
const PORT = process.env.PORT || 3000;

// Serve static files from Vite build output
app.use(express.static(path.join(__dirname, '../client/dist')));

// Mount backend API routes
app.use('/api', routes);

// Fallback to frontend index.html for SPA routing
app.get('*', (req, res) => {
  res.sendFile(path.join(__dirname, '../client/dist/index.html'));
});

app.listen(PORT, () => {
  console.log(`Server listening on port ${PORT}`);
});