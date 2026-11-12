import re


EMAIL_PATTERN = re.compile(
    r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
)

PHONE_PATTERN = re.compile(
    r"(?<![\w+])(?:\+62|62|0)[\s().-]*8(?:[\s().-]*\d){8,11}(?!\d)"
)

NIK_PATTERN = re.compile(
    r"(?<!\d)\d{16}(?!\d)"
)

RT_RW_PATTERN = re.compile(
    r"\bRT\s*\d{1,3}\s*/\s*RW\s*\d{1,3}\b",
    re.IGNORECASE,
)

# Address labels in the Indonesian and English spellings commonly found on
# CVs. The five test CVs use "Full address", "Home address", "Address",
# "Residential address" and "Mailing address".
ADDRESS_LABEL_PATTERN = re.compile(
    r"(?i)^\s*(?:"
    r"(?:full|home|residential|mailing|current|correspondence|postal)\s+address"
    r"|address"
    r"|alamat(?!\s+e-?mail)"
    r"(?:\s+(?:rumah|lengkap|domisili|korespondensi|ktp|tinggal))?"
    r"|domisili"
    r")\s*(?:\([^)]*\))?\s*[:\-]\s*(?P<value>.+)$"
)

DATE_OF_BIRTH_PATTERN = re.compile(
    r"(?i)^\s*(?:"
    r"date\s+of\s+birth|birth\s+date|dob"
    r"|tanggal\s+lahir|ttl|tempat\s*,?\s*tanggal\s+lahir"
    r")\s*(?:\([^)]*\))?\s*[:\-]\s*(?P<value>.+)$"
)

EMERGENCY_CONTACT_PATTERN = re.compile(
    r"(?i)^\s*(?:emergency\s+contact|kontak\s+darurat)"
    r"\s*(?:\([^)]*\))?\s*[:\-]\s*(?P<value>.+)$"
)

# Label-less address detection: a line that starts with a street or building
# keyword and also contains a number is treated as an address. Requiring a
# number keeps technical text such as "Drive innovation" or "St. Mary's
# School" from being masked by mistake.
STREET_KEYWORDS = (
    r"jl\.?|jln\.?|jalan|gg\.?|gang|lorong|simpang|"
    r"komplek(?:s)?|komp\.?|perumahan|perum\.?|blok|"
    r"kav(?:ling)?\.?|ruko|"
    r"street|st\.|road|rd\.|avenue|boulevard|blvd\."
)

STREET_LINE_PATTERN = re.compile(
    rf"(?i)^(?:{STREET_KEYWORDS})(?![a-z])(?=.*\d).*$"
)

# Checked in order so that a longer label (address) is not swallowed by a
# shorter one (date of birth / emergency contact).
LABEL_RULES = (
    (ADDRESS_LABEL_PATTERN, "[ADDRESS_REDACTED]"),
    (DATE_OF_BIRTH_PATTERN, "[DOB_REDACTED]"),
    (EMERGENCY_CONTACT_PATTERN, "[EMERGENCY_CONTACT_REDACTED]"),
)

SEGMENT_SEPARATOR = "|"


def mask_personal_information(text: str) -> str:
    """Mask common personal identifiers in CV text.

    Each line is handled separately and split on ``|`` so that several
    identifiers sharing a line - for example an address followed by a date
    of birth - are masked with the correct label instead of one blanket
    replacement eating the whole line.
    """

    return "".join(_mask_line(line) for line in text.splitlines(keepends=True))


def _mask_line(line: str) -> str:
    body, ending = _split_line_ending(line)
    masked = SEGMENT_SEPARATOR.join(
        _mask_segment(segment) for segment in body.split(SEGMENT_SEPARATOR)
    )
    return masked + ending


def _split_line_ending(line: str) -> tuple[str, str]:
    for ending in ("\r\n", "\n", "\r"):
        if line.endswith(ending):
            return line[: -len(ending)], ending
    return line, ""


def _mask_segment(segment: str) -> str:
    for pattern, placeholder in LABEL_RULES:
        match = pattern.match(segment)
        if match:
            value = segment[match.start("value"): match.end("value")]
            trailing = value[len(value.rstrip()):]
            return (
                segment[: match.start("value")]
                + placeholder
                + trailing
                + segment[match.end("value"):]
            )

    leading_chars = re.match(r"^[\s•*\-–—]*", segment).group(0)
    content = segment[len(leading_chars):].rstrip()
    if content and STREET_LINE_PATTERN.match(content):
        trailing = segment[len(leading_chars) + len(content):]
        return leading_chars + "[ADDRESS_REDACTED]" + trailing

    segment = EMAIL_PATTERN.sub("[EMAIL_REDACTED]", segment)
    segment = PHONE_PATTERN.sub("[PHONE_REDACTED]", segment)
    segment = NIK_PATTERN.sub("[NIK_REDACTED]", segment)
    segment = RT_RW_PATTERN.sub("[RT_RW_REDACTED]", segment)
    return segment
