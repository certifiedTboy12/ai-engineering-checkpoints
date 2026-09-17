# LCEL No-JSON Example

This project shows how I used LangChain Expression Language (LCEL) to create a simple question-answering pipeline without using JSON.

I used the LCEL pipe (`|`) to connect the different parts of the workflow. The first step breaks the main question into up to three smaller questions. These questions are then parsed and sent to another prompt that generates an answer and a few steps for each one.

I used `batch()` to process the sub-questions together because they are independent of each other. This is more efficient than answering each question separately and can help reduce the overall processing time.

Finally, the answers are formatted and passed to another prompt, which combines them into a short final answer.
