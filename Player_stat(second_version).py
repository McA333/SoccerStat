import pandas as pd
import streamlit as st
import Open_files
import plotly.express as px

st.title("Analyse individuelle, des joueurs de foot")
st.divider()

joueur_selectionne = None
donnees_joueur_selectionne = None
df_joueurs = Open_files.df_soccer_doc.copy()

def generer_boite_stat(label, valeur, couleur_bordure):

    html = f"""
    <div style="border:3px solid {couleur_bordure}; 
                padding:12px; 
                border-radius:10px; 
                text-align:center; 
                min-height:72px;">
        <div style="font-size:20px; font-weight:600; margin-bottom:6px;">{valeur}</div>
        <div style="color:#bbb;">{label}</div>
    </div>
    """
    return html

def joueurs_stats_position():

    global joueur_selectionne, donnees_joueur_selectionne, df_joueurs

    joueur_selectionne = st.selectbox(
        "Sélectionne le joueur que tu souhaites analyser",
        options=df_joueurs["Player"].dropna().unique(),
        key="select_player"
    )

    donnees_joueur_selectionne = df_joueurs[df_joueurs["Player"] == joueur_selectionne]

def joueurs_stats_nb_buts():

    global joueur_selectionne, donnees_joueur_selectionne, df_joueurs

    if joueur_selectionne and not donnees_joueur_selectionne.empty:
       
        # Calcul des stats

        total_buts = int(donnees_joueur_selectionne['Gls'].sum())
        colonnes_position = ['Pos', 'Position', 'position']
        colonne_position = next((col for col in colonnes_position if col in df_joueurs.columns), None)
        position_joueur = (
            donnees_joueur_selectionne[colonne_position].mode().iloc[0]
            if colonne_position and not donnees_joueur_selectionne[colonne_position].dropna().empty
            else "N/A"
        )
    else:
        total_buts, position_joueur = 0, "—"

    # Affichage des deux boîtes (buts et position)

    col_gauche, col_droite = st.columns(2)
    col_gauche.markdown(generer_boite_stat("Buts marqués", total_buts, "#98BF64"), unsafe_allow_html=True)
    col_droite.markdown(generer_boite_stat("Position sur le terrain", position_joueur, "#FFFFFF"), unsafe_allow_html=True)



def joueurs_stats_nv_experience():

    global joueur_selectionne, donnees_joueur_selectionne, df_joueurs

    if joueur_selectionne is None or donnees_joueur_selectionne.empty:
        st.write("**Expérience — 0%**")
        st.progress(0)
        return

    colonnes_exp = ['MP', 'Minutes', 'MatchesPlayed', 'Mins']
    colonne_exp = next((col for col in colonnes_exp if col in df_joueurs.columns), None)

    if colonne_exp is None:
        st.warning("Aucune donnée d'expérience disponible pour ce joueur.")
        return

    # Calcul du pourcentage d'expérience

    valeur_joueur = pd.to_numeric(donnees_joueur_selectionne[colonne_exp], errors='coerce').sum()
    valeur_max = pd.to_numeric(df_joueurs[colonne_exp], errors='coerce').max()
    pourcentage_exp = int((valeur_joueur / valeur_max) * 100) if valeur_max > 0 else 0
    pourcentage_exp = max(0, min(100, pourcentage_exp))

    # création du camembert

    stats_exp = {
        "Acquis": pourcentage_exp,
        "Restant": 100 - pourcentage_exp
    }

    fig = px.pie(
        names=list(stats_exp.keys()),
        values=list(stats_exp.values()),
        color_discrete_sequence=["#98BF64", "#FFFFFF"],
        title=f"Expérience de {joueur_selectionne}"
    )
    st.plotly_chart(fig)
    st.write(f"**{joueur_selectionne}** a atteint **{pourcentage_exp}%** de l'expérience maximale.")


def call_my_functions() :

    joueurs_stats_position()
    st.divider()
    joueurs_stats_nb_buts()
    st.divider()
    joueurs_stats_nv_experience()
