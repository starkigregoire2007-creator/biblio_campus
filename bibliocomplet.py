#!/usr/bin/env python3
# =============================================================================
#  BiblioCampus — Application de gestion de bibliothèque universitaire
#  Projet collaboratif Git/GitHub · Mlle SOGNON
#  Exécuter : python bibliocampus.py
# =============================================================================

import json
import os
import sys
from datetime import datetime

# ─────────────────────────────────────────────────────────────────────────────
# COULEURS (terminal ANSI)
# ─────────────────────────────────────────────────────────────────────────────
class C:
    RESET  = "\033[0m"
    BOLD   = "\033[1m"
    RED    = "\033[91m"
    GREEN  = "\033[92m"
    YELLOW = "\033[93m"
    BLUE   = "\033[94m"
    CYAN   = "\033[96m"
    WHITE  = "\033[97m"
    GREY   = "\033[90m"

def couleur(texte, couleur):
    return f"{couleur}{texte}{C.RESET}"

def titre(texte):
    print(f"\n{C.BOLD}{C.BLUE}{'═' * 50}{C.RESET}")
    print(f"{C.BOLD}{C.WHITE}  {texte}{C.RESET}")
    print(f"{C.BOLD}{C.BLUE}{'═' * 50}{C.RESET}\n")

def separateur():
    print(f"{C.GREY}{'─' * 50}{C.RESET}")

def succes(msg):
    print(f"\n{C.GREEN}  ✔  {msg}{C.RESET}\n")

def erreur(msg):
    print(f"\n{C.RED}  ✘  {msg}{C.RESET}\n")

def info(msg):
    print(f"{C.CYAN}  ℹ  {msg}{C.RESET}")

def avertissement(msg):
    print(f"{C.YELLOW}  ⚠  {msg}{C.RESET}")

# ─────────────────────────────────────────────────────────────────────────────
# STORAGE — lecture / écriture JSON  (storage.py)
# ─────────────────────────────────────────────────────────────────────────────
FILEPATH = os.path.join(os.path.dirname(__file__), "data", "library.json")

def _init_fichier():
    os.makedirs(os.path.dirname(FILEPATH), exist_ok=True)
    if not os.path.exists(FILEPATH):
        with open(FILEPATH, "w", encoding="utf-8") as f:
            json.dump({"livres": [], "emprunts": []}, f, indent=2, ensure_ascii=False)

def charger_donnees():
    _init_fichier()
    with open(FILEPATH, encoding="utf-8") as f:
        return json.load(f)

def sauvegarder_donnees(data):
    _init_fichier()
    with open(FILEPATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

# ─────────────────────────────────────────────────────────────────────────────
# BOOKS — gestion des livres  (books.py)
# ─────────────────────────────────────────────────────────────────────────────

def ajouter_livre():
    titre_livre("AJOUTER UN LIVRE")
    titre_input = input(f"  {C.CYAN}Titre du livre  : {C.RESET}").strip()
    if not titre_input:
        erreur("Le titre ne peut pas être vide.")
        return
    auteur = input(f"  {C.CYAN}Auteur          : {C.RESET}").strip()
    if not auteur:
        erreur("L'auteur ne peut pas être vide.")
        return
    annee = input(f"  {C.CYAN}Année (optionnel): {C.RESET}").strip()
    genre = input(f"  {C.CYAN}Genre (optionnel): {C.RESET}").strip()

    data = charger_donnees()

    # vérifier doublon
    for livre in data["livres"]:
        if livre["titre"].lower() == titre_input.lower() and livre["auteur"].lower() == auteur.lower():
            avertissement(f"Ce livre existe déjà (ID {livre['id']}).")
            return

    nouvel_id = max((l["id"] for l in data["livres"]), default=0) + 1
    livre = {
        "id"        : nouvel_id,
        "titre"     : titre_input,
        "auteur"    : auteur,
        "annee"     : annee if annee else "—",
        "genre"     : genre if genre else "—",
        "disponible": True,
        "ajoute_le" : datetime.now().strftime("%d/%m/%Y")
    }
    data["livres"].append(livre)
    sauvegarder_donnees(data)
    succes(f"Livre ajouté avec l'ID {nouvel_id} : « {titre_input} »")


def lister_livres():
    titre_livre("LISTE DES LIVRES")
    data = charger_donnees()
    livres = data["livres"]
    if not livres:
        info("Aucun livre dans la bibliothèque pour l'instant.")
        return

    print(f"  {C.BOLD}{'ID':<5} {'TITRE':<30} {'AUTEUR':<22} {'ANNÉE':<7} {'STATUT'}{C.RESET}")
    separateur()
    for l in livres:
        statut = couleur("Disponible", C.GREEN) if l["disponible"] else couleur("Emprunté  ", C.RED)
        titre_affiche = l["titre"][:28] + ".." if len(l["titre"]) > 30 else l["titre"]
        auteur_affiche = l["auteur"][:20] + ".." if len(l["auteur"]) > 22 else l["auteur"]
        print(f"  {C.YELLOW}{l['id']:<5}{C.RESET} {titre_affiche:<30} {auteur_affiche:<22} {l.get('annee','—'):<7} {statut}")
    separateur()
    print(f"  {C.GREY}Total : {len(livres)} livre(s){C.RESET}\n")


def rechercher_livre():
    titre_livre("RECHERCHER UN LIVRE")
    mot = input(f"  {C.CYAN}Mot-clé (titre ou auteur) : {C.RESET}").strip().lower()
    if not mot:
        erreur("Veuillez saisir un mot-clé.")
        return

    data = charger_donnees()
    resultats = [
        l for l in data["livres"]
        if mot in l["titre"].lower() or mot in l["auteur"].lower()
    ]

    if not resultats:
        info(f"Aucun résultat pour « {mot} ».")
        return

    print(f"\n  {C.BOLD}{len(resultats)} résultat(s) trouvé(s) :{C.RESET}\n")
    for l in resultats:
        statut = couleur("✔ Disponible", C.GREEN) if l["disponible"] else couleur("✘ Emprunté", C.RED)
        print(f"  {C.YELLOW}[{l['id']}]{C.RESET} {C.BOLD}{l['titre']}{C.RESET} — {l['auteur']} ({l.get('annee','—')}) · {statut}")
    print()


def supprimer_livre():
    titre_livre("SUPPRIMER UN LIVRE")
    lister_livres()
    try:
        livre_id = int(input(f"  {C.CYAN}ID du livre à supprimer : {C.RESET}").strip())
    except ValueError:
        erreur("ID invalide.")
        return

    data = charger_donnees()
    livre = _trouver_livre(data, livre_id)
    if not livre:
        erreur(f"Aucun livre avec l'ID {livre_id}.")
        return
    if not livre["disponible"]:
        erreur("Ce livre est actuellement emprunté. Impossible de le supprimer.")
        return

    confirmation = input(f"  Supprimer « {livre['titre']} » ? {C.RED}(oui/non){C.RESET} : ").strip().lower()
    if confirmation == "oui":
        data["livres"] = [l for l in data["livres"] if l["id"] != livre_id]
        sauvegarder_donnees(data)
        succes(f"Livre « {livre['titre']} » supprimé.")
    else:
        info("Suppression annulée.")


# ─────────────────────────────────────────────────────────────────────────────
# LOANS — emprunts et retours  (loans.py)
# ─────────────────────────────────────────────────────────────────────────────

def _trouver_livre(data, livre_id):
    for l in data["livres"]:
        if l["id"] == livre_id:
            return l
    return None


def emprunter_livre():
    titre_livre("EMPRUNTER UN LIVRE")
    # afficher seulement les disponibles
    data = charger_donnees()
    disponibles = [l for l in data["livres"] if l["disponible"]]
    if not disponibles:
        info("Aucun livre disponible à l'emprunt.")
        return

    print(f"  {C.BOLD}Livres disponibles :{C.RESET}\n")
    for l in disponibles:
        print(f"  {C.YELLOW}[{l['id']}]{C.RESET} {l['titre']} — {l['auteur']}")
    print()

    try:
        livre_id = int(input(f"  {C.CYAN}ID du livre à emprunter : {C.RESET}").strip())
    except ValueError:
        erreur("ID invalide.")
        return

    emprunteur = input(f"  {C.CYAN}Nom de l'emprunteur    : {C.RESET}").strip()
    if not emprunteur:
        erreur("Le nom de l'emprunteur est requis.")
        return

    data = charger_donnees()
    livre = _trouver_livre(data, livre_id)
    if not livre:
        erreur(f"Aucun livre avec l'ID {livre_id}.")
        return
    if not livre["disponible"]:
        erreur(f"« {livre['titre']} » est déjà emprunté.")
        return

    livre["disponible"] = False
    emprunt = {
        "id"          : max((e["id"] for e in data["emprunts"]), default=0) + 1,
        "livre_id"    : livre_id,
        "titre"       : livre["titre"],
        "emprunteur"  : emprunteur,
        "date_emprunt": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "rendu"       : False
    }
    data["emprunts"].append(emprunt)
    sauvegarder_donnees(data)
    succes(f"« {livre['titre']} » emprunté par {emprunteur} le {emprunt['date_emprunt']}.")


def rendre_livre():
    titre_livre("RENDRE UN LIVRE")
    data = charger_donnees()
    en_cours = [e for e in data["emprunts"] if not e["rendu"]]
    if not en_cours:
        info("Aucun emprunt en cours.")
        return

    print(f"  {C.BOLD}Emprunts en cours :{C.RESET}\n")
    for e in en_cours:
        print(f"  {C.YELLOW}[Emprunt {e['id']}]{C.RESET} « {e['titre']} » · {e['emprunteur']} · depuis le {e['date_emprunt']}")
    print()

    try:
        emprunt_id = int(input(f"  {C.CYAN}ID de l'emprunt à clôturer : {C.RESET}").strip())
    except ValueError:
        erreur("ID invalide.")
        return

    emprunt = next((e for e in data["emprunts"] if e["id"] == emprunt_id), None)
    if not emprunt:
        erreur(f"Aucun emprunt avec l'ID {emprunt_id}.")
        return
    if emprunt["rendu"]:
        avertissement("Ce livre a déjà été rendu.")
        return

    emprunt["rendu"] = True
    emprunt["date_retour"] = datetime.now().strftime("%d/%m/%Y %H:%M")
    livre = _trouver_livre(data, emprunt["livre_id"])
    if livre:
        livre["disponible"] = True
    sauvegarder_donnees(data)
    succes(f"« {emprunt['titre']} » rendu par {emprunt['emprunteur']}. Merci !")


def historique_emprunts():
    titre_livre("HISTORIQUE DES EMPRUNTS")
    data = charger_donnees()
    emprunts = data["emprunts"]
    if not emprunts:
        info("Aucun emprunt enregistré.")
        return

    print(f"  {C.BOLD}{'ID':<5} {'TITRE':<28} {'EMPRUNTEUR':<20} {'DATE':<17} {'STATUT'}{C.RESET}")
    separateur()
    for e in reversed(emprunts):
        statut = couleur("Rendu     ", C.GREEN) if e["rendu"] else couleur("En cours  ", C.YELLOW)
        titre_aff = e["titre"][:26] + ".." if len(e["titre"]) > 28 else e["titre"]
        nom_aff   = e["emprunteur"][:18] + ".." if len(e["emprunteur"]) > 20 else e["emprunteur"]
        print(f"  {C.YELLOW}{e['id']:<5}{C.RESET} {titre_aff:<28} {nom_aff:<20} {e['date_emprunt']:<17} {statut}")
    separateur()
    print(f"  {C.GREY}Total : {len(emprunts)} emprunt(s){C.RESET}\n")


# ─────────────────────────────────────────────────────────────────────────────
# STATS — statistiques  (stats.py)
# ─────────────────────────────────────────────────────────────────────────────

def afficher_stats():
    titre_livre("TABLEAU DE BORD — STATISTIQUES")
    data = charger_donnees()
    livres   = data["livres"]
    emprunts = data["emprunts"]

    total       = len(livres)
    disponibles = sum(1 for l in livres if l["disponible"])
    empruntes   = total - disponibles
    total_emp   = len(emprunts)
    en_cours    = sum(1 for e in emprunts if not e["rendu"])
    rendus      = total_emp - en_cours

    # genres
    genres = {}
    for l in livres:
        g = l.get("genre", "—")
        genres[g] = genres.get(g, 0) + 1

    # top emprunteurs
    compteur = {}
    for e in emprunts:
        compteur[e["emprunteur"]] = compteur.get(e["emprunteur"], 0) + 1
    top = sorted(compteur.items(), key=lambda x: x[1], reverse=True)[:3]

    def barre(val, total_val, largeur=20):
        if total_val == 0:
            return "░" * largeur
        plein = int((val / total_val) * largeur)
        return couleur("█" * plein, C.BLUE) + couleur("░" * (largeur - plein), C.GREY)

    print(f"  {C.BOLD}📚 LIVRES{C.RESET}")
    print(f"    Total dans la bibliothèque : {C.YELLOW}{total}{C.RESET}")
    print(f"    Disponibles  {barre(disponibles, total)} {C.GREEN}{disponibles}{C.RESET}")
    print(f"    Empruntés    {barre(empruntes,   total)} {C.RED}{empruntes}{C.RESET}")
    print()

    print(f"  {C.BOLD}🔖 EMPRUNTS{C.RESET}")
    print(f"    Total enregistrés : {C.YELLOW}{total_emp}{C.RESET}")
    print(f"    En cours     {barre(en_cours, total_emp)} {C.YELLOW}{en_cours}{C.RESET}")
    print(f"    Rendus       {barre(rendus,   total_emp)} {C.GREEN}{rendus}{C.RESET}")
    print()

    if genres:
        print(f"  {C.BOLD}🏷  GENRES{C.RESET}")
        for g, nb in sorted(genres.items(), key=lambda x: x[1], reverse=True):
            print(f"    {g:<20} {barre(nb, total, 15)} {nb}")
        print()

    if top:
        print(f"  {C.BOLD}🏆 TOP EMPRUNTEURS{C.RESET}")
        medailles = ["🥇", "🥈", "🥉"]
        for i, (nom, nb) in enumerate(top):
            print(f"    {medailles[i] if i < 3 else '  '} {nom:<20} {nb} emprunt(s)")
        print()


# ─────────────────────────────────────────────────────────────────────────────
# MENU  (menu.py)
# ─────────────────────────────────────────────────────────────────────────────

def titre_livre(texte):
    """Affiche un sous-titre de section."""
    print(f"\n  {C.BOLD}{C.CYAN}── {texte} ──{C.RESET}\n")


def afficher_menu():
    os.system("cls" if os.name == "nt" else "clear")
    print(f"""
{C.BOLD}{C.BLUE}
  ╔══════════════════════════════════════════════╗
  ║          📖  B I B L I O C A M P U S        ║
  ║     Bibliothèque Universitaire · v1.0        ║
  ╚══════════════════════════════════════════════╝
{C.RESET}
  {C.BOLD}── LIVRES ──────────────────────────────────{C.RESET}
  {C.YELLOW} 1{C.RESET}  ➜  Ajouter un livre
  {C.YELLOW} 2{C.RESET}  ➜  Lister tous les livres
  {C.YELLOW} 3{C.RESET}  ➜  Rechercher un livre
  {C.YELLOW} 4{C.RESET}  ➜  Supprimer un livre

  {C.BOLD}── EMPRUNTS ─────────────────────────────────{C.RESET}
  {C.YELLOW} 5{C.RESET}  ➜  Emprunter un livre
  {C.YELLOW} 6{C.RESET}  ➜  Rendre un livre
  {C.YELLOW} 7{C.RESET}  ➜  Historique des emprunts

  {C.BOLD}── STATISTIQUES ─────────────────────────────{C.RESET}
  {C.YELLOW} 8{C.RESET}  ➜  Tableau de bord

  {C.BOLD}── QUITTER ──────────────────────────────────{C.RESET}
  {C.YELLOW} 0{C.RESET}  ➜  Quitter l'application
""")


def pause():
    input(f"  {C.GREY}Appuyez sur Entrée pour continuer...{C.RESET}")


# ─────────────────────────────────────────────────────────────────────────────
# MAIN — point d'entrée  (main.py)
# ─────────────────────────────────────────────────────────────────────────────

def main():
    actions = {
        "1": ajouter_livre,
        "2": lister_livres,
        "3": rechercher_livre,
        "4": supprimer_livre,
        "5": emprunter_livre,
        "6": rendre_livre,
        "7": historique_emprunts,
        "8": afficher_stats,
    }

    while True:
        afficher_menu()
        choix = input(f"  {C.BOLD}Votre choix : {C.RESET}").strip()

        if choix == "0":
            print(f"\n{C.CYAN}  Au revoir ! À bientôt sur BiblioCampus. 📚{C.RESET}\n")
            sys.exit(0)
        elif choix in actions:
            try:
                actions[choix]()
            except KeyboardInterrupt:
                print(f"\n{C.GREY}  Action annulée.{C.RESET}")
            pause()
        else:
            erreur("Choix invalide. Entrez un numéro entre 0 et 8.")
            pause()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{C.CYAN}  BiblioCampus fermé. À bientôt ! 📚{C.RESET}\n")
        sys.exit(0)