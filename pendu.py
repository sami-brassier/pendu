import pygame
import random

# Initialisation de Pygame
pygame.init()

# Définition des constantes
LARGEUR_FENETRE = 900
HAUTEUR_FENETRE = 400
LARGEUR = 640
HAUTEUR = 480
BLANC = (255, 255, 255)
NOIR = (0, 0, 0)
ROUGE = (255, 0, 0)
VERT = (0, 255, 0)
BLEU = (0, 0, 255)
GRIS = (128, 128, 128)
ORANGE = (255, 165, 0)
POLICE = pygame.font.SysFont("Arial", 40)
BLOCS_PAR_LETTRE = 2
BLOCS_PENDU = 6
BLOCS_PENDU_X = 60
BLOCS_PENDU_Y = 50

# Définition des variables globales
mot = ""
lettres_trouvees = set()
lettres_tentees = set()
erreurs = 0

# Fonction pour choisir un mot aléatoire dans le fichier "mots.txt"
def choisir_mot():
    with open("mots.txt", "r") as file:
        mots = file.read().splitlines()
    return random.choice(mots)

# Fonction pour initialiser une nouvelle partie
def nouvelle_partie():
    global mot, lettres_trouvees, lettres_tentees, erreurs
    mot = choisir_mot()
    lettres_trouvees = set()
    lettres_tentees = set()
    erreurs = 0

# Fonction pour afficher le pendu
def afficher_pendu():
    """Affiche le pendu"""
    x = LARGEUR_FENETRE // 2 - 150
    y = HAUTEUR_FENETRE - 50
    largeur = 200
    hauteur = 20

    # Dessiner la base
    pygame.draw.rect(fenetre, NOIR, (x, y, largeur, hauteur))

    # Dessiner le poteau vertical
    pygame.draw.rect(fenetre, NOIR, (x, y - 200, hauteur, 200))

    # Dessiner le poteau horizontal
    pygame.draw.rect(fenetre, NOIR, (x, y - 200, 100, hauteur))

    # Dessiner la corde
    pygame.draw.line(fenetre, NOIR, (x + 100, y - 200), (x + 100, y - 180), 5)

    # Dessiner la tête
    if erreurs >= 1:
        pygame.draw.circle(fenetre, NOIR, (x + 100, y - 165), 15)

    # Dessiner le corps
    if erreurs >= 2:
        pygame.draw.line(fenetre, NOIR, (x + 100, y - 150), (x + 100, y - 100), 5)

    # Dessiner le bras gauche
    if erreurs >= 3:
        pygame.draw.line(fenetre, NOIR, (x + 100, y - 130), (x + 80, y - 100), 5)

    # Dessiner le bras droit
    if erreurs >= 4:
        pygame.draw.line(fenetre, NOIR, (x + 100, y - 130), (x + 120, y - 100), 5)

    # Dessiner la jambe gauche
    if erreurs >= 5:
        pygame.draw.line(fenetre, NOIR, (x + 100, y - 100), (x + 80, y - 70), 5)

    # Dessiner la jambe droite
    if erreurs >= 6:
        pygame.draw.line(fenetre, NOIR, (x + 100, y - 100), (x + 120, y - 70), 5)


# Fonction pour afficher le mot avec les lettres trouvées
def afficher_mot():
    texte = ""
    for lettre in mot:
        if lettre in lettres_trouvees:
            texte += lettre.upper() + " "
        else:
            texte += "_ "
    texte_surface = POLICE.render(texte, True, NOIR)
    fenetre.blit(texte_surface, (20, HAUTEUR - 50))

# Fonction pour afficher les lettres déjà tentées
def afficher_lettres_tentees():
    texte = "Lettres tentées : " + " ".join(sorted(list(lettres_tentees)))
    texte_surface = POLICE.render(texte, True, NOIR)
    fenetre.blit(texte_surface, (20, 20))

# Fonction pour vérifier si le joueur a gagné
def a_gagne():
    return all(lettre in lettres_trouvees for lettre in mot)

# Fonction pour vérifier si le joueur a perdu
def a_perdu():
    return erreurs >= BLOCS_PENDU

# Création de la fenêtre
fenetre = pygame.display.set_mode((LARGEUR, HAUTEUR))
pygame.display.set_caption("Le jeu du pendu")

# Boucle principale
nouvelle_partie()
en_jouant = True
while en_jouant:
    # Gestion des événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
                en_jouant = False
        elif event.type == pygame.KEYDOWN and event.unicode.isalpha():
                lettre = event.unicode.lower()
                if lettre in lettres_tentees:
                    continue
                lettres_tentees.add(lettre)
                if lettre in mot:
                    lettres_trouvees.add(lettre)
                    if a_gagne():
                        nouvelle_partie()
                else:
                    erreurs += 1
                    if a_perdu():
                        nouvelle_partie()

    # Affichage de la fenêtre
    fenetre.fill(BLANC)
    afficher_pendu()
    afficher_mot()
    afficher_lettres_tentees()
    pygame.display.flip()

# Fermeture de Pygame
pygame.quit()