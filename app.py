import streamlit as st
from annotated_text import annotated_text
import pandas as pd
import spacy
from spacy.tokens import DocBin

st.title('Utsusemi: Japanese Dependency Parsing')

# data
@st.cache(allow_output_mutation=True)
def load_model():
    return spacy.load('ja_core_news_sm')
nlp = load_model()

option = st.selectbox(
    'Select text to search',
    ('万葉集 (Manyoshū)', '古今集 (Kokinshū)'))

@st.cache(allow_output_mutation=True)
def get_data(option):
    if option == '万葉集 (Manyoshū)':
        from_csv = pd.read_csv('manyoshu.csv')
    elif option == '古今集 (Kokinshū)':
        from_csv = pd.read_csv('kokinshu_sents.csv')
    return from_csv
from_csv = get_data(option)

# search
def word_search(search, raw_title, spacy_doc):
    if len(raw_title.split('_')[0]) > 0:
        title = f'{raw_title.split("_")[0].strip()} -- Poem {raw_title.split("_")[1]}'
    else:
        title = f'Poem {raw_title.split("_")[1]}'

    for token in spacy_doc:
        if ((token.text.lower() == search) or (token.text.title() == search)) and (token.head.pos_ != 'PUNCT'):
            st.markdown(f'*from {title}*')
            annotated_text(
                (token.text, token.pos_), 
                (token.head.text, token.head.pos_)
                )
            st.write(spacy_doc.text)
            st.markdown('<hr>',unsafe_allow_html=True)

# interface
search = st.text_input('Search term', '空蝉')

if option == '万葉集 (Manyoshū)':
    bytes_file = open('serialized_data/manyoshu_spacy_output','rb').read()
    st.markdown(f'Currently searching: [{option}](https://jti.lib.virginia.edu/japanese/manyoshu/AnoMany.html)')
elif option == '古今集 (Kokinshū)':
    bytes_file = open('serialized_data/kokinshu_spacy_output','rb').read()
    st.markdown(f'Currently searching: [{option}](https://jti.lib.virginia.edu/japanese/kokinshu/kikokin.html)')

doc_bin = DocBin().from_bytes(bytes_file)
from_csv['spacy_docs'] =  pd.Series(doc_bin.get_docs(nlp.vocab))
st.markdown('<hr>',unsafe_allow_html=True) 

p = from_csv.apply(lambda x: word_search(search.lower(), x['title'], x['spacy_docs']),axis=1)

st.markdown('<small>Assembled by Peter Nadel | TTS Research Technology</small>', unsafe_allow_html=True)