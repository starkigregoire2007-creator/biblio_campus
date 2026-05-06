books = []

def ajouter_livre(titre, auteur):
    livre = {'titre': titre, 'auteur': auteur, 'disponible': True}
    books.append(livre)
    return livre
def lister_livres():
    return books

def rechercher_livre(titre):
    return [b for b in books if titre.lower() in b['titre'].lower()]
