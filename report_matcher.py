# Use KMP to search features like "brown eyes", "red shirt", etc.

def kmp_search(text, pattern):
    # return True if pattern exists in text
    ...

def match_report(child_reports, observed_description):
    matched_reports = []
    for name, report_text in child_reports.items():
        if kmp_search(report_text.lower(), observed_description.lower()):
            matched_reports.append(name)
    return matched_reports

# report_matcher.py
def build_lps(pattern):
    lps = [0] * len(pattern)
    length = 0  # length of the previous longest prefix suffix
    i = 1

    while i < len(pattern):
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1
    return lps

def kmp_search(text, pattern):
    text = text.lower()
    pattern = pattern.lower()
    lps = build_lps(pattern)
    i = j = 0

    while i < len(text):
        if pattern[j] == text[i]:
            i += 1
            j += 1

        if j == len(pattern):
            return True  # Match found
        elif i < len(text) and pattern[j] != text[i]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1
    return False

def match_report(child_reports, observed_description):
    matched = []
    for name, report in child_reports.items():
        if kmp_search(report, observed_description):
            matched.append(name)
    return matched
