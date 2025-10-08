import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

st.set_page_config(page_title="MARIEMAVIE - SoccerStat", layout="wide")

sns.set_theme(style="whitegrid")
st.markdown(
    """
    <style>
    .main { background-color: #f9fafb; }
    h1, h2, h3 { color: #1a1a1a; }
    </style>
    """,
    unsafe_allow_html=True
)

def safe_read_csv(path):
    for sep in [",", ";", "\t", "|"]:
        try:
            df = pd.read_csv(path, sep=sep)
            if df.shape[1] > 1:
                return df
        except Exception:
            continue
    raise ValueError(f"Impossible de lire correctement le fichier : {path}")

df = safe_read_csv("top5-players.csv")
df = df.drop_duplicates().dropna(how="all")
df["Nation_code"] = df["Nation"].str.split(" ").str[-1]

st.sidebar.header("Filtres & Navigation")
section = st.sidebar.radio("Aller à :", ["Accueil", "Joueurs par poste", "Joueurs par nation"])
st.sidebar.divider()
st.sidebar.write("Créé par : **MARIEMAVIE**")

if section == "Accueil":
    st.title("Dashboard officiel de Rajeeva")
    st.markdown("""
    ### Bienvenue sur le projet *SoccerStat*  

    Explorez les données des meilleurs joueurs des 5 grands championnats européens (2023/24).  
    Vous pouvez analyser :
    - La répartition des joueurs par poste  
    - La représentation par nation  
    - Utiliser des filtres interactifs pour affiner votre analyse
    """)
    st.info("Utilisez le menu à gauche pour naviguer entre les sections.")

elif section == "Joueurs par poste":
    st.header("Répartition des joueurs par poste")
    
    postes = sorted(df["Pos"].dropna().unique())
    selected_postes = st.multiselect("Sélectionnez un ou plusieurs postes :", postes, default=postes)
    filtered_df = df[df["Pos"].isin(selected_postes)]

    fig, ax = plt.subplots(figsize=(8, 5))
    sns.countplot(x="Pos", data=filtered_df, order=filtered_df["Pos"].value_counts().index, palette="viridis", ax=ax)
    ax.set_title("Distribution des joueurs par poste", fontsize=14)
    ax.set_xlabel("Poste")
    ax.set_ylabel("Nombre de joueurs")
    st.pyplot(fig)

    st.subheader("Statistiques clés")
    col1, col2 = st.columns(2)
    col1.metric("Postes affichés", len(selected_postes))
    col2.metric("Total joueurs", len(filtered_df))

elif section == "Joueurs par nation":
    st.header("Répartition des joueurs par nation")

    top_n = st.slider("Choisissez combien de nations afficher :", 5, 30, 15)
    nation_counts = df["Nation_code"].value_counts().head(top_n)

    col1, col2 = st.columns([2, 1])

    with col1:
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(x=nation_counts.values, y=nation_counts.index, palette="magma", ax=ax)
        ax.set_title(f"Top {top_n} nations représentées", fontsize=15, fontweight="bold")
        ax.set_xlabel("Nombre de joueurs", fontsize=12)
        ax.set_ylabel("Nation", fontsize=12)
        st.pyplot(fig)

    with col2:
        st.subheader("Répartition (camembert)")
        fig2, ax2 = plt.subplots(figsize=(4, 4))
        ax2.pie(
            nation_counts.values,
            labels=nation_counts.index,
            autopct="%1.1f%%",
            startangle=90,
            colors=sns.color_palette("magma", len(nation_counts))
        )
        ax2.axis("equal")
        st.pyplot(fig2)

    st.info(f"Le top {top_n} inclut les nations les plus représentées dans les 5 grands championnats.")
