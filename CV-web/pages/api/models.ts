import { NextApiRequest, NextApiResponse } from 'next';
import { createClient } from '@supabase/supabase-js';

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL || '';
const supabaseAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY || '';
const supabase = createClient(supabaseUrl, supabaseAnonKey);

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  const { searchQuery = "", tagsFilter = "all", categoryFilter = "all", currentPage = 1, modelId = -1 } = req.query
  let query = supabase
    .from('model_cards')
    .select('*', { count: 'exact' });

  if (categoryFilter !== "all") {
    query = query.ilike('category', `%${categoryFilter}%`);
  }

  if (searchQuery != "") {
    query = query.ilike('desc', `%${searchQuery}%`);
  }

  if (tagsFilter != "all") {
    query = query.contains('tags', [tagsFilter]);
  }

  if (modelId != -1) {
    query = query.eq('id', modelId);
  }

  const { data, error, count } = await query.range((Number(currentPage) - 1) * 30, Number(currentPage) * 30 - 1);

  if (error) {
    return res.status(500).json({ error: error.message });
  }

  res.status(200).json({ data, totalPages: Math.ceil((count ?? 0) / 30) });
}
