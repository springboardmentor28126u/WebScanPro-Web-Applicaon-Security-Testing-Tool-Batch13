import re

XSS_PATTERNS = [
    r"<script>",
    r"alert\(",
    r"onerror=",
    r"onload="
]

def extract_xss_features(normal_text, injected_text, status_code):

    # 1️⃣ Reflection detection
    reflection = 1 if "<script>alert(1)</script>" in injected_text else 0

    # 2️⃣ Script count difference
    script_diff = injected_text.count("<script>") - normal_text.count("<script>")

    # 3️⃣ Length difference
    length_diff = len(injected_text) - len(normal_text)

    # 4️⃣ Suspicious keyword score (SAFE REGEX)
    keyword_score = 0
    for pattern in XSS_PATTERNS:
        if re.search(pattern, injected_text.lower()):
            keyword_score += 1

    return [
        reflection,
        script_diff,
        length_diff,
        keyword_score,
        status_code
    ]