import re

SQL_ERROR_PATTERNS = [
    "sql syntax",
    "mysqli",
    "mysql",
    "warning",
    "fatal error"
]

def extract_features(normal_text, injected_text, status_code, normal_time, injected_time):

    length_diff = len(injected_text) - len(normal_text)

    error_score = 0
    for pattern in SQL_ERROR_PATTERNS:
        if re.search(pattern, injected_text):
            error_score += 1

    time_diff = injected_time - normal_time

    return [
        length_diff,
        error_score,
        status_code,
        time_diff
    ]