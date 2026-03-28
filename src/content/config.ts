import { defineCollection, z } from 'astro:content';

const blog = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    date: z.coerce.date(),
    description: z.string().optional().default(''),
    heroImage: z.string().optional(),
    tags: z.array(z.string()).optional().default([]),
    author: z.string().optional().default('HERMES'),
    draft: z.boolean().optional().default(false),
  }),
});

export const collections = { blog };
