import { z } from "zod";

export interface Guild {
  id: string;
  created: string;
  modified: string;
  name: string;
  avatar: string | null;
  banner: string | null;
}

export const CreateGuildSchema = z.object({
  name: z.string().nonempty(),
  avatar: z.string().nullable(),
  banner: z.string().nullable(),
});

export type CreateGuildSchema = z.infer<typeof CreateGuildSchema>;

export const UpdateGuildSchema = z
  .partial(CreateGuildSchema)
  .refine((obj) => Object.values(obj).some(Boolean));

export type UpdateGuildSchema = z.infer<typeof UpdateGuildSchema>;
