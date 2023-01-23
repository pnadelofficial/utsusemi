import streamlit as st 
import spacy
from spacy import displacy
import base64
from annotated_text import annotated_text

nlp = spacy.load('ja_core_news_sm')

st.title('Utsusemi Exercise')

# POEMS = [
#     'うつせみの命を惜しみ波に濡れ伊良湖の島の玉藻をきり食む',
#     'うつせみは数なき身なり山川のさやけき見つつ道を尋ねな'
# ]

POEMS = {
    'Manyoshu 871':('''
    うつせみの
    命を惜しみ
    波に濡れ
    伊良湖の島の
    玉藻をきり食む
    ''', '''
    Loathe to leave
    This cicada husk life, 
    Wet with waves, 
    I cut and eat 
    The seaweed of Irago Island.
    '''),
    'Manyoshu 849':('''
    うつせみは
    数なき身なり
    山川の
    さやけき見つつ
    道を尋ねな
    ''', '''
    I am but the evanescent 
    shell of a cicada—
    Let me gaze on the clarity 
    Of mountains and rivers
    While I search for the Way
    ''')
}

glosses = {
    'うつせみ':"cicada's husk",
    'の':'possessive particle',
    '命':'life',
    'は':'particle showing topic',
    '尋ね':'to be seeking out'
}

# from https://github.com/explosion/spacy-streamlit/blob/master/spacy_streamlit/util.py
def get_html(html: str):
    """Convert HTML so it can be rendered."""
    WRAPPER = """<div style="overflow-x: auto; border: 0px solid #e6e9ef; border-radius: 0.25rem; padding: 1rem; margin-bottom: 2.5rem">{}</div>"""
    # Newlines seem to mess with the rendering
    html = html.replace("\n", " ")
    return WRAPPER.format(html)

def get_svg(svg: str, style: str = "", wrap: bool = True):
    """Convert an SVG to a base64-encoded image."""
    b64 = base64.b64encode(svg.encode("utf-8")).decode("utf-8")
    html = f'<img src="data:image/svg+xml;base64,{b64}" style="{style}"/>'
    return get_html(html) if wrap else html

def get_deps(nlp, text):
    doc = nlp(text.replace('\n    ',''))
    words = []
    for token in doc:
        if token.text == 'うつせみ':
            annotated_text(
                (token.text, token.pos_), 
                (token.head.text, token.head.pos_)
            )
            words.append(token.text)
            c = [child for child in token.children][0]
            words.append(c.text)
            words.append(token.head.text)

    subdoc = nlp(''.join(words))
    deps_parse = displacy.parse_deps(subdoc)
    for d in deps_parse['words']:
        d['lemma'] = f"{glosses[d['text']]}"
    html = displacy.render(
        deps_parse, style='dep',manual=True
    )
    html = html.replace('\n\n','\n')
    st.write(get_svg(html),unsafe_allow_html=True)
    st.write("<hr style='width: 75%;margin: auto;'>",unsafe_allow_html=True)
    

for i, poem in enumerate(POEMS):
    st.write(f'**{poem}**')
    col1, col2 = st.columns(2)
    with col1:
        st.write(f"{POEMS[poem][0].replace('    ','<br>')}", unsafe_allow_html=True)
    with col2:
        st.write(f"{POEMS[poem][1].replace('    ','<br>')}", unsafe_allow_html=True)
    get_deps(nlp, POEMS[poem][0])