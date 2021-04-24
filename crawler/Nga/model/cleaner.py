import re

def cleanRealEstateDescription(texts):
    result = []
    for text in texts:
        text = text.lower()
        regrex_pattern = re.compile(pattern="["
                                            u"\U0001F600-\U0001F64F"  # emoticons
                                            u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                                            u"\U0001F680-\U0001F6FF"  # transport & map symbols
                                            u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                                            "]+", flags=re.UNICODE)
        text = regrex_pattern.sub(r'', text)
        text = re.sub("(0[0-9]{9})|([0-9]{4}\.[0-9]{3}\.[0-9]{3})", "#PHONE", text)
        text = re.sub("[0-9]+,?[0-9]*","#NUMBER", text)
        result.append(text)
    return result