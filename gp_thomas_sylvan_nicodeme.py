# -*- coding: utf-8 -*-
"""
Created on Mon Apr 12 13:19:47 2021

@author: Buhard
"""
# =============================================================================
# début du programme
# =============================================================================
# importation des modules
from tkinter import*
from random import*
from math import sqrt
import winsound
#creation de la fenetre
Mafenetre = Tk()
#creation du cancvas
can2 = Canvas(Mafenetre,width = 1500, height = 700 , bd=0, bg="white")
can2.pack(padx=0,pady=0)

#-----creation des images----

# images des objets base
case_maison=PhotoImage(file="case_maison1.png")
case_portail=PhotoImage(file="portaill.png")
base_neutre=PhotoImage(file="case_maison_neutre.png")

#image de fond de jeu
arene1=PhotoImage(file="arene3.png")
arene=PhotoImage(file="arene2.png")
fond_jeu=PhotoImage(file="fond2.png")

photo1=PhotoImage(file="jouer3.png")
photo2=PhotoImage(file="option4.png")

fond_option=PhotoImage(file="fond_option4.png")
fond_information=PhotoImage(file="fond_inforamtion10.png")
f_information=PhotoImage(file="information2.png")

#images des objets troupes
vilains_droite=PhotoImage(file="ennemie-droite.png")
vilains_face=PhotoImage(file="ennemie-face.png")
vilains_dos=PhotoImage(file="ennemie-dos.png")
vilains_gauche=PhotoImage(file="ennemie-gauche.png")
gentils_droite=PhotoImage(file="perso1-droite.png")
gentil_face=PhotoImage(file="perso1-face.png")
gentil_dos=PhotoImage(file="perso1-dos.png")
gentil_gauche=PhotoImage(file="perso1-gauche.png")

# dictionnaire des images des troupes 
dict_image={"vilains": { "droite":vilains_droite, "face":vilains_face, "dos":vilains_dos , "gauche": vilains_gauche},
            "gentils": { "droite":gentils_droite, "face":gentil_face, "dos":gentil_dos, "gauche":gentil_gauche }
               }

#creation de la map
dic_mat={"1":arene,"2":arene1}

#---------------- definition des classes----------------   
    
class Troupe :
    
    def __init__(self,x,y,d,base,team):
        """chaque troupe apparait aux coordonées x,y et dans la team
        vilains ou gentil
        
        self.x : les cordonées en x
        self.y : les cordonées en y
        self.d : la direction(haut bas gauche droite)
        self.team : vilains ou gentil
        """
        self.x = x
        self.y = y
        self.d = d
        self.team = team
        self.base = base
        self.target = None

    def affiche_troupe(self):
        """affiche la troupe a ses cordonnées """  
        self.perso=can1.create_image(self.x,self.y,image=dict_image[self.team.nom][self.d],anchor="nw")
        
    def atk_temp(self):
        """methode simple et rapide 
        pour trouver un chemin qui mène a la base que l'on vise"""
        
        # si la troupe n'a pas de cible, elle attend devant la base'
        if self.target==None:
            return()
        #dépalement a droite
        xy=self.target.get_coords()
        x=xy[0]
        y=xy[1]
        if self.x < x:
            self.x += 1
            can1.coords(self.perso,self.x, self.y)
            can1.itemconfig(self.perso,image=dict_image[self.team.nom]["droite"])
        
        #deplacement a gauche
        if self.x > x:
            self.x -= 1
            can1.itemconfig(self.perso,image=dict_image[self.team.nom]["gauche"])
            can1.coords(self.perso,self.x, self.y)
            
        #deplacement en haut
        if self.y > y:
            self.y -= 1
            can1.itemconfig(self.perso,image=dict_image[self.team.nom]["dos"])
            can1.coords(self.perso,self.x, self.y)

        #deplacment en bas  
        if self.y < y:
            self.y += 1
            can1.itemconfig(self.perso,image=dict_image[self.team.nom]["face"])
            can1.coords(self.perso,self.x, self.y)
        
    def test_case(self,can1,liste_base):#il faudrait qu'il teste s'il est sur une base alliée alors il rentre + le déplacer a la classe troupe idée d'un lock
            """test si la troupe est sur la case d'une base alliée , alors il s'ajoute au compteur de la base,
            ou ennemie et il meurt en tuant 1 ennemi retranché"""
            # tupple des coordonées
            tupl=(self.x,self.y)
            #pour chaque base de la liste
            for bse in liste_base:
                #si il est sur la case de sa base
                if tupl == bse.get_coords():
                    #si bse est dans la liste des bases de sa team
                    if bse in self.team.liste_base:
                        # le troupe s'ajoute à l'effectif de la base
                        bse.compteur+=1
                        del self.base.liste_troupes[self.base.liste_troupes.index(self)] 
                        can1.delete(self.perso)
                        can1.itemconfig(bse.texte_pnj,text=str(bse.compteur))
                        return()
                
                    else:
                        # si il ont les mm coords, il pop
                        del self.base.liste_troupes[self.base.liste_troupes.index(self)] 
                        can1.delete(self.perso)
                        bse.test_base(self.team)
                        return()
    
class Base:
    
    def __init__(self,x,y,team):
        """chaque base apparait aux coordonées x,y et dans la team
        vilains ou gentil
        self.x : les cordonées en x
        self.y : les cordonées en y
        self.team : vilains ou gentil
        self.compteur: nbr de troupe dans la base"""
        
        self.x = x
        self.y = y
        self.team = team 
        # dictionnaire d'images par team
        self.dico_base = {"vilains":case_portail,"gentils":case_maison,"Neutres":base_neutre}
        # compteur de troupe dans la base
        self.compteur = 0
        # liste des troupes en dehors de la base
        self.liste_troupes = []
        # zone de texte avec le nbr de troupes dedans
        self.rec=a = can1.create_rectangle(self.x+15, self.y-17,self.x+43, self.y-3, fill='white')
        self.texte_pnj = can1.create_text(self.x+30,self.y-10,text=str(self.compteur),font=("Arial",10,'bold'),fill="black")
        

    def affiche_base(self):
        """affiche la base"""
        self.image=can1.create_image(self.x,self.y,image=self.dico_base[self.team.nom],anchor="nw")
        
    def recruter(self):
        """recrute 1 troupe dans la base"""
        self.compteur += 1
        # MAJ de la zone de texte
        can1.itemconfig(self.texte_pnj,text=str(self.compteur))
        
    def sortir(self,n): 
        """fais sortir n troupe de la base """
        #on fait l'opération n fois
        for i in range (n):
            # si il reste des troupes disponibles dans la base
            if self.compteur > 0:
                # creation d'un objet troupe à chaque itération
                trp = Troupe(self.x,self.y,"droite",self,self.team) 
                self.liste_troupes.append(trp)
                # coordonées non egales pour avoir un décalage plus ésthétique
                trp.x += randint(-20,20)
                trp.y += randint(-20,20)
                trp.affiche_troupe()
                # la troupe n'est plus en garnison, oon enleve 1 au compteur
                self.compteur -= 1
                can1.itemconfig(self.texte_pnj,text=str(self.compteur))
            
    def get_coords(self)->tuple: 
        """retourne un tuple des coordonées de la base """
        tpl=(self.x,self.y)
        return(tpl)
    
    def test_base(self,team_chg):
        """test si la base est neutre, ennemie, ou alliée 
        a partir du nombre de troupes en garnison"""
        
        # si le compteur est positif
        if self.compteur >= 1:
            # les troupes se battent et perdent 1 de chaque coté
            self.compteur -= 1
            can1.itemconfig(self.texte_pnj,text=str(self.compteur))
        
        # si la base est déja vide, aucune troupe n'est perdu est la base est prise'
        elif self.compteur < 1:
                     
            self.idc=0
            # elle s'ajoute donc a la team qui attaque'
            chg = self.team.liste_base.pop(self.team.liste_base.index(self))
            team_chg.liste_base.append(chg)
            self.team = team_chg
            # MAJ de l'image de la base et du compteur
            
            can1.itemconfig(self.image,image=self.dico_base[self.team.nom])
            can1.itemconfig(self.texte_pnj,text=str(self.compteur))
            
            # si la base est prise alors que des troupes sont sorties, elle sont dnées a l'equipe adverse'
            for trp in self.liste_troupes:
                can1.delete(trp.perso)
                trp.team=team_chg
                trp.affiche_troupe()    
                
class Team:
    
    def __init__(self,nom,jeu):
        """ une équipe qui joue est enregistrée avec un nom et dans un jeu en particulier
        self.nom : str, le nom de l'équipe'
        self.liste_base : liste d'objet de toutes les bases de la Team 
        self.jeu: le jeu dans lequel est la team """
        self.nom = nom
        self.liste_base = [] 
        self.jeu = jeu
        
    def ajoute_base(self,x,y,can,avantage=None):
        """ajoute un objet base au jeu aux coords x,y dans le can1,
        avec un avantage pour les neutres"""
        #creation d'un objet base et on l'affiche
        bse=Base(x,y,self)
        bse.affiche_base()
        # on l'append a la liste de bases de la Team
        self.liste_base.append(bse)
        self.jeu.liste_bases.append(bse)
        # on donne un avantage pour les neutres seulement
        if avantage!=None:
            bse.compteur=avantage
            can1.itemconfig(bse.texte_pnj,text=str(bse.compteur))
        
    def IA(self,Gentils,Vilains,Neutres): #point d'arret= ajustements prévus
        """" L'ennemi du jeu est cette IA"""
        
        # pour chauque base que possède l'ennemi'
        for bse in self.liste_base:
            if len(bse.liste_troupes)==0:
                # si le compteur est plus grand que 5, il sort 3 troupes
                if bse.compteur >= 5: 
                    bse.sortir(3)
                # on tire un numéro au hasard pour chaque base, qui ne fera donc pas forcement le meme chose
                hsr = randint(0,6)  
                # ajoute du hasard, soit il attaque, soit il fais des renforts
                if hsr!=3: 
                    # bse.sortir(3)
                    for trp in bse.liste_troupes:
                        trp.target=dist(Neutres.liste_base + Gentils.liste_base ,bse.get_coords())
                    
                elif hsr == 3 :
                    # sinon une base au hasard dans sa liste pour faire des déplacements
                    for trp in bse.liste_troupes:
                        trp.target = self.liste_base[randint(0,len(self.liste_base)-1)]
            #si la base est trop peuplée on envoie 7 soldats
            if bse.compteur>=10:
                bse.sortir(7)
                # on change la cible de toutes les troupes de la base
                for trp in bse.liste_troupes:
                       trp.target=dist(Neutres.liste_base + Gentils.liste_base ,bse.get_coords())
        
class Jeu :
    
    def __init__(self,dico,fond):
        """le fond et le dictionnaire du niveau choisi"""
#        self.matrice=matrice
        self.dico=dico
        #str avec la clé pour le fond
        self.fond=fond
        # liste des equipes du jeu
        self.liste_team=[]
        #liste des bases du jeu
        self.liste_bases=[]
               
    def dessine_matrice(self,can):
        """dessine la matrice dans le canevas choisi"""
        can.create_image(0,0,image=self.dico[self.fond],anchor="nw")
 
    def ajoute_team(self,obj):
        """ajoute une base au jeu"""
        #creation d'un objet base et on l'affiche
        self.liste_team.append(obj)
       
#----------------programme principal-------------------
  
#---variables globale--- 
lock = False   
score = 0
dead = False  
compteur_monde = 1
       
#---fonctions globales---

def menu() :
    """affichage du menu"""
    global can2,bou1,bou2,bou3,bou5,bou6,fond_jeu,image_fond,mixer,na
    can2=Canvas(Mafenetre,width=1500,height=700,bg='grey')
    can2.place(x=0,y=0)
    image_fond=can2.create_image(0,0,image=fond_jeu,anchor="nw")
    #creé un canva pour le menu
    bou1=Button(Mafenetre,text="JOUER",command=jouers)
    bou1.place(x=580,y=13)
    bou1.config(image=photo1,width=380,height=92,bd=0)
    bou2=Button(Mafenetre,text="OPTION",command=option)
    bou2.place(x=538,y=155)
    bou2.config(image=photo2,width=380,height=75,bd=0)
    bou3=Button(Mafenetre,text="Quitter",command=quitter)
    bou3.place(x=711,y=675)
    #créé les boutons du menu
    na='napoleon.wav'
    winsound.PlaySound(na,winsound.SND_LOOP|winsound.SND_ASYNC)
    #ajoute la musique du menu


def jouers():
    """lance la musique du jeu et la fonction endless"""
    global bo2
    bo2='bo2.wav'
    winsound.PlaySound(bo2,winsound.SND_LOOP|winsound.SND_ASYNC)
    #lance la musique du jeu
    endless()
    
def quitter():
    """fonction quitter pour arreter le son son qd on presse le bouton quitter"""
    Mafenetre.destroy() #detruit la fentre et enleve le son
    winsound.PlaySound(None, 0)

  
def option():
    """page du choix des niveaux"""
    global can2,bou1,bou2,bou3,bou4,bou5,bou6,fond_option,f_information,image_fond,fond_jeu
    bou1.place_forget()
    bou2.place_forget()
    bou3.place_forget()
    #detruit les boutonsdu menu
    bou4=Button(Mafenetre,text="retour",command=menu)
    bou4.place(x=711,y=675) #créé un bouton retour
    can2.itemconfig(image_fond,image=fond_option) #change l'image 
    bou5=Button(Mafenetre,text="INFORMATION",command=information)
    bou5.place(x=876,y=558) #créé un bouton information
    bou5.config(image=f_information,width=380,height=80,bd=0)
    
def information():
    """page des informations du jeu"""
    global can2,bou1,bou2,bou3,bou4,bou5,bou6,fond_information,image_fond,fond_jeu
    bou1.place_forget()
    bou2.place_forget()
    bou3.place_forget()
    bou4.place_forget()
    bou5.place_forget() #detruit les boutons 
    bou6=Button(Mafenetre,text="retour",command=option)
    bou6.place(x=711,y=675) #créé un bouton retour et change l'image 
    can2.itemconfig(image_fond,image=fond_information) 
 
def game_over():
    """créé une fenetre un texte game over et un boutton quand on perd"""
    can1=Canvas(Mafenetre,bg="black",width=1500,height=700)
    can1.place(x=0,y=0)
    #créé une fenetre
    can1.create_text(730,300,text="GAME OVER ",font=("Impact",100),fill="red")
    can1.create_text(730,400,text="score : "+str(score),font=("Impact",70),fill="red")
    #créé un texte en rouge marque game over et affiche le score
    bou10=Button(Mafenetre,text="menu",command=menu)
    bou10.place(x=711,y=675) #créé un bouton qui retourne au menu
    
def aff_score(can1):
    """affiche le score a chaque round"""
    texte2=can1.create_text(730,390,text="score : "+str(score),font=("Impact",70),fill="yellow")
    #créé un texte qui affiche le score
    Mafenetre.update()
    
def manche(can1):
    """fais un compte a rebours de 3 sec avant de lancer chaque manche"""
    c=3
    
    while c!=0:
        t=(str(c))
        texte=can1.create_text(730,300,text=t,font=("Impact",100),fill="Yellow")
        Mafenetre.update()
        #créé un texte commancant a c=3 qui se detruit chaque seconde et se recréé avec c-=1 donc fais un compte a rebours
        can1.after(1000,can1.delete(texte))
        c-=1
        
def victoire(can1):
    """affiche un texte victoire a chaque fois que l'on gagne"""
    texte1=can1.create_text(730,300,text="Victoire",font=("Impact",85),fill="yellow")    
    Mafenetre.update()
    #créé un texte victoire qui se detruit 2 sec apres 
    can1.after(2000,can1.delete(texte1))
    
    
def dist(voisin:list,tupl:tuple)->object:
    """fonction qui calcule la distance entre des coordonées sous forme 
    de tuple, et les coordonées d'une liste d'objet base.
    Elle trouve la base la plus proche ou l'on a clické dans la liste voisin
    ,et renvoie un objet base
    voisin : liste
    tupl : tuple"""
    #objet le plus proche
    proche = None
    #distance qui sépare l'objet le plus proche et les cordonées indiquées
    prec = 1500
    #pour toutes les abses de la liste
    for elt in voisin:
        #calcul de la distance
        d=sqrt((tupl[0]-elt.x)**2+(tupl[1]-elt.y)**2)
        #si l'element est plus proche que le precedent alors on le remplace
        if d < prec:
            prec = d
            proche = elt
    #on retourne l'objet le plus proche
    return proche
              

#-------boucle principale------
    
def jouer_endless(can1,niveau1,Gentils,Vilains,Neutres):
    """fonction infinie pour joueur une partie dans le canvas"""
#    compteur de tours
    global dead
    c=0
    #tant qu'il nous reste une base, ou tant qu'il reste une base aux ennemis
    while (len(Gentils.liste_base)!=0 and len(Vilains.liste_base)!=0) :
        
        #on ajoute une troupe aux bases ennemies et alliées
        for bse in Gentils.liste_base:
            if c%100==0:
                bse.recruter()
                
        for bse in Vilains.liste_base:
            if c%100==0:
                bse.recruter()
            
        #pour chaque base du niveau
        for bse in niveau1.liste_bases:
            #pour chaque troupe de la base
            for trp in bse.liste_troupes:
                #fonction de déplacement de la troupe
                trp.atk_temp()
                #test des coordonées
                trp.test_case(can1,niveau1.liste_bases)
            #tour de l'IA
            Vilains.IA(Gentils,Vilains,Neutres)
        #on ajoute 1 au compteur  
        c+=1
        #update apres 5 mili-secondes
        can1.after(2)
        Mafenetre.update()
    
    #on determine qui a perdu et on affiche le canvas adapté
    if len(Gentils.liste_base) == 0:
        dead=True
        return()
        
    elif Vilains.liste_base == 0:
        dead=False
        
        
def endless():
    """fais une boucle infinie de parties de battle territory,
    qui continue et augmente le score jusqu'a ce que le joueur perde une partie.
    Le jeu se passe dans le meme canvas, seul le background et les images changent
    Au debut de chaque round, on prend des coordonées prédéfinies et assosiées au niveau pour les bases"""
    global can1,score,dead,chx,dic_mat,compteur_monde,bou9
    #creation du canvas
    can1 = Canvas(Mafenetre,width = 1500, height = 700 , bd=0, bg="white")
    can1.place(x=0,y=0)
    #on place le bouton qui fais retour menu
    bou9=Button(Mafenetre,text="menu",command=menu)
    bou9.place(x=711,y=675)
    #variable pour le choix d'une base a cibler
    chx = None  
    def Full_atk(event):
        """envoie toutes les troupes vers une certaine base"""
        #base ciblée
        global chx
        #tuple des coordonées du clic
        tupl=(int(event.x),int(event.y))
#        objet l eplus proche du clic
        obj = dist(niveau1.liste_bases,tupl)
        # si on a fait un choix parmi les bases aliées
        if chx==None:
              
            for bse in Gentils.liste_base: 
                if bse != obj:
                    bse.sortir(1)
                    for trp in bse.liste_troupes:
                        trp.target=obj
        #sinon toutes les bases sont selectionées
        else:
            chx.sortir(1)
            #toutes les troupes de la abse selectionée uniquement
            for trp in chx.liste_troupes:
                   trp.target = obj
                
    def choix(event):
        """fais le choix d'une base alliée pour changer ses troupes.
        La condition permet de désélectionner la base"""
        global chx,lock
        #verrou pour changer la base alliées selectionée si aucun base n'est deja selectionée
        if lock == False:
            tupl = (int(event.x),int(event.y))
            chx = dist(Gentils.liste_base,tupl)
            lock = True
            return()
        #si une base est déja selectionée, on remet la variable a None 
        elif lock == True:
            chx = None
            lock = False
            return()
        
    def sort(event):
        for elt in Gentils.liste_base:
            elt.sortir(1)
            
    can1.bind_all('<space>',sort) 
    can1.bind('<ButtonPress-1>',Full_atk)  
    can1.bind('<ButtonPress-3>',choix) 
    
    if compteur_monde%2 == 0:
        
        niveau1=Jeu(dic_mat,"2")
        niveau1.dessine_matrice(can1)
        # on crée les deux teams
        Gentils=Team("gentils",niveau1)
        Vilains=Team("vilains",niveau1)
        Neutres=Team("Neutres",niveau1)
        #on créé les base par team
        Gentils.ajoute_base(390,50,can1)
        Gentils.ajoute_base(290,200,can1)
        Vilains.ajoute_base(1100,300,can1)
        Vilains.ajoute_base(1100,500,can1)
        
        Neutres.ajoute_base(1150,100,can1,5)
        Neutres.ajoute_base(150,420,can1,5)
        Neutres.ajoute_base(650,70,can1,5)
        Neutres.ajoute_base(750,520,can1,5)
        Neutres.ajoute_base(690,300,can1,15)
        
    else:
        
        niveau1=Jeu(dic_mat,"1")
        niveau1.dessine_matrice(can1)
        # on crée les deux teams
        Gentils=Team("gentils",niveau1)
        Vilains=Team("vilains",niveau1)
        Neutres=Team("Neutres",niveau1)
        #on créé les base par team
        Vilains.ajoute_base(150,50,can1)
        Vilains.ajoute_base(240,450,can1)
        Gentils.ajoute_base(1150,400,can1)
        Gentils.ajoute_base(1100,50,can1)
    
        Neutres.ajoute_base(650,100,can1,5)
        Neutres.ajoute_base(710,480,can1,5)
        Neutres.ajoute_base(150,225,can1,5)
        Neutres.ajoute_base(1100,225,can1,5)
        Neutres.ajoute_base(650,300,can1,15)
        
    compteur_monde+=1
    #le décompte
    manche(can1)   
    # une fois qu'on a tout fait, on joue 
    jouer_endless(can1,niveau1,Gentils,Vilains,Neutres)
    # si on a perdi on affiche un canvas game over
    if dead == True:
        # print("vous avez perdu retour au main menu")
        game_over()

    #sinon on continue
    else:
        score+=1
        aff_score(can1)
        #canavs qui affiche la victoire
        victoire(can1)
        endless()

# on crée le jeu
menu()
Mafenetre.mainloop()

