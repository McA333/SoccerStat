import streamlit as st
import partie1
import partie3

st.set_page_config(page_title="SoccerStat - Dashboard complet", layout="wide")

st.sidebar.title("Navigation")
page = st.sidebar.radio("Aller à :", ["Partie 1 - Nations & Postes", "Partie 3 - Ligues & Joueurs"])

if page == "Partie 1 - Nations & Postes":
    partie1.main()   # appelle la fonction main() que tu définis dans partie1.py
elif page == "Partie 3 - Ligues & Joueurs":
    partie3.main()   # appelle celle de partie3.py

