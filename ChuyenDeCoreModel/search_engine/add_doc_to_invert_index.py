from search_engine.invert_index import InvertIndex
from joblib import load
from search_engine.text_process import TextProcess
import pandas as pd
from joblib import dump

ivt_index : InvertIndex = load("invert_index.lib")


data = pd.read_csv('crawling_real_estate_mogi.vn.csv',header=None,
                   names=['title', 'value', 'area', 'address', 'ward', 'district', 'province',
                          'type', 'description', 'sellerName', 'time', 'source', 'image'])

text_processor = TextProcess()

for idx,row in data.iterrows():
    set_words = text_processor.extract_words(row["description"])
    ivt_index.add_doc(doc_name="mogi"+str(idx), set_tokens=set_words)

dump(ivt_index,"invert_index.lib")




