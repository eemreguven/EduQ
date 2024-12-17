PROMPT_TEMPLATE = """
Answer the question based only on the following context:

{context}

---

Answer the question based on the above context: {question}
"""

ALLOWED_EXTENSIONS = {'pdf', 'txt', 'doc', 'docx'}

CHROMA_FOLDER_PATH = "rag-system\chroma"
UPLOAD_FOLDER_PATH = "rag-system\data"
DOWNLOAD_FOLDER_PATH = "downloads"
MAX_CONTENT_LENGTH =  5 * 1024 * 1024
CHARACTER_LIMIT = 100000

question_types = [
        "True/False",
        "Multiple Choice",
        "Fill-in-the-Blank",
        "Scenario-Based",
        "Comparison",
        "Cause and Effect",
        "Argument-Based",
        "Creative Suggestion",
        "Open-Ended Problem Solving"
    ]

prompt_templates = {
    "True/False": {
        "question_format": """Generate a True/False question in the following format:
            - Question: True or False? [Write a statement here that can be answered as True or False.]
            - Answer: [True/False]""",
        "easy": "Create a simple true/false question that tests the reader's recall of basic facts based on the context provided.",
        "medium": "Write a true/false question that tests the reader's understanding of a slightly nuanced fact or concept based on the context provided.",
        "difficult": "Develop a challenging true/false question that requires the reader to evaluate a complex concept or a less commonly known fact based on the context provided.",
    },
    "Multiple Choice": {
        "question_format": """Generate a multiple-choice question in the following format:
            - Question: [Question text here]
                Options:
                    A) [Option 1]
                    B) [Option 2]
                    C) [Option 3]
                    D) [Option 4]
            - Answer: [Correct option letter, e.g., A)]""",
        "easy": "Create a multiple-choice question with one correct answer and three simple distractors, focusing on basic facts based on the context provided.",
        "medium": "Write a multiple-choice question that tests the reader's understanding of concepts based on the context provided. Include one correct answer and three plausible distractors that require careful thought.",
        "difficult": "Generate a complex multiple-choice question that requires the reader to apply knowledge or analyze a concept based on the context provided. Include subtle distractors.",
    },
    "Fill-in-the-Blank": {
        "question_format": """Generate a fill-in-the-blank question in the following format:
            - Question: [Sentence with a blank space represented as ______ here]
            - Answer: [The correct word or phrase to fill in the blank]""",
        "easy": "Write a simple fill-in-the-blank question that tests the recall of basic facts or terms based on the context provided.",
        "medium": "Create a fill-in-the-blank question that tests understanding of a concept based on the context provided.",
        "difficult": "Generate a challenging fill-in-the-blank question that requires the reader to synthesize knowledge or recall complex terms based on the context provided.",
    },
    "Scenario-Based": {
        "question_format": """Generate a scenario-based question in the following format:
            - Question: [Provide a detailed description of the scenario.]
                        [Ask a question related to the scenario that requires applying knowledge or reasoning.]
            - Answer: [Provide the solution or explanation for the question.]""",
        "easy": "Write a scenario-based question that asks the reader to apply basic knowledge from the context provided to a simple and familiar situation.",
        "medium": "Create a scenario-based question that involves applying knowledge from the context provided to a moderately complex or slightly unfamiliar situation.",
        "difficult": "Develop a complex scenario-based question that requires applying advanced knowledge or solving a multi-step problem based on the context provided.",
    },
    "Comparison": {
        "question_format": """Generate a comparison question in the following format:
            - Question: Compare [Concept A] and [Concept B] and identify their key similarities and/or differences.
            - Answer: [Provide the key similarities or differences between the concepts.]""",
        "easy": "Write a comparison question that asks the reader to identify simple differences or similarities between two basic concepts based on the context provided.",
        "medium": "Create a comparison question that requires the reader to analyze and compare two moderately complex concepts based on the context provided.",
        "difficult": "Develop a challenging comparison question that involves evaluating subtle distinctions or trade-offs between advanced concepts based on the context provided.",
    },
    "Cause and Effect": {
        "question_format": """Generate a cause-and-effect question in the following format:
            - Question: [Cause-and-effect relationship question]
            - Answer: [Explanation of the cause and effect]""",
        "easy": "Create a cause-and-effect question that asks the reader to identify a straightforward relationship based on the context provided.",
        "medium": "Write a cause-and-effect question that requires understanding and explanation of a moderately complex relationship based on the context provided.",
        "difficult": "Generate a challenging cause-and-effect question that requires evaluating complex interactions or chains of events based on the context provided.",
    },
    "Argument-Based": {
        "question_format": """Generate an argument-based question in the following format:
            - Question: [Question text here]\n
            - Answer: [Position/justification]""",
        "easy": "Write an argument-based question that asks the reader to take a simple position on a basic issue based on the context provided and justify it.",
        "medium": "Create an argument-based question that requires the reader to analyze and take a position on a moderately complex issue based on the context provided.",
        "difficult": "Develop a challenging argument-based question that requires the reader to construct a nuanced argument or counterargument on a complex issue based on the context provided.",
    },
    "Creative Suggestion": {
        "question_format": """Generate a creative suggestion question in the following format:
            - Question: Suggest an innovative solution or improvement for the following problem: [Problem description here].
            - Answer: [Provide a creative or innovative solution to the problem.]""",
        "easy": "Create a question that asks the reader to suggest a simple improvement or idea based on the context provided.",
        "medium": "Write a question that requires the reader to propose a moderately innovative solution to a real-world problem based on the context provided.",
        "difficult": "Generate a creative suggestion question that challenges the reader to think of an innovative, out-of-the-box solution to a complex issue based on the context provided.",
    },
    "Open-Ended Problem Solving": {
        "question_format": """Generate an open-ended problem-solving question in the following format:
            - Question: Propose a solution to the following problem: [Problem description here].
            - Answer: [Provide a solution, explaining the approach or reasoning used to solve the problem.]""",
        "easy": "Write a simple open-ended problem-solving question that asks the reader to propose a basic solution to a well-defined problem based on the context provided.",
        "medium": "Create an open-ended problem-solving question that involves solving a moderately complex problem based on the context provided.",
        "difficult": "Generate an open-ended problem-solving question that requires proposing a comprehensive solution to a complex or multi-faceted problem based on the context provided.",
    },
}
