// supabaseAuth.ts

import { createClient } from '@supabase/supabase-js'; import type { Express, Request, Response, NextFunction } from 'express';

const supabaseUrl = process.env.SUPABASE_URL!; const supabaseAnonKey = process.env.SUPABASE_ANON_KEY!;

export const supabase = createClient(supabaseUrl, supabaseAnonKey);

// Optional middleware to attach user to request if JWT is provided export function withSupabaseAuth(app: Express) { app.use(async (req: Request, res: Response, next: NextFunction) => { const authHeader = req.headers.authorization; if (!authHeader) return next();

const token = authHeader.replace('Bearer ', '');

const {
  data: { user },
  error,
} = await supabase.auth.getUser(token);

if (error) {
  console.warn('Supabase auth error:', error.message);
} else {
  (req as any).user = user; // attach user to request
}

next();

}); }