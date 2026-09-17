from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import Runnable, RunnableLambda
from langchain_openai import ChatOpenAI
import re
from typing import cast


# ---------------------------------------------------------
# 1. DECOMPOSER
# ---------------------------------------------------------

decompose_prompt = PromptTemplate.from_template(
    "Split the question into up to 3 concise sub-questions. "
    "Return them as a numbered list (1., 2., 3.), nothing else.\n\n"
    "Question:\n{question}"
)

decomposer = (
    decompose_prompt
    | ChatOpenAI(model="gpt-3.5-turbo", temperature=0.0)
)


def parse_numbered_subquestions(base_msg: object) -> list[str]:
    text = getattr(base_msg, "content", str(base_msg)).strip()

    lines = re.split(r"\r?\n", text)
    subquestions: list[str] = []

    for line in lines:
        match = re.match(r"\s*\d+[.)]\s*(\S.*)$", line)

        if match:
            subquestions.append(match.group(1).strip())

    # Fallback if the model did not return a numbered list
    if not subquestions and text:
        subquestions = [text]

    # Ensure there are never more than 3
    return subquestions[:3]


parse_subq_runnable = RunnableLambda(parse_numbered_subquestions)


# ---------------------------------------------------------
# 2. ANSWER EACH SUB-QUESTION
# ---------------------------------------------------------

answer_prompt = PromptTemplate.from_template(
    "You are a concise assistant. For the sub-question below, produce:\n"
    "Answer: <one-line answer>\n"
    "Steps:\n"
    "- <step1>\n"
    "- <step2>\n"
    "Keep it short.\n\n"
    "Sub-question: {subq}"
)

answer_chain = (
    answer_prompt
    | ChatOpenAI(model="gpt-3.5-turbo")
)


def run_answers(subquestions: list[str]) -> list[dict[str, object]]:
    inputs: list[dict[str, str]] = [
        {"subq": question} for question in subquestions
    ]

    # Run all sub-question answers as a batch
    outputs = answer_chain.batch(inputs)

    parsed: list[dict[str, object]] = []

    for output in outputs:
        text = getattr(output, "content", str(output)).strip()

        answer_line = None
        steps: list[str] = []

        for line in text.splitlines():

            if line.lower().startswith("answer:"):
                answer_line = line.split(":", 1)[1].strip()

            elif re.match(r"\s*[-•]\s+", line):
                step = re.sub(
                    r"^\s*[-•]\s+",
                    "",
                    line
                ).strip()

                steps.append(step)

        parsed.append(
            {
                "answer": answer_line or text,
                "steps": steps or ["(no steps parsed)"],
                "raw": text
            }
        )

    return parsed


run_answers_runnable = RunnableLambda(run_answers)


# ---------------------------------------------------------
# 3. FORMAT SUB-ANSWERS
# ---------------------------------------------------------

def format_subanswers_block(answer_list: list[dict[str, object]]) -> str:
    blocks: list[str] = []

    for i, answer in enumerate(answer_list, start=1):
        blocks.append(
            f"{i}. Answer: {answer['answer']}"
        )

        blocks.append("   Steps:")

        for step in cast(list[str], answer["steps"]):
            blocks.append(f"   - {step}")

    return "\n".join(blocks)


def format_answers_for_prompt(
    answers: list[dict[str, object]],
) -> dict[str, str]:
    return {
        "subanswers_text": format_subanswers_block(answers)
    }


format_runnable = RunnableLambda(
    format_answers_for_prompt
)


# ---------------------------------------------------------
# 4. COMBINER
# ---------------------------------------------------------

combine_prompt = PromptTemplate.from_template(
    "Synthesize a single concise final answer from these "
    "numbered sub-answer blocks.\n\n"
    "Input:\n"
    "{subanswers_text}\n\n"
    "Return exactly three lines:\n"
    "1) Final Answer: <one line>\n"
    "2) Key points: - <p1>; - <p2>\n"
    "3) Confidence: <low/medium/high>"
)

combiner = (
    format_runnable
    | combine_prompt
    | ChatOpenAI(model="gpt-3.5-turbo", temperature=0.0)
)


# ---------------------------------------------------------
# 5. COMPLETE LCEL PIPELINE
# ---------------------------------------------------------

pipeline: Runnable[dict[str, str], object] = (
    decomposer
    | parse_subq_runnable
    | run_answers_runnable
    | combiner
)


# ---------------------------------------------------------
# 6. RUN
# ---------------------------------------------------------

if __name__ == "__main__":

    question = (
        "How can I reduce latency in a web app "
        "that serves ML predictions?"
    )

    final = pipeline.invoke({
        "question": question
    })

    print("\nFinal Result:\n")
    print(getattr(final, "content", str(final)))