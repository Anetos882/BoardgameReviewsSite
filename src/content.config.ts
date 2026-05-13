import { defineCollection, z } from "astro:content";
import { glob } from "astro/loaders";

const games = defineCollection({
  loader: glob({
    base: "./src/content/games",
    pattern: "**/*.md",
  }),
  schema: z.object({
    title: z.string(),
    bgg_id: z.number(),
    date_added: z.coerce.date().optional(),
    my_rating: z.number().optional(),
    plays: z.number().optional(),
    year: z.number().optional(),
    bgg_rank: z.number().optional(),
    bayes_rating: z.number().optional(),
    average_rating: z.number().optional(),
    users_rated: z.number().optional(),
    localization: z.string().optional(),
    bgg_url: z.string().optional(),
    image: z.string().optional(),
  }),
});

export const collections = {
  games,
};