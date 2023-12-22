import doctest

#-----------------Algo Rabin-karp---------------#
def rabin_karp(texte, motif): 
    """
    texte - str : Le texte dans lequel la recherche du motif sera effectuée.
    motif - str : Le motif à rechercher dans le texte.
    Sortie - index (list) : Une liste d'indices des occurrences du motif dans le texte.
                    Si aucune occurrence n'est trouvée, la liste est vide.
    >>> rabin_karp("abcabca", "ca")
    [2, 5]
    >>> rabin_karp("abcdef", "xyz")
    []
    >>> rabin_karp("", "x")
    []
    >>> rabin_karp("cqfzqqz#", " ")
    []
    >>> rabin_karp("cqfzqqz#", "")
    [0, 1, 2, 3, 4, 5, 6, 7, 8]
    
    Des tests additionnels sont dans le main du fichier principal.
    """
    texte = texte.replace('\n', '') #On retire les retours à la ligne
    n = len(texte)
    m = len(motif)
    index = []

    for i in range(n - m + 1):
        if hash(texte[i:i+m]) == hash(motif):
            if texte[i:i+m] == motif:
                index.append(i)
    
    return index
 #------------------Algo Naif--------------------#

def naif(motif, chaine):
    """ 
    chaine - str : la chaine de caractère qu'on recherche dans le motif.
    motif - str : un motif dans lequel on cherche texte.
    Sortie - index (list) : Une liste d'indices des occurrences du motif dans le texte.
    Si aucune occurrence n'est trouvée, la liste est vide.
    >>> naif("abcabca", "ca")
    [2, 5]
    >>> naif("abcdef", "xyz")
    []
    >>> naif("", "x")
    []
    >>> naif("cqfzqqz#", " ")
    []
    >>> naif("cqfzqqz#", "")
    [0, 1, 2, 3, 4, 5, 6, 7, 8]
    
    Des tests additionnels sont dans le main du fichier principal.
    
    """
    motif = motif.replace('\n', '') #on retire les retours à la ligne
    result = []
    for i in range(len(motif)-len(chaine)+1):
        mot = ""
        for j in range(len(chaine)):
            mot = mot + motif[i+j]
        if mot == chaine:
            result.append(i)
    return result

#---------------Boyer-Moore-------------------#

def decalage(chaine):
    """
    chaine - str : une chaine de caractère.
    Sortie - Dict : Dictionnaire dont les clés sont des lettres et la valeur,
    le nombre de décalage nécessaire pour atteindre la lettre en question dans le motif. Il s'agit
    d'une fonction intermédiaire utilisée dans boyer_moore().
    Cette dernière est utilisée pour appliquer la "règle du mauvais caractère".
    >>> decalage("Ceci est un teste")
    {'C': 16, 'e': 3, 'c': 14, 'i': 13, ' ': 5, 's': 2, 't': 1, 'u': 7, 'n': 6}
    >>> decalage("D")
    {}
    >>> decalage("DDDDD")
    {'D': 1}
    >>> decalage("DFDDD")
    {'D': 1, 'F': 3}
    >>> decalage("")
    {}
    """

    dictionnaire = {}
    for i in range(len(chaine)-1):
        dictionnaire[chaine[i]]=len(chaine)-1-i
    return dictionnaire


def Indice_suffixe(suffixe, mot):  
    """ 
    suffixe - int : le suffixe qu'on recherche dans mot. 
    mot - str : mot (motif) dans lequel on recherche le suffixe.
    Sortie - tab : Tableau d'indice (int) des occurences de suffixe dans mot.
    >>> Indice_suffixe("abcdefgh", "ab")
    []
    
    >>> Indice_suffixe("avion", "J'ai râté l'avion bon sang...")
    [12]
    
    >>> Indice_suffixe("suffixe", "A la recherche de ce suffixe, ce suffixe" )
    [21, 33]
    """
    

    return [i for i in range(len(mot)) if mot.startswith(suffixe, i)]

def est_PresentSuffixe(suffixe, mot):
    """ 
    suffixe - str : suffixe (caractères valides parcourus dans le motif) dont on veut
    savoir si il contient un sous-suffixe présent dans mot.
    mot - str : le mot dans lequel on recherche si suffixe ou un sous-suffixe est présent
    Sortie - Bool ou str : Renvoie False si aucun suffixe ou sous-suffixe est présent dans mot.
    Sinon, l'indice d'occurence du sous-suffixe ou du suffixe présent dans mot est renvoyé.
    
    >>> est_PresentSuffixe("cet", "Le suffixe 'cet' est dans  cet exemple" )
    'cet'
    
    >>> est_PresentSuffixe("avion", "J'ai râté l'avion bon sang...")
    'avion'
    
    >>> est_PresentSuffixe("suffixe", "A la recherche de ce suffixe, ce suffixe" )
    'suffixe'
    
    >>> est_PresentSuffixe("re", "il y a un sous-suffixe présent dans 'dire'")
    're'
    
    >>> est_PresentSuffixe("re", "il y a un sous-suffixe présent dans 'dier'")
    False
    
    >>> est_PresentSuffixe("Non", "Le suffixe n'est pas présent dans cet exemple")
    False
    
    >>> est_PresentSuffixe("DEAB", "DBACCBCADCABBCE")
    'AB'
    
    >>> est_PresentSuffixe('DC', "DCB")
    'DC'
    
    """
    

    for i in range(len(suffixe), 1, -1): #on s'arrête à un minimum de 2 caractères, sinon ça n'est plus un suffixe
        nouvSuffixe = suffixe[:i] #on fait progressivement diminuer le suffixe
        nouvSuffixe1 = suffixe[i*-1:]
        if nouvSuffixe in mot:
            return nouvSuffixe
        elif (nouvSuffixe1 in mot):
            return nouvSuffixe1
    return False
    



def verif_correspondance(chaine, mot, indice_chaine):
    """
    chaine - str : La chaine de caractère dans laquelle pourrait se trouver mot.
    mot - str : La mot qu'on souhaite retrouver dans chaine.
    indice_chaine : int - L'indice à laquelle on positionne mot dans chaine (par le droite).
    Sortie - bool : Vérifie lettre par lettre la correspondance entre une partie
    de la chaine de caractère et le mot. Si chaque lettre de mot correspond dans chaine à l'indice
    donnée, alors renvoie True. Si seulement une partie des lettres (suffixe) de chaine correspondent à mot,
    le programme vérifie si le suffixe ou la dernière lettre non présente dans se trouve ailleurs dans le mot,
    si c'est le cas, renvoie un int correspondant au glissement nécessaire pour atteindre la lettre / le suffixe dans mot, 
    false est renvoyé sinon.
    
    >>> verif_correspondance("Ceci est une chaine // Ceci est une chaine", "est", 11)
    2
    
    >>> verif_correspondance("Ceci est une chaine // Ceci est une chaine", "est", 19)
    False
    
    >>> verif_correspondance("Cas du mauvais caractère", "miuvans", 13)
    5

    >>> verif_correspondance("Cas du aiuvais bon suffixe", "ainvais", 13)
    3
    """
    indice = len(mot) -1
    indice_actuel = indice_chaine
    i_chaineMinimum = indice_chaine-(len(mot)-1)
    corresp = True
    Carac_Parcourus = ''
    while (indice_actuel >= i_chaineMinimum) and (corresp == True): #On verifie 1 à 1 pour voir si le mot se trouve dans notre chaine
        if mot[indice] != chaine[indice_actuel]:  #Mismatch détecté on arrête de parcourir
            corresp = False
        if mot[indice] == chaine[indice_actuel]:
            Carac_Parcourus = chaine[indice_actuel] + Carac_Parcourus
            indice -= 1
            indice_actuel -= 1
    if corresp == False:  #Echec de la correspondance ; mot ne se trouve pas à l'indice donnée
        #mot[:indice*-1] permet de retirer le suffixe (déjà parcouru) à la fin du mot
        suffixe = est_PresentSuffixe(Carac_Parcourus, mot[:indice*-1])
        if (suffixe != False):  #Règle "du bon suffixe"
            position_suffixe =  Indice_suffixe(suffixe, mot) #Retourne tableau de l'ensemble des occurences de suffixe dans mot 
            position_suffixe_i_chaine = indice_chaine+1-position_suffixe[-1] #obtention de l'indice du suffixe dans la chaine
            return (indice_chaine + 1) - (position_suffixe_i_chaine)  #Retourne le glissement nécessaire 
        elif chaine[indice_actuel] in decalage(mot):   #Règle du mauvais caractère
            return decalage(mot)[chaine[indice_actuel]]
        return False  #La dernière lettre parcourue n'est pas dans mot, on avance donc de len(mot)
    return corresp #corresp est ici True, cela signifie que mot se trouve à l'indice_actuel dans chaine

def boyer_moore(chaine, mot):
    """
    chaine - str : Une chaine de caractère.
    mot - str : ensemble de caractère recherché dans la chaine.
    Sortie - index (list) : Une liste d'indices des occurrences du mot dans le texte.
    Si aucune occurrence n'est trouvée, la liste est vide. Les majuscules et les espaces sont
    aussi pris en compte.
    >>> boyer_moore("abcabca", "ca")
    [2, 5]
    >>> boyer_moore("abcdef", "xyz")
    []
    >>> boyer_moore("", "x")
    []
    >>> boyer_moore("cqfzqqz#", " ")
    []
    >>> boyer_moore("cqfzqqz#", "")
    [0, 1, 2, 3, 4, 5, 6, 7, 8]
    """
    chaine = chaine.replace('\n', '') #On retire les retours à la ligne.
    indice_occurence = []
    i_chaine = len(mot)-1
    if mot == "":
        return [i for i in range(len(chaine)+1)]
    while i_chaine < len(chaine):
        if (chaine[i_chaine] == mot[-1]): #On vérifie si les lettres de fin correspondent
            resultat =  verif_correspondance(chaine, mot, i_chaine) #si c'est le cas, on parcourt jusqu'à correspondance 
            if not(isinstance(resultat, bool)):  #Si resultat est un nombre (indice du décalage)
                i_chaine += resultat
            elif resultat == True: 
                indice_occurence.append(i_chaine - (len(mot)-1))
                i_chaine += len(mot)
            else: #resultat False / Règle du mauvais caractère
                i_chaine += len(mot)  #Cas ou il n'y a pas de correspondance
        elif (chaine[i_chaine] in decalage(mot)): #Si la dernière lettre de chaine est contenue dans mot...
            i_chaine += decalage(mot)[chaine[i_chaine]] 
        else:
            i_chaine += len(mot)
    return indice_occurence

doctest.testmod()