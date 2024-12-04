from random import randint, choice

class ListeObjet:
    """Classe contenant la liste de tous les objets"""

    def __init__(self) :
        self.listeObjet = []

    def ajouterObjet(self, *objets):
        """ajoute k fois les zones fournis

        Paramètres:
            *objet(Objet) : l'objet / les objets que l'on veut ajouter
        """
        for objet in objets: # on parcours la liste d'objets qu'on veut ajouter
            self.listeObjet.append(objet) # et on l'ajoute


class Objet:
    """Classe contenant les objets
    """
    def __init__(self, nom, vie, attaque, defense, agilite, crit, viemax,armorpen,
                 activable, effet= None):
        self.nom = nom
        self.bonus = {
            "Vie": vie,
            "Attaque": attaque,
            "Defense": defense,
            "Agilité": agilite,
            "CritChance": crit,
            "VieMax": viemax,
            "ArmorPen": armorpen
        }
        self.activable = activable
        self.capacite = effet

    def appliquer_bonus(self, personnage):
        """
        Applique les bonus de l'objet au personnage.

        Paramètres :
            personnage (Personnage) : Le personnage qui utilise l'objet.
        """
        text = f"Utilisation de {self.nom}\n"
        for stat, value in self.bonus.items(): # on ajoute les stats bonus au personnage en parcourant la liste de bonus
            
            personnage.stats[stat] += value
            if value >0:
                text += f"{stat} +{value}\n"
            if personnage.stats['Vie'] > personnage.stats['VieMax']:
                personnage.stats['Vie'] = personnage.stats['VieMax']

        return text

        

    def activer_effet_special(self, personnage, ennemi=None):
        """
        Active l'effet spécial de l'objet.

        Paramètres :
            personnage (Personnage) : Le personnage qui utilise l'objet.
            ennemi (Ennemi) : L'ennemi sur lequel l'effet spécial agit.
        """
        if self.activable: # on regarde si on peut activer l'objet 
               
            text= self.capacite(personnage, ennemi) # on lance la capacité spéciale
            return (f"\n\n{personnage.nom} active l'effet spécial de {self.nom} !\n") +text  # on renvoie le texte a afficher
        else : return ""



def effet_fleche_de_lumiere(personnage, ennemi):
    """Capacité spéciale qui inflige des dégats
    
    Paramètres:
        personnage (Personnage) : Le personnage qui utilise la capacité.
        ennemi (Ennemi) : L'ennemi sur lequel la capacité agit.
    """

    ennemi.stats["Vie"] = max(ennemi.stats["Vie"] - personnage.stats['Attaque']*0.75, 0) #cacule des degats + actualisation de la vie de l'ennemi
    ennemi.stats["Vie"] = round(ennemi.stats["Vie"], 2) # on l'arrondi
    return   f"\n{personnage.nom} attaque avec une flèche de lumère, l'ennemi perd {round(personnage.stats['Attaque']*0.75)} points de vie et ne peut attaquer !"



def effet_pierre_declipsia(personnage, ennemi):
    """Capacité spéciale qui inflige des dégats
    
    Paramètres:
        personnage (Personnage) : Le personnage qui utilise la capacité.
        ennemi (Ennemi) : L'ennemi sur lequel la capacité agit.
    """
    personnage.stats["Vie"] = personnage.stats["VieMax"] # on remet la vie au max du personnaeg
    return f"\n{personnage.nom} utilise la pierre d'Eclipsia, restaurant complètement sa vie !"


def effet_lame_de_crepuscule(personnage, ennemi):
    """Capacité spéciale qui inflige des dégats
    
    Paramètres:
        personnage (Personnage) : Le personnage qui utilise la capacité.
        ennemi (Ennemi) : L'ennemi sur lequel la capacité agit.
    """
    ennemi.stats["Vie"] = max(ennemi.stats["Vie"] - personnage.stats["Attaque"]*0.8,0)  #cacule des degats + actualisation de la vie de l'ennemi
    ennemi.stats["Vie"] = round(ennemi.stats["Vie"], 2)
    return         f"\n{personnage.nom} attaque avec la Lame de Crepuscule, infligeant {max(personnage.stats["Attaque"]*0.8,0)} dégâts et contournant la Defense de l'ennemi !"





