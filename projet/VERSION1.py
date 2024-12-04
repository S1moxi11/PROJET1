import os
	




from PyQt5.QtWidgets import  QInputDialog,QHBoxLayout, QProgressBar, QApplication, QMainWindow, QPushButton, QGridLayout, QVBoxLayout, QTextBrowser, QWidget, QDialog, QToolTip, QLabel, QMessageBox
from PyQt5.QtGui import QTransform, QPixmap, QFont, QIcon, QDesktopServices
from PyQt5.QtCore import QPropertyAnimation, QEasingCurve, QTimer,QUrl, Qt, QPoint
from cpersonnage import *
from cennemi import *
from cobjet import *
from random import randint 
import sqlite3, keyboard
fin = None
class FenetreDeFin(QDialog):
    """Fenetre qui s'affiche lorsqu'on termine le jeu ou bien qu'on meurt"""
    def __init__(self, victory=True):
        super().__init__()
        
        self.setWindowTitle("Fin du Jeu")  # Le nom qui est affiché pour la fenêtre
        self.setGeometry(0, 0, 100,100)  # la taille de base de la fenêtre

        # Définir le fond en fonction de la victoire ou de la défaite
        background_color = "#2ecc71" if victory else "#e74c3c"
        self.setStyleSheet(f"background-color: {background_color};")  # Pour donner du style !

        # Créer le label de résultat avec les modifications de style demandées
        self.resultat = QLabel("Tu as gagné ! Bravo !" if victory else "Tu as perdu ! Essaie encore ;)")
        self.resultat.setStyleSheet("font-size: 30px; font-weight: bold; color: black; font-family: 'Comic Sans MS';")

        # Créer un layout et ajouter le label
        layout = QVBoxLayout()
        layout.addWidget(self.resultat)

        # Centrer le label à l'intérieur du layout
        self.resultat.setAlignment(Qt.AlignCenter)
        layout.setAlignment(Qt.AlignCenter)  # Centrer le layout verticalement et horizontalement

        self.showMaximized()
        self.setLayout(layout)


        bouton_quitter = StyleBouton("Fermer")  # creation d'un bouton avec un style
        bouton_quitter.clicked.connect(self.close) # on ajoute une fonction au bouton

        composition = QVBoxLayout()
        composition.addWidget(self.resultat, alignment=Qt.AlignCenter)# on ajoute le widget dans la fenetre
        composition.addWidget(bouton_quitter, alignment=Qt.AlignCenter)# on ajoute le widget dans la fenetre
        composition.setContentsMargins(20, 20, 20, 20)

        self.setLayout(composition) # et on applique le layout a la fenetre

    def resizeEvent(self, event):
        self.resultat.move(int(self.width()/3),int(self.height()/5))
        

class BoutonInventaire(QPushButton):
    """pareil que ce que j'ai fait au dessus"""
    def __init__(self, nom_item,is_used, parent=None):
        super().__init__(nom_item, parent)
        self.nom_item = nom_item
        if is_used:
            self.setStyleSheet("""
                QPushButton {
                    background-color: #7aafdf;
                    color: white;
                    border: 2px solid #7aafdf;
                    border-radius: 5px;
                    padding: 5px;
                }
                QPushButton:hover {
                    background-color: #65b3d0;
                    border: 2px solid #65b3d0;
                }
                QPushButton:pressed {
                    background-color: #3d85c6;
                    border: 2px solid #3d85c6;
                }
            """)# Pour donner du style !
        else: 
            self.setStyleSheet("""
                QPushButton {
                    background-color: #2ecc71;
                    color: white;
                    border: 2px solid #2ecc71;
                    border-radius: 5px;
                    padding: 5px;
                }
                QPushButton:hover {
                    background-color: #27ae60;
                    border: 2px solid #27ae60;
                }
                QPushButton:pressed {
                    background-color: #1f8b4c;
                    border: 2px solid #1f8b4c;
                }
            """)




class FenetreCombat(QDialog):
    """la fenetre qu'on utilise pour se battre"""
    global fin
    def __init__(self, personnage,ennemis, numEnnemi, imgperso, imgennemi, current, presitge):
        
        super().__init__()

        self.ennemis = ennemis
        # variable qui sont utilisée dans le code pour diverse chose
        self.imgperso=imgperso
        self.imgennemi=imgennemi

        self.descriptions = [
            "Une créature humanoïde recouverte d'une écorce sombre, capable de se fondre dans les ombres. Elle attaque avec des griffes tranchantes et est particulièrement agile dans l'obscurité.",
            "Une entité éthérée qui se manifeste au cœur des arbres. Il a le pouvoir de manipuler les illusions, rendant difficile la distinction entre la réalité et le rêve. Ses attaques psychiques sont déroutantes et redoutables.",
            "Un esprit maléfique lié aux arbres de la Forêt Sombre. Il contrôle les racines pour piéger ses proies et peut lancer des malédictions mortelles. Son corps est formé d'écorce en décomposition.",
            "Une créature gigantesque faite de roches et de minéraux. Sa force brutale et son endurance en font un adversaire redoutable. Il peut provoquer des éboulements pour surprendre ses ennemis.",
            "Un serpent draconique couvert d'écailles cristallines. Il crache des jets de lumière cristalline mortelle et est capable de se camoufler dans les parois rocheuses.",
            "Des créatures ailées avec des serres tranchantes et des cris perçants. Elles chassent en essaim et attaquent en piqué, harcelant leurs proies des hauteurs.",
            "Une créature réanimée par les forces sombres du désert. Elle traque ses proies avec une voracité implacable, dévorant tout sur son passage.",
            "Un insecte géant aux ailes irisées. Il crée des tempêtes de sable en battant des ailes et utilise ses mandibules pour broyer ses proies.",
            "Un être spectral qui se dissimule dans les mirages du désert. Il draine la vie de ses ennemis à distance en utilisant des attaques de magie noire.",
            "Un esprit féminin pleurant de manière lugubre. Sa lamentation a le pouvoir de désorienter et de terrifier, affaiblissant ceux qui l'entendent.",
            "Un monstre serpentiforme avec des yeux pétrifiants et des tentacules venimeux. Elle traque ses proies en utilisant la végétation aquatique comme camouflage.",
            "Un reptile amphibie capable de se fondre dans les ténèbres. Il surgit des eaux stagnantes pour saisir sa proie avec ses mâchoires acérées.",
            "Une créature mi-humaine, mi-éthérée, montée sur un destrier spectral. Il manie une lance d'énergie astrale et peut charger à une vitesse fulgurante.",
            "Un oiseau électrifié aux plumes lumineuses. Il génère des éclairs mortels et utilise des pouvoirs électriques pour surprendre ses ennemis.",
            "Une entité insaisissable qui se déplace avec le vent. Il peut devenir invisible à volonté et frappe avec des attaques fantomatiques.",
            "Une entité qui émerge des parois de la caverne, utilisant son corps d'obsidienne pour absorber la lumière. Ses attaques ont des effets corrosifs.",
            "Une créature faite de roche noire et de cristaux, capable de contrôler les ombres pour créer des illusions dérangeantes. Il peut également manipuler la pierre pour créer des armes.",
            "Des champignons maléfiques qui libèrent des spores toxiques. Ils peuvent infecter les intrus, provoquant hallucinations et affaiblissements.",
            "Autrefois messager divin, il a été corrompu par l'ombre. Il manie une épée d'obsidienne et a le pouvoir de drainer l'énergie vitale de ses ennemis.",
            "Une créature majestueuse mi-lion, mi-aigle, avec des ailes d'éclairs. Il attaque avec des serres puissantes et peut générer des tempêtes électriques.",
            "Un être de lumière et d'énergie qui se déplace à une vitesse éblouissante. Elle utilise des projectiles de lumière et peut confondre les sens de ses adversaires.",
            "Une créature délicate aux ailes incrustées d'étoiles. Elle utilise des poudres stellaires pour aveugler ses ennemis et peut invoquer des illusions.",
            "Une créature massive faite de cristaux translucides. Il utilise des attaques de lumière éblouissantes et peut se régénérer en absorbant la lumière ambiante.",
            "Une entité lumineuse qui protège les Champs Miroitants. Il manipule des lances de lumière et peut créer des barrières énergétiques.",
            "Gardiens créés par le Roi de l'Infini, ils sont faits d'ombres cristallisées. Ils manient des lames d'obsidienne et sont immunisés contre la plupart des attaques conventionnelles.",
            "Une entité orbiculaire qui absorbe et déforme la lumière. Elle peut altérer la réalité autour d'elle, créant des illusions déconcertantes.",
            "Une créature enflammée issue des ténèbres. Elle utilise le feu noir pour incinérer ses ennemis et peut se régénérer en absorbant les ombres.",
            "La source de l'obscurité qui a plongé Avorat dans le chaos. Il possède des pouvoirs divins, manipulant les ténèbres et corrompant la lumière. Son aura sombre rend tout espoir éphémère.",
            "La source de l'obscurité qui a plongé Avorat dans le chaos. Il possède des pouvoirs divins, manipulant les ténèbres et corrompant la lumière. Son aura sombre rend tout espoir éphémère."
        ]

        
        self.lesobjets = ListeObjet()
        # creation des objets du jeu
        self.lesobjets.ajouterObjet(Objet("Éclat de Lueur", 125, 0, 5, 0, 0, 0,0, False, None),
        Objet("Pierre d'Éclipsia", 0, 12, 7.5, 0, 0, 0,0, True, effet_pierre_declipsia),
        Objet("Amulette du Gardien", 0, 0, 12.5, 10, 0, 0,0, False, None),
        Objet("Potion d'Ombre", 0, 0, 0, 30, 0, 0,0, False, None),
        Objet("Flèche de Lumière", 0, 25, 0, 0, 0, 0,0, True, effet_fleche_de_lumiere),
        Objet("Élixir de Sérénité", 50, 0, 0, 0, 0, 100,0, False, None),
        Objet("Lame de Crépuscule", 0, 20, 0, 0, 0, 0,0, True, effet_lame_de_crepuscule),
        Objet("Orbe Astral", 50, 10, 5, 10, 0, 50,0, False, None),
        Objet("Corne de Vigilance", 0, 0, 0, 20, 0, 0,0, False, None),
        Objet("Bouclier Lunaire", 0, 0, 20, 0, 0, 40,0, False, None),
        Objet("Pierre de Régénération", 500, 0, 0, 0, 0, 0,0, False, None),
        Objet("Graine d'Harmonie", 10, 10, 5, 10, 0, 100,0, False, None),
        Objet("Boussole Stellaire", 0, 0, 0, 20, 0, 0,0, False, None),
        Objet("Bougie Bénie", 0, 0, 0, 0, 10, 0,2, False, None),
        Objet("Arcane Prismatique", 0, 30, 0, 0, 0, 0,0, False, None))
              
        self.current = current
        self.ennemi = self.ennemis[int(numEnnemi)-1]
        self.ennemi.setLevel(self.current+1+self.ennemi.nb_battu+ (presitge * 10))
        self.textes = ""

        # creation des objets du jeu

         # on lui choisi une classe
        self.personnage = personnage
        self.timer = QTimer(self) # pour eviter une erreur comme quoi il est pas défini

        # pour savoir si jamais l'ennemi peut jouer
        self.canPlay = True

        # tous ce qui est en rapport avec la fenetre
        self.setWindowTitle("Le Crépuscule du Roi - Combat") # Le nom qui est affiché pour la fenetre
        self.setGeometry(0, 0, 800, 600) # la taille de base de la fenetre
        self.setWindowIcon(QIcon("incon.ico")) # l'icone de la fenetre

        # pour definir la fenetre
        self.stats_dialog = None # pour definir la fenetre

        # creation des boutons de jeu
        self.bouton_attaquer = StyleBouton("Attaque", self) # creation d'un bouton avec un style
        self.attaque_speciale_bouton = StyleBouton("Attaque Spéciale", self) # creation d'un bouton avec un style
        self.bouton_defendrere = StyleBouton("Défendre", self) # creation d'un bouton avec un style
        #self.bouton_stats = StyleBouton("Voir les Stats", self) # creation d'un bouton avec un style



        # tous ce qui est info du joueur ( barre de vie, barre de mana, pseudo ) ainsi que les animations des barres
        self.pseudo_joueur = QLabel(self)
        self.pseudo_joueur.setStyleSheet("""
            QLabel {
                font-size: 18px;
                font-weight: bold;
                color: #AA35F7;
            }
        """)# Pour donner du style !
        self.barre_de_vie_joueur = QProgressBar(self) # creation de la barre de vie
        self.barre_de_mana_joueur = QProgressBar(self) # creation de la barre de vie
        self.barre_de_vie_joueur.setMaximum(int(self.personnage.stats['VieMax'])) # la valeur max que la barre peut atteindre
        self.barre_de_vie_joueur.setStyleSheet("QProgressBar::chunk { background-color: #42A362; color:white ;}")# Pour donner du style !
        self.barre_de_mana_joueur.setMaximum(100) # le max que la barre peut atteindre
        self.barre_de_mana_joueur.setStyleSheet(f"QProgressBar::chunk {{ background-color: #1066D9; }}")# Pour donner du style !

        self.anim_vie_joueur = QPropertyAnimation(self.barre_de_vie_joueur, b"value") # creation de l'animation pour la bar de vie quand on change de valeur
        self.anim_vie_joueur.setEasingCurve(QEasingCurve.InOutCubic) # animation de transition entre les valeurs
        self.viePrecP = int(int(self.personnage.stats['VieMax'])) # pour savoir quelle etait la vie du joueur avant le changement

        self.anim_mana_joueur = QPropertyAnimation(self.barre_de_mana_joueur, b"value") # pareil mais pour le mana
        self.anim_mana_joueur.setEasingCurve(QEasingCurve.InOutCubic) # ----
        self.mpPrec = int(100) # ----


        # pareil mais pour l'ennemi

        self.nom_ennemi = QLabel(self) # label pour afficher le nom de l'ennemi
        self.barre_de_vie_ennemi = QProgressBar(self) # barre de vie de l'ennemi
        self.barre_de_vie_ennemi.setStyleSheet("QProgressBar::chunk { background-color: red; }")# Pour donner du style !
        self.nom_ennemi.setStyleSheet("""
            QLabel {
                font-size: 18px;
                font-weight: bold;
                color: #e74c3c;
            }
        """)# Pour donner du style !


        self.anim_vie_ennemi = QPropertyAnimation(self.barre_de_vie_ennemi, b"value") # creation de l'animation pour la barre de vie de l'ennemi qui se lance quand on change de valeur
        self.anim_vie_ennemi.setEasingCurve(QEasingCurve.InOutCubic) # transition entre chaque valeur
        self.viePrecE = int(self.ennemi.stats['VieMax']) # vie avant le changement



        # la zone de texte ( la mini page html )

        self.text_display = QTextBrowser(self) # creation de l'endroit ou on affichera le texte du jeu
        self.text_display.setStyleSheet(
            "font-size: 16px; color: white; background-color: rgba(0, 0, 0, 150); border: none;"
        )# Pour donner du style !
        

        # comment la page est agencée

        bouton_composition = QHBoxLayout()   # layout qui fait en une seule ligne
        bouton_composition.addWidget(self.bouton_attaquer)# on ajoute le widget dans la "liste" de widget
        bouton_composition.addWidget(self.attaque_speciale_bouton)# on ajoute le widget dans la "liste" de widget
        bouton_composition.addWidget(self.bouton_defendrere)# on ajoute le widget dans la "liste" de widget
        #bouton_composition.addWidget(self.bouton_stats)# on ajoute le widget dans la "liste" de widget


        # fait l'agencement final avec les deux catégories
        layout_principal = QVBoxLayout()
        layout_principal.setAlignment(Qt.AlignCenter)  # Alignement des éléments au centre vertical

        # Ajout du layout de boutons en haut
        layout_principal.addLayout(bouton_composition)

        # Layout pour les barres de vie/mana du joueur et l'affichage du texte au milieu
        layout_central = QHBoxLayout()
        layout_central.setAlignment(Qt.AlignCenter)  # Alignement des éléments au centre horizontal
        layout_bars_joueur = QVBoxLayout()

        image_label = QLabel(self)
        layout_bars_joueur.addWidget(image_label)
        layout_bars_joueur.setAlignment(Qt.AlignTop)

        
        pixmap = self.imgperso
        scaled_pixmap = pixmap.scaled(200, 200, Qt.KeepAspectRatio)  # Ajustez les valeurs de largeur et de hauteur selon vos besoins
        # Assigner l'image redimensionnée à la QLabel
        image_label.setPixmap(scaled_pixmap)
        image_label.setAlignment(Qt.AlignCenter)

        layout_bars_joueur.addWidget(self.pseudo_joueur)
        layout_bars_joueur.addWidget(self.barre_de_vie_joueur)
        layout_bars_joueur.addWidget(self.barre_de_mana_joueur)

        layout_central.addLayout(layout_bars_joueur)
        layout_central.addWidget(self.text_display) 



        self.statsJ = QLabel(self)
        





        layout_bars_joueur.addWidget(self.statsJ)







        layout_barre_ennemi = QVBoxLayout()
        layout_barre_ennemi.setAlignment(Qt.AlignRight | Qt.AlignTop)


        image_label_ennemi = QLabel(self)
        pixmap_ennemi = imgennemi
        scaled_pixmap_ennemi = pixmap_ennemi.scaled(200, 200, Qt.KeepAspectRatio)  
        image_label_ennemi.setPixmap(scaled_pixmap_ennemi)
        layout_barre_ennemi.addWidget(image_label_ennemi)
        image_label_ennemi.setAlignment(Qt.AlignCenter)


        layout_barre_ennemi.addWidget(self.nom_ennemi)
        layout_barre_ennemi.addWidget(self.barre_de_vie_ennemi)

        


        layout_central.addLayout(layout_barre_ennemi)



        self.statsE = QLabel(self)
        

        layout_barre_ennemi.addWidget(self.statsE)


        desc = QLabel(self)
        desc.setWordWrap(True)
        desc_text = f"<div style='font-size: 16pt; text-align: center; font-family: Comic Sans MS;'>Description<br><p style='white-space: pre-wrap;font-size: 12pt'>{self.descriptions[numEnnemi]}</p></div>"
        desc.setText(desc_text)


        layout_barre_ennemi.addWidget(desc)



        layout_principal.addLayout(layout_central)
        



        # ajoute une fonction a executer lorsqu'on appuie sur un bouton
        self.bouton_attaquer.clicked.connect(self.attaquer) # on ajoute une fonction au bouton
        self.attaque_speciale_bouton.clicked.connect(self.attaqueSpeciale) # on ajoute une fonction au bouton
        self.bouton_defendrere.clicked.connect(self.defendre) # on ajoute une fonction au bouton
        #self.bouton_stats.clicked.connect(self.montrerStats)# on ajoute une fonction au bouton

        # on actualise les labels / barres de chaques chose pour que tous soit bien affiché lorsqu'on lance la page
        
        self.actu_joueur()
        self.actu_affichage_text("")
        self.actu_ennemi()
        self.actu_affichage_text("")
        self.actu_affichage_text("")

        self.finished = False
        self.grid_composition = QGridLayout()

        self.bouton_inventaire = []

        i = 0
        # pour que les boutons sois en 4*5
        for ligne in range(3):
            for col in range(5):
                if i < len(self.personnage.inventaire): # si on est encore dans l'inventaire on fait un bouton avec l'objet de l'inventaire
                    bouton = BoutonInventaire(f"{self.personnage.inventaire[i]}", True) # creation d'un bouton avec du syle
                    bouton.setToolTip("Cliquez pour utiliser l'objet")
                    bouton.clicked.connect(self.utiliser_item) # on ajoute une fonction au bouton
                else: # sinon bouton vide
                    bouton = BoutonInventaire(f"vide", False)# creation d'un bouton avec du syle
                    bouton.setToolTip("Le vide complet !")
                self.grid_composition.addWidget(bouton, ligne, col)# on ajoute le widget dans la fenetre
                self.bouton_inventaire.append(bouton)
                i+=1
        self.update_inventory()

        # on agence ca dans la fenetre
        container = QWidget()
        layout_principal.addLayout(self.grid_composition)
        self.setLayout(layout_principal)

        self.showMaximized()
    


    
    def verif_utiliser_item(self, nom_item):
        """fenetre de confirmation d'utilisation d'objets"""
        response = QMessageBox.question(self, "Utiliser l'objet", f"Voulez-vous utiliser l'objet '{nom_item}'?",QMessageBox.Yes | QMessageBox.No) # fenetre avec deux propositions
        return response == QMessageBox.Yes # et si on a choisi oui ou pas
    def update_inventory(self):
        """on actualise l'inventaire pour que les objets sois ceux actuels"""
        self.bouton_inventaire = []
        i = 0
        # pour que les boutons sois en 4*5
        for ligne in range(3):
            for col in range(5):
                # si on est encore dans l'inventaire du joueur
                if i < len(self.personnage.inventaire):
                    self.bouton = BoutonInventaire(f"{self.personnage.inventaire[i]}",True) # creation d'un bouton avec du syle
                    self.bouton.setToolTip("Cliquez pour utiliser l'objet")
                    self.bouton.clicked.connect(self.utiliser_item) # on ajoute une fonction au bouton
                else: # sinon on fait juste un bouton vide
                    self.bouton = BoutonInventaire(f"vide",False) # creation d'un bouton avec du syle
                    self.bouton.setToolTip("Le vide complet !")
                self.grid_composition.addWidget(self.bouton, ligne, col)# on ajoute le widget dans la fenetre
                self.bouton_inventaire.append(self.bouton)
                i+=1
        

    def utiliser_item(self):
        """on fait pour que le joueur utilise l'objet qu'il a cliqué"""
        if not self.finished:
            sender_bouton = self.sender() # le bouton qu'on a appuyé
            response = self.verif_utiliser_item(sender_bouton.nom_item) # on demande confirmation
            if response: # si oui
                QToolTip.showText(sender_bouton.mapToGlobal(sender_bouton.pos()), "Objet utilisé!") # on affiche un petit objet utilié
                text = self.personnage.utiliser_objet(sender_bouton.nom_item,self.ennemi,self.lesobjets) # on utilise l'objet qu'on a cliqué
                self.update_inventory() # on actualise l'inventaire pour enlever celui qu'on a utilisé
                self.write(text, 3)
                # et on actualise la fenetre de combat pour que la vie du joueur et de l'ennemi soit la bonne
                self.checkEnnemi()
                self.checkChangements()
                self.actu_joueur()
                self.actu_ennemi()


    def actu_ennemi(self):
        """actualise le label ainsi que la barre de vie de l'ennemi avec l'animation"""
        self.nom_ennemi.setText(f"{self.ennemi.nom} - Niveau {self.ennemi.niveau}") # on change le texte du label avec le nom de l'ennemi actuel et de la zone
        # print(self.ennemi.stats['Vie'])
        self.barre_de_vie_ennemi.setMaximum(int(self.ennemi.stats['VieMax'])) # on change le max en fonction de l'ennemi
        self.barre_de_vie_ennemi.setValue(int(self.ennemi.stats['Vie'])) # de même pour la valeur actuelle de l'ennemi

        if self.anim_vie_ennemi.state() == QPropertyAnimation.Stopped: # si une animation est pas en cours
            if self.ennemi.stats['Vie'] < self.ennemi.stats['VieMax']: # et si on est pas deja au max des pv
                self.anim_vie_ennemi.setStartValue(self.viePrecE) # on defini la valeur de début de l'animation
                self.anim_vie_ennemi.setEndValue(int(self.ennemi.stats['Vie'])) # et la valeur de fin
                self.anim_vie_ennemi.setDuration(500) # le temps que l'animation prendra
                self.anim_vie_ennemi.start() # et on la commence
        self.viePrecE = int(self.ennemi.stats['Vie']) # on change la vie que l'ennemi avait a la derniere actualisation


        stats_text = "<div style='font-size: 16pt; text-align: center; font-family: Comic Sans MS;'>Statistiques de l'Ennemi<br>"
        for stat, val in self.ennemi.stats.items():
            stats_text += f"<div style='font-size: 12pt; text-align: left;text-indent: 100px;'>{stat} : {round(val,2)}</div>"
        stats_text += "</div>"
        self.statsE.setText(stats_text)

    def actu_joueur(self):
        """actualise le label ainsi que la barre de mana et de vie du joueur avec l'animation"""

        # on actualise les barres pour qu'elle soit véridique
        self.barre_de_vie_joueur.setValue(int(self.personnage.stats['Vie'])) # on change la valeur de vie que le joueur a actuellement
        self.barre_de_vie_joueur.setMaximum(int(int(self.personnage.stats['VieMax']))) # on change la valeur max que le joueur peut avoir
        self.barre_de_mana_joueur.setValue(int(self.personnage.mp)) # et on actualise le mana aussi
        self.pseudo_joueur.setText(f"{self.personnage.nom} - Niveau {self.personnage.niveau}") # ainsi que le label qui montre le nombre de monstre battu et le niveau du joueur

        if self.anim_vie_joueur.state() == QPropertyAnimation.Stopped: # si il y a pas d'animation en cours
            if self.personnage.stats['Vie'] < int(self.personnage.stats['VieMax']): # et si on est pas au dela des pv max
                self.anim_vie_joueur.setStartValue(self.viePrecP) # on defini la valeur de début de l'animation
                self.anim_vie_joueur.setEndValue(int(self.personnage.stats['Vie'])) # et la valeur de fin
                self.anim_vie_joueur.setDuration(500) # le temps que l'animation prendra
                self.anim_vie_joueur.start() # et on la commence
        self.viePrecP = int(self.personnage.stats['Vie']) # on change la vie que le joueur avait a la derniere actualisation

        if self.anim_mana_joueur.state() == QPropertyAnimation.Stopped: # si il y a pas d'animation en cours
            if self.personnage.mp < 100:  # et si on est pas au dela des mp max
                self.anim_mana_joueur.setStartValue(self.mpPrec) # on defini la valeur de début de l'animation
                self.anim_mana_joueur.setEndValue(int(self.personnage.mp)) # et la valeur de fin
                self.anim_mana_joueur.setDuration(500) # le temps que l'animation prendra
                self.anim_mana_joueur.start() # et on la commence
        self.mpPrec = int(self.personnage.mp) # on change le mana que le joueur avait a la derniere actualisation


        stats_text = "<div style='font-size: 16pt; text-align: center; font-family: Comic Sans MS;'>Statistiques du héros<br>"
        for stat, val in self.personnage.stats.items():
            if stat == 'Exp':
                stats_text += f"<div style='font-size: 12pt; text-align: left;text-indent: 100px;'>{stat} : {round(val,2)} / {self.personnage.xpMax}</div>"
            else:
                stats_text += f"<div style='font-size: 12pt; text-align: left;text-indent: 100px;'>{stat} : {round(val,2)}</div>"
        stats_text += "</div>"
        self.statsJ.setText(stats_text)

        
    def attaquer(self):
        """la logique derriere le bouton attaquer"""
        result_text = "" # sert a faire un affichage de ce qu'il se passe pour le joueur
        result_text += self.personnage.attaquer(self.ennemi) # on ajoute le str que ca renvoie
        if self.ennemi.stats['Vie'] > 0 and self.canPlay: # si l'ennemi n'est pas mort et peut jouer
            result_text += self.ennemi.attaquer(self.personnage) # on ajoute le str que ca renvoie
        self.canPlay = True # on fait pour que l'ennemi puisse jouer
        result_text += self.checkEnnemi() + self.checkChangements() # on check tous et on ajoute les resultats de chaques check dans l'affichage


        # on actualise toujours le joueur et l'ennemi pour que l'affichage se fasse dynamiquement
        self.actu_joueur()
        self.actu_ennemi()
        self.write(result_text, 3) # et bien sur on affiche le texte


    def write(self, textT, ms):
        """méthode qui permet de faire un affichage du texte

        Paramètre:
            textT(str): le texte qu'on veut afficher
            ms(int): le nombre de ms que l'on veut entre l'affichage de chaque lettre"""
        
        if self.timer.isActive(): # pour eviter que 2 timers soit lancer en même temps on reset tous
            self.indice = 0 # on remets a 0
            self.textes = [""] # on remets a 0
            self.timer.timeout.disconnect() # on enleve une fonction au bouton
            self.timer.stop() # on arrete le timer
        self.timer = QTimer(self) # on réactualise le timer

        self.textes = self.listeDeStr(textT) # on transforme le str qu'on veut en une liste de str contenant chacun une lettre de plus que celui d'avant
        self.indice = 0 # on mets l'indice de début a 0
        self.timer.timeout.connect(lambda: self.actu_affichage_text(self.textes[min(self.indice, len(self.textes)-1)], self.textes)) # a chaque fois que le timer fait un tour c'est a dire a chaque fois que le temps donné passe, on lance l'affichage du texte ( mais seulement une lettre en plus a la fois )
        self.timer.start(ms) # on commence le timer avec une intervale

    def attaqueSpeciale(self):
        """la logique derrière le bouton attaque special"""
        result_text = "" # le texte qu'on voudra afficher a la fin

        if self.personnage.mp < 20: # on regarde si on a assez de mana
            result_text += "Vous n'avez pas assez de mana pour lancer votre attaque spéciale !"

        else: # et si oui alors on fait l'attaque speciale
            result_text += self.personnage.atqSpecial(self.ennemi) # on ajoute le str que ca renvoie
            self.canPlay = True # on remet a True pour eviter que l'ennemi ne puis pas attaquer au tour suivant si on l'a empeché avant
        result_text += self.checkEnnemi() + self.checkChangements() # on check tous et on ajoute les resultats de chaques check dans l'affichage

        # on actualise toujours
        self.actu_joueur()
        self.actu_ennemi()
        self.write(result_text, 3)  # et bien sur on affiche le texte


    def defendre(self):
        """la logique derriere le bouton defendre"""

        result_text = self.personnage.seDefendre(self.ennemi)

        if self.ennemi.stats['Vie'] > 0 and randint(0, 100) <= 50:
            # on a 50% de chance de faire pour que l'ennemi ne puisse pas attaquer au tour suivant
            self.canPlay = False # et dans ce cas la on le mets a False

        result_text += self.checkEnnemi() + self.checkChangements() # on check tous et on ajoute les resultats de chaques check dans l'affichage

        # on actualise toujours
        self.actu_joueur()
        self.actu_ennemi()
        self.write(result_text, 3) # et on affiche


    def actu_affichage_text(self, text, ls=None):
        """permet d'actualiser la mini page html avec le nouveau texte

        Paramètres:
        texte(str): le texte que l'on veut afficher
        ls(list): la liste du str final que l'on veut afficher avec une lettre en plus a chaque element"""
        self.text_display.clear() # on enleve le texte
        self.text_display.append(text) # on ajoute le texte
        

        if ls is not None: # si on a fourni une liste de str alors
            # on augmentre l'indice de 1 si on a pas fini de parcourir la liste sinon on arrete le timer
            if self.indice < len(ls)-1:
                self.indice += 1
                
            else:
                self.timer.stop()



    def listeDeStr(self, chaine):
        """permet de faire une liste de str qui contiendra une lettre de plus a chaque fois ( si on rentre "abc" : ['a','ab','abc'])

        Paramètres:
            chaine(str): la chaine de caractère que l'on veut diviser"""
        chaines = [chaine[:i+1] for i in range(len(chaine))] # liste de chaines de caracteres
        return chaines
    def checkChangements(self):
        """"regarde si on est mort """
        global fin
        if self.personnage.stats['Vie'] <= 0: # si on est mort
            
            
            self.close()#on ferme la fenetre de combat
            fin = True
            return ""
        return ""

   
    def checkEnnemi(self):
        """regarde si l'ennemi est mort et agis en conséquence"""
        txt = ""
        if self.ennemi.stats["Vie"] <= 0: # si l'ennemi est mort alors
            txt +=self.ennemi.mourir(self.personnage,self.lesobjets.listeObjet)
            self.bouton_attaquer.clicked.disconnect() # on ajoute une fonction au bouton
            self.attaque_speciale_bouton.clicked.disconnect() # on ajoute une fonction au bouton
            self.bouton_defendrere.clicked.disconnect()
            self.personnage.nbEnnemiBattu += 1
            
            self.actu_joueur()
            self.actu_ennemi()
            self.update_inventory()
            self.finished = True
            
        return txt




class GameWindow(QDialog):

    def __init__(self, pseudo, classe):
        super().__init__()

        self.setWindowTitle("Le Crépuscule du Roi - Prologue") # Le nom qui est affiché pour la fenetre
        self.setGeometry(0, 0, 800, 600) # la taille de base de la fenetre

        texte_pro = (
            f"Dans les ténèbres éternelles d'Avorat, une prophétie murmure l'espoir d'une lumière perdue depuis des millénaires."
            f" C'est dans cette obscurité que naît {pseudo}, l'élu de la déesse Héméra, porteur du destin d'un monde jadis vibrant de magie et de splendeur. \n\n"
            f"{pseudo}, guidé par les croyants dévoués de la déesse de la lumière, s'éveille dans un monde peu illuminé. La Grande Guerre, vieille de 6412 ans, a plongé Avorat dans une ère sombre, où seul l'Ombre Primordiale règne en maître. \n\n"
            f"Les disciples d'Héméra ont attendu des millénaires, préparant l'élu à sa destinée. {pseudo} à choisi sa voie en devenant {classe}, car c'est par ses propres talents qu'il devra affronter le Roi de l'Infini. \n\n"
            f"La lueur d'espoir s'éveille en {pseudo}, et sa quête le mènera au légendaire temple des lumières. Là, dans l'ombre hautaine de l'Ombre Primordiale, {pseudo} devra triompher pour restaurer la lumière qui revient de droit à Avorat. Une nouvelle ère commence, façonnée par les pas de {pseudo}, l'élu de Héméra, prêt à défier les ténèbres et à réécrire l'histoire d'Avorat.")
        # QTextBrowser c'est en gros une page html pas ouf
        labeldebut = QTextBrowser() # creation de l'endroit ou on affichera le texte
        labeldebut.setPlainText(texte_pro) # on mets le texte qu'on veut
        labeldebut.setAlignment(Qt.AlignTop | Qt.AlignLeft) # on fait la disposition du texte
        labeldebut.setStyleSheet(
            "font-size: 16px; color: white; background-color: rgba(0, 0, 0, 150); border: none;"
        )# Pour donner du style !

        # on créer le bouton pour continuer vers la page de combat
        boutonContinue = StyleBouton("Continuer", self) # creation d'un bouton avec un style
        # renvoie accept lorsqu'on appuie sur le bouton et ferme la page
        boutonContinue.clicked.connect(self.accept) # on ajoute une fonction au bouton
        # comment la page est agencée
        composition = QVBoxLayout() # layout qui mets tous en vertical
        composition.addWidget(labeldebut) # on ajoute le widget au layout
        composition.addWidget(boutonContinue)# on ajoute le widget au layout
        self.setLayout(composition) # et on applique le layout a la fenetre

class Demarrage(QMainWindow):

    def __init__(self):
        super().__init__()
        self.conn = sqlite3.connect('projet/savedata.db')
        self.cursor = self.conn.cursor()

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS characters (
                name TEXT PRIMARY KEY,
                gender INTEGER,
                nbCoupCrit INTEGER,
                xpMax REAL,
                critChance REAL,
                Vie REAL,
                Attaque REAL,
                Defense REAL,
                Agilité REAL,
                Exp REAL,
                VieMax REAL,
                ArmorPen REAL,
                mp INTEGER,
                level INTEGER,
                classe TEXT,
                nbEnnemiBattu INTEGER,
                currentWorld INTEGER,
                nbTimesCompleted INTEGER
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS inventaire (
                name TEXT,
                itemname TEXT,
                count INTEGER,
                PRIMARY KEY (name, itemname)
            )
        ''')
        self.conn.commit()

        self.game_window = None # pour definir la fenetre
        self.fenetre = None
        self.setWindowTitle("Le Crépuscule du Roi") # Le nom qui est affiché pour la fenetre
        self.setWindowIcon(QIcon("projet/incon.ico")) # l'icone de la fenetre
        self.setGeometry(0, 0, 800, 600) # la taille de base de la fenetre


        # Créer les elements de la fenetre
        self.background_label = QLabel(self) # ce qui contiendra le fond

        self.nom_du_jeu = QLabel("Le Crépuscule du Roi", self) # le label avec le nom du jeu

        self.start_bouton = StyleBouton("Commencer", self) # creation d'un bouton avec un style
        self.start_bouton.clicked.connect(self.creation_du_perso_incoryable) # on ajoute une fonction au bouton

        self.bouton_info = StyleBouton("Informations", self) # creation d'un bouton avec un style
        self.bouton_info.clicked.connect(self.open_info) # on ajoute une fonction au bouton

        # les mets a jour pour qu'il apparaissent correctement au début
        self.actual_bouton_info()
        self.actual_bouton_start()
        self.actual_nom_du_jeu()
        self.update_background()
        self.showMaximized()


    def update_background(self):
        """ajuste l'image de fond en fonction de la taille de la fenetre"""
        background_image = QPixmap("projet/fond.png") # on mets dans la var l'image
        self.background_label.setPixmap(
        background_image.scaled(self.width(), self.height())) # on mets les dimensions de l'image dans le label
        self.background_label.setGeometry(0, 0, self.width(), self.height()) # la taille qu'on affichera l'image pour qu'il scale avec la page

    

    def actual_nom_du_jeu(self):
        """actualise le titre en fonction de la taille de la fenetre et lui mets un peu de style"""
        self.nom_du_jeu.setGeometry(0,
                                         self.height() // 4, self.width(),
                                         self.height() // 4) # pour qu'il scale avec la page
        self.nom_du_jeu.setAlignment(Qt.AlignCenter) # la position du texte dans le label
        font = QFont()
        font.setPointSize(int(self.height() / 20)) # pour que la taille du texte augmente avec la fenetre
        font.setBold(True)
        self.nom_du_jeu.setFont(font) # on lui applique le style de texte
        self.nom_du_jeu.setStyleSheet("color: white;")# Pour donner du style !

    def actual_bouton_start(self):
        """actualise le bouton info en fonction de la taille de la fenetre"""
        self.start_bouton.setGeometry(self.width() // 4,
                                      self.height() // 2,
                                      self.width() // 2,
                                      self.height() // 10) # pour qu'il scale avec la page


    def actual_bouton_info(self):
        """actualise le bouton info en fonction de la taille de la fenetre"""
        self.bouton_info.setGeometry(20, self.height() - 70, 100, 40) # pour qu'il scale avec la page

    def commencer(self, pseudo, classePerso,genre, is_saved = False):
        """ouvre la fenetre de prologue et de jeu"""
        self.game_window = GameWindow(pseudo, classePerso) # on mets la fenetre dans une var
        result = self.game_window.exec_() # on l'execute et on mets ce qu'il renvoie ( la façon dont la fenetre s'est fermée ) dans une var
        if result == QDialog.Accepted: # si la fenetre s'est fermée
            # si on appuie sur continuer dans game_window
            self.conn.close()
            self.fenetre = Fenetre(pseudo, classePerso, genre, is_saved) # on mets la fenetre dans une var
            

            self.close() # on ferme celle actuelle
            self.fenetre.show() # on affiche celle de combat ( car elle hérite de QMainWindow et donc on a pas besoin de l'executer )


    def open_info(self):
        """Ouvre la page index.html"""
        QDesktopServices.openUrl(
            QUrl("index.html"
                 )) # on ouvre le fichier

    def creation_du_perso_incoryable(self):
        """la fenetre de creation de personnage ou de chargement"""
        # Check if there are any saved characters in the database
        self.cursor.execute("SELECT name, level, nbTimesCompleted, currentWorld FROM characters")
        saved_characters = self.cursor.fetchall()
        
        if saved_characters:
            # If there are saved characters, ask the player if they want to load one or create a new one
            load_or_create, ok = QInputDialog.getItem(
                self, "Choix du personnage",
                "Voulez-vous charger un personnage existant ou en créer un nouveau?",
                ["Charger", "Créer"], 0, False
            )
            
            if ok and load_or_create == "Charger":
                # Let the player choose which character to load
                character_list = [f"{char[0]} (Niveau: {char[1]}, Victoires: {char[2]}, Monde: {char[3]})" for char in saved_characters]
                character_choice, ok = QInputDialog.getItem(
                    self, "Chargement de personnage",
                    "Choisissez votre personnage:",
                    character_list, 0, False
                )
                if ok and character_choice:
                    chosen_character = character_choice.split(" ")[0]  # Get the character name
                    self.cursor.execute("SELECT name, classe, gender FROM characters WHERE name=?", (chosen_character,))
                    char_data = self.cursor.fetchone()
                    if char_data:
                        self.commencer(char_data[0], char_data[1], char_data[2],True),
                else:
                    QMessageBox.warning(self, "Attention", "Annulation du chargement du personnage.")
            elif ok and load_or_create == "Créer":
                self.create_new_character()
            else:
                QMessageBox.warning(self, "Attention", "Annulation de la sélection du personnage.")
        else:
            # If no saved characters, proceed to create a new character
            self.create_new_character()

    def create_new_character(self):
        """Handle the creation of a new character."""
        while True:
            pseudo, ok = QInputDialog.getText(
                self, "Création de personnage",
                "Entrez le nom de votre personnage:"
            )  # fenetre ou on saisi du texte
            
            # Check if the entered name contains only alphanumeric characters
            if ok and pseudo and pseudo.strip().replace(' ', '') == pseudo:
                # Check if the entered name already exists in the database
                self.cursor.execute("SELECT name FROM characters WHERE name=?", (pseudo,))
                existing_character = self.cursor.fetchone()
                if existing_character:
                    QMessageBox.warning(self, "Attention", "Ce nom est déjà pris. Veuillez en choisir un autre.")
                else:
                    break
            else:
                # If the input is empty or contains blank spaces
                QMessageBox.warning(self, "Attention", "Le nom ne peut pas être vide ou contenir des espaces.")
                return
        
        classes = ["Guerrier", "Mage", "Assassin", "Archer", "Dieu"]  # choix de classes
        nClasse, ok = QInputDialog.getItem(
            self, "Création de personnage",
            "Choisissez votre classe:",
            classes, 0, False
        )  # menu pour choisir la classe
        # si on a bien choisi une classe
        if ok and nClasse:
            genre = ["Garçon", "Fille"]
            nGenre, ok = QInputDialog.getItem(
                self, "Création de personnage",
                "Choisissez votre genre:",
                genre, 0, False
            )  # menu pour choisir le genre
            # alors on commence l'aventure
            if ok and nGenre:
                self.commencer(pseudo, nClasse, nGenre)  # on lance
            else:
                QMessageBox.warning(
                    self, "Attention",
                    "Annulation de la création du personnage."
                )  # si on a pas bien rentré les infos
        else:
            QMessageBox.warning(
                self, "Attention",
                "Annulation de la création du personnage."
            )  # si on a pas bien rentré les infos

    def resizeEvent(self, event):
        """permet d'actualiser tous quand l'event se produit ( c'est une méthode qui fonctionne toute seule avec un event fait par pyqt5 )"""
        self.update_background()
        self.actual_nom_du_jeu()
        self.actual_bouton_start()
        self.actual_bouton_info()







class StyleBouton(QPushButton):
    """bouton plus stylé et pour eviter de le mettre a chaque fois qu'on créer un bouton j'en ai fait une classe"""
    def __init__(self, text, parent=None):
        super().__init__(text, parent)# pour qu'il hérite de la fenetre qu'il l'appelle et de la classe bouton pour pouvoir donner le style au bouton sans passer par la creation d'un nouveau bouton
        self.setStyleSheet("""
            QPushButton {
                background-color: #444444;
                color: white;
                border: 2px solid #444444;
                border-radius: 5px;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #666666;
                border: 2px solid #666666;
            }
            QPushButton:pressed {
                background-color: #555555;
                border: 2px solid #555555;
            }
        """)# Pour donner du style !

class Fenetre(QMainWindow):
    global fin
    def __init__(self,nom,classe,genre, savedCharacter = False):
        super().__init__()
        self.game_over_window = None 
        
        # Définitions des ennemis
        self.ennemisListe = [
        Ennemi("Écorche-ombre", 450, 50, 30, 35),
        Ennemi("Spectre sylvestre", 400, 55, 35, 20),
        Ennemi("Arbrisseur maudit", 525, 40, 20, 60),
        
        Ennemi("Géant de Pierre", 525, 60, 40, 60),
        Ennemi("Wyrm cristallin", 600, 45, 25, 70),
        Ennemi("Harpie des Cieux", 550, 70, 80, 30),
        
        Ennemi("Goule du Désert", 650, 40, 50, 70),
        Ennemi("Scarabée d'Émeraude", 850, 30, 70, 95),
        Ennemi("Marabout des Sables", 500, 75, 25, 50),
        
        Ennemi("Banshee des Marais", 500, 80, 10, 150),
        Ennemi("Méduse des Marécages", 650, 70, 45, 80),
        Ennemi("Croc-d'ombre", 900, 100, 20, 10),
        
        Ennemi("Centaure astral", 1000, 35, 95, 75),
        Ennemi("Siffleur d'Éclairs", 625, 110, 90, 30),
        Ennemi("Spectre errant", 600, 40, 80, 20),
        
        Ennemi("Spectre d'Obsidienne", 1200, 450, 30, 150),
        Ennemi("Nécro-minéral", 1250, 25, 20, 150),
        Ennemi("Spores de l'Ombre", 500, 30, 70, 25),
        
        Ennemi("Ange Déchu", 1000, 80, 100, 25),
        Ennemi("Griffon d'Orage", 900, 70, 125, 60),
        Ennemi("Fée Tourbillon", 450, 40, 400, 30),
        
        Ennemi("Papillon Astral Corrompu", 600, 60, 290, 50),
        Ennemi("Golem de Cristal Corrompu", 1500, 75, 80, 180),
        Ennemi("Gardien des Éclats Corrompu", 750, 140, 30, 150),
        
        Ennemi("Sentinelle Éternelle", 2000, 90, 100, 120),
        Ennemi("Sphère d'Ombre", 1000, 170, 25, 200),
        Ennemi("Phoenix des Abysses", 2200, 100, 150, 40),
        
        Ennemi("L'Ombre Primordiale, le Roi de l'Infini", 2300, 190, 170, 154)
        ]
        self.currentMap = 0
        self.foisTermine = 0              


        self.lastVal = -1
        
        #  ce qui est pour la fenetre
        self.setWindowTitle("Le Crépuscule du Roi") # Le nom qui est affiché pour la fenetre
        self.setGeometry(0, 0, 50*16, 50*9) # la taille de base de la fenetre
        
        
        # Ce qui est relatif au personnage
        self.nomPerso = nom # pour pouvoir le mettre dans le combat
        self.classe = classe # pareillement
        self.personnage = Personnage(nom) # on cree le personnage
        self.personnage.choisirClasse(classe)
        
        # on regarde si c'était un personnage déjà enregistré et si oui on change les stats en la version sauvegardé
        if savedCharacter:
            # connection a la base de donnée et on fait une requete pour acceder au stats du personnage
            conn = sqlite3.connect('projet/savedata.db')
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM characters WHERE name=?", (self.personnage.nom,))
            existing_character = cursor.fetchone()
            
            
            # print(existing_character) # pour tester si jamais on a bien la bonne save
            self.personnage.nbCoupCrit=int( existing_character[2])
            self.personnage.xpMax=float(existing_character[3])
            self.personnage.critChance=int(existing_character[4])
            self.personnage.stats['Vie']=float(existing_character[5])
            self.personnage.stats['Attaque']=float(existing_character[6])
            self.personnage.stats['Defense']=float(existing_character[7])
            self.personnage.stats['Agilité']=float(existing_character[8])
            self.personnage.stats['Exp']=float(existing_character[9])
            self.personnage.stats['VieMax']=float(existing_character[10])
            self.personnage.stats['ArmorPen']=float(existing_character[11])
            self.personnage.mp=int(existing_character[12])
            self.personnage.niveau=int(existing_character[13])
            self.personnage.nbEnnemiBattu=int(existing_character[15])
            self.currentMap = int(existing_character[16])
            self.foisTermine = int(existing_character[17])
            # on fait pareil pour l'inventaire 
            inv = (cursor.execute("SELECT * FROM inventaire WHERE name=?", (self.personnage.nom,)).fetchall())
            # print(inv)
            # on ajoute les items
            for items in inv:
                for _ in range(int(items[2])):
                    self.personnage.ajouter_objet(items[1])
        ordre2 = [f"ennemi({x})" for x in range(1,29)]
        order = ["dec1.png","dec2.png","dec3.png","dec4.png","dec5.png","po1.png","po2.png","po3.png","r1.png","deadend1.png","threeway1.png","straight1.png","straight2.png","turn1.png","4way1.png","4way2.png","po4.gif"]
    
        self.lablimgs = [[QLabel(self) for i in range(34*2)] for i in range(18)]

        self.fenetreCombat = None # pour contenir la fenetre de combat avec les infos qu'on aura après
        self.perso = QLabel(self) # label pour le personnage
        
        
        

        imagesPersoG = [] # pour les images de chaque version du perso
        imagesPersoF = [] # idem
        
        #haut bas droite gauche pour l'ordre dans laquel on prends les images
        ordre = ["haut(1)","haut(2)", "haut(3)", "bas(1)", "bas(2)","bas(3)", "droite(1)", "droite(2)","droite(3)", "gauche(1)", "gauche(2)", "gauche(3)"] # l'ordre dans laquelle on charge les images du perso 
        for nom in ordre: # on parcours l'ordre
            for filename in os.listdir("projet/gars"): # le dossier
                if nom in filename: # on compare
                    imagesPersoG.append(QPixmap(os.path.join("projet/gars", filename))) # et on l'ajoute au label si c'est le bon
        for nom in ordre: # idem
            for filename in os.listdir("projet/fille"): # idem
                if nom in filename: # idem
                    imagesPersoF.append(QPixmap(os.path.join("projet/fille", filename))) # idem

        personnages = [imagesPersoG,imagesPersoF] # on mets les personnages dans une liste
        
        # pour tout ce qui est la map qui est dans le fichier TXT et on les copies dans des listes
        self.map = [] 
        self.imageMap = []
        self.fichier = open("projet/map.txt")
        self.fichier2 = open("projet/mapboss.txt")
        self.mapTXT = []
        self.map2TXT = []
        for ligne in self.fichier:
            self.mapTXT.append(ligne.replace('\n', ''))
        for ligne in self.fichier2:
            self.map2TXT.append(ligne.replace('\n', ''))
        # print(self.mapTXT)
        i = 0
             
        #  pour verif si jamais c'est bien la bonne longueur
        # for i in range(len(self.imageMap)):
        #     print(len(self.imageMap[i]))


        #  pour savoir quelle image on prends pour les caracteres dans le fixhier texte et deux car il y a 2 maps et il faut des infos différentes
        self.char_to_index = {'a': (0,False,0), 'e': (1,False,0), 'o': (2,False,0), 'u': (3,False,0), 'p': (4,True,1), 'r': (5,True,0), 't': (6,True,0), 'n': (7,False,0), 'U': (8,True,0), 'y': (9,True,0), '=': (10,True,0), '-': (11,True,0), 'c': (12,True,0), 'k': (13,True,0), 'K': (14,True,0)}
        self.char_to_index2 = {'a': (0,False,0,0), 'e': (1,False,0,0), 'o': (2,False,0,0), 'u': (3,False,0,0), 'p': (4,False,1,0), 'r': (5,True,0,0), 't': (6,True,1,1), 'n': (7,False,0,0), 'U': (8,False,0,0), 'y': (9,False,0,0), '=': (10,True,0,0), '-': (11,True,0,0), 'c': (12,False,0,0), 'k': (13,False,0,0), 'K': (14,False,0,0)}
        self.listePassable = []
        self.mMonstre = 0
          
        
        
        # ENNEMIS
        self.ennemis = [] 
        self.onretest = 0
        
        for nom in ordre2: # on parcours dans l'ordre
            
            for filename in os.listdir("projet/image"): # le dossier
                if nom in filename: # on compare
                    self.ennemis.append(QPixmap(os.path.join("projet/image", filename))) # et on ajoute dans la liste si c'est le bon"""
                    
        
        self.nmennemi = 0 # dernier ennemi battu
        self.genre = genre # le genre qu'on a choisi lors de la creation
        self.persoChoisi = personnages[self.genre=="Fille"] # si c'est = a fille alors c'est 1 donc l'elem de la liste 1 qui sont les images du perso fille
        self.imgperso = self.persoChoisi[4] # l'image du bas pour faire l'idle du perso
        self.perso.setPixmap(self.imgperso.scaled(int(self.width()/28),int(self.height()/28),Qt.KeepAspectRatio)) 
        
        self.initializeUI() # Pour faire que le deplacement se fasse 
        self.startShow = 17 # pour qu'on apparaisse au milieu ~, c'est a partir de quelle image qu'on affiche
        self.endShow = 17+34  # et celle qu'on affiche en dernier
        # var pour le deplacement 
        self.zd, self.hautd = 0,0
        self.zq, self.hautg = 0,0
        self.sq, self.basg = 0,0
        self.sd, self.basd = 0,0
        self.z, self.haut = 0,0
        self.s, self.bas = 0,0
        self.q, self.gauche = 0,0
        self.d, self.droite = 0,0
        # pour savoir avec la zone dans laquel on est quelle ennemis il y a 
        self.appartenanceEnnemi = {1 : [1,2,3], 2: [4,5,6], 3: [7,8,9], 4:[10,11,12], 5: [13,14,15], 6:[16,17,18],7:[19,20,21],8:[22,23,24],9:[25,26,27],10:{28}}
        # print(len(self.map))
        # Le labl qui contient les infos qui son,t en bas a gauche 
        self.labltext = QLabel(self, text=f'Monde Sauvé : {self.foisTermine}\nEnnemis Battu : {self.personnage.nbEnnemiBattu}/10\nMap Actuelle : {self.currentMap+1}/10')
        self.labltext.setStyleSheet('font-size: 12pt; color : white; background: rbga(0,0,0,0.3)')
        self.labltext.setWindowFlags(Qt.WindowStaysOnTopHint) # pour qu'il soit bien devant les images de la map
        self.labltext.setGeometry(0,0,self.width(), 100)
        self.labltext.move(50, self.height()*2-50)


        # bouton sauvegarder
        self.sauvegarder_btn = QPushButton('Sauvegarder', self)
        self.sauvegarder_btn.setGeometry(self.width() - 200, self.height() - 80, 150, 50)
        self.sauvegarder_btn.clicked.connect(self.sauvegarder)

        # on note les noms des zones pour qu'on puissnet les afficher
        self.mondes = [
            " La Forêt Sombre ",
            " Les Montagnes Éternelles ",
            " Le Désert des Illusions ",
            " Les Marais Maudits ",
            " Les Plaines Éthérées ",
            " Les Grottes Obsidiennes ",
            " Les Cieux Perdus ",
            " Les Champs Miroitants ",
            " Le Temple des Lumières ", 
            " Domaine du Roi de l'Infini "
        ]

        # le labl ou on affiche le monde et tous ce qu'on veut faire pour le rendre beau ( fond / police )
        self.txtmonde = QLabel(self)
        self.txtmonde.setText(self.mondes[self.currentMap])
        
        self.font = QFont()
        self.font.setPointSize(20)
        self.font.setBold(True)
        self.txtmonde.setFont(self.font)
        # et on le bouge en l'ajustant a la taille 
        self.txtmonde.adjustSize()
        self.label_width = self.txtmonde.width()
        self.txtmonde.move(int((self.width() - self.label_width) / 2), 100)






        # on charge la map actuelle, le +1 car c'est de 1 à 10 et non de 0 à 9 que sont nommé les fichiers
        self.charger_map(self.currentMap+1)


        # on actualise tous ça
        self.update_background()
        
        self.showMaximized()

    def sauvegarder(self):
        # on se connecte a la base de donnée et on request les saves qui ont le même pseudo
        conn = sqlite3.connect('projet/savedata.db')
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM characters WHERE name = ?', (self.personnage.nom,))
        exists = cursor.fetchone()[0]
        # si jamais il en existe alors on demande confirmation qu'on 
        if exists:
            
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Warning)
            msg_box.setText(f"Un personnage portant le nom '{self.personnage.nom}' existe déjà.")
            msg_box.setInformativeText("Voulez-vous les remplacer?")
            msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            msg_box.setDefaultButton(QMessageBox.No)
            response = msg_box.exec_()
            
            if response == QMessageBox.No:
                return
        retries = 10
        # et si on veut écraser la save actuelle alors
        for attempt in range(retries):
            try:
                # tous les parametres que l'on veut save
                param = (self.personnage.nom,self.genre, self.personnage.nbCoupCrit,self.personnage.xpMax,self.personnage.critChance,self.personnage.stats['Vie'],self.personnage.stats['Attaque'],self.personnage.stats['Defense'],self.personnage.stats['Agilité'],self.personnage.stats['Exp'],self.personnage.stats['VieMax'],self.personnage.stats['ArmorPen'],self.personnage.mp,self.personnage.niveau,self.personnage.classe,self.personnage.nbEnnemiBattu,self.currentMap,self.foisTermine)
                # on le fait
                cursor.execute('''
                    REPLACE INTO characters (name, gender, nbCoupCrit, xpMax, critChance, Vie, Attaque, Defense, Agilité, Exp, VieMax,ArmorPen, mp , level, classe, nbEnnemiBattu, currentWorld, nbTimesCompleted)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?,?)
                ''', param)
                conn.commit()
                
                # pareil avec l'inventaire
                param = []
                cursor.execute('''
                    DELETE FROM inventaire
                    WHERE name = ?
                ''', (self.personnage.nom,))
                itemCOunt = {}
                # on compte le nombre d'item de chaque type dans l'inventaire
                for item in self.personnage.inventaire:
                    if item in itemCOunt:
                        itemCOunt[item] += 1
                    else:
                        itemCOunt[item] = 1
                # et on les ajoutes au parametre
                for item, count in itemCOunt.items():
                    param.append((self.personnage.nom,item,count))
                # et pour chaque parametre on commit les infos
                for para in param:
                    cursor.execute('''
                        REPLACE INTO inventaire (name, itemname, count)
                        VALUES (?, ?, ?)
                    ''', para)
                    conn.commit()
                # point de coordonnée pour indiquer ou le tooltip s'affiche car on peut pas mettre des coordonnées simple
                q = QPoint()
                q.setY(int(self.height()/2))
                q.setX(int(int(self.width()/2)))
                QToolTip.showText(q, "Partie Sauvegardée !")
                break
            except sqlite3.OperationalError as e: # si on a une erreur
                if 'database is locked' in str(e): # si on a oublié de close la connection alors on reteste
                    if attempt < retries - 1:
                        conn.close()  
                    else:
                        QMessageBox.warning(self, 'Erreur', 'La base de donnée est déjà ouverte !') # si même apres les essaies alors on abandonne et on affiche ça
                else:
                    QMessageBox.warning(self, 'Erreur', f'Impossible de sauvegarder: {e}') # pareil si l'erreur n'est pas que la la base sql n'est pas ferme et on affiche l'erreur
                    break
        conn.close()

    def charger_map(self, mapa):
        
        # l'odre dans laquelle on load les images 
        order = ["dec1.png","dec2.png","dec3.png","dec4.png","dec5.png","po1.png","po2.png","po3.png","r1.png","deadend1.png","threeway1.png","straight1.png","straight2.png","turn1.png","4way1.png","4way2.png","po4.gif"]
        
        nbmap = mapa # la map que l'on veut charger
        self.imageMap = []
        self.map = []
        # pour savoir quelle fichier texte on utilise
        if mapa < 10:
            mape = self.mapTXT
            mapee = self.char_to_index
        else: 
            mape = self.map2TXT
            mapee = self.char_to_index2
        
        for nom in order:
            for folder in os.listdir("projet/carte"): # le dossier
                a = int(''.join(x for x in folder if x.isdigit()))
                # print(a, nbmap)
                if a == nbmap:
                    
                    for filename in os.listdir(f"projet/carte/"+folder):
                        
                        if nom in filename: # on compare
                            
                            self.imageMap.append(QPixmap(os.path.join(f"projet/carte/({a})", filename)))
        for ligne in mape:
            imgs = []
            for j in range(0, len(ligne) - 1, 2):
                car = ligne[j]
                rotation = int(ligne[j+1])
                angle = (rotation+4) * 90  # convert the rotation to degrees
                if car in mapee:  # check if the character is a valid image identifier
                    # print(len(self.imageMap))
                    img = self.imageMap[mapee[car][0]] # get the corresponding image
                    rotated_img = img.transformed(QTransform().rotate(angle))  # rotate the image
                    if mapa == 10:
                        imgs.append([rotated_img, mapee[car][1], mapee[car][2], mapee[car][3]])
                    else: 
                        imgs.append([rotated_img, mapee[car][1], mapee[car][2]])
            if len(imgs):
                self.map.append(imgs)
        # print("a")
                
        for i in range(len(self.map)): # on mets l'image dans le label
            # print(len(self.lablimgs), len(self.map[self.currentMap]))
            # print(i)
            for j in range(len(self.map[i])):
                #print(j)
                
                self.lablimgs[i][j].setPixmap(self.map[i][j][0])
                if self.map[i][j][1]:
                    self.listePassable.append(self.lablimgs[i][j])

    def update_background(self):
            """ajuste l'image de fond en fonction de la taille de la fenetre"""

            #fond = QPixmap("map.png") # on mets dans la var l'image
            #self.fond.setPixmap(fond.scaled(self.width(), self.height())) # on mets les dimensions de l'image dans le label
            #self.fond.setGeometry(0, 0, self.width(), self.height()) # la taille qu'on affichera l'image pour qu'il scale avec la page
            
            #texte = QPixmap("texte.png").scaled(self.width(), self.height(),Qt.KeepAspectRatio) # on scale l'image comme dans le init
        
            #self.texte_label.setPixmap(texte) # on le remet dans le label 
            #self.texte_label.setGeometry(0, 0, self.width(), self.height()) # on change sa forme pour qu'il s'affiche en entier
            #self.texte_label.move((0), int(-self.height()/10)*2) # et on le bouge au bonne endroit
            
            self.txtmonde.adjustSize()
            self.label_width = self.txtmonde.width()
            self.txtmonde.move(int((self.width() - self.label_width) / 2), 100)
            self.txtmonde.setStyleSheet("background-color: rgba(250, 255, 250, 128);")

            self.sauvegarder_btn.move(self.width() - self.sauvegarder_btn.width() - 20, self.height() - self.sauvegarder_btn.height() - 20)
            if len(self.map) > 0:
                self.perso.setPixmap(self.imgperso.scaled(int(self.width()/20),int(self.height()/20),Qt.KeepAspectRatio)) # idem
                q = self.imgperso.scaled(int(self.width()/20),int(self.height()/20)) # l'image du perso scale
                self.perso.setGeometry(0, 0,int(q.width()*0.8888888889), int(q.height()*0.98)) # idem que pour l'autre
                self.perso.move(int(self.width()/2), int(self.height()/7)*5) # idem
                self.listePassable = []
                # self.a.setGeometry(0,0,self.width(), 50)
                # self.a.move(50, self.height()*2)
                pady=0
                padx = 0
                for i in range(len(self.lablimgs)):
                    padx = 0
                    for j in range(self.startShow,self.endShow):
                        #print(j)
                        #print(len(self.lablimgs[i]))
                        # print(len(self.map))
                        # print(i% len(self.lablimgs))
                        #print(j)
                        
                        q = self.map[i% len(self.lablimgs)][j% len(self.lablimgs[0])][0].scaled(int(self.width()/34),int(self.height()/len(self.lablimgs)),Qt.KeepAspectRatio) # l'image scaled des carreaux
                        y = q.height()
                        lbl = self.lablimgs[i% len(self.lablimgs)][j% len(self.lablimgs[0])]
                        lbl.setPixmap((q)) # on ajoute l'image au label
                        lbl.setGeometry(0, 0, (q.width()), q.height())
                        lbl.move(padx, pady)
                        if self.map[i% len(self.lablimgs)][j% len(self.lablimgs[0])][1]:
                            self.listePassable.append(lbl)
                            
                        self.widthImg = q.width()
                        self.heightImg = q.height()
                        #print(self.lablimgs[i][j].width())
                        padx += q.width()
                        #print(padx, pady)
                        
                        
                    pady += y

                self.tp_rapide()

            
            """pado = 0 # le padding du début 
            for i in range(28): # on parcours chaque images d'ennemis
                pad = int(self.width()/100)* ((i)%3 == 0) # on calcule le pad par groupe de 3
                if i == 27:
                    pad += int(self.width()/100) # si c'est le dernier on va ajouter encore plus de padding
                q = self.ennemis[i].scaled(int(self.width()/38),int(self.height()/15),Qt.KeepAspectRatio) # l'image scaled des ennemis
                self.lablEnnemi[i].setPixmap(self.ennemis[i].scaled(int(self.width()/38),int(self.height()/15),Qt.KeepAspectRatio)) # on ajoute l'image au label
                self.lablEnnemi[i].setGeometry(0, 0, q.width(), q.height()) # on change pour que la taille soit adaptée
                self.lablEnnemi[i].move(int(self.width()/93+ self.width()/34*(i+1)+pad +pado), int(self.height()/30)*18) # pour le bouger 
                
                pado += pad # on ajoute le pad d'avant 
                """
            
            
    def resizeEvent(self, event):
        """permet d'actualiser tous quand l'event se produit ( c'est une méthode qui fonctionne toute seule avec un event fait par pyqt5 )"""
       
        self.update_background() 

    def initializeUI(self):
        # VOIR AUTRE QTIMER
        self.timer = QTimer(self) 
        self.timer.timeout.connect(lambda: self.update_function(self.persoChoisi))
        self.timer.start(5)
        
    def update_function(self, liste):
        width = self.imgperso.scaled(int(self.width()/28),int(self.height()/29)).width()/2
        height = int(self.imgperso.scaled(int(self.width()/28),int(self.height()/29)).height()/1.5)
        speed = 4+ int(self.width()/300)
        if keyboard.is_pressed("shift"):
            speed = 10 + int(self.width()/280*1.5)
        x = self.perso.x()
 
        y = self.perso.y()

        # pour le déplacement, on test pour coordonnée pour les bords aussi pour pas dépasser
        if 1 == 1:
            if keyboard.is_pressed("r"):
                if not self.doesitmoveitmoveit(0,0):
                    self.tp_rapide()
            elif (keyboard.is_pressed("z") or keyboard.is_pressed("up")) and (keyboard.is_pressed("d") or keyboard.is_pressed("right")):
                self.character_movement(speed, -speed, liste, "zd", "hautd", 6, 15)
            elif (keyboard.is_pressed("z") or keyboard.is_pressed("up")) and (keyboard.is_pressed("q") or keyboard.is_pressed("left")):
                self.character_movement(-speed, -speed, liste, "zq", "hautg", 9, 15)
            elif (keyboard.is_pressed("s") or keyboard.is_pressed("down")) and (keyboard.is_pressed("d") or keyboard.is_pressed("right")):
                self.character_movement(speed, speed, liste, "sd", "basd", 6, 15)
            elif (keyboard.is_pressed("s") or keyboard.is_pressed("down")) and (keyboard.is_pressed("q") or keyboard.is_pressed("left")):
                self.character_movement(-speed, speed, liste, "sq", "basg", 9, 15)
            elif keyboard.is_pressed("z") or keyboard.is_pressed("up"):
                self.character_movement(0, -speed, liste, "z", "haut", 0)
            elif keyboard.is_pressed("q") or keyboard.is_pressed("left"):
                self.character_movement(-speed, 0, liste, "q", "gauche", 9)
            elif keyboard.is_pressed("s") or keyboard.is_pressed("down"):
                self.character_movement(0, speed, liste, "s", "bas", 3)
            elif keyboard.is_pressed("d") or keyboard.is_pressed("right"):
                self.character_movement(speed, 0, liste, "d", "droite", 6)

            else: # l'idle image quand on bouge pas
                self.perso.setPixmap(liste[3].scaled(int(self.width()/28),int(self.height()/28),Qt.KeepAspectRatio))
         # pour les collision

    def character_movement(self, dx, dy, liste, var, var2,ad, ch=8):
        
        value2 = ((getattr(self, var2)+ 1 ) % 3)+ad
        setattr(self, var2, value2)
        value1 = getattr(self, var) +1
        setattr(self, var, value1)
        player_x, player_y = self.perso.x(), self.perso.y()
        #print(self.perso.width())
        gridx = player_x//self.widthImg
        l = 0
        if value1 >= ch:
            #print(self.doesitmoveitmoveit(dx,dy))
            xx = int(dx > 0)
            chmgt = (gridx >(31)) - (gridx < (1))
            if (gridx < 1 or gridx > 31) and (xx == self.lastVal or self.lastVal == -1) and xx == ((chmgt)>0) and dx != 0 and self.doesitmoveitmoveit(dx,dy):
                l = 1
                if value1 == 20:
                    self.update_visible_area((gridx >(31)) - (gridx < (1)))
                    self.lastVal = int(dx > 0)
                    l = 0
                    x = -1
                    xa = False
                    # print(player_x,player_y)
                    iterations = 0
                    while not self.doesitmoveitmoveit(x,0):
                        xa = True
                        if iterations >= 100:
                            # print("probleme, rien après 100 iterations.")
                            x = 0
                            
                            break
                        signe = lambda num: 1 if num > 0 else -1 if num < 0 else 0
                        x+= -signe(dx)
                        iterations+=1
                    if x == 0:
                        self.tp_rapide()
                    elif xa: 
                        self.perso.move(player_x+x,player_y)
                    

                #self.perso.move(self.perso.x() + dx, self.perso.y())
            elif self.doesitmoveitmoveit(dx,dy):
                self.perso.move(self.perso.x() + dx, self.perso.y() + dy)
                self.lastVal = -1
            else:
                pass
                
            self.perso.setPixmap(liste[value2].scaled(int(self.width()/28),int(self.height()/29),Qt.KeepAspectRatio))
            if l == 0:
                setattr(self, var, 0)
    def tp_rapide(self):
        queue = [((self.perso.x() // self.widthImg), self.perso.y() // self.heightImg)]
        visited = set(queue)
        # print(queue, self.startShow)
        failsafe = 0
        while queue and failsafe < 68*18:
            x, y = queue.pop(0)
            if y == 0 :
                y = 1
            # print(f"conditoin self.map[y][x][1] {self.map[y][x][1]}")
            if self.map[y%18][(self.startShow+x)%len(self.map[y%18])][1]:
                
                if x* self.widthImg > self.width():
                    dx = ((x-2)* self.widthImg - self.width())//self.widthImg
                    self.startShow += dx+5
                    self.endShow += dx+5
                    # print(f"x: {x}, {x* self.widthImg}, {self.width()}")
                    
                    self.update_visible_area(0)
                    self.tp_rapide()
                    
                    #self.perso.move( x* self.widthImg, y * self.heightImg)
                else:
                    self.perso.move( x* self.widthImg, y * self.heightImg)
                return

            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                new_x, new_y = x + dx, y + dy
                # print(f"condition {(0 <= new_x < (67) and 0 <= new_y < len(self.map) and
                #     (new_x, new_y) not in visited)}, x: {new_x}, y: {new_y}")
                if (0 <= new_x < (67) and 0 <= new_y < len(self.map) and
                    (new_x, new_y) not in visited):
                    queue.append((new_x, new_y))
                    visited.add((new_x, new_y))
                    
            failsafe +=1

    def doesitmoveitmoveit(self,dx,dy):
        global fin
        new_x = self.perso.x() + dx
        new_y = self.perso.y() + dy
        img_width = int(self.perso.width()/1)
        # new_x2 = self.perso.x() + dx + img_width/1.08
        img_height = int(self.perso.height()/1.1)
        # new_y2 = self.perso.y() + dy+ img_height/1.08
        # print(img_width)
        left_gridx = new_x // self.widthImg
        top_gridy = new_y // self.heightImg
        right_gridx = (new_x + img_width) // self.widthImg -1
        bottom_gridy = (new_y + img_height) // self.heightImg

        # print(f"New position in pixels: ({new_x}, {new_y})")
        # print(f"New position in grid coordinates: ({left_gridx}, {top_gridy})")
        # print(f"Tile position in pixels: ({self.lablimgs[top_gridy][self.startShow+left_gridx].x()}, {self.lablimgs[top_gridy][self.startShow+left_gridx].y()})")
        # print(f"New position in pixels: ({new_x2}, {new_y2})")
        # print(f"New position in grid coordinates: ({right_gridx}, {bottom_gridy})")
        # print(f"Tile position in pixels: ({self.lablimgs[bottom_gridy][self.startShow+right_gridx].x()}, {self.lablimgs[top_gridy][self.startShow+left_gridx].y()})")
        # print(not self.map[top_gridy][self.startShow+left_gridx][1],not self.map[top_gridy][self.startShow+right_gridx][1],not self.map[bottom_gridy][self.startShow+left_gridx][1], not self.map[bottom_gridy][self.startShow+right_gridx][1])
        # print(len(self.map[self.currentMap]))
        if not self.map[top_gridy% len(self.map)][(self.startShow+left_gridx)% len(self.lablimgs[0])][1] or \
                not self.map[top_gridy% len(self.map)][(self.startShow+right_gridx)% len(self.lablimgs[0])][1] or \
                not self.map[bottom_gridy% len(self.map)][(self.startShow+left_gridx)% len(self.lablimgs[0])][1] or \
                not self.map[bottom_gridy% len(self.map)][(self.startShow+right_gridx)% len(self.lablimgs[0])][1] or not  0<=bottom_gridy<=17 or  not 0<=top_gridy<=18:
            return False
        
        # print(len(self.map))
        # for i in range(len(self.map)):
        #     print(len(self.map[i]))
        #     for j in range(len(self.map[i])):
        #         print(len(self.map[i][j]))
        #         for k in range(len(self.map[i][j])):
        #             print(len(self.map[i][j][k]))
        
        if self.currentMap == 9:
            self.labltext.setText(f"Monde Sauvé : {self.foisTermine}\nEnnemi Battu : {0}/1\nMap Actuelle : {self.currentMap+1}/10")
            if (self.map[top_gridy% len(self.map)][(self.startShow+left_gridx)% len(self.lablimgs[0])][3] or \
                 self.map[top_gridy% len(self.map)][(self.startShow+right_gridx)% len(self.lablimgs[0])][3] or \
                 self.map[bottom_gridy% len(self.map)][(self.startShow+left_gridx)% len(self.lablimgs[0])][3] or \
                 self.map[bottom_gridy% len(self.map)][(self.startShow+right_gridx)% len(self.lablimgs[0])][3]) \
                 and not self.onretest:
                     self.fenetreCombat = FenetreCombat(self.personnage,self.ennemisListe, 28, self.imgperso, self.ennemis[28-1], self.currentMap, self.foisTermine) # on mets la fenetre dans une var
                     result = self.fenetreCombat.exec_()
                     if fin == True:
                        self.game_over_window = FenetreDeFin(False)
                    
                        self.close()#on ferme la fenetre de combat
                        self.game_over_window.exec_()
        if (self.map[top_gridy% len(self.map)][(self.startShow+left_gridx)% len(self.lablimgs[0])][2] or \
                 self.map[top_gridy% len(self.map)][(self.startShow+right_gridx)% len(self.lablimgs[0])][2] or \
    self.map[bottom_gridy% len(self.map)][(self.startShow+left_gridx)% len(self.lablimgs[0])][2] or \
                 self.map[bottom_gridy% len(self.map)][(self.startShow+right_gridx)% len(self.lablimgs[0])][2]) \
                 and not self.onretest and (self.personnage.nbEnnemiBattu >= 10 or self.currentMap == 9):
            self.currentMap = (self.currentMap +1)%10
            if self.currentMap == 0:
                self.foisTermine += 1
                for ennemi in self.ennemis:
                    ennemi.nb_battu = 0
            # print(self.currentMap)
            self.onretest = 1
            self.personnage.nbEnnemiBattu = 0
            self.charger_map(self.currentMap+1)
            
            self.update_background()
            self.labltext.setText(f"Monde Sauvé : {self.foisTermine}\nEnnemi Battu : {self.personnage.nbEnnemiBattu}/10\nMap Actuelle : {self.currentMap+1}/10")
        else: 
            self.onretest = 0
        
                     
                     
                     
        if randint(0,100) == 0 and  self.currentMap != 9:
            ennemi = self.appartenanceEnnemi[self.currentMap+1][randint(0,2)]
            self.fenetreCombat = FenetreCombat(self.personnage,self.ennemisListe, ennemi, self.imgperso, self.ennemis[ennemi-1], self.currentMap, self.foisTermine) # on mets la fenetre dans une var
            result = self.fenetreCombat.exec_()
            # print(fin)
            if fin == True:
                self.game_over_window = FenetreDeFin(False)
            
                self.close()#on ferme la fenetre de combat
                self.game_over_window.exec_()
            self.labltext.setText(f"Monde Sauvé : {self.foisTermine}\nEnnemi Battu : {self.personnage.nbEnnemiBattu}/10\nMap Actuelle : {self.currentMap+1}/10")
            
        return True




    

        
        

        
    def update_visible_area(self, dx):
        for i in range(len(self.lablimgs)):
            for j in range(self.startShow,self.endShow):
                self.lablimgs[i][j % len(self.lablimgs[i])].move(-10000, -10000)

        # print(dx)
        self.startShow += dx
        self.endShow += dx

        pady=0
        for i in range(len(self.lablimgs)):
            padx = 0
            for j in range(self.startShow,self.endShow):
                q = self.map[i % len(self.map)][j % len(self.map[0])][0].scaled(int(self.width()/34),int(self.height()/len(self.lablimgs)),Qt.KeepAspectRatio) # l'image scaled des carreaux
                y = q.height()

                self.lablimgs[i % len(self.lablimgs)][j % len(self.lablimgs[0])].setPixmap((q)) # on ajoute l'image au label
                self.lablimgs[i % len(self.lablimgs)][j % len(self.lablimgs[0])].setGeometry(0, 0, q.width(), q.height())
                self.lablimgs[i % len(self.lablimgs)][j % len(self.lablimgs[0])].move(padx, pady)
                self.widthImg = q.width()
                #print(self.lablimgs[i % len(self.lablimgs)][j % len(self.lablimgs[0])].width())
                padx += q.width()

            pady += y
            
            

                
                
                
    
                
# Création d'une instance de l'application Qt
app = QApplication([])
start_screen = Demarrage()
start_screen.show()
app.exec_()
# Exécution de l'application Qt




































