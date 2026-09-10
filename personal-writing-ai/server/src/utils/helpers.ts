import { PDFParse } from "pdf-parse";
import mammoth from "mammoth";
import type { UploadedFile } from "./types.ts";

const MAX_FILE_SIZE = 20 * 1024 * 1024; // 20 MB
const MAX_DOCUMENT_CHARS = 60_000;

function cleanText(text: string): string {
  return text
    .replace(/\r/g, "")
    .replace(/[ \t]+/g, " ")
    .replace(/\n{3,}/g, "\n\n")
    .trim();
}

export function limitText(text: string, max: number): string {
  if (text.length <= max) {
    return text;
  }

  return text.slice(0, max) + "\n\n[Document content truncated]";
}

async function extractPdfText(buffer: Buffer): Promise<string> {
  const parser = new PDFParse({ data: buffer });
  const data = await parser.getText();
  await parser.destroy();

  return cleanText(data.text ?? "");
}

async function extractDocxText(buffer: Buffer): Promise<string> {
  const result = await mammoth.extractRawText({
    buffer,
  });

  return cleanText(result.value ?? "");
}

async function extractTextFile(buffer: Buffer): Promise<string> {
  return cleanText(buffer.toString("utf-8"));
}

async function extractDocumentText(file: UploadedFile): Promise<string> {
  if (file.buffer.length > MAX_FILE_SIZE) {
    throw new Error(`${file.filename} is larger than the 20MB limit.`);
  }

  switch (file.mimeType) {
    case "application/pdf":
      return extractPdfText(file.buffer);

    case "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
      return extractDocxText(file.buffer);

    case "text/plain":
    case "text/markdown":
    case "text/csv":
      return extractTextFile(file.buffer);

    default:
      throw new Error(`Unsupported file type: ${file.mimeType}`);
  }
}

export async function processUploadedFiles(
  files: UploadedFile[],
): Promise<string> {
  if (!files.length) {
    return "";
  }

  const documents: string[] = [];

  for (const file of files) {
    try {
      const text = await extractDocumentText(file);

      if (!text.trim()) {
        documents.push(
          `
[DOCUMENT: ${file.filename}]

No extractable text was found.
`,
        );

        continue;
      }

      documents.push(
        `
============================================================
DOCUMENT: ${file.filename}
============================================================

${limitText(text, MAX_DOCUMENT_CHARS)}
`,
      );
    } catch (error) {
      console.error(`Failed to process ${file.filename}`, error);

      documents.push(
        `
[DOCUMENT: ${file.filename}]

This document could not be processed.
`,
      );
    }
  }

  return documents.join("\n\n");
}
