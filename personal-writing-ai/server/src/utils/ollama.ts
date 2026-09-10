import { ollama } from "ollama-ai-provider-v2";
import { generateObject, generateText, stepCountIs, tool } from "ai";
import { MODEL } from "../lib/constants.ts";
import { tavilySearch } from "@tavily/ai-sdk";
import { z } from "zod";
import { assignmentRequirementsSchema } from "../models/models.ts";
import { limitText, processUploadedFiles } from "./helpers.ts";

import type { UploadedFile, AssignmentRequirements } from "./types.ts";

const MAX_WEB_CONTENT_CHARS = 40_000;

async function analyzeAssignment(
  prompt: string,
  courseMaterials: string,
): Promise<AssignmentRequirements> {
  const { object } = await generateObject({
    model: ollama(MODEL!),

    schema: assignmentRequirementsSchema,

    prompt: `
You are an assignment requirements analyzer.

Analyze the user's request and any provided
course material.

Do NOT answer the assignment.

Identify:

- assignment type
- topic
- every question
- every sub-question
- word count
- citation style
- academic level
- formatting requirements
- required sources
- explicit instructions
- whether external research is necessary

If course materials contain assignment instructions,
treat those instructions as authoritative.

USER REQUEST:

${prompt}

COURSE MATERIALS:

${courseMaterials || "No course materials provided."}
`,
  });

  // The generated schema type includes explicit `undefined` for optional
  // properties, while AssignmentRequirements uses exact optional properties.
  return object as unknown as AssignmentRequirements;
}

/**
 * ============================================================
 * WEB SEARCH TOOL
 * ============================================================
 *
 * Tavily handles actual web search.
 *
 * The AI SDK currently provides a Tavily integration for
 * real-time web search and web research.
 *
 * ============================================================
 */

const searchWeb = tool({
  description: `
Search the public internet for reliable information
needed to complete an academic assignment.

Use this tool whenever:

- The assignment requires research.
- Current information is needed.
- Citations are required.
- The provided course materials are insufficient.
- The topic requires external verification.

Search multiple times when necessary.

Prefer:

1. Peer-reviewed research
2. Universities
3. Government sources
4. International organizations
5. Official documentation
6. Reputable publications
7. Reference sources

Do not rely on one source when multiple credible
sources are available.
`,

  inputSchema: z.object({
    query: z.string().min(3).max(500).describe("Focused research query"),

    topic: z
      .enum(["academic", "official", "news", "general"])
      .default("academic"),
  }),

  execute: async ({ query, topic }) => {
    let searchQuery = query;

    if (topic === "academic") {
      searchQuery = `${query} academic research`;
    }

    if (topic === "official") {
      searchQuery = `${query} official`;
    }

    if (topic === "news") {
      searchQuery = `${query} latest news`;
    }

    /**
     * Tavily performs the actual web search.
     */
    const result = await tavilySearch({
      query: searchQuery,
    });

    return result;
  },
});

/**
 * ============================================================
 * SOURCE EXTRACTION TOOL
 * ============================================================
 *
 * Tavily search results may already contain useful content.
 * This tool allows the agent to explicitly retrieve a URL
 * when it needs additional source material.
 *
 * ============================================================
 */

const fetchWebPage = tool({
  description: `
Retrieve readable content from a public webpage.

Use this when a search result looks useful but the
available search content is insufficient.

Use the retrieved content as evidence.

Do not use private or authenticated URLs.
`,

  inputSchema: z.object({
    url: z.string().url(),
  }),

  execute: async ({
    url,
  }): Promise<{
    url: string;
    content: string;
  }> => {
    const response = await fetch(url, {
      signal: AbortSignal.timeout(15_000),

      headers: {
        "User-Agent": "AssignmentResearchAssistant/1.0",
        Accept: "text/html,application/xhtml+xml",
      },
    });

    if (!response.ok) {
      throw new Error(`Unable to retrieve webpage. HTTP ${response.status}`);
    }

    const html = await response.text();

    /**
     * Remove scripts/styles.
     */
    const cleaned = html
      .replace(/<script[\s\S]*?<\/script>/gi, "")
      .replace(/<style[\s\S]*?<\/style>/gi, "")
      .replace(/<noscript[\s\S]*?<\/noscript>/gi, "")
      .replace(/<[^>]+>/g, " ")
      .replace(/\s+/g, " ")
      .trim();

    return {
      url,

      content: limitText(cleaned, MAX_WEB_CONTENT_CHARS),
    };
  },
});

/**
 * ============================================================
 * SYSTEM PROMPT
 * ============================================================
 */

const SYSTEM_PROMPT = `
You are an advanced academic research and
assignment-writing assistant.

Your job is to help users research, understand,
organize, write, revise, and complete academic
assignments.

============================================================
PRIMARY WORKFLOW
============================================================

Always follow this workflow when dealing with
an academic assignment:

ASSIGNMENT
    ↓
ANALYZE
    ↓
SEARCH
    ↓
READ SOURCES
    ↓
COMPARE EVIDENCE
    ↓
SYNTHESIZE
    ↓
WRITE
    ↓
CHECK CITATIONS
    ↓
CHECK REQUIREMENTS
    ↓
FINAL ANSWER

Do not skip research when the assignment requires
research.

============================================================
COURSE MATERIALS
============================================================

The user may provide:

- PDFs
- lecture notes
- textbooks
- Word documents
- assignment instructions
- rubrics
- course readings
- discussion prompts

Use these materials as primary context.

If the course material contains explicit
assignment instructions, follow them.

Do not ignore course-specific terminology.

External sources may supplement course material
when necessary.

============================================================
WEB RESEARCH
============================================================

For research assignments:

Use searchWeb.

Do not rely entirely on your internal knowledge.

Perform multiple searches when necessary.

Research each major part of the assignment.

Prefer authoritative sources.

Prioritize:

1. Peer-reviewed research
2. Universities
3. Government organizations
4. International organizations
5. Official organizations
6. Reputable publications
7. Recognized reference sources

============================================================
SOURCE READING
============================================================

A search result is not automatically evidence.

When a source is important:

Use fetchWebPage to retrieve additional content.

Use the source's actual content to determine
whether it supports the claim.

============================================================
SOURCE QUALITY
============================================================

Evaluate sources based on:

- authority
- relevance
- publication date
- evidence
- methodology
- reputation
- agreement with other credible sources

Do not treat Wikipedia or a general website
as equivalent to peer-reviewed research.

============================================================
CITATIONS
============================================================

Never invent:

- authors
- titles
- journals
- dates
- statistics
- URLs
- quotations
- citations

Only cite sources that were actually provided
or retrieved.

If APA is requested, use APA.

If MLA is requested, use MLA.

If Harvard is requested, use Harvard.

If Chicago is requested, use Chicago.

If IEEE is requested, use IEEE.

============================================================
ACADEMIC WRITING
============================================================

Write at the academic level requested.

For essays:

Introduction
Body
Conclusion
References

For reports:

Use clear headings and sections.

For discussions:

Use a natural academic discussion style.

For multiple questions:

Answer every question separately unless
the instructions require essay format.

============================================================
WORD COUNT
============================================================

Respect the requested word count.

If a range is given, stay inside the range.

If an exact word count is given, aim as close
to it as practical.

Do not artificially inflate the response.

============================================================
EVIDENCE
============================================================

Separate:

- evidence
- interpretation
- opinion
- assumptions

Do not present an unsupported assumption
as an established fact.

If credible sources disagree, acknowledge
the disagreement.

============================================================
FINAL QUALITY CHECK
============================================================

Before returning the final answer:

[ ] Every question is answered.
[ ] Every sub-question is answered.
[ ] Assignment instructions are followed.
[ ] Course materials were considered.
[ ] Research was performed when required.
[ ] Multiple sources were considered.
[ ] Important sources were inspected.
[ ] Citations are supported.
[ ] No citations were fabricated.
[ ] References correspond to citations.
[ ] Word count is respected.
[ ] Requested structure is followed.
[ ] Academic tone is appropriate.
[ ] The answer directly addresses the assignment.

Return the completed assignment unless the
user asks for an explanation instead.
`;

/**
 * FINAL ASSIGNMENT REVIEW
 */

const reviewAssignment = async ({
  prompt,
  requirements,
  answer,
}: {
  prompt: string;

  requirements: AssignmentRequirements;

  answer: string;
}) => {
  const { object } = await generateObject({
    model: ollama(MODEL!),

    schema: z.object({
      passed: z.boolean(),

      missingRequirements: z.array(z.string()),

      citationProblems: z.array(z.string()),

      structuralProblems: z.array(z.string()),

      wordCountProblem: z.boolean(),

      correctedAnswer: z.string(),
    }),

    prompt: `
You are the final quality-control editor for
an academic assignment.

Review the answer against the assignment.

Do not invent sources.

ASSIGNMENT:

${prompt}

ASSIGNMENT REQUIREMENTS:

${JSON.stringify(requirements, null, 2)}

ANSWER:

${answer}

Check:

1. Did the answer address every question?
2. Did it follow every instruction?
3. Is the requested structure correct?
4. Is the citation style correct?
5. Are citations actually supported?
6. Are references present when required?
7. Is the word count appropriate?
8. Did it use appropriate academic language?
9. Did it rely on unsupported claims?
10. Is anything important missing?

If corrections are necessary, return the complete
corrected answer.

Do not add fabricated references.
`,
  });

  return object;
};

/**
 * ============================================================
 * MAIN FUNCTION
 * ============================================================
 */

export const runConversation = async (
  prompt: string,
  files: UploadedFile[] = [],
) => {
  try {
    /**
     * --------------------------------------------------------
     * 1. Process uploaded documents
     * --------------------------------------------------------
     */

    const courseMaterials = await processUploadedFiles(files);

    /**
     * --------------------------------------------------------
     * 2. Analyze assignment
     * --------------------------------------------------------
     */

    const requirements = await analyzeAssignment(prompt, courseMaterials);

    /**
     * --------------------------------------------------------
     * 3. Generate assignment
     * --------------------------------------------------------
     */

    const { text, steps } = await generateText({
      model: ollama(MODEL!),

      system: SYSTEM_PROMPT,

      prompt: `
============================================================
USER REQUEST
============================================================

${prompt}

============================================================
ASSIGNMENT REQUIREMENTS
============================================================

${JSON.stringify(requirements, null, 2)}

============================================================
COURSE MATERIALS
============================================================

${courseMaterials || "No course materials were uploaded."}

============================================================
RESEARCH REQUIREMENT
============================================================

${
  requirements.requiresResearch
    ? `
Research is REQUIRED.

Use searchWeb.

Perform multiple focused searches where
necessary.

Use fetchWebPage for important sources
when additional source content is needed.

Do not write the final answer until enough
evidence has been gathered.
`
    : `
Research is not strictly required.

However, use searchWeb if external
verification is necessary.
`
}

============================================================
FINAL TASK
============================================================

Complete the assignment.

Use the following workflow:

1. Understand the requirements.
2. Research where necessary.
3. Read important sources.
4. Compare evidence.
5. Synthesize the information.
6. Write the answer.
7. Apply the requested citation style.
8. Check every question.
9. Check the word count.
10. Check the assignment requirements.

Do not fabricate sources or citations.

The final answer should be ready for the
user to review and edit.
`,

      tools: {
        searchWeb,
        fetchWebPage,
      },

      /**
       * Allow enough iterations for:
       *
       * search
       * search
       * search
       * fetch
       * fetch
       * synthesis
       * writing
       */
      stopWhen: stepCountIs(10),
    });

    /**
     * --------------------------------------------------------
     * 4. Final quality check
     * --------------------------------------------------------
     */

    const review = await reviewAssignment({
      prompt,

      requirements,

      answer: text,
    });

    /**
     * --------------------------------------------------------
     * 5. Return result
     * --------------------------------------------------------
     */

    return {
      result: review.correctedAnswer || text,

      assignment: requirements,

      review: {
        passed: review.passed,

        missingRequirements: review.missingRequirements,

        citationProblems: review.citationProblems,

        structuralProblems: review.structuralProblems,

        wordCountProblem: review.wordCountProblem,
      },

      filesProcessed: files.map((file) => file.filename),

      steps: steps.length,

      model: MODEL,
    };
  } catch (error) {
    console.error("Assignment assistant error:", error);

    return {
      error:
        error instanceof Error
          ? error.message
          : "Something went wrong while processing the assignment.",
    };
  }
};
