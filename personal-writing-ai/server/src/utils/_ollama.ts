// // import { ollama } from "ollama-ai-provider-v2";
// // import { generateText, stepCountIs, tool } from "ai";
// // import { z } from "zod";

// // type SearchResult = {
// //   title: string;
// //   url: string;
// //   snippet: string;
// //   source: string;
// // };

// // type DuckDuckGoTopic = {
// //   FirstURL?: string;
// //   Text?: string;
// //   Topics?: DuckDuckGoTopic[];
// // };

// // type DuckDuckGoResponse = {
// //   AbstractText?: string;
// //   AbstractSource?: string;
// //   AbstractURL?: string;
// //   RelatedTopics?: DuckDuckGoTopic[];
// // };

// // type WikipediaSearchResponse = {
// //   query?: {
// //     search?: Array<{
// //       title: string;
// //       snippet: string;
// //     }>;
// //   };
// // };

// // const stripMarkup = (value: string) =>
// //   value
// //     .replace(/<!\[CDATA\[([\s\S]*?)\]\]>/g, "$1")
// //     .replace(/<[^>]+>/g, "")
// //     .replace(/&amp;/g, "&")
// //     .replace(/&quot;/g, '"')
// //     .replace(/&#39;/g, "'")
// //     .replace(/&lt;/g, "<")
// //     .replace(/&gt;/g, ">")
// //     .trim();

// // const fetchRssResults = async (
// //   url: URL,
// //   source: string,
// // ): Promise<SearchResult[]> => {
// //   const response = await fetch(url, {
// //     signal: AbortSignal.timeout(10_000),
// //     headers: { Accept: "application/rss+xml, application/xml, text/xml" },
// //   });

// //   if (!response.ok) {
// //     throw new Error(`${source} search failed with status ${response.status}.`);
// //   }

// //   const xml = await response.text();
// //   const results: SearchResult[] = [];
// //   for (const item of xml.matchAll(/<item>([\s\S]*?)<\/item>/gi)) {
// //     const content = item[1] ?? "";
// //     const title = content.match(/<title>([\s\S]*?)<\/title>/i)?.[1];
// //     const link = content.match(/<link>([\s\S]*?)<\/link>/i)?.[1];
// //     const description = content.match(
// //       /<description>([\s\S]*?)<\/description>/i,
// //     )?.[1];

// //     if (title && link) {
// //       results.push({
// //         title: stripMarkup(title),
// //         url: stripMarkup(link),
// //         snippet: stripMarkup(description ?? ""),
// //         source,
// //       });
// //     }
// //   }

// //   return results.slice(0, 5);
// // };

// // const searchGoogleNews = (query: string) => {
// //   const url = new URL("https://news.google.com/rss/search");
// //   url.searchParams.set("q", query);
// //   url.searchParams.set("hl", "en-US");
// //   url.searchParams.set("gl", "US");
// //   url.searchParams.set("ceid", "US:en");
// //   return fetchRssResults(url, "Google News");
// // };

// // const searchBingNews = (query: string) => {
// //   const url = new URL("https://www.bing.com/news/search");
// //   url.searchParams.set("q", query);
// //   url.searchParams.set("format", "rss");
// //   return fetchRssResults(url, "Bing News");
// // };

// // const searchWikipedia = async (query: string): Promise<SearchResult[]> => {
// //   const url = new URL("https://en.wikipedia.org/w/api.php");
// //   url.searchParams.set("action", "query");
// //   url.searchParams.set("list", "search");
// //   url.searchParams.set("srsearch", query);
// //   url.searchParams.set("srlimit", "3");
// //   url.searchParams.set("format", "json");
// //   url.searchParams.set("origin", "*");

// //   const response = await fetch(url, {
// //     signal: AbortSignal.timeout(10_000),
// //     headers: { Accept: "application/json" },
// //   });
// //   if (!response.ok) {
// //     throw new Error(`Wikipedia search failed with status ${response.status}.`);
// //   }

// //   const data = (await response.json()) as WikipediaSearchResponse;
// //   return (data.query?.search ?? []).map((item) => ({
// //     title: item.title,
// //     url: `https://en.wikipedia.org/wiki/${encodeURIComponent(item.title.replace(/ /g, "_"))}`,
// //     snippet: stripMarkup(item.snippet),
// //     source: "Wikipedia",
// //   }));
// // };

// // const searchWeb = tool({
// //   description:
// //     "Search multiple public web sources, including Google News, Bing News, " +
// //     "Wikipedia, and DuckDuckGo, for current or niche information unavailable locally.",
// //   inputSchema: z.object({
// //     query: z.string().min(2).max(500).describe("The focused web search query"),
// //   }),
// //   execute: async ({ query }): Promise<{ query: string; results: SearchResult[]; markdown: string }> => {
// //     const duckDuckGo = async (): Promise<SearchResult[]> => {
// //       const url = new URL("https://api.duckduckgo.com/");
// //       url.searchParams.set("q", query);
// //       url.searchParams.set("format", "json");
// //       url.searchParams.set("no_html", "1");
// //       url.searchParams.set("skip_disambig", "1");
// //       const response = await fetch(url, {
// //         signal: AbortSignal.timeout(10_000),
// //         headers: { Accept: "application/json" },
// //       });
// //       if (!response.ok) {
// //         throw new Error(`DuckDuckGo search failed with status ${response.status}.`);
// //       }
// //       const data = (await response.json()) as DuckDuckGoResponse;
// //       const results: SearchResult[] = [];
// //       if (data.AbstractText && data.AbstractURL) {
// //         results.push({
// //           title: data.AbstractSource ?? "DuckDuckGo instant answer",
// //           url: data.AbstractURL,
// //           snippet: data.AbstractText,
// //           source: "DuckDuckGo",
// //         });
// //       }
// //       return results;
// //     };

// //     const searches = await Promise.allSettled([
// //       searchGoogleNews(query),
// //       searchBingNews(query),
// //       searchWikipedia(query),
// //       duckDuckGo(),
// //     ]);
// //     const results = searches.flatMap((search) =>
// //       search.status === "fulfilled" ? search.value : [],
// //     );
// //     const uniqueResults = results.filter(
// //       (result, index, all) =>
// //         all.findIndex((candidate) => candidate.url === result.url) === index,
// //     );
// //     const markdown =
// //       uniqueResults.length === 0
// //         ? `No results were found for **${query}**.`
// //         : uniqueResults
// //             .slice(0, 12)
// //             .map(
// //               (result) =>
// //                 `- **[${result.title}](${result.url})** (${result.source}): ${result.snippet}`,
// //             )
// //             .join("\n");

// //     return { query, results: uniqueResults.slice(0, 12), markdown };
// //   },
// // });

// // export const runConversation = async (prompt: string) => {
// //   try {
// //     const { text } = await generateText({
// //       model: ollama("llama3.1:8b"),
// //       system:
// //         "Answer using your local knowledge first. If the requested information is " +
// //         "current, niche, or unavailable locally, use the searchWeb tool before answering. " +
// //         "When you use it, rely on agreement between credible sources where possible, " +
// //         "and present the answer in clear Markdown with inline source links.",
// //       prompt,
// //       tools: { searchWeb },
// //       stopWhen: stepCountIs(3),
// //     });

// //     return { result: text };
// //   } catch (error) {
// //     return { error: "Something went wrong while processing your request." };
// //   }
// // };

// import { ollama } from "ollama-ai-provider-v2";
// import { generateObject, generateText, stepCountIs, tool } from "ai";
// import { z } from "zod";

// /**
//  * ============================================================
//  * TYPES
//  * ============================================================
//  */

// type AssignmentType =
//   | "assignment"
//   | "discussion"
//   | "essay"
//   | "report"
//   | "research"
//   | "question"
//   | "summary"
//   | "rewrite"
//   | "unknown";

// type CitationStyle = "APA" | "MLA" | "Chicago" | "Harvard" | "IEEE" | "none";

// type SearchResult = {
//   title: string;
//   url: string;
//   snippet: string;
//   source: string;
//   publishedAt?: string;
// };

// type AssignmentRequirements = {
//   type: AssignmentType;

//   topic: string;

//   questions: string[];

//   wordCount?: {
//     min?: number | undefined;
//     max?: number | undefined;
//     exact?: number | undefined;
//   } | undefined;

//   citationStyle: CitationStyle;

//   requirements: string[];

//   academicLevel?: string | undefined;

//   requiresResearch: boolean;

//   requiredSources?: string[] | undefined;

//   formatting?: string[] | undefined;
// };

// type WebPage = {
//   url: string;
//   title?: string;
//   content: string;
// };

// type ResearchSource = {
//   title: string;
//   url: string;
//   source: string;
//   snippet: string;
//   content?: string;
//   credibilityScore: number;
// };

// /**
//  * ============================================================
//  * CONSTANTS
//  * ============================================================
//  */

// const OLLAMA_MODEL = process.env.OLLAMA_MODEL ?? "llama3.1:8b";

// const FETCH_TIMEOUT = 15_000;

// const MAX_PAGE_CONTENT = 30_000;

// /**
//  * ============================================================
//  * HELPERS
//  * ============================================================
//  */

// /**
//  * Remove basic HTML/XML markup.
//  */
// const stripMarkup = (value: string): string => {
//   return value
//     .replace(/<!\[CDATA\[([\s\S]*?)\]\]>/g, "$1")
//     .replace(/<script[\s\S]*?<\/script>/gi, "")
//     .replace(/<style[\s\S]*?<\/style>/gi, "")
//     .replace(/<[^>]+>/g, "")
//     .replace(/&amp;/g, "&")
//     .replace(/&quot;/g, '"')
//     .replace(/&#39;/g, "'")
//     .replace(/&lt;/g, "<")
//     .replace(/&gt;/g, ">")
//     .replace(/\s+/g, " ")
//     .trim();
// };

// /**
//  * Give sources a rough credibility score.
//  *
//  * This is only a first-pass ranking mechanism.
//  * The model should still evaluate sources based on relevance
//  * and evidence.
//  */
// const getSourcePriority = (url: string): number => {
//   try {
//     const hostname = new URL(url).hostname.toLowerCase();

//     if (hostname.endsWith(".gov")) return 10;

//     if (hostname.endsWith(".edu")) return 10;

//     if (hostname.endsWith(".ac.uk")) return 10;

//     if (hostname.endsWith(".int")) return 9;

//     if (
//       hostname.includes("who.int") ||
//       hostname.includes("un.org") ||
//       hostname.includes("worldbank.org")
//     ) {
//       return 10;
//     }

//     if (
//       hostname.includes("nature.com") ||
//       hostname.includes("sciencedirect.com") ||
//       hostname.includes("springer.com") ||
//       hostname.includes("pubmed.ncbi.nlm.nih.gov") ||
//       hostname.includes("nih.gov")
//     ) {
//       return 9;
//     }

//     if (hostname.includes("reuters.com") || hostname.includes("apnews.com")) {
//       return 8;
//     }

//     if (hostname.includes("wikipedia.org")) {
//       return 6;
//     }

//     return 3;
//   } catch {
//     return 1;
//   }
// };

// /**
//  * Deduplicate search results.
//  */
// const deduplicateResults = (results: SearchResult[]): SearchResult[] => {
//   const unique = new Map<string, SearchResult>();

//   for (const result of results) {
//     if (!result.url) continue;

//     const normalizedUrl = result.url.trim().replace(/\/$/, "");

//     if (!unique.has(normalizedUrl)) {
//       unique.set(normalizedUrl, result);
//     }
//   }

//   return [...unique.values()];
// };

// /**
//  * ============================================================
//  * RSS SEARCH
//  * ============================================================
//  */

// const fetchRssResults = async (
//   url: URL,
//   source: string,
// ): Promise<SearchResult[]> => {
//   const response = await fetch(url, {
//     signal: AbortSignal.timeout(10_000),

//     headers: {
//       Accept: "application/rss+xml, application/xml, text/xml",
//       "User-Agent": "AssignmentResearchAssistant/1.0",
//     },
//   });

//   if (!response.ok) {
//     throw new Error(`${source} search failed with status ${response.status}.`);
//   }

//   const xml = await response.text();

//   const results: SearchResult[] = [];

//   for (const item of xml.matchAll(/<item>([\s\S]*?)<\/item>/gi)) {
//     const content = item[1] ?? "";

//     const title = content.match(/<title>([\s\S]*?)<\/title>/i)?.[1];

//     const link = content.match(/<link>([\s\S]*?)<\/link>/i)?.[1];

//     const description = content.match(
//       /<description>([\s\S]*?)<\/description>/i,
//     )?.[1];

//     const pubDate = content.match(/<pubDate>([\s\S]*?)<\/pubDate>/i)?.[1];

//     if (title && link) {
//       results.push({
//         title: stripMarkup(title),
//         url: stripMarkup(link),
//         snippet: stripMarkup(description ?? ""),
//         source,
//         ...(pubDate ? { publishedAt: stripMarkup(pubDate) } : {}),
//       });
//     }
//   }

//   return results.slice(0, 10);
// };

// /**
//  * ============================================================
//  * GOOGLE NEWS
//  * ============================================================
//  */

// const searchGoogleNews = (query: string): Promise<SearchResult[]> => {
//   const url = new URL("https://news.google.com/rss/search");

//   url.searchParams.set("q", query);
//   url.searchParams.set("hl", "en-US");
//   url.searchParams.set("gl", "US");
//   url.searchParams.set("ceid", "US:en");

//   return fetchRssResults(url, "Google News");
// };

// /**
//  * ============================================================
//  * BING NEWS
//  * ============================================================
//  */

// const searchBingNews = (query: string): Promise<SearchResult[]> => {
//   const url = new URL("https://www.bing.com/news/search");

//   url.searchParams.set("q", query);
//   url.searchParams.set("format", "rss");

//   return fetchRssResults(url, "Bing News");
// };

// /**
//  * ============================================================
//  * WIKIPEDIA
//  * ============================================================
//  */

// type WikipediaSearchResponse = {
//   query?: {
//     search?: Array<{
//       title: string;
//       snippet: string;
//     }>;
//   };
// };

// const searchWikipedia = async (query: string): Promise<SearchResult[]> => {
//   const url = new URL("https://en.wikipedia.org/w/api.php");

//   url.searchParams.set("action", "query");
//   url.searchParams.set("list", "search");
//   url.searchParams.set("srsearch", query);
//   url.searchParams.set("srlimit", "5");
//   url.searchParams.set("format", "json");
//   url.searchParams.set("origin", "*");

//   const response = await fetch(url, {
//     signal: AbortSignal.timeout(10_000),

//     headers: {
//       Accept: "application/json",
//       "User-Agent": "AssignmentResearchAssistant/1.0",
//     },
//   });

//   if (!response.ok) {
//     throw new Error(`Wikipedia search failed with status ${response.status}.`);
//   }

//   const data = (await response.json()) as WikipediaSearchResponse;

//   return (data.query?.search ?? []).map((item) => ({
//     title: item.title,

//     url:
//       `https://en.wikipedia.org/wiki/` +
//       encodeURIComponent(item.title.replace(/ /g, "_")),

//     snippet: stripMarkup(item.snippet),

//     source: "Wikipedia",
//   }));
// };

// /**
//  * ============================================================
//  * DUCKDUCKGO
//  * ============================================================
//  */

// type DuckDuckGoTopic = {
//   FirstURL?: string;
//   Text?: string;
//   Topics?: DuckDuckGoTopic[];
// };

// type DuckDuckGoResponse = {
//   AbstractText?: string;
//   AbstractSource?: string;
//   AbstractURL?: string;

//   RelatedTopics?: DuckDuckGoTopic[];
// };

// const searchDuckDuckGo = async (query: string): Promise<SearchResult[]> => {
//   const url = new URL("https://api.duckduckgo.com/");

//   url.searchParams.set("q", query);
//   url.searchParams.set("format", "json");
//   url.searchParams.set("no_html", "1");
//   url.searchParams.set("skip_disambig", "1");

//   const response = await fetch(url, {
//     signal: AbortSignal.timeout(10_000),

//     headers: {
//       Accept: "application/json",
//       "User-Agent": "AssignmentResearchAssistant/1.0",
//     },
//   });

//   if (!response.ok) {
//     throw new Error(`DuckDuckGo search failed with status ${response.status}.`);
//   }

//   const data = (await response.json()) as DuckDuckGoResponse;

//   const results: SearchResult[] = [];

//   if (data.AbstractText && data.AbstractURL) {
//     results.push({
//       title: data.AbstractSource ?? "DuckDuckGo Instant Answer",

//       url: data.AbstractURL,

//       snippet: data.AbstractText,

//       source: "DuckDuckGo",
//     });
//   }

//   return results;
// };

// /**
//  * ============================================================
//  * SEARCH ALL SOURCES
//  * ============================================================
//  */

// const searchAllSources = async (query: string): Promise<SearchResult[]> => {
//   const searches = await Promise.allSettled([
//     searchGoogleNews(query),
//     searchBingNews(query),
//     searchWikipedia(query),
//     searchDuckDuckGo(query),
//   ]);

//   const results = searches.flatMap((search) =>
//     search.status === "fulfilled" ? search.value : [],
//   );

//   const unique = deduplicateResults(results);

//   return unique
//     .sort((a, b) => getSourcePriority(b.url) - getSourcePriority(a.url))
//     .slice(0, 20);
// };

// /**
//  * ============================================================
//  * SEARCH TOOL
//  * ============================================================
//  */

// const searchWeb = tool({
//   description: `
// Search multiple public internet sources for information
// needed to research an academic assignment.

// Use this tool when:

// - The user asks for research.
// - The user provides an assignment.
// - The user asks for current information.
// - The answer requires citations.
// - The answer requires external evidence.
// - The topic is niche or uncertain.

// Use multiple searches when necessary.

// Prioritize authoritative sources, academic sources,
// government sources, universities, international organizations,
// official documentation, and reputable publications.

// Do not assume that one search result is sufficient.
// `,

//   inputSchema: z.object({
//     query: z
//       .string()
//       .min(2)
//       .max(500)
//       .describe("A focused academic research query"),

//     sourceType: z
//       .enum(["academic", "official", "news", "reference", "general"])
//       .default("general"),

//     maxResults: z.number().int().min(1).max(20).default(10),
//   }),

//   execute: async ({ query, sourceType, maxResults }) => {
//     let modifiedQuery = query;

//     /**
//      * Improve searches according to source type.
//      */
//     if (sourceType === "academic") {
//       modifiedQuery = `${query} academic research study journal`;
//     }

//     if (sourceType === "official") {
//       modifiedQuery = `${query} official government organization`;
//     }

//     if (sourceType === "news") {
//       modifiedQuery = `${query} latest news`;
//     }

//     const results = await searchAllSources(modifiedQuery);

//     const limited = results.slice(0, maxResults);

//     return {
//       query,

//       sourceType,

//       results: limited,

//       markdown:
//         limited.length === 0
//           ? `No results found for "${query}".`
//           : limited
//               .map(
//                 (result) =>
//                   `- **${result.title}**\n` +
//                   `  URL: ${result.url}\n` +
//                   `  Source: ${result.source}\n` +
//                   `  ${result.snippet}`,
//               )
//               .join("\n\n"),
//     };
//   },
// });

// /**
//  * ============================================================
//  * WEBPAGE FETCH TOOL
//  * ============================================================
//  */

// const fetchWebPage = tool({
//   description: `
// Fetch a public webpage and extract its readable text.

// Use this after searchWeb identifies a potentially useful
// source.

// Use it to inspect the actual source rather than relying
// only on the search-result snippet.

// Do not use it for private, login-protected, or authenticated
// pages.
// `,

//   inputSchema: z.object({
//     url: z.string().url(),
//   }),

//   execute: async ({ url }): Promise<WebPage> => {
//     const response = await fetch(url, {
//       signal: AbortSignal.timeout(FETCH_TIMEOUT),

//       headers: {
//         Accept: "text/html,application/xhtml+xml",
//         "User-Agent":
//           "Mozilla/5.0 (compatible; AssignmentResearchAssistant/1.0)",
//       },
//     });

//     if (!response.ok) {
//       throw new Error(`Failed to fetch ${url}: HTTP ${response.status}`);
//     }

//     const html = await response.text();

//     const title = html.match(/<title[^>]*>([\s\S]*?)<\/title>/i)?.[1];

//     const content = stripMarkup(html).slice(0, MAX_PAGE_CONTENT);

//     return {
//       url,

//       ...(title ? { title: stripMarkup(title) } : {}),

//       content,
//     };
//   },
// });

// /**
//  * ============================================================
//  * ASSIGNMENT REQUIREMENTS SCHEMA
//  * ============================================================
//  */

// const assignmentRequirementsSchema = z.object({
//   type: z.enum([
//     "assignment",
//     "discussion",
//     "essay",
//     "report",
//     "research",
//     "question",
//     "summary",
//     "rewrite",
//     "unknown",
//   ]),

//   topic: z.string(),

//   questions: z.array(z.string()),

//   wordCount: z
//     .object({
//       min: z.number().optional(),
//       max: z.number().optional(),
//       exact: z.number().optional(),
//     })
//     .optional(),

//   citationStyle: z.enum(["APA", "MLA", "Chicago", "Harvard", "IEEE", "none"]),

//   requirements: z.array(z.string()),

//   academicLevel: z.string().optional(),

//   requiresResearch: z.boolean(),

//   requiredSources: z.array(z.string()).optional(),

//   formatting: z.array(z.string()).optional(),
// });

// /**
//  * ============================================================
//  * ASSIGNMENT ANALYZER
//  * ============================================================
//  */

// const analyzeAssignment = async (
//   prompt: string,
// ): Promise<AssignmentRequirements> => {
//   const { object } = await generateObject({
//     model: ollama(OLLAMA_MODEL),

//     schema: assignmentRequirementsSchema,

//     prompt: `
// Analyze the following user request.

// Do NOT answer the assignment.

// Your task is only to identify the assignment requirements.

// Extract:

// - assignment type
// - topic
// - every question
// - every sub-question
// - word count
// - citation style
// - academic level
// - formatting requirements
// - required sources
// - whether research is required
// - any explicit instructions

// If no citation style is specified,
// use "none".

// If no word count is specified,
// leave wordCount undefined.

// USER REQUEST:

// ${prompt}
// `,
//   });

//   return object;
// };

// /**
//  * ============================================================
//  * SYSTEM PROMPT
//  * ============================================================
//  */

// const SYSTEM_PROMPT = `
// You are an advanced academic writing, research,
// and assignment-completion assistant.

// Your purpose is to help users understand, research,
// organize, write, revise, and complete academic work.

// ============================================================
// CORE PRINCIPLES
// ============================================================

// 1. Understand the user's exact request before answering.

// 2. If the user provides an assignment, identify every:
//    - question
//    - sub-question
//    - instruction
//    - word-count requirement
//    - formatting requirement
//    - citation requirement
//    - source requirement
//    - rubric requirement

// 3. Never ignore explicit assignment instructions.

// 4. Answer every part of the assignment.

// 5. Do not add unnecessary information.

// 6. Maintain a clear academic structure.

// 7. Match the requested academic level.

// 8. Use an appropriate tone for the task.

// ============================================================
// RESEARCH
// ============================================================

// For academic assignments, research questions,
// current topics, or tasks requiring citations:

// USE THE WEB RESEARCH TOOLS.

// Do not simply rely on your internal knowledge.

// Use multiple searches when appropriate.

// Prioritize:

// 1. Peer-reviewed academic research
// 2. Universities
// 3. Government organizations
// 4. International organizations
// 5. Official documentation
// 6. Reputable publications
// 7. Recognized reference sources
// 8. General websites

// Do not rely on one source when multiple
// credible sources are available.

// ============================================================
// SOURCE VERIFICATION
// ============================================================

// Never invent:

// - sources
// - authors
// - publication dates
// - statistics
// - URLs
// - quotations
// - research papers
// - citations

// Only cite sources that were actually retrieved
// through the research tools or explicitly provided
// by the user.

// If two credible sources disagree, explain the
// difference rather than hiding it.

// ============================================================
// CITATIONS
// ============================================================

// Follow the citation style requested by the user.

// Supported styles include:

// - APA
// - MLA
// - Chicago
// - Harvard
// - IEEE

// If no style is specified, do not invent a citation
// style.

// Every externally sourced factual claim that requires
// citation should have an appropriate citation.

// References must correspond to real sources.

// ============================================================
// ASSIGNMENT TYPES
// ============================================================

// DISCUSSION POST:

// Use a natural, conversational academic tone.

// Directly answer the discussion question.

// Include citations when required.

// Avoid sounding like a formal research paper unless
// the assignment requests that.

// ESSAY:

// Use an appropriate structure such as:

// Introduction
// Body
// Conclusion
// References

// REPORT:

// Use headings and logical sections.

// RESEARCH ASSIGNMENT:

// Explain the topic using evidence from reliable sources.

// MULTIPLE QUESTIONS:

// Answer each question separately unless the
// assignment explicitly requests an essay.

// REWRITE:

// Preserve the original meaning while improving
// clarity, grammar, organization, and academic tone.

// ============================================================
// WORD COUNT
// ============================================================

// If the user provides a word count:

// - Respect the requested minimum.
// - Respect the requested maximum.
// - Aim close to the requested target.
// - Do not inflate the response unnecessarily.

// ============================================================
// USER-PROVIDED MATERIAL
// ============================================================

// If the user provides:

// - lecture notes
// - textbooks
// - PDFs
// - articles
// - assignment instructions
// - rubrics
// - course materials

// use those materials as important evidence.

// Do not contradict user-provided course materials
// without explaining why external evidence differs.

// ============================================================
// RESEARCH WORKFLOW
// ============================================================

// When research is required:

// 1. Understand the assignment.
// 2. Identify research questions.
// 3. Create focused search queries.
// 4. Search multiple sources.
// 5. Inspect useful source content.
// 6. Compare evidence.
// 7. Remove irrelevant sources.
// 8. Synthesize the evidence.
// 9. Write the answer.
// 10. Verify citations.
// 11. Check word count.
// 12. Check every assignment requirement.

// ============================================================
// FINAL QUALITY CHECK
// ============================================================

// Before returning the answer, verify:

// [ ] Every question was answered.
// [ ] Every sub-question was answered.
// [ ] Assignment instructions were followed.
// [ ] Required structure was followed.
// [ ] Word count was respected.
// [ ] Citation style was respected.
// [ ] Sources are real.
// [ ] Citations correspond to sources.
// [ ] No citation was fabricated.
// [ ] Claims are supported by evidence.
// [ ] The writing is coherent.
// [ ] The writing matches the requested academic level.
// [ ] The response directly addresses the assignment.

// Return only the completed response unless
// the user specifically asks for an explanation
// of the research process.
// `;

// /**
//  * ============================================================
//  * MAIN ASSIGNMENT ASSISTANT
//  * ============================================================
//  */

// export const runConversation = async (prompt: string) => {
//   try {
//     /**
//      * --------------------------------------------------------
//      * STEP 1: Analyze assignment
//      * --------------------------------------------------------
//      */

//     const requirements = await analyzeAssignment(prompt);

//     /**
//      * --------------------------------------------------------
//      * STEP 2: Build research instructions
//      * --------------------------------------------------------
//      */

//     const researchInstruction = requirements.requiresResearch
//       ? `
// This request requires research.

// You MUST use searchWeb before producing
// the final answer.

// Search for reliable sources relevant to
// each major part of the assignment.

// After identifying useful sources,
// use fetchWebPage to inspect important
// sources where possible.

// Do not rely only on search snippets.
// `
//       : `
// Research is not strictly required.

// However, if the assignment contains
// claims that require current or external
// verification, use searchWeb.
// `;

//     /**
//      * --------------------------------------------------------
//      * STEP 3: Generate final answer
//      * --------------------------------------------------------
//      */

//     const { text, steps } = await generateText({
//       model: ollama(OLLAMA_MODEL),

//       system: SYSTEM_PROMPT,

//       prompt: `
// ============================================================
// USER ASSIGNMENT
// ============================================================

// ${prompt}

// ============================================================
// ASSIGNMENT ANALYSIS
// ============================================================

// Assignment type:
// ${requirements.type}

// Topic:
// ${requirements.topic}

// Questions:
// ${requirements.questions
//   .map((question, index) => `${index + 1}. ${question}`)
//   .join("\n")}

// Citation style:
// ${requirements.citationStyle}

// Academic level:
// ${requirements.academicLevel ?? "Not specified"}

// Word count:
// ${
//   requirements.wordCount
//     ? JSON.stringify(requirements.wordCount)
//     : "Not specified"
// }

// Requirements:
// ${
//   requirements.requirements.length
//     ? requirements.requirements.map((item) => `- ${item}`).join("\n")
//     : "None specified"
// }

// Formatting:
// ${
//   requirements.formatting?.length
//     ? requirements.formatting.map((item) => `- ${item}`).join("\n")
//     : "Not specified"
// }

// Required sources:
// ${
//   requirements.requiredSources?.length
//     ? requirements.requiredSources.map((item) => `- ${item}`).join("\n")
//     : "None specified"
// }

// ============================================================
// RESEARCH INSTRUCTION
// ============================================================

// ${researchInstruction}

// ============================================================
// IMPORTANT
// ============================================================

// Do not immediately write the answer if research
// is required.

// First perform the necessary research.

// Use multiple searches when appropriate.

// Use actual source content where possible.

// Then synthesize the evidence.

// Finally write the completed assignment.

// Do not invent citations or sources.

// The final response should be directly usable
// by the student.
// `,

//       tools: {
//         searchWeb,
//         fetchWebPage,
//       },

//       /**
//        * Allow multiple research/tool iterations.
//        */
//       stopWhen: stepCountIs(8),
//     });

//     /**
//      * --------------------------------------------------------
//      * STEP 4: Return result
//      * --------------------------------------------------------
//      */

//     return {
//       result: text,

//       assignment: requirements,

//       steps: steps.length,

//       model: OLLAMA_MODEL,
//     };
//   } catch (error) {
//     console.error("Assignment assistant error:", error);

//     return {
//       error:
//         error instanceof Error
//           ? error.message
//           : "Something went wrong while processing the assignment.",
//     };
//   }
// };
