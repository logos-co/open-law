import re

# as per recommendation from @freylis, compile once only
CLEANR = re.compile("<.*?>")


def clean_html(raw_html):
    clean_text = re.sub(CLEANR, "", raw_html)
    return clean_text
