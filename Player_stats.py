import pandas as pd
import streamlit as st
import Open_files
import plotly.express as px

def joueurs_stats_position():
    
    with st.expander("Stat des joueurs en fonction de leur position et performances"):

        selected_players_names = st.multiselect(
            "Sélectionnez un ou plusieurs joueur(s)",
            options=Open_files.df_soccer_doc["Player"].unique(),
            key="multiselect_position_camembert"
        )

        if not selected_players_names:
            return

        filtered_df = Open_files.df_soccer_doc[Open_files.df_soccer_doc["Player"].isin(selected_players_names)]

        # Camembert buts vs passes décisives

        for _, row in filtered_df.iterrows():
            
            st.markdown(f"**{row['Player']}** - Position : {row['Pos']}")
            stats = {"Buts": row["Gls"], "Passes décisives": row["Ast"]}
            fig_pie = px.pie(
                names=list(stats.keys()),
                values=list(stats.values()),
                title=f"{row['Player']} : buts marqués et passes décisives"
            )
            st.plotly_chart(fig_pie)
            st.divider()



def joueurs_stats_nv_experience():
    
    with st.expander("Stat des joueurs en fonction de leur niveau d'experience") :

        selected_players_names = st.multiselect(
            "Sélectionnez un ou plusieurs joueur(s)",
            options = Open_files.df_soccer_doc["Player"].unique()
        )

        if not selected_players_names:
            return

        filtered_df = Open_files.df_soccer_doc[Open_files.df_soccer_doc["Player"].isin(selected_players_names)]

        result = px.histogram(
            filtered_df,
            x="MP",
            y="Player",
            title="stat player experience",
            orientation="h"
        )
        st.plotly_chart(result)


def joueurs_stats_nb_buts():

    with st.expander("Stat des joueurs en fonction de leur buts marqués"):

        df_result = Open_files.df_soccer_doc[['Player', 'Gls']].copy()
        df_result['Gls'] = pd.to_numeric(df_result['Gls'], errors='coerce').fillna(0)

        # choix joueur(s)
        selected_players = st.multiselect(
            "Sélectionnez le(s) joueur(s)",
            sorted(df_result['Player'].unique(), reverse=True),
            key='Player'
        )

        if not selected_players:
            st.info("Sélectionnez au moins un joueur pour afficher les stats.")
            return

        # Filtrer pour une apparition de joueur
        df_fusion = df_result[df_result['Player'].isin(selected_players)]
        df_grouped = df_fusion.groupby('Player', as_index=False)['Gls'].sum()

        # Afficher une metric pour chaque joueur (disposition en colonnes)
        cols = st.columns(min(4, len(df_grouped)))  # max 4 colonnes sur une ligne, mais adapte si plus
        for i, row in enumerate(df_grouped.itertuples(index=False)):
            col = cols[i % len(cols)]
            col.metric(label=row.Player, value=int(row.Gls))

joueurs_stats_nb_buts()
joueurs_stats_position()
joueurs_stats_nv_experience()