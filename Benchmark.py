
import fitz
from TextSearch import *
import time
import matplotlib.pyplot as pl
#faire pip install PyMUPDF


 
#------------Version du code dédiée au benchmark-------------#


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


def Recherche_Textuelle(objet, mot, algo):
    """
    objet - object : Instance de fitz.Document représentant un document PDF.
    Ce dernier contient un tableau dont les éléments sont eux-mêmes
    des objets représentant le contenu d'une page spécifique du PDF. La méthode .get_text()
    peut être utilisée pour extraire le texte sous forme de chaîne de caractères d'une page PDF.
    algo - function : fonction d'algorithme de recherche
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
        presence = algo(texte, mot)
        if  presence != []: #On vérifie si le mot est contenu dans la page
            for element in presence:  #Rappel : la fonction Boyer Moore renvoie un tableau d'indice il faut donc parcourir les éléments
                occurences.append(f"Page {i+1} Ligne {dictionnaire[element]}") 
    return occurences


def Page_vers_str(objet, page):
    """
    objet - object : Instance de fitz.Document représentant un document PDF.
    Ce dernier contient un tableau dont les éléments sont eux-mêmes
    des objets représentant le contenu d'une page spécifique du PDF. La méthode .get_text()
    peut être utilisée pour extraire le texte sous forme de chaîne de caractères d'une page PDF.
    algo - function : fonction d'algorithme de recherche
    """
     
    texte = objet[page].get_text().lower()
    texte = texte.lower() #On met tout en minuscule
    return texte

    
#--------------Benchmark--------------#


def duree(f, mot):
    """
    f - function
    mot - str le mot qu'on recherche
    Sortie: float - temps nécessaire au traitement de la fonction f (moyenne)
    """
    moyenne = 0
    i = 0
    while i < 500:  #Le nombre d'essais
        start = time.time()
        a = f(txt, mot)
        tps = time.time() - start
        moyenne += tps
        i += 1
    moyenne = moyenne/i
    return moyenne
    






if __name__ == '__main__':
    #txt = open("miserable.txt").read()

    txt = ""
    pages = []
    #print(txt)
    pdfFileObj = fitz.open("lesmiserables.pdf")
    # tableau des entiers de 100 Ã  4000
    nombre_Page = []  #tableau de str qui contient le nombre d'occurence d'un mot du tableau Mots

    # création du tableau des durÃ©es pour chaque fonction
    rabin_karpTAB = []                             # algo01
    boyer_mooreTAB = []                             # algo02
    naif_TAB = []                                      #algo 03
    mot = "Tout ce qui l’entourait"   #le caractère qu'on recherche
    for i in range(0, pdfFileObj.page_count, 100):
        txt += Page_vers_str(pdfFileObj, i) #ajout progressif du texte 
        rabin_karpTAB.append(duree(rabin_karp, mot))
        naif_TAB.append(duree(naif, mot))
        boyer_mooreTAB.append(duree(boyer_moore, mot))
        pages.append(i+1)
        print(i)
        
        
    # courbes des temps de traitement en fonction de l'entier n
    # rabin_karp en rouge pointillés
    # boyer_moore en bleu continu
    # naif en vert pointillé
    T01, = pl.plot(pages, rabin_karpTAB, 'r--')
    T02, = pl.plot(pages, boyer_mooreTAB, 'b')
    T03, = pl.plot(pages, naif_TAB, 'g--')
    print("Nb occurence Boyer_moore", len(boyer_moore(txt,mot )))
    print("Nb occurence naif", len(naif(txt,mot )))
    print("Nb occurence rabin_karp", len(rabin_karp(txt,mot )))
    
    pl.legend( [T01, T02, T03], ["rabin_karp()", "boyer_moore()", "naif()"])
    pl.xlabel("Nombre de pages : une page compte en moyenne 96 mots  (95 731 mots total)")
    pl.ylabel("Temps d'exécution : t (ms)")
    pl.grid()
    pl.show()
    



    
   