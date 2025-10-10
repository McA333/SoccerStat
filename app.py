import streamlit as st
import partie1
import partie3

st.set_page_config(page_title="SoccerStat - Dashboard global", layout="wide")

#MENU PRINCIPAL
st.sidebar.title("Navigation générale")
page = st.sidebar.radio(
    "Aller à :", 
    ["Partie 1 - Nations & Postes", "Partie 3 - Ligues & Joueurs"]
)

#ROUTAGE DES PAGES
if page == "Partie 1 - Nations & Postes":
    partie1.main()  

elif page == "Partie 3 - Ligues & Joueurs":
    partie3.main()
