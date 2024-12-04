from random import randint, choice

class Classes:
    """Classe contenant la liste des classes"""
    def __init__(self) :
        self.listeClasses = [
        Personnage("Guerrier", 790, 69, 38, 34, 15, epee_de_feu, 100, True),
        Personnage("Mage", 696, 112, 30, 30, 20, eclair, 100, True),
        Personnage("Assassin", 770, 70, 22, 70, 40, laceration_sanglante, 100, True),
        Personnage("Archer", 730, 97, 26, 33, 15, fleche_explosive, 100, True),
        Personnage("Dieu", 100000, 100000, 100000, 100000, 100000, jugement_divin, 100000, True)
        ] # on créer les classe du jeu
        
class Personnage:
    """Classe représentant un personnage


    """
    def __init__(self, nom:str, vie:int= 0, attaque:int= 0, defense:int= 0, agilite:int= 0, crit:int= 0, atqS= None, mpMax= 100, est_classe:bool= False ):
        self.nbCoupCrit = 0
        self.xpMax = 180
        self.mpMax = mpMax
        self.mp = mpMax
        self.nom = nom
        self.critChance = crit
        self.stats = {
            "Vie": vie,
            "Attaque": attaque,
            "CritChance": crit,
            "Defense": defense,
            "Agilité": agilite,
            "Exp": 0,
            "VieMax": vie,
            "ArmorPen": 0
        }
        self.inventaire = []

        self.niveau = 1

        self.statsBase = {
            "Vie": vie,
            "Attaque": attaque,
            "Defense": defense,
            "Agilité": agilite,
            "Exp": 0,
            "VieMax": vie
        }

        self.atqSpe = atqS
        if not est_classe: # si ce n'est pas une classe
            self.classes = Classes() # on créer un objet qui contient les classes possibles

        self.nbEnnemiBattu = 0
        self.classe = None

    def choisirClasse(self, nom):
        """on choisi la classe qu'on veut

        Paramètres:
            nom (str): le nom de la classe
        """
        for classe in self.classes.listeClasses: # on regarde la classe qu'on a choisi et on ajuste les stats
            if classe.nom == nom: 
                self.stats = classe.stats
                self.statsBase = classe.statsBase
                self.atqSpe = classe.atqSpe
                self.critChance = classe.critChance
                self.mp = classe.mp
                self.mpMax = classe.mpMax
        self.classe = nom


    def recupPV(self, prct):
        """
        Récupère une portion des points de vie du personnage.

        Paramètres :

            prct (float) : Le pourcentage de points de vie à récupérer.
        """
        soin = round(self.stats["VieMax"] * (1 - (prct / 100)), 2) # on recup 100-prct % de pv
        self.stats["Vie"] = min(self.stats["Vie"] + soin, self.stats["VieMax"]) # on actualise la vie en faisant attention de prendre au max la vie max du person
        return  f" {self.nom} à regagné {soin} HP. Vie actuelle : {round(self.stats['Vie'], 2)}"  # on renvoie le texte d'affichage
    def ajouter_objet(self, objet):
        """Ajoute un objet dans l'inventaire du personnage

        Paramètres:
            objet (Objet): L'objet à ajouter.
        """
        self.inventaire.append(objet) # on ajoute l'objet
        return (f"{self.nom} a obtenu l'objet : {objet}") # on renvoie le texte d'affichage

    def utiliser_objet(self, nom_objet, ennemi,lobjet):
        """
        Utilise un objet de l'inventaire du personnage.
        Paramètres :

            objet (Objet) : L'objet à utiliser
            ennemi (Ennemi) : l'ennemi sur lequel on veut utiliser l'objet
        """
        text = ""
        # on met objet_trouver a la valeur de l'objet si jamais l'objet qu'on veut utiliser est dans l'inventaire
        objet_trouve = None # on defini l'objet que l'on veut utiliser
        for objet in self.inventaire: #on parcours notre inventaire
            if objet == nom_objet: # si il est dedans alors on actualise la variable de l'objet que l'on veut utiliser
                for item in lobjet.listeObjet:
                    if item.nom == objet:
                        objet_trouve = item
                break # et on arrete de parcourir l'inventaire
        # si c'est pas = a None alors on peut utiliser l'objet
        if objet_trouve: 
            text += objet_trouve.appliquer_bonus(self) # on ajoute les stats de l'objet au personnage
            if self.critChance >100:
                self.critChance = 100
            
            text += objet_trouve.activer_effet_special(
                self, ennemi)  #  on fait l'attaque speciale de l'objet
            self.inventaire.remove(
                objet_trouve.nom
            )   # on enleve l'objet de l'inventaire
            ennemi.check() # on actualise la vie de l'ennemi
            return text+"\n"  # on renvoie le texte d'affichage



    def attaquer(self, ennemi):
        """
        Attaque un ennemi avec une chance de coup critique.

        Paramètres :

            ennemi (Ennemi) : L'ennemi à attaquer.
        """
        texte = f"{self.nom} attaque {ennemi.nom} ! " # texte a afficher
        if self.classe != 'Dieu':
            
            degats = self.stats["Attaque"] * (1 - ((ennemi.stats["Defense"]*(1-self.stats['ArmorPen']/100)) / ((ennemi.stats["Defense"]*(1-self.stats['ArmorPen']/100)) + 100)))  # calcule des degats

            if randint(0, 100) <= min((ennemi.stats['Agilité']/self.stats['Agilité'])*100,10): # pour que l'ennemi esquive l'attaque 
                texte += f" Mais {ennemi.nom} esquive l'attaque !" # texte a afficher
                return texte  # on renvoie le texte d'affichage

            if randint(0, 100) <= self.critChance: # faire un coup critique
                texte += f"Et il fait un coup critique !" # texte a afficher
                degats *= 1.75 # on augmente les degats
                self.nbCoupCrit += 1 # on incremente le compteur
            
            texte += f"\n{ennemi.nom} perd {round(degats, 1)} points de vie." # texte a afficher

            ennemi.stats["Vie"] = max(ennemi.stats["Vie"] - degats, 0) # on fait les degats a l'ennemi
            ennemi.stats["Vie"] = round(ennemi.stats["Vie"], 2) # on arrondi
            ennemi.check() # on actualise la vie de l'ennemi
        else: 
            texte += f"\nSeulement, {self.nom} juge que {self.ennem}"
        return texte  # on renvoie le texte d'affichage

    def setLevel(self, niveau):
        """
        Augmente le niveau du personnage et ajuste les stats en conséquence.

        Paramètres :

            niveau (int) : Le nouveau niveau du personnage.
        """
        for stat, val in self.statsBase.items(): # on remets les stats au niveau 1
            self.stats[stat] = val
        for i in range(niveau):
            self.gagnerExp(self.xpMax) # on augmente le niveau

    def gagnerExp(self, exp):
        """
        Ajoute de l'expérience au personnage et gère le passage de niveau.

        Paramètres :

            exp (int) : L'expérience à ajouter.
        """
        texte = ""  # texte à afficher
        xpSup = 0  # l'xp supplémentaire au passage de niveau
        self.stats["Exp"] += exp  # on ajoute l'xp gagné

        # Tant que l'expérience est suffisante pour passer au niveau suivant
        while self.stats["Exp"] >= self.xpMax:
            if self.stats["Exp"] > self.xpMax:
                xpSup = self.stats["Exp"] - self.xpMax  # on calcule l'expérience supplémentaire
            texte += self.gagnerNiveau()  # texte à afficher
            self.stats["Exp"] = xpSup  # réinitialise l'expérience à celle supplémentaire

        return texte + f"\n\nNiveau {self.niveau}, {round(self.stats['Exp'])} / {round(self.xpMax)} xp."


    def gagnerNiveau(self):
        """
        Gère le passage de niveau du personnage en augmentant ses stats.
        """
        texte = (f"\n\n{self.nom} est passé niveau {self.niveau + 1} !") # texte a afficher

        self.stats["Exp"] = 0 # on remet l'xp a zéro
        self.xpMax = round(self.xpMax * 1.03 + 350) # on augmente l'exp max
        self.niveau += 1 # on augmente le niveau

        for stat, base_value in self.statsBase.items(): # on augmente les stats du perso
            if stat == "Attaque":
                self.stats[stat] += round(self.statsBase[stat] / 15+base_value * 0.05, 10)
            elif stat == "Defense":
                self.stats[stat] += round(base_value * 0.0005, 10)
            else:
                self.stats[stat] += round(
                    self.statsBase[stat] / 15 + self.stats[stat] * 0.075, 10)
                
        for stat in self.stats:
            self.stats[stat] = min(self.stats[stat], 2147483647)
            

        self.stats["Vie"] = self.stats["VieMax"] # on remet la vie du joueur a fond
        self.mp = self.mpMax # on remet les mp a fond
    
        return texte  # on renvoie le texte d'affichage


    def seDefendre(self, ennemi):
        """
        Tente de se défendre contre une attaque ennemie.

        Paramètres :

            ennemi (Ennemi) : L'ennemi à contrer.
        """
        degats = (ennemi.stats["Attaque"] * (1 - self.stats["Defense"] / (self.stats["Defense"] + 25))) # dégats réduit
        degatsN = (ennemi.stats["Attaque"] * (1 - self.stats["Defense"] / (self.stats["Defense"] + 100))) # dégats normaux

        contre_chance = min(int(((self.stats["Defense"] + self.stats["Agilité"]) / (2*ennemi.stats['Agilité']))*100),20) # chance de contrer ( entre ~ 0% et 20% )

        defense_chance = randint(0, round(ennemi.stats["Agilité"] * 3)) # chance de defendre

        texte = (f"{self.nom} essaie de se défendre ! ") # texte a afficher
        if randint(0,100) <= contre_chance: # si on genere un nombre en dessous de la chance de contre on prends des degats reduits et on contre attaque
            texte += f"Il réussit à se défendre mais prend quand même {round(degats, 1)} points de vie. \n" # texte a afficher
            texte +=("Et par un coup de chance, il arrive à contre-attaquer !\n\n") # texte a afficher
            self.stats["Vie"] -= degats # on actualise la vie 
            self.stats["Vie"] = round(self.stats["Vie"], 2) # on l'arrondi
            texte += self.attaquer(ennemi) # texte a afficher
            ennemi.check() # on actualise la vie de l'ennemi
        elif randint(0, 100) <= 5: # si on genere un nombre en dessous de 5 on ne prends pas de degats
            texte += (f"Et il réussit à se défendre complètement !") # texte a afficher


        elif defense_chance <= self.stats["Agilité"]: # si on genere un nombre en dessous de l'agilité du perso alors on prends des degats réduits
            texte += f"Et il réussit à se défendre mais prend quand même {round(degats, 1)} points de vie." # texte a afficher

            self.stats["Vie"] -= degats # on actualise la vie
            self.stats["Vie"] = round(self.stats["Vie"], 2) # on l'arrondi
        else: # si on n'a pas de chance alors on prends les degats normaux
            texte += f"Mais n'arrive pas à se défendre et perd {round(degatsN, 1)} points de vie." # texte a afficher

            self.stats["Vie"] -= degatsN # on prends les degats normaux
            self.stats["Vie"] = round(self.stats["Vie"], 2) # on arrondi la vie
        

        return texte  # on renvoie le texte d'affichage
     
    def __str__(self):
        return f"{self.nom}, niveau :  {self.niveau} (Vie : {round(self.stats['Vie'])}, Attaque : {round(self.stats['Attaque'])}, Defense : {round(self.stats['Defense'])}, Agilité : {round(self.stats['Agilité'])}, Taux de Crit : {round(self.stats['CritChance'])})"  # on renvoie le texte d'affichage

    def atqSpecial(self, ennemi):
        """
        Effectue une attaque spéciale sur un ennemi en consommant de la mana.

        Paramètres :

            ennemi (Ennemi) : L'ennemi à attaquer.
        """
        tout = (self.atqSpe(self.stats['Attaque'], ennemi.stats['Defense'], self.nom, ennemi.nom)) # texte a afficher et degats
        ennemi.stats["Vie"] -= round(tout[0]) # on actualise la vie de l'ennemi avec les degats de l'attaque spéciale
        self.mp -= 20 # on actualise le mana
        ennemi.check() # on actualise la vie de l'ennemi
        return tout[1]  # on renvoie le texte d'affichage

        
def eclair(attaque, defenseE, nom, nomE):
    """Capacité spéciale qui inflige des dégats
    
    Paramètres:
        attaque (float) : l'attaque du perso qui utlise la capacité
        defenseE (float) : la défense de l'ennemi sur lequel on utlise la capacité
        nom (str) : le nom du perso qui utlise la capacité
        nomE (str) : le nom de l'ennemi sur lequel on utlise la capacité

    """
    degats = (attaque * 1.9) * (1 - ((defenseE - defenseE * 0.1) /
                                    ((defenseE - defenseE * 0.1) + 100))) # calcule des dégats

    return degats, f"{nom} lance un éclair sur {nomE}, il lui inflige {round(degats)} dégâts ! \n{nomE} reste figé jusqu'au prochain tour."  # on renvoie le texte d'affichage et les degats


def epee_de_feu(attaque, defenseE, nom, nomE):
    """Capacité spéciale qui inflige des dégats
    
    Paramètres:
        attaque (float) : l'attaque du perso qui utlise la capacité
        defenseE (float) : la défense de l'ennemi sur lequel on utlise la capacité
        nom (str) : le nom du perso qui utlise la capacité
        nomE (str) : le nom de l'ennemi sur lequel on utlise la capacité

    """
    degats = (attaque * 2.1) * (1 - (defenseE / (defenseE + 100))) # calcule des dégats

    return degats, f"{nom} enflamme son épée et attaque {nomE}, il lui inflige {round(degats)} dégâts ! \n{nomE} n'arrive pas a se deplacer pour attaquer."# on renvoie le texte d'affichage et les degats


def laceration_sanglante(attaque, defenseE, nom, nomE):
    """Capacité spéciale qui inflige des dégats
    
    Paramètres:
        attaque (float) : l'attaque du perso qui utlise la capacité
        defenseE (float) : la défense de l'ennemi sur lequel on utlise la capacité
        nom (str) : le nom du perso qui utlise la capacité
        nomE (str) : le nom de l'ennemi sur lequel on utlise la capacité

    """
    degats = (attaque * 1.6) * (1 - (defenseE / 2) / ((defenseE / 2) + 100)) # calcule des dégats

    return degats, f"{nom} lacère et ensanglante {nomE}, il lui inflige {round(degats)} dégâts ! \n{nomE} reste sur place surpris par l'attaque." # on renvoie le texte d'affichage et les degats


def fleche_explosive(attaque, defenseE, nom, nomE):
    """Capacité spéciale qui inflige des dégats
    
    Paramètres:
        attaque (float) : l'attaque du perso qui utlise la capacité
        defenseE (float) : la défense de l'ennemi sur lequel on utlise la capacité
        nom (str) : le nom du perso qui utlise la capacité
        nomE (str) : le nom de l'ennemi sur lequel on utlise la capacité

    """
    degats = (attaque * 1.8) * ((defenseE - defenseE * 0.3) /
                                ((defenseE - defenseE * 0.3) + 100)) # calcule des dégats

    return degats,  f"{nom} lance une flèche explosive sur {nomE}, elle explose et lui inflige {round(degats)} dégâts ! \n{nomE} est projeté et ne peut pas" # on renvoie le texte d'affichage et les degats

def jugement_divin(attaque, defenseE, nom, nomE):
    """Capacité spéciale qui inflige des dégats
    
    Paramètres:
        attaque (float) : l'attaque du perso qui utlise la capacité
        defenseE (float) : la défense de l'ennemi sur lequel on utlise la capacité
        nom (str) : le nom du perso qui utlise la capacité
        nomE (str) : le nom de l'ennemi sur lequel on utlise la capacité

    """
    return 10E100,  f"{nom} juge {nomE}, malheureusement, il trouve que {nomE}, n'est pas digne d'exister..." # on renvoie le texte d'affichage et les degats


if __name__ == '__main__':
    perso = Personnage("test")
    perso.choisirClasse("Mage")
    perso.setLevel(100)
    print(perso)
