import streamlit as st

st.title("Sobre o Lucas")

col1, col2 = st.columns(2,gap= "small", vertical_alignment="center")

with col1:
    st.image("assets/okr_expert.png")
with col2:
    st.markdown("""
Lucas é o seu especialista em OKRs (Objetivos e Resultados-Chave), sempre disponível para ajudar você a criar, revisar e entender melhor suas metas. Criado pela AIMANA especialmente para os funcionários do Marista, o Lucas combina conhecimento profundo em OKRs com uma abordagem amigável e acessível.

Seja você um iniciante ou alguém com experiência em OKRs, o Lucas está aqui para responder suas dúvidas, oferecer sugestões personalizadas e guiar você em cada etapa da criação de objetivos alinhados e eficazes. Com Lucas, você terá um apoio constante para garantir que suas metas estejam sempre claras, mensuráveis e impactantes.

Explore todas as funcionalidades do Lucas e veja como ele pode facilitar seu caminho para o sucesso!""")





