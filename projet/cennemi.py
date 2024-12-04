from random import randint, choice
class Zones:
    """Classe contenant les zones"""

    def __init__(self):
        self.zones = []


    def ajouterZone(self, *zones):
        """ajoute k fois les zones fournis

        Paramètres:
            *zone(Dict[nom : str, ennemi : List[Ennemi]]) : la zone / les zones que l'on veut ajouter
        """
        for zone in zones: # on parcours la liste de zones qu'on veut ajouter
            self.zones.append(zone) # et on les ajoutes

class Ennemi:
    """Classe contenant les ennemis
    """

    def __init__(self, nom, vie, attaque, defense, agilite):
        self.nom = nom

        self.nb_battu = 0

        self.stats = {
            "Vie": vie,
            "Attaque": attaque,
            "Defense": defense,
            "Agilité": agilite,
            "VieMax": vie
        }

        self.niveau = 1

        self.statsBase = {
            "Vie": vie,
            "Attaque": attaque,
            "Defense": defense,
            "Agilité": agilite,
            "VieMax": vie
        }


    def attaquer(self, personnage, redDegat=0):
        """
        Attaque un personnage avec une chance de fuite.

        Paramètres :

            personnage (Personnage) : Le personnage à attaquer.
            redDegat (int) : La réduction de dégâts.
        """

        degats = (self.stats["Attaque"] *
                  (1 - personnage.stats["Defense"]*0.9 /
                   (personnage.stats["Defense"]*0.9 + 100))) * (1 - redDegat / 100) # calcule des dégatsz

        texte = f"\n\n\n{self.nom} attaque {personnage.nom} !" # texte a afficher

        if randint(0, 100) <= min((personnage.stats['Agilité']/self.stats['Agilité'])*100,10): # si on genere un nombre en dessous de l'agilité du personnage il ne prends pas de degats
            texte +=(f" Mais {personnage.nom} esquive l'attaque !")# texte a afficher

        else: # et si il esquive pas
            texte +=(f"\n{personnage.nom} perd {round(degats,1)} points de vie.") # texte a afficher
            personnage.stats["Vie"] -= degats # on actualise la vie
            personnage.stats["Vie"] = round(personnage.stats["Vie"], 2) # et on l'arrondi

        return texte # on renvoie le texte d'affichage

    def mourir(self, personnage, lobjets):
        """
        Indique que l'ennemi est mort, donne de l'expérience au personnage.

        Paramètres :

            personnage (Personnage) : Le personnage qui a vaincu l'ennemi.
        """
        texte = f"\n\n{self.nom} est mort et a donné {round(sum(self.stats.values()) / len(self.stats),1)} xp !" # texte a afficher

        texte += personnage.recupPV(95)
        self.stats["Vie"] = 0 # on met la vie a 0

        self.nb_battu += 1 # on incremente le compteur
        texte += personnage.gagnerExp(sum((self.stats.values())) / len(self.stats)) # texte a afficher + calcule de l'exp ( moyenne des stats )

        if randint(0,100) < 25: # le prct de chance que l'ennemi donne un objet
            objet_laisse_tomber = choice(lobjets) # on donne un objet aleatoire
            texte += (f"\n\n{self.nom} a laissé tomber {objet_laisse_tomber.nom} !\n\n") # texte a afficher
            if len(personnage.inventaire) == 20:   # si l'inventaire est plein
                texte += "\n\nMais votre inventaire est plein, vous le laissez donc par terre..." # texte a afficher
            else:
                texte += personnage.ajouter_objet(objet_laisse_tomber.nom) # texte a afficher
        # self.stats["Vie"] = self.stats["VieMax"] # on remet la vie au max pour qu'il ne soit pas mort a la prochaine rencontre
        return texte # on renvoie le texte 
    def setLevel(self, niveau):
        """
        Définit le niveau de l'ennemi et ajuste ses stats en conséquence.

        Paramètres :

            niveau (int) : Le niveau à définir.
        """

        self.niveau = abs(int(niveau)) # on actualise le niveau
        # Augmentation des stats
        for stat in self.stats: # on augmente les stats en fonction du niveau entré
            self.stats[stat] = self.statsBase[stat]
            
            for _ in range(niveau - 1): # et on augmente les autres stats que l'attaque
                if stat == "Attaque": # on augmente l'attaque un peut moins
                    self.stats[stat] += round(self.statsBase[stat]*0.025 * niveau, 10)
                elif stat == "Defense": # on augmente l'attaque un peut moins
                    self.stats[stat] += round(self.statsBase[stat]*0.00035 * niveau, 10)
                else : self.stats[stat] += round( self.statsBase[stat] / 15 + self.stats[stat] * 0.00375, 10)
            self.stats[stat] = min(self.stats[stat], 2147483647)
        # pour reset la vie ( on sait jamais )
        self.stats["Vie"] = self.stats["VieMax"] 


    def check(self):
        # on remet la vie a 0 s'il faut
        if self.stats['Vie']< 0:
            self.stats['Vie'] = 0

