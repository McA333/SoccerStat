import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import plotly.express as px

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

#SECTION 1 - ACCUEIL
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

    total_players = len(df)
    total_nations = df["Nation_code"].nunique()
    total_positions = df["Pos"].nunique()

    st.divider()
    st.subheader("Résumé global des données")
    col1, col2, col3 = st.columns(3)
    col1.metric("Nombre total de joueurs", total_players)
    col2.metric("Nombre de nations", total_nations)
    col3.metric("Nombre de postes", total_positions)
    st.divider()

    st.info("Utilisez le menu à gauche pour naviguer entre les sections.")

#SECTION 2 - JOUEURS PAR POSTE
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

#SECTION 3 - JOUEURS PAR NATION
elif section == "Joueurs par nation":
    st.header("Répartition des joueurs par nation")

    #Option de tri dynamique
    sort_option = st.radio(
        "Méthode de tri :",
        ["Top joueurs", "Ordre alphabétique"],
        horizontal=True
    )

    top_n = st.slider("Choisissez combien de nations afficher :", 5, 30, 15)
    nation_counts = df["Nation_code"].value_counts()

    if sort_option == "Ordre alphabétique":
        nation_counts = nation_counts.sort_index()
    else:
        nation_counts = nation_counts.sort_values(ascending=False)

    nation_counts = nation_counts.head(top_n)

    col1, col2 = st.columns([2, 1])

    with col1:
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(x=nation_counts.values, y=nation_counts.index, palette="magma", ax=ax)
        ax.set_title(f"Top {top_n} nations représentées", fontsize=15, fontweight="bold")
        ax.set_xlabel("Nombre de joueurs", fontsize=12)
        ax.set_ylabel("Nation", fontsize=12)
        st.pyplot(fig)

    with col2:
        st.subheader("Répartition interactive")

        pie_data = nation_counts.copy()
        if len(pie_data) > 8:
            autres = pie_data[8:].sum()
            pie_data = pie_data.head(8)
            pie_data.loc["Autres"] = autres

        pie_df = pie_data.reset_index()
        pie_df.columns = ["Nation_code", "count"]

        fig_pie = px.pie(
            pie_df,
            names="Nation_code",
            values="count",
            color="Nation_code",
            color_discrete_sequence=px.colors.sequential.Magma,
            title="Répartition des nations (interactif)",
            hole=0.4
        )
        fig_pie.update_traces(textposition="inside", textinfo="percent+label")
        fig_pie.update_layout(showlegend=True, legend_title_text="Nation")
        st.plotly_chart(fig_pie, use_container_width=True)

    st.info(f"Le top {top_n} inclut les nations les plus représentées dans les 5 grands championnats.")

    st.subheader("Répartition géographique")

    show_all = st.checkbox("Afficher toutes les nations sur la carte", value=False)

    if show_all:
        map_data = df["Nation_code"].value_counts().reset_index()
        map_data.columns = ["Nation_code", "Joueurs"]
        map_title = "Répartition mondiale de toutes les nations"
    else:
        map_data = nation_counts.reset_index()
        map_data.columns = ["Nation_code", "Joueurs"]
        map_title = f"Répartition géographique des {top_n} nations"

    fig_map = px.choropleth(
        map_data,
        locations="Nation_code",
        color="Joueurs",
        color_continuous_scale="magma",
        title=map_title,
    )
    st.plotly_chart(fig_map, use_container_width=True)
