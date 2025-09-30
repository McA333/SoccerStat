import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# --- Page Streamlit ---
st.set_page_config(page_title="MARIEMAVIE - SoccerStat", layout="centered")

# --- Lecture sécurisée du CSV ---
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

# Nettoyage
df = df.drop_duplicates().dropna(how="all")
df["Nation_code"] = df["Nation"].str.split(" ").str[-1]

# --- Titre principal ---
st.title("SOCCERSTAT")

st.write("") 

st.markdown("""
Bienvenue dans le dashboard **SoccerStat**  

Vous pouvez explorer :  


- [ Nombre de joueurs par poste](#joueurs-par-poste)  
- [ Répartition des joueurs par nation](#joueurs-par-nation)  


"""


)
st.write("") 
st.write("") 
st.write("") 
st.write("")  
st.write("")   
st.write("")   
st.write("")   
st.write("")   
st.write("")   
st.write("")   
st.write("")   

st.divider()

# --- Joueurs par poste ---
st.markdown("##  Joueurs par poste", unsafe_allow_html=True)
fig1, ax1 = plt.subplots(figsize=(8,5))
sns.countplot(x="Pos", data=df, order=df["Pos"].value_counts().index, palette="viridis", ax=ax1)
ax1.set_title("Répartition des joueurs par poste", fontsize=14)
ax1.set_xlabel("Poste")
ax1.set_ylabel("Nombre de joueurs")
st.pyplot(fig1)

st.divider()

# --- Joueurs par nation ---
st.markdown("##  Joueurs par nation", unsafe_allow_html=True)

top_n = st.number_input("Entrer le nombre de nations à afficher (Top N) :", min_value=1, max_value=50, value=15, step=1)

nation_counts = df["Nation_code"].value_counts().head(top_n)

fig2, ax2 = plt.subplots(figsize=(10,6))
sns.barplot(x=nation_counts.values, y=nation_counts.index, palette="magma", ax=ax2)
ax2.set_title(f"Top {top_n} des nations représentées", fontsize=14)
ax2.set_xlabel("Nombre de joueurs")
ax2.set_ylabel("Nation")
st.pyplot(fig2)
