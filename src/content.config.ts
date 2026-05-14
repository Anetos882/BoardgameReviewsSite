import { defineCollection, z } from "astro:content";

const games = defineCollection({
  type: "content",
  schema: z.object({
    bgg_url: z.string().optional(),
    bgg_id: z.number().optional(),

    localization: z.string().optional(),
    date_added: z.coerce.date().optional(),
    plays: z.number().optional(),
    my_rating: z.number().optional(),

    image: z.string().nullable().optional(),
    title: z.string().nullable().optional(),

    year: z.coerce.number().nullable().optional(),
    bgg_rank: z.coerce.number().nullable().optional(),
    bayes_rating: z.coerce.number().nullable().optional(),
    average_rating: z.coerce.number().nullable().optional(),
    users_rated: z.coerce.number().nullable().optional(),
  }),
});

export const collections = {
  games,
};
