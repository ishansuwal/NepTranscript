
from backend.translation import translate_text


sentences = [
    "हामीले वाचन सुन्यौँ।",
    "हामीले पुराणको पाठ सुन्यौँ।",
    "हामीले पुराणको कथा सुन्यौँ।",
    "हामीले ऐतिहासिक पुराण सुन्यौँ।"
]
for sentence in sentences:
    result = translate_text(sentence)

    print("\n===== ENGLISH TRANSLATION =====")
    print(result)
