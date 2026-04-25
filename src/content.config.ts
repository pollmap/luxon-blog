import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

// v2 Devlog 5-category taxonomy — orthogonal to existing `tags` (topic-level).
// `category` captures editorial intent: building / field / failure / deep-dive / retro.
// All v2 fields are optional so 214 legacy posts continue to build unmodified
// until backfill_category.py tags them.
export const CATEGORIES = [
  'building',
  'field',
  'failure',
  'deep-dive',
  'retro',
] as const;
export type BlogCategory = (typeof CATEGORIES)[number];

const blog = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/blog' }),
  schema: z.object({
    title: z.string(),
    date: z.coerce.date(),
    description: z.string().optional().default(''),
    heroImage: z.string().optional(),
    tags: z.array(z.string()).optional().default([]),

    // v2 additions — all optional for backward compatibility
    category: z.enum(CATEGORIES).optional(),
    prereq: z.array(z.string()).optional(),
    readingTime: z.number().int().positive().optional(),
  }),
});

export const collections = { blog };
