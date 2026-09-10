import { z } from "zod";

export const assignmentRequirementsSchema = z.object({
  type: z.enum([
    "assignment",
    "discussion",
    "essay",
    "report",
    "research",
    "question",
    "summary",
    "rewrite",
    "unknown",
  ]),

  topic: z.string(),

  questions: z.array(z.string()),

  wordCount: z
    .object({
      min: z.number().optional(),
      max: z.number().optional(),
      exact: z.number().optional(),
    })
    .optional(),

  citationStyle: z.enum(["APA", "MLA", "Chicago", "Harvard", "IEEE", "none"]),

  academicLevel: z.string().optional(),

  requirements: z.array(z.string()),

  formatting: z.array(z.string()).optional(),

  requiredSources: z.array(z.string()).optional(),

  requiresResearch: z.boolean(),
});
