import streamlit as st
from annotated_text import annotated_text
import pandas as pd
import spacy
from spacy.tokens import DocBin

st.title('Utsusemi: Japanese Dependency Parsing')
st.markdown('Searching [万葉集](https://jti.lib.virginia.edu/japanese/manyoshu/AnoMany.html)')

# data
@st.cache(allow_output_mutation=True)
def load_model():
    return spacy.load('ja_core_news_sm')
nlp = load_model()

@st.cache(allow_output_mutation=True)
def get_data():
    from_csv = pd.read_csv('manyoshu.csv')
    return from_csv
from_csv = get_data()

bytes_file = open('serialized_data/manyoshu_spacy_output','rb').read()
doc_bin = DocBin().from_bytes(bytes_file)
from_csv['spacy_docs'] =  pd.Series(doc_bin.get_docs(nlp.vocab))

# search
def word_search(search, spacy_doc, lemma_search=False):
    if lemma_search:
        for token in spacy_doc:
            if ((token.lemma_.lower() == search) or (token.lemma_.title() == search)) and (token.head.pos_ != 'PUNCT'):
                annotated_text(
                    (token.text, token.pos_), 
                    (token.head.text, token.head.pos_)
                    )
                st.write(spacy_doc.text)
                st.markdown('<hr>',unsafe_allow_html=True)   
    else:
        for token in spacy_doc:
            if ((token.text.lower() == search) or (token.text.title() == search)) and (token.head.pos_ != 'PUNCT'):
                annotated_text(
                    (token.text, token.pos_), 
                    (token.head.text, token.head.pos_)
                    )
                st.write(spacy_doc.text)
                st.markdown('<hr>',unsafe_allow_html=True)

# interface
lemma_search = st.checkbox('Search lemmas')
search = st.text_input('Search term', '空蝉')

for i,sd in enumerate(from_csv['spacy_docs'].to_list()):
    word_search(search.lower(), sd, lemma_search)

st.markdown('<small>Assembled by Peter Nadel | TTS Research Technology</small>', unsafe_allow_html=True)