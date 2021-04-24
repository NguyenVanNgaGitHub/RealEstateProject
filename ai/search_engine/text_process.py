import re

class TextProcess:
    def extract_words(self, text):
        text = text.lower()
        regrex_pattern = re.compile(pattern="["
                                            u"\U0001F600-\U0001F64F"  # emoticons
                                            u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                                            u"\U0001F680-\U0001F6FF"  # transport & map symbols
                                            u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                                            "]+", flags=re.UNICODE)
        text = regrex_pattern.sub(r'', text)
        text = re.sub(r'[\n\t.,;?!()=\[\]{}\-\^:–—_+*/`”“’"\'\\$%#@&|<>…]',' ',text)
        text = re.sub(r'[0-9]',' ',text)
        text = text.strip()
        tokens = re.split("[ ]+",text)
        return set([tok for tok in tokens if len(tok)>=1])