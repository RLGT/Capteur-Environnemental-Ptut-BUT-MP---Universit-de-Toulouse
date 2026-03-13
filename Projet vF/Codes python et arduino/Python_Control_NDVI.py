# -----------------------------
# IMPORTS
# -----------------------------
import tkinter as tk                           # Interface graphique
from tkinter import ttk, filedialog, simpledialog  # Composants avancés, dialogues fichiers et saisie
import pandas as pd                            # Gestion des données tabulaires
import matplotlib.pyplot as plt                # Graphiques
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg  # Intégration matplotlib dans Tkinter
from datetime import timedelta                 # Manipulation des durées

# -----------------------------
# FENETRE PRINCIPALE
# -----------------------------
root = tk.Tk()                                 # Création de la fenêtre principale
root.title("Station Arduino – Analyse")        # Titre de la fenêtre
root.geometry("1500x1000")                     # Taille initiale de la fenêtre

# -----------------------------
# FRAME DES BOUTONS
# -----------------------------
frame_btn = tk.Frame(root, bg="#e0e0e0")      # Frame contenant les boutons
frame_btn.pack(fill=tk.X, pady=5)             # Remplit horizontalement avec un peu d'espace vertical

# -----------------------------
# NOTEBOOK POUR LES ONGLETS
# -----------------------------
notebook = ttk.Notebook(root)                 # Onglets pour organiser les pages
notebook.pack(fill=tk.BOTH, expand=True)      # Remplit tout l'espace disponible

# -----------------------------
# PAGES DASHBOARD & TABLEAU
# -----------------------------
page_dashboard = tk.Frame(notebook, bg="#f5f5f5")   # Page "Dashboard"
notebook.add(page_dashboard, text="Dashboard")      # Ajout à l'onglet

page_table = tk.Frame(notebook, bg="#f5f5f5")       # Page "Historique"
notebook.add(page_table, text="Historique")         # Ajout à l'onglet

# -----------------------------
# LABELS DASHBOARD
# -----------------------------
lbl_tempBME = tk.Label(page_dashboard, text="TempBME: -- °C", font=("Arial",24), fg="orange", bg="#f5f5f5")  # Label température BME
lbl_tempBME.pack(pady=5)                          # Espacement vertical

lbl_tempAS1 = tk.Label(page_dashboard, text="TempAS1: -- °C", font=("Arial",24), fg="red", bg="#f5f5f5")   # Température capteur 1
lbl_tempAS1.pack(pady=5)

lbl_tempAS2 = tk.Label(page_dashboard, text="TempAS2: -- °C", font=("Arial",24), fg="purple", bg="#f5f5f5") # Température capteur 2
lbl_tempAS2.pack(pady=5)

lbl_press = tk.Label(page_dashboard, text="PressBME: -- hPa", font=("Arial",24), fg="green", bg="#f5f5f5")  # Pression
lbl_press.pack(pady=5)

lbl_hum = tk.Label(page_dashboard, text="HumBME: -- %", font=("Arial",24), fg="blue", bg="#f5f5f5")        # Humidité
lbl_hum.pack(pady=5)

lbl_ndvi = tk.Label(page_dashboard, text="NDVI: --", font=("Arial",24), fg="darkgreen", bg="#f5f5f5")     # NDVI
lbl_ndvi.pack(pady=5)

# -----------------------------
# PAGES GRAPHIQUES
# -----------------------------
graph_pages = []     # Liste des pages graphiques
canvas_pages = []    # Liste des canvas matplotlib
lines_pages = []     # Liste des lignes pour chaque graphique

# Graphique 1 : Températures
page_temp = tk.Frame(notebook, bg="#f5f5f5")   # Page graphique température
notebook.add(page_temp, text="Températures")  # Ajout onglet
graph_pages.append(page_temp)

fig_temp, ax_temp = plt.subplots(figsize=(12,4))   # Création figure matplotlib
lines_temp = []
for col, color in zip(["TempBME","TempAS1","TempAS2"], ["orange","red","purple"]):  # Pour chaque capteur
    line, = ax_temp.plot([], [], label=col, color=color)  # Ligne vide initiale
    lines_temp.append(line)
ax_temp.set_ylabel("Temp (°C)")                # Label axe Y
ax_temp.set_xlabel("Temps")                    # Label axe X
ax_temp.legend()                               # Affiche légende
canvas_temp = FigureCanvasTkAgg(fig_temp, master=page_temp)  # Canvas Tkinter pour la figure
canvas_temp.get_tk_widget().pack(fill=tk.BOTH, expand=True)
canvas_pages.append(canvas_temp)
lines_pages.append(lines_temp)

# Graphique 2 : NDVI
page_ndvi = tk.Frame(notebook, bg="#f5f5f5")
notebook.add(page_ndvi, text="NDVI")
graph_pages.append(page_ndvi)

fig_ndvi, ax_ndvi = plt.subplots(figsize=(12,4))
line_ndvi, = ax_ndvi.plot([], [], label="NDVI", color="green")
ax_ndvi.set_ylabel("NDVI")
ax_ndvi.set_xlabel("Temps")
ax_ndvi.legend()
canvas_ndvi = FigureCanvasTkAgg(fig_ndvi, master=page_ndvi)
canvas_ndvi.get_tk_widget().pack(fill=tk.BOTH, expand=True)
canvas_pages.append(canvas_ndvi)
lines_pages.append([line_ndvi])

# Graphique 3 : Pression
page_press = tk.Frame(notebook, bg="#f5f5f5")
notebook.add(page_press, text="Pression")
graph_pages.append(page_press)

fig_press, ax_press = plt.subplots(figsize=(12,4))
line_press, = ax_press.plot([], [], label="PressBME", color="green")
ax_press.set_ylabel("Pression (hPa)")
ax_press.set_xlabel("Temps")
ax_press.legend()
canvas_press = FigureCanvasTkAgg(fig_press, master=page_press)
canvas_press.get_tk_widget().pack(fill=tk.BOTH, expand=True)
canvas_pages.append(canvas_press)
lines_pages.append([line_press])

# Graphique 4 : Humidité
page_hum = tk.Frame(notebook, bg="#f5f5f5")
notebook.add(page_hum, text="Humidité")
graph_pages.append(page_hum)

fig_hum, ax_hum = plt.subplots(figsize=(12,4))
line_hum, = ax_hum.plot([], [], label="HumBME", color="blue")
ax_hum.set_ylabel("Humidité (%)")
ax_hum.set_xlabel("Temps")
ax_hum.legend()
canvas_hum = FigureCanvasTkAgg(fig_hum, master=page_hum)
canvas_hum.get_tk_widget().pack(fill=tk.BOTH, expand=True)
canvas_pages.append(canvas_hum)
lines_pages.append([line_hum])

# -----------------------------
# TABLEAU
# -----------------------------
cols = ("Date","Heure","TempBME","TempAS1","TempAS2","PressBME","HumBME","NDVI")  # Colonnes tableau
tree = ttk.Treeview(page_table, columns=cols, show="headings")  # Tableau Treeview
for c in cols:
    tree.heading(c,text=c)        # Nom colonne
    tree.column(c,width=120,anchor="center")  # Largeur et centrage
tree.pack(fill=tk.BOTH, expand=True)         # Remplissage page

# -----------------------------
# VARIABLE GLOBALE
# -----------------------------
df_global = pd.DataFrame()  # Stocke toutes les données chargées

# -----------------------------
# FONCTIONS
# -----------------------------
def update_dashboard(df):
    """Met à jour les labels du dashboard avec les moyennes actuelles"""
    if df.empty: return
    lbl_tempBME.config(text=f"TempBME: {df['TempBME'].mean():.1f} °C" if 'TempBME' in df else "TempBME: -- °C")  # Moyenne TempBME
    lbl_tempAS1.config(text=f"TempAS1: {df['TempAS1'].mean():.1f} °C" if 'TempAS1' in df else "TempAS1: -- °C")
    lbl_tempAS2.config(text=f"TempAS2: {df['TempAS2'].mean():.1f} °C" if 'TempAS2' in df else "TempAS2: -- °C")
    lbl_press.config(text=f"PressBME: {df['PressBME'].mean():.1f} hPa" if 'PressBME' in df else "PressBME: -- hPa")
    lbl_hum.config(text=f"HumBME: {df['HumBME'].mean():.1f} %" if 'HumBME' in df else "HumBME: -- %")
    lbl_ndvi.config(text=f"NDVI: {df['NDVI'].mean():.2f}" if 'NDVI' in df else "NDVI: --")  # Moyenne NDVI

def update_graphs(df, labels):
    """Met à jour tous les graphiques"""
    # Températures
    for line, col in zip(lines_pages[0], ["TempBME","TempAS1","TempAS2"]):
        y = df[col] if col in df.columns else [0]*len(df)  # Données ou zéro
        line.set_data(range(len(y)), y)
    ax_temp.set_xlim(0, max(len(df)-1,1))
    ax_temp.set_xticks(range(0,len(labels), max(len(labels)//10,1)))
    ax_temp.set_xticklabels([labels[i] for i in range(0,len(labels), max(len(labels)//10,1))], rotation=45)
    ax_temp.relim(); ax_temp.autoscale_view()
    canvas_temp.draw_idle()

    # NDVI
    y = df["NDVI"] if "NDVI" in df.columns else [0]*len(df)
    lines_pages[1][0].set_data(range(len(y)), y)
    ax_ndvi.set_xlim(0, max(len(df)-1,1))
    ax_ndvi.set_xticks(range(0,len(labels), max(len(labels)//10,1)))
    ax_ndvi.set_xticklabels([labels[i] for i in range(0,len(labels), max(len(labels)//10,1))], rotation=45)
    ax_ndvi.relim(); ax_ndvi.autoscale_view()
    canvas_ndvi.draw_idle()

    # Pression
    y = df["PressBME"] if "PressBME" in df.columns else [0]*len(df)
    lines_pages[2][0].set_data(range(len(y)), y)
    ax_press.set_xlim(0, max(len(df)-1,1))
    ax_press.set_xticks(range(0,len(labels), max(len(labels)//10,1)))
    ax_press.set_xticklabels([labels[i] for i in range(0,len(labels), max(len(labels)//10,1))], rotation=45)
    ax_press.relim(); ax_press.autoscale_view()
    canvas_press.draw_idle()

    # Humidité
    y = df["HumBME"] if "HumBME" in df.columns else [0]*len(df)
    lines_pages[3][0].set_data(range(len(y)), y)
    ax_hum.set_xlim(0, max(len(df)-1,1))
    ax_hum.set_xticks(range(0,len(labels), max(len(labels)//10,1)))
    ax_hum.set_xticklabels([labels[i] for i in range(0,len(labels), max(len(labels)//10,1))], rotation=45)
    ax_hum.relim(); ax_hum.autoscale_view()
    canvas_hum.draw_idle()

def update_table(df):
    """Met à jour le tableau avec les 200 dernières lignes"""
    tree.delete(*tree.get_children())  # Supprime anciennes lignes
    for _,row in df.tail(200).iterrows():
        values = []
        for col in cols:
            if col in df.columns:
                if col in ["TempBME","TempAS1","TempAS2","PressBME","HumBME"]:
                    values.append(f"{row[col]:.1f}")
                elif col=="NDVI":
                    values.append(f"{row[col]:.2f}")
                else:
                    values.append(row[col])
            else:
                values.append("--")
        tree.insert("", "end", values=values)  # Ajoute ligne au tableau

def load_csv():
    """Charge un CSV et met à jour dashboard, graphiques et tableau"""
    global df_global
    path = filedialog.askopenfilename(filetypes=[("CSV","*.csv")])  # Dialogue ouverture fichier
    if not path: return
    df = pd.read_csv(path, sep=';')                  # Lecture CSV
    df['DateTime'] = pd.to_datetime(df['Date'] + " " + df['Heure'], errors='coerce')  # Création colonne datetime
    df_global = df                                   # Sauvegarde globale

    daily = df.groupby(df['DateTime'].dt.date)[    # Moyennes journalières
        ["TempBME","TempAS1","TempAS2","PressBME","HumBME","NDVI"]
    ].mean().reset_index()
    daily['DateTime'] = pd.to_datetime(daily['DateTime'])
    labels = daily['DateTime'].dt.strftime("%d-%m-%Y").tolist() if not daily.empty else []

    update_dashboard(daily)                         # Mise à jour dashboard
    update_graphs(daily, labels)                    # Mise à jour graphiques
    update_table(df)                                # Mise à jour tableau complet

def show_day():
    """Affiche les données pour un jour donné"""
    if df_global.empty: return
    date_str = simpledialog.askstring("Jour","JJ-MM-AAAA")  # Saisie date
    if not date_str: return
    date = pd.to_datetime(date_str, dayfirst=True).date()
    df_day = df_global[df_global['DateTime'].dt.date == date]  # Filtre ce jour
    labels = df_day['DateTime'].dt.strftime("%H:%M").tolist()
    update_dashboard(df_day)
    update_graphs(df_day, labels)
    update_table(df_day)

def show_day_hour():
    """Affiche les données pour un jour + heure précis (±30min)"""
    if df_global.empty: return
    d = simpledialog.askstring("Jour","JJ-MM-AAAA")  # Saisie jour
    h = simpledialog.askstring("Heure","HH:MM")       # Saisie heure
    if not d or not h: return
    center = pd.to_datetime(d + " " + h, dayfirst=True)
    start = center - timedelta(minutes=30)           # Début intervalle
    end = center + timedelta(minutes=30)             # Fin intervalle
    df_zoom = df_global[(df_global['DateTime']>=start) & (df_global['DateTime']<=end)]  # Filtre ±30min
    labels = df_zoom['DateTime'].dt.strftime("%H:%M").tolist()
    update_dashboard(df_zoom)
    update_graphs(df_zoom, labels)
    update_table(df_zoom)

# -----------------------------
# BOUTONS
# -----------------------------
tk.Button(frame_btn,text="Charger CSV",command=load_csv,bg="#00bfff",fg="white").pack(side=tk.LEFT,padx=5)  # Bouton chargement CSV
tk.Button(frame_btn,text="Voir un jour",command=show_day,bg="#ff9900",fg="white").pack(side=tk.LEFT,padx=5)  # Filtrer jour
tk.Button(frame_btn,text="Voir jour + heure",command=show_day_hour,bg="#33cc33",fg="white").pack(side=tk.LEFT,padx=5)  # Filtrer ±30min

# -----------------------------
# LANCEMENT
# -----------------------------
root.mainloop()  # Démarre la boucle Tkinter
