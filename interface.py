import os
import fitz
from TextSearch import *
import tkinter as tk
from tkinter import filedialog

#faire pip install PyMUPDF
#pip install tkinter
#pip install tk

 


    
#-----------------------Partie II-----------------------#
def indice_vers_ligne(Page):
    """
    Page - str : Chaine de caractère provenant d'une page PDF marqué par des retours
    à la ligne.
    Sortie - dict : Un dictionnaire dont chacune des clés représente l'indice d'une lettre
    de Page et dont la valeur de cette dernière est le numéro de ligne à laquelle elle
    appartient dans page. Pour déterminer le numéro de ligne d'une lettre
    nous nous fions à la présence des '/n' qui représentent les retours à la ligne.
    """
    indice_vers_ligne = {}
    ligne = 1 #la ligne de départ
    for i in range(len(Page)):
        if Page[i] == '\n':
            ligne += 1
            if not Page[i+1:].lstrip():
                continue
        indice_vers_ligne[i] = ligne
    return indice_vers_ligne


def Recherche_Textuelle(objet, mot, methode):
    """
    objet - object : Instance de fitz.Document représentant un document PDF.
    Ce dernier contient un tableau dont les éléments sont eux-mêmes
    des objets représentant le contenu d'une page spécifique du PDF. La méthode .get_text()
    peut être utilisée pour extraire le texte sous forme de chaîne de caractères d'une page PDF.
    mot - str :  le mot à rechercher dans l'ensemble de notre page pdf.
    Sortie : Tableau dont les éléments sont des str. Chaque élément du tableau
    indique la page et la ligne à laquelle est présent mot dans le pdf.
    """
    mot = mot.lower() #On met tout en minuscule
    occurences = []
    for i in range(0, len(objet)):
        texte = objet[i].get_text().lower()
        #print(texte)
        dictionnaire = indice_vers_ligne(texte) #A chaque indice on associe une ligne dans la page
        presence = methode(texte, mot)
        if  presence != []: #On vérifie si le mot est contenu dans la page
            for element in presence:  #Rappel : la fonction Boyer Moore renvoie un tableau d'indice il faut donc parcourir les éléments
                occurences.append(f"Page {i+1} Ligne {dictionnaire[element]}") 
    return occurences


#------------------Interface de commande-----------------#


def choixPDF():
    """
    Affiche les pdfs présent dans la console et demande à l'utilisateur de choisir
    parmi un de ceux présent dedans. Retourne un le nom d'un des fichiers choisi
    par l'utilisateur (str).
    """
    entries = os.listdir() #Obtention de tous les fichiers du dossier
    PDF = []
    for entry in entries:
        if(entry.endswith(".pdf")):  #Trie des fichiers (on ne garde que les pdf)
            print(entry)
            PDF.append(entry)
    if PDF == []:
        print("\n\nIl n'y a pas de document PDF. Veuillez ajouter un PDF dans le même dossier que le fichier python")
    choix = input("\nVeuillez sélectionner un document PDF dans la liste en l'écrivant (format : nomFichier.pdf) : ")
    while not(choix in PDF):
        for fichier in PDF:
            print(fichier)
        choix = input("\nLe fichier sélectionné doit être un PDF. Assurez vous de l'avoir bien écrit (format : nomFichier.pdf) : ")
    return choix

def choixAlgo():
    print("\nVoici les algorithmes de recherche disponibles : \n boyer-moore : 1\n naif : 2\n rabin-karp : 3\n(écrivez un numéro)")
    algo = input("\nQuel algorithme choisir ? : ")
    if algo == 'retour':
        return 'retour'
    while not(algo in ['1','2','3']):
        print("\n(Voici les algorithmes de recherche disponibles : \n boyer-moore : 1\n naif : 2\n rabin-karp : 3\n(sélectionnez un numéro)")
        algo = input("\nNuméro incorrect... Vous devez écrire un des numéros ci-dessus pour sélectionner un algorithme ou bien écrire 'retour' afin sélectionner un autre pdf : ")
        if algo == "retour":
            return 'retour'
    return algo

#--------------Bonus--------------#

#--------------Interface Graphique--------------#

chemin_fichier_pdf = ""
algorithme_selectionne = "Boyer-Moore"  # Algo par défaut

def selectionner_fichier_pdf():
    """
    Fonction de sélection d'un fichier PDF à l'aide de la boîte de dialogue de fichier Tkinter.
    Met à jour la variable globale chemin_fichier_pdf.
    """
    global chemin_fichier_pdf
    chemin_fichier = filedialog.askopenfilename(filetypes=[("Fichiers PDF", "*.pdf")])
    if chemin_fichier:
        chemin_fichier_pdf = chemin_fichier
        label_fichier.config(text=f"Fichier PDF sélectionné : {os.path.basename(chemin_fichier)}")

def definir_algorithme(algorithme):
    """
    Fonction permettant de définir l'algorithme de recherche sélectionné.
    
    algorithm - str, Nom de l'algorithme de recherche.
    """
    global algorithme_selectionne
    algorithme_selectionne = algorithme

def effectuer_recherche():
    """
    Fonction permettant d'effectuer une recherche de texte dans le fichier PDF sélectionné.
    Affiche le résultat dans l'étiquette_résultat de l'interface graphique.
    """
    if not chemin_fichier_pdf:
        label_resultat.config(text="Veuillez sélectionner un fichier PDF.")
        return

    mot_recherche = entry_recherche.get()
    if not mot_recherche:
        label_resultat.config(text="Veuillez saisir un mot de recherche.")
        return

    objet_fichier_pdf = fitz.open(chemin_fichier_pdf)

    # On appelle ici notre fonction de recherche textuelle
    resultats_recherche = Recherche_Textuelle(objet_fichier_pdf, mot_recherche, obtenir_algorithme_recherche(algorithme_selectionne))

    if resultats_recherche:
        texte_resultat = "\n".join(resultats_recherche)
    else:
        texte_resultat = "Aucun mot correspondant n'a été trouvé."

    label_resultat.config(text=texte_resultat)

def obtenir_algorithme_recherche(nom_algorithme):
    """
    Fonction permettant de faire correspondre les noms d'algorithmes aux fonctions de recherche.

    nom_algorithme - str, Nom de l'algorithme de recherche.

    Sortie:
        str, Fonction de recherche associée à l'algorithme.
    """
    if nom_algorithme == "Boyer-Moore":
        return boyer_moore
    elif nom_algorithme == "Naif":
        return naif
    elif nom_algorithme == "Rabin-Karp":
        return rabin_karp


if __name__ == "__main__":
    racine = tk.Tk()
    racine.title("Recherche de texte dans le PDF")
    racine.geometry("720x720")

    label_fichier = tk.Label(racine, text="Fichier PDF sélectionné :")
    label_fichier.pack(pady=10)

    bouton_selection = tk.Button(racine, text="Sélectionner le fichier PDF", command=selectionner_fichier_pdf, width=50, height=3)
    bouton_selection.pack(pady=10)

    # Menu déroulant pour la sélection de l'algorithme
    options_algorithme = ["Boyer-Moore", "Naif", "Rabin-Karp"]
    var_algorithme = tk.StringVar(racine)
    var_algorithme.set(options_algorithme[0])  # Valeur par défaut
    menu_algorithme = tk.OptionMenu(racine, var_algorithme, *options_algorithme)
    menu_algorithme.pack(pady=10)

    entry_recherche = tk.Entry(racine, width=100)
    entry_recherche.pack(pady=10)

    # Bouton pour définir l'algorithme sélectionné
    bouton_definir_algorithme = tk.Button(racine, text="Définir l'algorithme", command=lambda: definir_algorithme(var_algorithme.get()), width=50, height=3)
    bouton_definir_algorithme.pack(pady=10)

    bouton_recherche = tk.Button(racine, text="Recherche", command=effectuer_recherche, width=50, height=3)
    bouton_recherche.pack(pady=10)

    label_resultat = tk.Label(racine, text="")
    label_resultat.pack(pady=10)

    racine.mainloop()   # Pour accéder à l'interface de la console, il suffit de fermer l'interface graphique
    


    algo = ["boyer_moore","naif", "rabin_karp"]
    
    decision = choixPDF()
    pdfFileObj = fitz.open(decision)
    AlgoChoisi = choixAlgo()
    while AlgoChoisi == "retour":
        decision = choixPDF()
        pdfFileObj = fitz.open(decision)
        AlgoChoisi = choixAlgo()
        
    while True:
        mot = input(f"\nLe document sélectionné est {decision} avec l'algorithme {algo[int(AlgoChoisi)-1]}, quel mot souhaitez-vous rechercher ?\nPour retourner à la sélection des documents pdf, écrivez 'retour' ")
        if (mot == "retour") or (AlgoChoisi == 'retour'):
            decision = choixPDF()
            pdfFileObj = fitz.open(decision)
            AlgoChoisi = choixAlgo()
        
        else:
            tabIndices = Recherche_Textuelle(pdfFileObj, mot, boyer_moore)
            for element in tabIndices:
                print(element)
            if tabIndices == []:
                print("\nAucun mot n'a été trouvé.")
                

   
    
#-----------------------------Tests---------------------#
    pdfFileObj = fitz.open("lesmiserables.pdf")
    texte = "je pense donc je suis"
    print(texte)
    resultat = [i for i in range(len(texte)) if texte.startswith("uis", i)] #Méthode de python pour la recherche textuelle
    print(boyer_moore("je pense donc je suis", "uis") == resultat )
    print(boyer_moore("je pense donc je su\nis", "uis") == resultat)
    print(rabin_karp("je pense donc je suis", "uis") == resultat)
    print(rabin_karp("je pense donc je su\nis", "uis") == resultat)
    print(naif("je pense donc je suis", "uis") == resultat)
    print(naif("je pense donc je su\nis", "uis") == resultat)
    

    
    
    texte = "cablabdcabcabn69é*cabpabpcabcaebc"
    resultat = [i for i in range(len(texte)) if texte.startswith("abc", i)]
    print(boyer_moore(texte, "abc"))
    print(resultat)
    print(boyer_moore(texte, "abc") == resultat )
    print(rabin_karp(texte, "abc") == resultat)
    print(naif(texte, "abc") == resultat)
    
    texte = "Le mot recherché n'est pas dedans 😊😊😊"
    resultat = [i for i in range(len(texte)) if texte.startswith("Rien", i)]
    print(boyer_moore(texte, "Rien") == resultat )
    print(rabin_karp(texte, "Rien") == resultat)
    print(naif(texte, "Rien") == resultat)
    print(boyer_moore("je pense donc je suis", "uis"))
    print(boyer_moore("je pense donc je suis", "suis"))
    print(boyer_moore("je pense donc je suis", "pas"))
    print(boyer_moore("je pense donc je suis", "j"))
    print(boyer_moore("je pense donc je suis", "pas"))
    print(boyer_moore("je pense donc je suis je pense donc je suis", "je"))
    
     #-----------------Tests de recherche Textuelle sur le doc PDF les misérables (voir pièce jointe)------------#
    
    #Note : Pour tester, on compare ici les divers résultats de nos algorithmes
    boyer = Recherche_Textuelle(pdfFileObj, "couvent de la rue du temple", boyer_moore)
    rabin = (Recherche_Textuelle(pdfFileObj, "couvent de la rue du temple", rabin_karp )) 
    naif = (Recherche_Textuelle(pdfFileObj, "couvent de la rue du temple", naif )) 
    print((boyer == rabin) and (boyer == naif))
    
    
         
    #--------------------Autre Tests----------------#
    
    print(indice_vers_ligne("test, test,\n :) ") == {0: 1, 1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1, 8: 1, 9: 1, 10: 1, 11: 2, 12: 2, 13: 2, 14: 2, 15: 2})
    print(indice_vers_ligne("\n\n\n\n") == {})
    print(indice_vers_ligne("\n\n\n\nn") == {0: 2, 1: 3, 2: 4, 3: 5, 4: 5})
    print(indice_vers_ligne("Ceci \n cela \n de /n/n/nddd/n") == {0: 1, 1: 1, 2: 1, 3: 1, 4: 1, 5: 2, 6: 2, 7: 2, 8: 2, 9: 2, 10: 2, 11: 2, 12: 3, 13: 3, 14: 3, 15: 3, 16: 3, 17: 3, 18: 3, 19: 3, 20: 3, 21: 3, 22: 3, 23: 3, 24: 3, 25: 3, 26: 3, 27: 3})
    print(indice_vers_ligne("") == {})
    
