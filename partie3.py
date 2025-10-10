import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

st.set_page_config(page_title="Analyse Joueurs - Partie 3", layout="wide")

def load_data():
    df = pd.read_csv("top5-players.csv")
    df.rename(columns={"Comp": "League"}, inplace=True)
    return df

def preprocess_data(df):
    df["Gls_90"] = df["Gls"] / (df["Min"] / 90)
    df["Ast_90"] = df["Ast"] / (df["Min"] / 90)
    df["GA_90"] = (df["Gls"] + df["Ast"]) / (df["Min"] / 90)
    return df

def show_sidebar(df):
    st.sidebar.header("Filtres")
    st.session_state.min_minutes = st.sidebar.slider("Minutes minimales", 0, 3000, 900, step=100)
    st.session_state.league_choice = st.sidebar.selectbox("Choisir une Ligue", ["Toutes"] + sorted(df["League"].unique().tolist()))
    st.session_state.player_choice = st.sidebar.selectbox("Comparer un joueur", ["Aucun"] + sorted(df["Player"].unique().tolist()))

def render_analysis(df):
    filtered_df = df[df["Min"] >= st.session_state.min_minutes]
    if st.session_state.league_choice != "Toutes":
        filtered_df = filtered_df[filtered_df["League"] == st.session_state.league_choice]

    show_league_comparison(filtered_df)
    show_top_players(filtered_df)

    if st.session_state.player_choice != "Aucun":
        show_player_focus(df, st.session_state.player_choice)

    if "xG" in df.columns:
        show_efficiency_plot(filtered_df)

def show_league_comparison(filtered_df):
    st.header("Comparaison des Ligues")
    fig, ax = plt.subplots(1, 3, figsize=(18, 6))
    sns.boxplot(x="League", y="Gls", data=filtered_df, ax=ax[0], palette="Set2")
    ax[0].set_title("Répartition des buts par Ligue")
    sns.boxplot(x="League", y="Ast", data=filtered_df, ax=ax[1], palette="Set2")
    ax[1].set_title("Répartition des assists par Ligue")
    sns.boxplot(x="League", y="Min", data=filtered_df, ax=ax[2], palette="Set2")
    ax[2].set_title("Minutes jouées par Ligue")
    for a in ax:
        a.tick_params(axis="x", rotation=30)
    st.pyplot(fig)

def show_top_players(filtered_df):
    st.header("Top 5 joueurs par Ligue (contribution offensive /90min)")
    top_df = (
        filtered_df.groupby("League")
        .apply(lambda x: x.nlargest(5, "GA_90"))
        .reset_index(drop=True)
    )
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(data=top_df, x="GA_90", y="Player", hue="League", dodge=False, palette="Set2")
    ax.set_xlabel("G+A / 90 min")
    ax.set_ylabel("Joueur")
    st.pyplot(fig)

def show_player_focus(df, player_choice):
    st.header(f"Focus Joueur : {player_choice}")
    player_data = df[df["Player"] == player_choice].iloc[0]
    league_data = df[df["League"] == player_data["League"]]
    stats = ["Gls_90", "Ast_90", "GA_90"]
    player_values = [player_data[stat] for stat in stats]
    league_means = [league_data[stat].mean() for stat in stats]
    labels = ["Buts/90", "Assists/90", "G+A/90"]
    angles = np.linspace(0, 2 * np.pi, len(stats), endpoint=False).tolist()
    values = player_values + [player_values[0]]
    league_vals = league_means + [league_means[0]]
    angles += [angles[0]]
    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    ax.plot(angles, values, label=player_choice, linewidth=2)
    ax.fill(angles, values, alpha=0.25)
    ax.plot(angles, league_vals, label=f"Moyenne {player_data['League']}", linewidth=2, linestyle="--")
    ax.fill(angles, league_vals, alpha=0.15)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels)
    ax.legend(loc="upper right")
    st.pyplot(fig)

def show_efficiency_plot(filtered_df):
    st.header("Efficacité : Buts vs xG")
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.scatterplot(data=filtered_df, x="xG", y="Gls", hue="League", alpha=0.7, palette="Set2")
    ax.plot([0, filtered_df["xG"].max()], [0, filtered_df["xG"].max()], "r--")
    ax.set_xlabel("xG cumulés")
    ax.set_ylabel("Buts marqués")
    st.pyplot(fig)
