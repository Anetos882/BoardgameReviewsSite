import { defineCollection, z } from "astro:content";
import { glob } from "astro/loaders";

const games = defineCollection({
  loader: glob({
    base: "./src/content/games",
    pattern: "**/*.{md,mdx}",
  }),
  schema: z.object({
    bgg_url: z.string().optional(),
    bgg_id: z.number().optional(),

    localization: z.string().nullable().optional(),
    date_added: z.coerce.date().optional(),
    plays: z.number().optional(),
    my_rating: z.number().optional(),

    title: z.string().nullable().optional(),
    image: z.string().nullable().optional(),

    year: z.number().nullable().optional(),
    bgg_rank: z.number().nullable().optional(),
    bayes_rating: z.number().nullable().optional(),
    average_rating: z.number().nullable().optional(),
    users_rated: z.number().nullable().optional(),
  }),
});

export const collections = {
  games,
};
