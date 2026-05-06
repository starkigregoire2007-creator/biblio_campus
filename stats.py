from books import books
def afficher_stats():
    total = len(books)
    disponibles = len([b for b in books if b['disponible']])
    empruntes = total - disponibles
    print(f'Total livres    : {total}')
    print(f'Disponibles     : {disponibles}')
    print(f'Empruntés       : {empruntes}')
