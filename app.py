import streamlit as st
import partie1
import partie3

st.set_page_config(page_title="SoccerStat - Dashboard global", layout="wide")

#Chargement des données communes
df = partie1.safe_read_csv("top5-players.csv")
df = df.drop_duplicates().dropna(how="all")
df["Nation_code"] = df["Nation"].str.split(" ").str[-1]

#Barre latérale principale
st.sidebar.title("Navigation générale")
page = st.sidebar.radio("Aller à :", ["Partie 1 - Nations & Postes", "Partie 3 - Ligues & Joueurs"])

#PARTIE 1
if page == "Partie 1 - Nations & Postes":
    section = st.sidebar.radio("Sous-section :", ["Accueil", "Joueurs par poste", "Joueurs par nation"])
    if section == "Accueil":
        partie1.show_home(df)
    elif section == "Joueurs par poste":
        partie1.show_players_by_position(df)
    else:
        partie1.show_players_by_nation(df)

#PARTIE 3
elif page == "Partie 3 - Ligues & Joueurs":
    df3 = partie3.load_data()
    df3 = partie3.preprocess_data(df3)
    partie3.show_sidebar(df3)
    partie3.render_analysis(df3)
