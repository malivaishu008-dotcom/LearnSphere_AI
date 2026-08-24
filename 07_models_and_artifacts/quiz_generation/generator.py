def generate_quiz_questions(text_corpus, num_questions=5):
    return [
        {"question_id": i + 1, "prompt": f"Generated question {i + 1} from context."}
        for i in range(num_questions)
    ]