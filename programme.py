# Le jeu du pendu

from tkinter import *
from random import *

def jeu(lang):
    global alphabet     # C'est la seule variable pour laquelle je dois faire cela, comme je modifie les valeurs durant la partie je dois les remettre lorsqu'on appuie sur 'recommencer" et je dois mettre alphabet dans un global sinon ça ne marche pas

    if lang == 1:
        fichier = open("liste_mots_francais.txt")     # J'ouvre mon fichier dans une variable appelée fichier
        liste_mots = fichier.readlines()     # Je mets tous les mots du fichier dans une liste grâce à .readlines()
        deux_joueur = False
        fichier.close()     # Je ferme mon fichier ouvert au dessus car il est inutile
                            # C'est la même méthode pour le suivant elif
    elif lang == 2:
        fichier = open("liste_mots_anglais.txt")
        liste_mots = fichier.readlines()
        deux_joueur = False
        fichier.close()
    elif lang == "duo":
        deux_joueur = True     # Ici, pas besoin de mettre des mots dans une liste car le mot sera choisi grâce à la fonction "choix_mot()"

    alp = {"A":0,"B":1,"C":2,"D":3,"E":4,"F":5,"G":6,"H":7,"I":8,"J":9,"K":10,"L":11,"M":12,"N":13,"O":14,"P":15,"Q":16,"R":17,"S":18,"T":19,"U":20,"V":21,"W":22,"X":23,"Y":24,"Z":25}

    def netoyage(liste):     # Mes mots sont dans un fichier texte et il n'y a qu'un mot par ligne, mais comme je les ai mis dans une liste ils sont tous suivis d'un '/n' qui signifie un retour a la ligne
        for i in range(len(liste)):
            liste[i] = liste[i].rstrip()     # Je dois donc nettoyer ma liste grâce à 'rstripe()' qui supprime tous les carractères récurents à droite, le programme en déduit que comme il y a '/n' a chaque fois, ce sont des carractères indésirables

    def majuscule(mot):     # Pour que le jeu soit plus simple toutes les lettres sont en majuscules et cette fonction permet de mettre le mot en majuscule
        nouveau_mot = ''
        for i in range(len(mot)):
            nouveau_mot += mot[i].upper()     # ".upper()" permet de mettre les carractères en majuscules et si ils le sont déjà ça ne change rien
        return nouveau_mot

    def aide3():
        global aide
        aide = 1     # C'est pour qu'il n'y ai qu'une aide possible
        fInfos.destroy()

    def aide2():    # Ce sera la fonction qui sera utilisée si le joueur a besoin d'aide
        global fInfos, aide    # En me renseignant sur internet j'ai découvert que lorsque l'on modifie une variable dans une fonction elle n'est modifiée que dans cette fonction mais si l'on met "global" suivi de la variable à modifier elle sera modifiée pour tout le programme
        for i in range(len(mot_partiel)):
            if mot_partiel[i] == "_" and aide == 0:     # Je parcours le mot qui est affiché et dès qu'il y a un "_" je prends sa position et je donne sa valeur dans le mot à trouver
                phrase = "Dans le mot il y a au moins un :",mot_a_trouver[i]
        war2 = Label(fInfos,text=phrase).pack()     # Je crée un Label qui m'affiche mon aide mais j'ai du définir la phrase au préalable car dans un label tkinter on ne peut pas définir le texte par ("...",...,"...")
        bouton3 = Button(fInfos, text='OK', command=aide3).pack()

    def popup():     # Cette fonction est appelée quand il ne reste que deux erreurs au joueur
        global mot_partiel,aide, fInfos,aide
        fInfos = Toplevel()		  # Pour faire le popup on utilise Toplevel()
        fInfos.title('Attention')
        fInfos.grab_set()     # Grâce à ça le joueur ne peut pas interagir avec la fenêtre de jeu
        war = Label(fInfos,text="Attention il ne vous reste que deux essaies, voulez-vous de l'aide ?").pack()
        bouton1 = Button(fInfos, text='Oui', command=aide2).pack()     # Si on clique sur ce bouton la fonction au dessus est appelée
        bouton2 = Button(fInfos, text='Non', command=fInfos.destroy).pack()     # Si on clique ici, on détruit la fenêtre

    def choix_mot() :
        global mot_a_trouver,entree,window
        window = Toplevel()     # Comme pour "popup()" je crée un 'Toplevel'
        window.title('Choix du mot')
        window.grab_set()
        consigne = Label(window, text="Entrez le mot que votre amis va devoir chercher !").pack()     # Je mets ma consigne dans un label et crée un champs de saisi pour que le joueur note son mot
        entree = Entry(window, textvariable=str, width=30)
        entree.pack()
        bouton_ok = Button(window, text ="OK", command = mot_choisi).pack()     # Je crée un bouton qui renvoit vers la fonction 'mot_choisi()' définit en dessous

    def mot_choisi():
        global mot_a_trouver,mot_partiel
        mot_a_trouver = entree.get()     # Je récupère le mot entré dans le champs de saisi
        window.destroy()     # Je détruis la fenêtre
        mot_a_trouver = majuscule(mot_a_trouver)     # Je mets le mot en majuscule
        mot_partiel = "_"*len(mot_a_trouver)     # Je crée le mot qui sera affiché
        afficher_mot(mot_partiel)     # Et j'affiche le mot

    def tri_list(t):     # J'effectue un tri par insertion comme nous avons vu en cours, afin que la liste des lettres utilisées soient triées par ordre alphabétique
        for i in range(len(t)):
            x = t[i]
            j = i
            while j>0 and t[j-1]>x :
                t[j] = t[j-1]
                j = j-1
            t[j] = x
        return t

    def lettre_dans_mot(lettre):
        global arreter, mot_partiel, nberreur, lettres,lettre_essayee, pendu_dessin,photo
        if arreter == False:     # arreter est défini par defaut sur False et ne passe à True que quand la partie est finie, victoire ou non
            nouveau_mot_partiel=''     # Il y a 4 variables en rapport avec le mot, leurs détails sont disponibles à la fin du programme car ils sont trop longs pour les commentaires
            for i in range(len(mot_a_trouver)):
                if lettre == mot_a_trouver[i]:     # On vérifie si la lettre est bonne
                    nouveau_mot_partiel += lettre
                    emplacement = alp[lettre]
                    alphabet[emplacement].config(text="O",fg="green")
                else :
                    nouveau_mot_partiel += mot_partiel[i]     # Si elle n'est pas bonne on ajoute la lettre qui est a l'emplacement "i" du mot qui est affiché donc ça peut être une lettre comme un "_"
            if lettre not in mot_a_trouver :
                nberreur = nberreur + 1
                emplacement = alp[lettre]
                alphabet[emplacement].config(text="X",fg="red",command=NONE)
                nom_photo = "image/pendu_"+str(nberreur)+".gif"     # J'ai besoin de déterminer le nom de la photo avant car on ne peut pas faire des "..."+...+"..." dans une fonction tkinter
                photo=PhotoImage(file=nom_photo)     # Du coup ma photo devient l'image qui a pour nom ("pendu_"+str(nberreur)+".gif) dans mon dossier image
                pendu_dessin.config(image = photo)     # Je configure l'image de mon Label pendu-dessin qui devient ma photo définit au dessus
            if lettre not in lettre_essayee :     # lettre_essayee est une liste qui répertorie les lettres déjà essayées, comme la lettre n'est pas dans le mot je vérifie si elle est dans lettre_essayee et si elle n'y est pas je l'ajoute
                lettre_essayee.append(lettre)
                lettre_essayee = tri_list(lettre_essayee)
            mot_partiel = nouveau_mot_partiel     # Fin des interactions possibles donc mon mot_partiel devient nouveau_mot_partiel
            afficher_mot(mot_partiel)     # J'appelle ma fonction 'afficher_mot'
            if mot_partiel == mot_a_trouver:     # Maintenant que nous sommes à la fin du tour on vérifie si le mot partiel et le mot à trouver sont identiques
                if nberreur >= 4:     # Il y a une image de victoire pour chaque stade de la partie mais de la 4 a la 9 il n'y avait pas de différence donc nous vérifions si il y a 4 ou plus d'erreurs, si oui on définit nom_photo à l'image destinée pour les erreurs de 4 à 9
                    nom_photo = "image/pendu_4-9_V.gif"
                else:     # Sinon on définit nom_photo par la photo numéro "nberreur"
                    nom_photo = "image/pendu_"+str(nberreur)+"_V.gif"
                photo=PhotoImage(file=nom_photo)     # Puis on fait comme au dessus
                pendu_dessin.config(image = photo)
                arreter = True     # Comme la partie est finie on définit arreter sur True pour qu'il n'y ai plus d'interaction possible avec les lettres
            if nberreur == 7 and aide == 0:     # Si il y a 7 erreurs et que l'aide n'a pas encore été donnée on appelle la fonction "popup"
                popup()
            if nberreur == 9 :     # Si il y a 9 erreurs la partie est terminée
                arreter = True     # Donc on définit arreter sur True et on affiche le mot à trouver
                afficher_mot(mot_a_trouver)

    def afficher_mot(mot):
        global lettres
        mot_large = ""
        for i in range(len(mot)):
            mot_large = mot_large + mot[i] + " "     # Je recopie le mot en argument mais avec un espace entre toutes les lettres
        canevas.delete(ALL)     # Je retire tout ce qu'il y a dans le canvas
        essaie = 9 - nberreur
        lettres = canevas.create_text(320,60,text=mot_large,fill='black',font='Courrier 30')     # Je crée un texte dans mon canvas en 320px 60px avec pour texte le mot_large
        text_erreur = canevas.create_text(60,25,text="Fautes restantes :",fill='black',font='Courrier 10')     # Pour afficher le nombre d'essais restants il faut que j'utilise deux zones de texte, un qui restera constant et un autre qui changera
        afficher_erreur = canevas.create_text(120,25,text=essaie,fill='black',font='Courrier 10')     # Ici ça n'affichera que le nombre d'essais restants
        text_utilisee = canevas.create_text(60, 550,text="Lettres utilisées :",fill='black',font='Courrier 10')     # Pour cette zone de texte et celle des essais, j'aurai pu faire comme pour les photos, définir le texte au préalable et afficher ensuite
        afficher_utilisee = canevas.create_text(120,575,text=lettre_essayee,fill='black',font='Courrier 10')     # Ici on affiche toutes les lettres déjà utilisées répertoriées dans "lettre_dans_mot"



    def avant_partie():     # Cette fonction est la base de mon programme elle définit tout ce qu'on aura besoin plus tard
        global mot_a_trouver, mot_partiel, lettres,photo, alphabet
        global nberreur,aide, lettre_essayee, pendu_dessin, arreter
        arreter = False     # Cette variable changera en fin de partie pour stopper toutes interactions avec la page
        nberreur = 0
        lettre_essayee = []
        aide = 0
        photo=PhotoImage(file="image/pendu_0.gif")     # Je récupère mon image de base
        pendu_dessin = Label(canevas, image = photo, border = 0.5)     # Je crée mon Label qui acceuillera l'image
        pendu_dessin.place(x=120, y=140)     # Et je l'affiche
        if deux_joueur == True :     # Si il y a deux joueurs nous n'avons pas besoin de séléctionner un mot
            choix_mot()     # Donc on utilise la fonction "choix_mot()"
        else :      # Si le joueur est seul, on doit alors prendre un mot au hasard dans une liste
            netoyage(liste_mots)     # On doit nettoyer la liste pour supprimer tous les "/n" à la fin des mots
            emplacement = randint(0,len(liste_mots))     # On choisit un emplacement au hasard dans la liste
            if len(liste_mots[emplacement]) > longueur_mot :     # Je vérifie si le mot n'est pas plus long que la limite fixée par le joueur
                while len(liste_mots[emplacement]) > longueur_mot :
                    emplacement = randint(0,len(liste_mots))     # On choisit un autre emplacement jusqu'à ce que le mot auquel il correspond soit plus petit que la limite
            mot_a_trouver = liste_mots[emplacement]     # Maintenant on prend l'emplacement dans la liste on prend le mot correspondant et ça sera notre "mot_a_trouver"
            #print(mot_a_trouver)     # Je le print pour mes tests
            mot_partiel = "_"*len(mot_a_trouver)
            afficher_mot(mot_partiel)

    def rejouer ():
        global alphabet
        for i in range(len(alphabet)):
            alphabet[i].config(text=chr(i+65), fg="black", command=lambda x=i+65:lettre_dans_mot(chr(x)))     # Je modifie toutes les lettres pour leur mettre la lettre initiale en noir car elles ont pu devenir un X rouge ou un O vert dans la partie d'avant
        avant_partie()     # Et je lance une partie normale

    #Aspect visuel

    fenetre = Tk()     # Je crée ma fenêtre Tkinter
    fenetre.title("Le jeu du pendu")
    fenetre.iconbitmap("pendu.ico")
    fenetre.config(bg="#E1E1E1")

    canevas = Canvas(fenetre, bg='white', height=600, width=620)     # Je crée un Canvas, sur Tkinter c'est une zone rectangulaire destinée à contenir des photos, des zones de textes ect...
    canevas.pack(side=BOTTOM)

    alphabet = [0]*26     # Je crée une liste de 26 "0" que je modifie juste après
    for i in range(len(alphabet)):
        alphabet[i] = Button(fenetre,text=chr(i+65),command=lambda x=i+65:lettre_dans_mot(chr(x)))     # La commande "lambda" nous permet d'éviter de créer un fonction, au lieu de lambda nous aurions pu créer une fonction qui fait juste (x=i+65 puis lettre_dans_mot(chr(x)))
        alphabet[i].pack(side=LEFT)     # J'utilise le code ASCII, la lettre "A" est le numéro 65, la "B" est le numéro 66... donc je prends la valeur de i et j'y ajoute 65 pour avoir le numéro de la lettre puis je fais (chr()) qui met en carractère les nombres entiers sur base décimal

    bouton_quitter = Button(fenetre, text="Quitter", relief=GROOVE, command=fenetre.quit)     # Mon bouton fermera tout simplement la page
    bouton_quitter.pack(side=RIGHT)

    avant_partie()

    recom = Button(fenetre,text="Recommencer", relief=GROOVE, command= rejouer )     # Mon bouton ici exécute la fonction "avant_partie()" qui me permet d'initialiser une nouvelle partie
    recom.pack(side=RIGHT)

    lettres = canevas.create_text(320,60,text="",fill='black',font='Courrier 30')     # Je crée une zone de texte dans mon canvas, qui acceuilera les lettres



    fenetre.mainloop()
    fenetre.destroy()
# Fin de la fonction jeu, début de la phase de l'avant jeu

def ordi_francais():
    global longueur_mot
    longueur_mot = long.get()     # Je récupère la valeur définit par le joueur pour la longueur max de la longueur
    idee = 1     # Je suis obligé de faire ça sinon toutes les fonctions dans les boutons sont exécutées, je ne sais pas pourquoi mais mettre une simple condition ça fonctionne
    if idee==1:
        arreter = False
        miseenplace.destroy()     # Je ferme ma page
        jeu(1)     # Je lance ma fonction "jeu" avec pour argument "1" qui est la langue française

def ordi_anglais():     # Même chose qu'au dessus
    global longueur_mot
    longueur_mot = long.get()
    idee = 1
    if idee==1:
        arreter = False
        miseenplace.destroy()
        jeu(2)

def parti_duo():     # Même chose qu'au dessus mais sans la limite de caractères
    idee = 1
    if idee==1:
        arreter = False
        miseenplace.destroy()
        jeu("duo")

def parti_solo():     # Là c'est la fonction qui va servir quand la personne veut jouer en solo
    global zone,photo_menu1,photo,longueur_mot,long
    idee = 1
    if idee == 1:
        photo=PhotoImage(file="image/langue.gif")
        photo_menu1.config(image = photo, border = 0.5)    # Je configure la photo déjà existante, je la remplace par une nouvelle
        test.config(text="Français", command=ordi_francais)
        test.place(x=120, y=570)
        test2.config(text="Anglais", command=ordi_anglais)
        test2.place(x=450, y=575)
        long = Scale(miseenplace, orient='horizontal', from_=4, to=15, length=578)     # Un "Scale" est un curseur où on peut varier entre deux valeurs dans un intervalle
        long.place(x=0, y=0)

#Fin de la fonction jeu

miseenplace = Tk()     # Je crée une première fenêtre pour que le joueur configure la partie
miseenplace.title("L'avant jeu")
miseenplace.iconbitmap("avant.ico")

zone = Canvas(miseenplace,height=600, width=620)     # Je crée un canvas pour ma photo et mes boutons
zone.pack(side=BOTTOM)

photo=PhotoImage(file="image/acceuil.gif")     # Je configure ma photo
photo_menu1 = Label(zone, image = photo, border = 0.5)
photo_menu1.pack()


test = Button(miseenplace,text="Jouer à deux", relief=GROOVE, command=parti_duo)
test.place(x=375, y=610)     # Mes deux boutons renvoient vers les fonctions 'partu_duo' et 'parti_solo'

test2 = Button(miseenplace,text="Jouer contre l'ordi", relief=GROOVE, command=parti_solo)
test2.place(x=70, y=615)

miseenplace.mainloop()    # Sans cela les interfaces Tkinter ne marchent pas


"""
Les 4 variables :
mot_a_trouver qui est définit à la ligne 111 et qui ne sera jamais modifié

mot_large qui est définit dans la fonction "afficher_mot(mot)" et n'est utilisé que dans celle ci, c'est grâce a lui qu'on affichera les mots en effet mot large aura les mêmes caractères que "mot" qui sera donné en argument mais avec un espace entre chaque caractère

mot_partiel qui est définit au début de partie par des "_" et il y en aura autant que le nombre de lettres dans le mot à trouver et cette variable sera possiblement modifier à la fin de chaque tour pour prendre les caractères de nouveau_mot_partiel car c'est le mot qui est affiché

nouveau_mot_partiel qui est le mot crée au début de chaque tour on comparera si la lettre choisi correspond à chaque lettre de mot à trouver.
    Si elle correspond, cette lettre est ajoutée à nouveau_mot_partiel mais si elle ne corresopond pas c'est la lettre du mot_partiel qui est ajoutée.
    On utilise nouveau_mot_partiel pour pouvoir faire des modifications à mot_partiel plus facilement
"""