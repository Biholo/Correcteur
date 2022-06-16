import subprocess
import csv
import os

def recup_nom():
    os.chdir("eleves_bis")
    text = subprocess.check_output(["ls", "-l"]) 
    return text

def ajoute_lst():
    Lst = []
    text = str(recup_nom())
    text = text.split(".c")
    for L in text:  
        L+='\n'
        pos = L.find("2019")
        var = L[pos+5:-1]
        Lst.append([var])
    return Lst

def test_programme(execute, valeur1, valeur2):
    test1 = subprocess.run([execute, str(valeur1), str(valeur2)],capture_output=True, text=True)
    test1 = test1.stdout
    verif = "La somme de " + str(valeur1) + " et " + str(valeur2) + " vaut " + str(valeur1 + valeur2) + "\n"

    if(test1 == verif):
        return 1
    else:
        return 0

def nb_lignes(file):
    compt = 0
    comment = '/*'
    fichier = open(file,"r")
    lignes = fichier.readlines()
    for ligne in lignes:
        if comment in ligne:
            compt+=1
    return compt        


def execute(lst):
    #Stock les valeurs des test dans 2 tableaux
    num1 = [0,1,0,1,12,12,-1]
    num2 = [0,0,1,1,12,-43,-52]

    for i in range(len(lst)-1):
        execute = "./" + lst[i][0]
        var = lst[i][0] + ".c"
        compt_test = 0

            
        try:
            result = subprocess.run(["gcc", var, "-o",lst[i][0], "-Wall"], capture_output=True, text=True)
            err_1 = result.stderr
            nb_warning = err_1.count("warning")
            commentaire = nb_lignes(var)
            
            for j in range(len(num1)):
                if(test_programme(execute, num1[j], num2[j]) == 1):
                    compt_test+=1

            lst[i].append(1)
            lst[i].append(nb_warning)
            lst[i].append(compt_test)
            lst[i].append(commentaire)

        except:
            lst[i].append(0)
            lst[i].append(0)
            lst[i].append(0)
            lst[i].append(0)
            
    return lst



def vers_csv(lst):
    #Place les notes dans un fichier csv
    os.chdir("../")
    with open('note.csv','w', newline='') as fichiercsv:
        writer=csv.writer(fichiercsv)
        writer.writerow(['Nom','Validité compilation','Nb warning','test réussie','Ligne comment','Note compilation','Note Final'])
        for i in range(len(lst)-1):
            writer.writerow([lst[i][0], lst[i][1], lst[i][2], lst[i][3], lst[i][4]])

        
tab = ajoute_lst()
resultat = execute(tab)
vers_csv(tab)
print("Fin de la correction !")
