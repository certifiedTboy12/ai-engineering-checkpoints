def generate_chat_response(message: str) -> str:
    return f"AI response to: {message}"


def generate_quiz(topic: str, number_of_questions: int) -> list[dict[str, object]]:
    questions: list[dict[str, object]] = []

    for _i in range(1, number_of_questions + 1):
        questions.append({
            "question": f"What is an important concept in {topic}?",
            "options": [
                "Option A",
                "Option B",
                "Option C",
                "Option D"
            ],
            "answer": "Option A"
        })

    return questions


def generate_summary(text: str, max_bullets: int):
    sentences = [
        sentence.strip()
        for sentence in text.split(".")
        if sentence.strip()
    ]

    return sentences[:max_bullets]