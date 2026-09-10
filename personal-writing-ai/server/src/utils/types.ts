type AssignmentType =
  | "assignment"
  | "discussion"
  | "essay"
  | "report"
  | "research"
  | "question"
  | "summary"
  | "rewrite"
  | "unknown";

type CitationStyle = "APA" | "MLA" | "Chicago" | "Harvard" | "IEEE" | "none";

export type UploadedFile = {
  filename: string;
  mimeType: string;
  buffer: Buffer;
};

export type AssignmentRequirements = {
  type: AssignmentType;

  topic: string;

  questions: string[];

  wordCount?: {
    min?: number;
    max?: number;
    exact?: number;
  };

  citationStyle: CitationStyle;

  academicLevel?: string;

  requirements: string[];

  formatting?: string[];

  requiredSources?: string[];

  requiresResearch: boolean;
};

export type ResearchSource = {
  title: string;

  url: string;

  source: string;

  content: string;

  score?: number;
};
