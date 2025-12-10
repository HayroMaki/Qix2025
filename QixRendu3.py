from fltk import *
from time import sleep, time
from random import randint, choice
import os
chemin = os.path.dirname(os.path.abspath(__file__))+"\\data\\"

if __name__ == '__main__' :

    ##### Variables #####
    largeurfenetre = 1200
    hauteurfenetre = 800
    GameSpaceTaille = 600
    GameSpacex1 = (largeurfenetre//2)-(GameSpaceTaille//2)
    GameSpacey1 = 100
    GameSpacex2 = (largeurfenetre//2)+(GameSpaceTaille//2)
    GameSpacey2 = hauteurfenetre-50

    Life = 3
    lostGame = False
    SpawnX = (largeurfenetre//2)
    SpawnY = (hauteurfenetre-50)
    PlayerX = SpawnX
    PlayerY = SpawnY
    vitesse = 2 # 1,2,5 ou 10
    sens = None
    LastMove = None

    InPath = True
    DrawMode = False
    LastModewasDraw = False

    LastPointX = None
    LastPointY = None

    BuildingPath = []

    chemins = [
        ((GameSpacex1,GameSpacey1),(GameSpacex2,GameSpacey1)),
        ((GameSpacex2,GameSpacey1),(GameSpacex2,GameSpacey2)),
        ((GameSpacex1,GameSpacey1),(GameSpacex1,GameSpacey2)),
        ((GameSpacex1,GameSpacey2),(GameSpacex2,GameSpacey2)),
        ]
    
    oldchemins = []

    TotalSurface=float((GameSpacex1-GameSpacex2)*(GameSpacey1-GameSpacey2))
    SurfaceActuel=0.0

    DrawPolygone = []
    EntirePolygone = []

    DoQix=True
    cx=GameSpacex1+2
    cy=GameSpacey1+2
    taille=100
    vitesseQix = 2
    Qixdep = 1
    ColorQix="purple"

    NbSparx=2 #entre 0 et 6
    vitesseSparx = 2
    Sparxlst=[]

    ay=50
    ax=(largeurfenetre//2)

    mx=0
    my=0
    tx=530
    ty=100
    mcote=1500

    bx=450
    by=200
    bx1=750
    by1=300

    start=False
    Score=0
    invincible=False
    boost=0
    boostrate=1

    csx=50
    csy=220
    cscote=70
    cscolor='darkgreen'
    cscolor2='darkgreen'
    cscolor3='darkgreen'
    obstacle=True
    bonus1234=True
    config=True
    level=1
    #####################

    cree_fenetre(largeurfenetre,hauteurfenetre)
    rectangle(0,0,largeurfenetre,hauteurfenetre,"black","black",)
    rectangle(GameSpacex1,GameSpacey1,GameSpacex2,GameSpacey2,"white",'',5)

    def AfficheLife(life):
        if life==3:
            life1x=largeurfenetre/2-30
            life2x=largeurfenetre/2
            life3x=largeurfenetre/2+30
            life1y=life2y=life3y=hauteurfenetre-25
            life1=[(life1x,life1y+10),(life1x+10,life1y),(life1x,life1y-10),(life1x-10,life1y)]
            life2=[(life2x,life2y+10),(life2x+10,life2y),(life2x,life2y-10),(life2x-10,life2y)]
            life3=[(life3x,life3y+10),(life3x+10,life3y),(life3x,life3y-10),(life3x-10,life3y)]

        elif Life==2:
            life1x=largeurfenetre/2-15
            life2x=largeurfenetre/2+15
            life1y=life2y=hauteurfenetre-25
            life1=[(life1x,life1y+10),(life1x+10,life1y),(life1x,life1y-10),(life1x-10,life1y)]
            life2=[(life2x,life2y+10),(life2x+10,life2y),(life2x,life2y-10),(life2x-10,life2y)]

        elif Life==1:
            life1x=largeurfenetre/2
            life1y=hauteurfenetre-25
            life1=[(life1x,life1y+10),(life1x+10,life1y),(life1x,life1y-10),(life1x-10,life1y)]

        if Life>=1:
            polygone(life1,"white","blue",4)
        if Life>=2:
            polygone(life2,"white","blue",4)
        if Life>=3:
            polygone(life3,"white","blue",4)

    def perdu():
        efface_tout() 
        rectangle(0, 0, largeurfenetre, hauteurfenetre, "black", "black")
        texte(largeurfenetre // 3, hauteurfenetre // 2, "Vous avez perdu !", taille=40, couleur="red")
        mise_a_jour()
        sleep(1)
        ferme_fenetre()

    def gagne():
        efface_tout() 
        rectangle(0, 0, largeurfenetre, hauteurfenetre, "black", "black")
        texte(largeurfenetre // 3, hauteurfenetre // 2, "Vous avez gagné !", taille=40, couleur="green")
        mise_a_jour()
        sleep(1)

    def lvlup(level):
        level+=1
        efface_tout() 
        rectangle(0, 0, largeurfenetre, hauteurfenetre, "black", "black")
        texte(largeurfenetre // 2, hauteurfenetre // 2, "Niveau "+str(level), taille=40, couleur="green", ancrage='center')
        mise_a_jour()
        sleep(1)
    
    def bouton(x, y,x1,y1,text):
        rectangle(x, y, x1, y1, "black" ,"dimgrey",3)
        texte(x+148,y+50,text,'black', "center", "Helvetica", 30)

    def menu(x,y,cote,x2,y2):
        rectangle(x, y, x + cote, y + cote, "dimgrey" ,"dimgrey",2)
        texte(x2,y2,'QIX','white', "sw", "Helvetica", 50)
        bouton(bx,by,bx1,by1,'Jouer')
        bouton(bx,by+150,bx1,by1+150, 'Quitter')
        bouton(bx,by+300,bx1,by1+300, '2 Joueurs')
        case(csx,csy,cscote,"Obstacle",cscolor)
        case(csx,csy+140,cscote,"Bonus",cscolor2)
        case(csx,csy+290,cscote,"Config",cscolor3)

    def case(x, y, cote, text, cscolor):
        rectangle(x, y, x + cote, y + cote,
              "black",cscolor,3)
        texte(x+105,y+35,text,"white","w", "Helvetica",20)

    def Obstacle(ObstacleCos):
        for i in range(len(ObstacleCos)):                       
            ((Ox,Oy),(Ox2,Oy2),couleur)=ObstacleCos[i]
            rectangle(Ox,Oy,Ox2,Oy2, 'dimgray', couleur, 2)  

    def SetObstacleMode():
        for e in os.listdir(chemin):
            if e=="obstacles.txt":return e
        return "Random"

    def ReadObstacleFile(file):
        with open(chemin+file,'r') as f:
            chaine=f.read()
        FirstList=chaine.split('!')
        resultlist=[]
        for e in FirstList:
            datas=list(filter(None,e.split('\n')))
            resultlist.append((
                (int(datas[0].replace('first-corner-x:','')),int(datas[1].replace('first-corner-y:',''))),
                (int(datas[2].replace('second-corner-x:','')),int(datas[3].replace('second-corner-y:',''))),
                datas[4].replace('color:','')))
        return resultlist

    def InChemin(lst, x, y):
        # Ultra-optimized: inline all operations, minimize function calls
        for ligne in lst:
            (sx, sy), (ex, ey) = ligne
            
            # Inline min/max with single comparison per axis
            # This avoids function call overhead
            if sx < ex:
                if not (sx <= x <= ex):
                    continue
            else:
                if not (ex <= x <= sx):
                    continue
            
            if sy < ey:
                if not (sy <= y <= ey):
                    continue
            else:
                if not (ey <= y <= sy):
                    continue
            
            # If we get here, point is in the ligne
            return sx, ex, sy, ey
        
        return None

    def DecrypteChemin(chemin):
        if chemin != None:
            (x1,x2,y1,y2)=chemin
            return ((x1,y1),(x2,y2))
        else : return None

    def direction():
        if touche_pressee("Up"):
            return "Up"
        elif touche_pressee("Down"):
            return "Down"
        elif touche_pressee("Left"):
            return "Left"
        elif touche_pressee("Right"):
            return "Right"
        else : return None

    def Invert_direction(direction):
        if direction not in ["Up","Down","Left","Right"]:
            return None
        else:
            if direction=="Up": return "Down"
            if direction=="Down": return "Up"
            if direction=="Left": return "Right"
            if direction=="Right": return "Left"

    def ActivateDrawMode():
        if touche_pressee("space"):
            return True
        else :
            return False

    def AfficheLignes(lst,color):
        for i in lst:
            p1,p2 = i
            x1,y1 = p1
            x2,y2 = p2
            ligne(x1,y1,x2,y2,color,5)

    def AfficheZone(lst):
        for forme in lst:
            polygone(forme,'','blue')

    def testalldirect(x,y,actual):
        if actual == "Up" or actual == "Down":
            if InChemin(chemins,x+vitesse,y)!= None:
                return "Right"
            elif InChemin(chemins,x-vitesse,y)!= None:
                return "Left"
        elif actual == "Right" or actual == "Left":
            if InChemin(chemins,x,y+vitesse)!= None:
                return "Down"
            elif InChemin(chemins,x,y-vitesse)!= None:
                return "Up"
        else : return None

    def testalldirect_oldchemins(x,y,actual):
        if actual == "Up" or actual == "Down":
            if InChemin(oldchemins,x+vitesse,y)!= None:
                return "Right"
            elif InChemin(oldchemins,x-vitesse,y)!= None:
                return "Left"
        elif actual == "Right" or actual == "Left":
            if InChemin(oldchemins,x,y+vitesse)!= None:
                return "Down"
            elif InChemin(oldchemins,x,y-vitesse)!= None:
                return "Up"
        else : return None

    def Ini_Mat(l,c):
        t=[]
        for i in range(l):
            t.append([0]*c)
        return t 

    def AfficheMat(t):
        txt = ""
        if len(t)!=0:
            if type(t[0])==list:
                for i in range(len(t)):
                    for j in t[i]:
                        txt+=str(j)
                        txt+=" "
                    txt+="\n"
            return txt

    def diviseLigne(ligne,x,y):
        ((x1,y1),(x2,y2))=ligne
        ligne1=((x1,y1),(x,y))
        ligne2=((x,y),(x2,y2))
        return ligne1, ligne2

    def diviseLigne3(ligne,xa,ya,xb,yb):
        ((x1,y1),(x2,y2))=ligne
        if y1<y2:
            y1,y2=y2,y1
            x1,x2=x2,x1
        if x1<x2:
            x1,x2=x2,x1
            y1,y2=y2,y1
        if ya<yb:
            ya,yb=yb,ya
            xa,xb=xb,xa
        if xa<xb:
            xa,xb=xb,xa
            ya,yb=yb,ya
        ligne1=((x1,y1),(xa,ya))
        ligne2=((xa,ya),(xb,yb))
        ligne3=((xb,yb),(x2,y2))
        return ligne1, ligne2, ligne3

    def AdaptChemin(polygone,chemins):
        x1,y1 = polygone[0]
        x2,y2 = polygone[-1]

        Path1 = DecrypteChemin(InChemin(chemins,x1,y1))
        Path2 = DecrypteChemin(InChemin(chemins,x2,y2))

        chemins.remove(Path1)

        if Path1==Path2:
            Pathpart1, Pathpart2, Pathpart3 = diviseLigne3(Path1,x1,y1,x2,y2)
            chemins.append(Pathpart1)
            chemins.append(Pathpart3)
            oldchemins.append(Pathpart2)
            return chemins
        
        chemins.remove(Path2)

        Pathpart1,Pathpart2 = diviseLigne(Path1,x1,y1)
        Pathpart3,Pathpart4 = diviseLigne(Path2,x2,y2)
        
        IsTrue = False
        for path in [Pathpart1,Pathpart2]:
            if IsTrue == True:
                chemins.append(path)
            ((ppx1,ppy1),(ppx2,ppy2)) = path
            if (ppx1,ppy1) == (x1,y1):
                if (ppx2,ppy2) == polygone[1] or (ppx2,ppy2) == polygone[-2]:
                    oldchemins.append(path)
                    IsTrue = True
            elif (ppx2,ppy2) == (x1,y1):
                if (ppx1,ppy1) == polygone[1] or (ppx1,ppy1) == polygone[-2]:
                    oldchemins.append(path)
                    IsTrue = True
            if IsTrue == False:
                chemins.append(path)
        
        IsTrue = False
        for path in [Pathpart3,Pathpart4]:
            if IsTrue == True:
                chemins.append(path)
            ((ppx1,ppy1),(ppx2,ppy2)) = path
            if (ppx1,ppy1) == (x2,y2):
                if (ppx2,ppy2) == polygone[1] or (ppx2,ppy2) == polygone[-2]:
                    oldchemins.append(path)
                    IsTrue = True
            elif (ppx2,ppy2) == (x2,y2):
                if (ppx1,ppy1) == polygone[1] or (ppx1,ppy1) == polygone[-2]:
                    oldchemins.append(path)
                    IsTrue = True
            if IsTrue == False:
                chemins.append(path)
        
        for i in range(0,len(polygone)-1):
            x1,y1 = polygone[i]
            x2,y2 = polygone[i+1]
            for l in chemins:
                ((xc1,yc1),(xc2,yc2)) = l
                if (x1,x2)==(xc1,xc2) or (x2,x1)==(xc1,xc2):
                    if (y1,y2)==(yc1,yc2) or (y2,y1)==(yc1,yc2): 
                        chemins.remove(l)
                        oldchemins.append(l)
                        break
        return chemins

    def ray_tracing(x,y,poly):
        n = len(poly)
        inside = False
        pol2x = 0.0
        pol2y = 0.0
        xints = 0.0
        pol1x,pol1y = poly[0]
        for i in range(n+1):
            pol2x,pol2y = poly[i % n]
            if y > min(pol1y,pol2y):
                if y <= max(pol1y,pol2y):
                    if x <= max(pol1x,pol2x):
                        if pol1y != pol2y:
                            xints = (y-pol1y)*(pol2x-pol1x)/(pol2y-pol1y)+pol1x
                        if pol1x == pol2x or x <= xints:
                            inside = not inside
            pol1x,pol1y = pol2x,pol2y

        return inside
        
    def Retire_doublons(lst):
        lst2 = []
        for e in lst:
            if e not in lst2:
                lst2.append(e)
        return lst2

    def AdaptZone(newZone,chemins):
        (Xfirst,Yfirst) = newZone[-1]
        (Xlast,Ylast) = newZone[0]
        PathL = InChemin(chemins,Xlast,Ylast)
        PathF = InChemin(chemins,Xfirst,Yfirst)

        (PathLx1,PathLx2,PathLy1,PathLy2)=PathL
        (PathFx1,PathFx2,PathFy1,PathFy2)=PathF

        if PathFx1==PathFx2: direction = "Up"
        elif PathFy1==PathFy2: direction = "Right"
        direction1 = direction
        x = Xfirst
        y = Yfirst

        matQix = Ini_Mat(hauteurfenetre,largeurfenetre)

        Poly1 = []
        Poly1.append((x,y))
        while (x,y) != (Xlast,Ylast):
            matQix[y][x]=1
            if direction=="Up":
                if InChemin(chemins,x,y-1)!=None:
                    y-=1
                else : 
                    direction = testalldirect(x,y,direction)
                    Poly1.append((x,y))
                    continue
            elif direction=="Down":
                if InChemin(chemins,x,y+1)!=None:
                    y+=1
                else : 
                    direction = testalldirect(x,y,direction)
                    Poly1.append((x,y))
                    continue
            elif direction=="Right":
                if InChemin(chemins,x+1,y)!=None:
                    x+=1
                else : 
                    direction = testalldirect(x,y,direction)
                    Poly1.append((x,y))
                    continue
            elif direction=="Left":
                if InChemin(chemins,x-1,y)!=None:
                    x-=1
                else : 
                    direction = testalldirect(x,y,direction)
                    Poly1.append((x,y))
                    continue
        Poly1.append((x,y))
        Poly1=Retire_doublons(Poly1)
        
        TestPoly=[]
        TestPoly.extend(newZone)
        TestPoly.extend(Poly1)
        TestPoly=Retire_doublons(TestPoly)
        for c in range(cx,cx+taille):
            for l in range(cy,cy+taille):
                QixIn=ray_tracing(c,l,TestPoly)
                if QixIn==True:break
            if QixIn==True:break
        if QixIn == False:
            chemins = AdaptChemin(Poly1,chemins)
            return Poly1, chemins 
        
        else:
            x = Xfirst
            y = Yfirst

            Poly2 = []
            Poly2.append((x,y))
            direction2=Invert_direction(direction1)
            direction=direction2
            while (x,y) != (Xlast,Ylast):
                if direction=="Up":
                    if InChemin(chemins,x,y-1)!=None:
                        y-=1
                    else : 
                        direction = testalldirect(x,y,direction)
                        Poly2.append((x,y))
                        continue
                elif direction=="Down":
                    if InChemin(chemins,x,y+1)!=None:
                        y+=1
                    else : 
                        direction = testalldirect(x,y,direction)
                        Poly2.append((x,y))
                        continue
                elif direction=="Right":
                    if InChemin(chemins,x+1,y)!=None:
                        x+=1
                    else : 
                        direction = testalldirect(x,y,direction)
                        Poly2.append((x,y))
                        continue
                elif direction=="Left":
                    if InChemin(chemins,x-1,y)!=None:
                        x-=1
                    else : 
                        direction = testalldirect(x,y,direction)
                        Poly2.append((x,y))
                        continue
            Poly2.append((x,y))
            Poly2=Retire_doublons(Poly2)
            if Poly2==Poly1:
                print("problème")
            chemins = AdaptChemin(Poly2,chemins)
            return Poly2, chemins
      
    def Qix(x, y, cote):
        rectangle(x, y, x + cote, y + cote,
              ColorQix,"",2, tag='Qix')

    def Sparx(x,y,cote):
        rectangle(x+cote,y+cote,x-cote,y-cote,"mediumseagreen","",3)

    def Respawn():
        randomchemin=choice(chemins)
        ((rdchx1,rdchy1),(rdchx2,rdchy2))=randomchemin
        if rdchx1==rdchx2 : 
            minimum = min(rdchy1,rdchy2)
            maximum = max(rdchy1,rdchy2)
            respawnx= rdchx1
            respawny= minimum+((maximum-minimum)//2)
            if respawny%2!=0: respawny+=1
        elif rdchy1==rdchy2 :
            minimum = min(rdchx1,rdchx2)
            maximum = max(rdchx1,rdchx2)
            respawnx= minimum+((maximum-minimum)//2)
            if respawnx%2!=0: respawnx+=1
            respawny= rdchy1
        else: return SpawnX, SpawnY
        return respawnx, respawny

    def Aire_polygone(poly):
        if len(poly)<3:
            return None
        
        aire = 0.0
        n = len(poly)
        for i in range(n):
            x1, y1 = poly[i]
            x2, y2 = poly[(i + 1) % n]

            aire += (x1 * y2 - x2 * y1)

        aire = abs(aire) / 2.0
        return aire

    def creer_bonus(nb_bonus):
        bonus=[]
        for nbb in range(nb_bonus):
            bx=randint(280,880)
            by=randint(0,730)
            for i in range(len(ObstacleCos)):
                if bx or by == ObstacleCos[i]:
                    bx=randint(GameSpacex1,GameSpacex2)
                    by=randint(GameSpacey1,GameSpacey2)
            bonus.append((bx,by))
        return bonus

    def SetBonusMode():
        for e in os.listdir(chemin):
            if e=="bonus.txt":return e
        return "Random"

    def ReadBonusFile(file):
        with open(chemin+file,'r') as f:
            chaine=f.read()
        FirstList=chaine.split('!')
        resultlist=[]
        for e in FirstList:
            datas=list(filter(None,e.split('\n')))
            resultlist.append((int(datas[0].replace('x:','')),int(datas[1].replace('y:',''))))
        return resultlist

    def affiche_bonus(bonus):
        for bonus in bonus:
            rectangle(bonus[0],bonus[1],bonus[0]+7,bonus[1]+7,'mediumpurple','mediumaquamarine', "2","bonus")

    def mange_bonus(bonus,joueur):
        for i in range(len(bonus)):
            if bonus[i][0] -5 <= joueur[0] <= bonus[i][0] + 5 and bonus[i][1] -5 <= joueur[1] <= bonus[i][1] + 5:
                bonus.pop(i)
                efface("bonus")
                break
        return bonus

    def SetConfigMode():
        for e in os.listdir(chemin):
            if e=="config.txt":return e
        return "Classic"

    def ReadConfigFile(file,DoQix,QixSize,QixSpeed,SparxNumber,GameHorizontalSpace):
        with open(chemin+file,'r') as f:
            chaine=f.read()
        FirstList=chaine.split('\n')
        result={
            'DoQix':DoQix,
            'QixSize':QixSize,
            'QixSpeed':QixSpeed,
            'SparxNumber':SparxNumber,
            'GameHorizontalSpace':GameHorizontalSpace
        }
        for e in FirstList:
            List=e.split(':')
            result[List[0]]=List[1]
        return result

    while start == False: #Menu
        menu(mx,my,mcote,tx,ty)
        cgx, cgy= attend_clic_gauche()
        if bx <= cgx <= bx1 and by <= cgy <= by1:
            start=True
            sleep(0.5)
        elif bx <= cgx <= bx1 and by + 150 <= cgy <= by1 + 150:
            ferme_fenetre()
        elif bx <= cgx <= bx1 and by + 300 <= cgy <= by1 + 300:
            print('Fonction a implémenter')

        #case
        elif csx <= cgx <= csx+cscote and csy <= cgy <= csy + cscote:
            if cscolor == "darkred":
                cscolor = "darkgreen"
                obstacle=True
            else:
                cscolor = "darkred"
                obstacle=False
            mise_a_jour()
        elif csx <= cgx <= csx+cscote and csy + 140 <= cgy <= (csy + 140) + cscote:
            if cscolor2 == "darkred":
                cscolor2 = "darkgreen"
                bonus1234=True
            else:
                cscolor2 = "darkred"
                bonus1234=False
        elif csx <= cgx <= csx+cscote and csy + 290 <= cgy <= (csy + 290) + cscote:
            if cscolor3 == "darkred":
                cscolor3 = "darkgreen"
                config=True
            else:
                cscolor3 = "darkred"
                config=False

    if config==True:
        ConfigMode = SetConfigMode()
        if ConfigMode != "Classic":
            print("fichier de config",ConfigMode,"chargé")
            Config=ReadConfigFile(ConfigMode,DoQix,taille,vitesseQix,NbSparx,GameSpaceTaille)
            DoQix=bool(Config['DoQix'])
            taille=int(Config['QixSize'])
            vitesseQix=int(Config['QixSpeed'])
            NbSparx=int(Config['SparxNumber'])
            GameSpaceTaille=int(Config['GameHorizontalSpace'])
            GameSpacex1 = (largeurfenetre//2)-(GameSpaceTaille//2)
            GameSpacey1 = 100
            GameSpacex2 = (largeurfenetre//2)+(GameSpaceTaille//2)
            GameSpacey2 = hauteurfenetre-50
            chemins = [
            ((GameSpacex1,GameSpacey1),(GameSpacex2,GameSpacey1)),
            ((GameSpacex2,GameSpacey1),(GameSpacex2,GameSpacey2)),
            ((GameSpacex1,GameSpacey1),(GameSpacex1,GameSpacey2)),
            ((GameSpacex1,GameSpacey2),(GameSpacex2,GameSpacey2)),
            ]
            TotalSurface=float((GameSpacex1-GameSpacex2)*(GameSpacey1-GameSpacey2))

    if obstacle==True:
        ObstacleMode = SetObstacleMode() #Spawn des Obstacles
        ObstacleCos = []
        if ObstacleMode == "Random":
            lstcouleur=["lightcoral","silver","lightsteelblue","lemonchiffon"]
            nbObstacle = 4
            ecart = 100
            for i in range(nbObstacle):
                Ox1=randint(GameSpacex1,700)
                Oy1=randint(GameSpacey1,700)
                randx = randint(0,1)
                if randx==1 : Ox2 = Ox1 + randint(5,ecart)
                else : Ox2 = Ox1 + randint(-ecart,-5)
                randy = randint(0,1)
                if randy==1 : Oy2 = Oy1 + randint(5,ecart)
                else : Oy2 = Oy1 + randint(-ecart,-5)
                couleur= choice(lstcouleur)
                lstcouleur.remove(couleur)
                result = ((Ox1,Oy1),(Ox2,Oy2),couleur)
                ObstacleCos.append(result)
        else : 
            print("fichier d'obstacles",ObstacleMode,"chargé")
            ObstacleCos = ReadObstacleFile(ObstacleMode)

    if NbSparx > 0: #Spawn des sparx
        Sparxlst.append((GameSpacex1,(GameSpacey2+GameSpacey1)//2+1,False,"Down"))
        if NbSparx >1:
            Sparxlst.append((GameSpacex2,(GameSpacey2+GameSpacey1)//2+1,False,"Up"))
            if NbSparx >2:
                Sparxlst.append(((GameSpacex2+GameSpacex1)//2,GameSpacey1,False,"Left"))
                if NbSparx >3:
                    Sparxlst.append(((GameSpacex2+GameSpacex1)//2,GameSpacey1,False,"Right"))
                    if NbSparx >4:
                        Sparxlst.append((GameSpacex2,(GameSpacey2+GameSpacey1)//2+1,False,"Down"))
                        if NbSparx >5:
                            Sparxlst.append((GameSpacex1,(GameSpacey2+GameSpacey1)//2+1,False,"Up"))

    if bonus1234==True:
        BonusMode = SetBonusMode()
        if BonusMode == 'Random': bonus=creer_bonus(3)
        else : 
            print("fichier de bonus",BonusMode,"chargé")
            bonus = ReadBonusFile(BonusMode)

    while True :

        efface_tout()
    
        rectangle(0,0,largeurfenetre,hauteurfenetre,"black","black",)
        
        if SurfaceActuel==0.0:
            texte(0,50,"Surface : 0 %","white","w")
        else :
            SurfacePercent=int((SurfaceActuel/TotalSurface)*100)
            AffichePercent = "Surface :"+str(SurfacePercent)+"%"
            texte(0,50,AffichePercent,"white","w")
            if SurfacePercent >= 75:
                if level>2:
                    gagne()
                    ferme_fenetre()
                    break
                else:
                    lvlup(level)
                    if True:
                        Life = 3
                        lostGame = False
                        SpawnX = (largeurfenetre//2)
                        SpawnY = (hauteurfenetre-50)
                        PlayerX = SpawnX
                        PlayerY = SpawnY
                        sens = None
                        LastMove = None
                        InPath = True
                        DrawMode = False
                        LastModewasDraw = False
                        LastPointX = None
                        LastPointY = None

                        BuildingPath = []
                        chemins = [
                            ((GameSpacex1,GameSpacey1),(GameSpacex2,GameSpacey1)),
                            ((GameSpacex2,GameSpacey1),(GameSpacex2,GameSpacey2)),
                            ((GameSpacex1,GameSpacey1),(GameSpacex1,GameSpacey2)),
                            ((GameSpacex1,GameSpacey2),(GameSpacex2,GameSpacey2)),
                            ]
                        oldchemins = []
                        TotalSurface=float((GameSpacex1-GameSpacex2)*(GameSpacey1-GameSpacey2))
                        SurfaceActuel=0.0
                        DrawPolygone = []
                        EntirePolygone = []
                    if DoQix==True:
                        cx=GameSpacex1+2
                        cy=GameSpacey1+2
                        taille+=20
                        vitesseQix+=2
                    if NbSparx>0:
                        NbSparx+=1
                        Sparxlst=[]
                        Sparxlst.append((GameSpacex1,(GameSpacey2+GameSpacey1)//2+1,False,"Down"))
                        if NbSparx >1:
                            Sparxlst.append((GameSpacex2,(GameSpacey2+GameSpacey1)//2+1,False,"Up"))
                            if NbSparx >2:
                                Sparxlst.append(((GameSpacex2+GameSpacex1)//2,GameSpacey1,False,"Left"))
                                if NbSparx >3:
                                    Sparxlst.append(((GameSpacex2+GameSpacex1)//2,GameSpacey1,False,"Right"))
                                    if NbSparx >4:
                                        Sparxlst.append((GameSpacex2,(GameSpacey2+GameSpacey1)//2+1,False,"Down"))
                                        if NbSparx >5:
                                            Sparxlst.append((GameSpacex1,(GameSpacey2+GameSpacey1)//2+1,False,"Up"))
                    if bonus1234==True:
                        if BonusMode == 'Random': bonus=creer_bonus(3)
                        else : 
                            bonus = ReadBonusFile(BonusMode)
    
        AfficheScore=("Score : "+str(int(SurfaceActuel)))
        texte(0,100,AfficheScore,"white","w")

        AfficheZone(EntirePolygone)
        AfficheLignes(BuildingPath,"blue")
        AfficheLignes(chemins,"white")
        AfficheLignes(oldchemins,"Gray")
        AfficheLife(Life)

        Qix(cx, cy, taille)
        if obstacle==True:
            Obstacle(ObstacleCos)

        if bonus1234==True:
            affiche_bonus(bonus)

        texte(largeurfenetre/2,50,(PlayerX,PlayerY),"white","c")

        ActualPath = InChemin(chemins,PlayerX,PlayerY)
        if ActualPath == None :
            InPath = False
        else :
            InPath = True

        # passage Draw Mode / Path Mod
        if ActivateDrawMode() == True and LastModewasDraw == False:
            DrawMode = True
            if InPath == True:
                LastPointX = PlayerX
                LastPointY = PlayerY
            elif InPath != True:
                LastPointX = LastPlayerX
                LastPointY = LastPlayerY
            DrawPolygone.append((LastPointX,LastPointY))

        if InPath == True and LastModewasDraw == True :
            DrawMode = False

            DrawPolygone.append((PlayerX,PlayerY))
            
            # Check if we actually moved (avoid creating false tiny chemins)
            # Calculate total distance moved
            if len(DrawPolygone) >= 2:
                start_point = DrawPolygone[0]
                end_point = DrawPolygone[-1]
                distance_moved = abs(start_point[0] - end_point[0]) + abs(start_point[1] - end_point[1])
                
                # Only process if we moved at least a minimum distance
                if distance_moved >= vitesse * 2:  # At least 2 movement steps
                    Poly,chemins = AdaptZone(DrawPolygone,chemins)
                    DrawPolygone.extend(Poly)

                    SurfacePoly=Aire_polygone(DrawPolygone)
                    if SurfacePoly!=None:
                        SurfaceActuel+=SurfacePoly

                        EntirePolygone.append(DrawPolygone)

                        # Add the final segment from last point to current position
                        final_segment = ((PlayerX,PlayerY),(LastPointX,LastPointY))
                        final_seg_length = abs(PlayerX - LastPointX) + abs(PlayerY - LastPointY)
                        if final_seg_length >= vitesse:
                            BuildingPath.append(final_segment)
                        
                        # Add all valid BuildingPath segments to chemins
                        # (segments already validated during drawing, but double-check)
                        chemins += BuildingPath
            
            DrawPolygone = []
            BuildingPath = []

        ### On Path Mod ###
        if DrawMode == False :
            # ne laisser le Player avancer QUE sur les chemins de la liste chemin
            if ActualPath == None :
                InPath = False
                if DrawMode != True :
                    PlayerX = LastPlayerX
                    PlayerY = LastPlayerY
            else :
                Pathx1, Pathx2, Pathy1, Pathy2 = ActualPath
                InPath = True

            if InPath == True :
                LastPlayerX = PlayerX
                LastPlayerY = PlayerY

            # Gestion de la direction du Player
            if InPath == True:
                sens0 = direction()
                if sens0 is not None :
                    if sens0 == "Up":
                        PlayerY -= vitesse
                        LastMove = "Up"
                    elif sens0 == "Down":
                        PlayerY += vitesse
                        LastMove = "Down"
                    if sens0 == "Left":
                        PlayerX -= vitesse
                        LastMove = "Left"
                    elif sens0 == "Right":
                        PlayerX += vitesse
                        LastMove = "Right"

            if InPath != True:
                ListPlayer = [(PlayerX,PlayerY+10),(PlayerX-10,PlayerY),(PlayerX,PlayerY-10),(PlayerX+10,PlayerY)]
            elif InPath == True:
                ListPlayer = [(LastPlayerX,LastPlayerY+10),(LastPlayerX-10,LastPlayerY),(LastPlayerX,LastPlayerY-10),(LastPlayerX+10,LastPlayerY)]
            if invincible==True:
                polygone(ListPlayer,"yellow",'',4)
            else:
                polygone(ListPlayer,"red",'',4)
        ### ### ### ### ###

        ### Drawing Mod ###
        elif DrawMode == True:

            LastPlayerX = PlayerX
            LastPlayerY = PlayerY

            ligne(PlayerX,PlayerY,LastPointX,LastPointY,"mediumblue",5)

            sens0 = direction()
            if sens0 is not None:
                if sens0 != LastMove:
                    NewPointX = PlayerX
                    NewPointY = PlayerY
                    # Only add segment if it has actual length
                    seg_length = abs(NewPointX - LastPointX) + abs(NewPointY - LastPointY)
                    if seg_length >= vitesse:
                        BuildingPath.append(((NewPointX,NewPointY),(LastPointX,LastPointY)))
                        DrawPolygone.append((LastPointX,LastPointY))
                        DrawPolygone.append((NewPointX,NewPointY))
                        LastPointX = NewPointX
                        LastPointY = NewPointY
                if sens0 == "Up":
                    PlayerY -= vitesse
                    LastMove = "Up"
                elif sens0 == "Down":
                    PlayerY += vitesse
                    LastMove = "Down"
                elif sens0 == "Left":
                    PlayerX -= vitesse
                    LastMove = "Left"
                elif sens0 == "Right":
                    PlayerX += vitesse
                    LastMove = "Right"

            CrossingBuildingPath = InChemin(BuildingPath,PlayerX,PlayerY)
            if CrossingBuildingPath != None:
                Life-=1
                if Life<=0:
                    perdu()
                    break

                else: #Remettre à l'origine + 1sec cooldown
                    InPath = True
                    DrawMode = False
                    LastModewasDraw = False
                    BuildingPath = []
                    DrawPolygone = []
                    SpawnX, SpawnY = Respawn()
                    PlayerX=SpawnX
                    PlayerY=SpawnY
                    LastPlayerX=SpawnX
                    LastPlayerY=SpawnY
                    ListPlayer = [(PlayerX,PlayerY+10),(PlayerX-10,PlayerY),(PlayerX,PlayerY-10),(PlayerX+10,PlayerY)]
                    efface_tout()
                    rectangle(0,0,largeurfenetre,hauteurfenetre,"black","black",)
                    AfficheZone(EntirePolygone)
                    AfficheLignes(BuildingPath,"mediumblue")
                    AfficheLignes(chemins,"white")
                    AfficheLignes(oldchemins,"Gray")
                    AfficheLife(Life)
                    polygone(ListPlayer,"white",'',4)
                    Qix(cx, cy, taille)
                    for i in range(len(Sparxlst)):
                            x,y,jm,sd = Sparxlst[i]
                            Sparx(x,y,5)
                    mise_a_jour()
                    sleep(1)
                    continue

            ListPlayer = [(PlayerX,PlayerY+10),(PlayerX-10,PlayerY),(PlayerX,PlayerY-10),(PlayerX+10,PlayerY)]
            if invincible==True:
                polygone(ListPlayer,"yellow",'',4)
            else:
                polygone(ListPlayer,"red",'',4)
        ### ### ### ### ###

        ###   Ennemies  ###
        if DoQix==True: # Qix
            lastcx=cx
            lastcy=cy

            # Déplacement aléatoire
            doQixdep=randint(0,100)
            if doQixdep==0:
                Qixdep=randint(1,4)
            if Qixdep == 1:
                cx+=vitesseQix
                cy+=vitesseQix
            elif Qixdep == 2:
                cx+=vitesseQix
                cy-=vitesseQix
            elif Qixdep == 3:
                cx-=vitesseQix
                cy+=vitesseQix
            elif Qixdep == 4:
                cx-=vitesseQix
                cy-=vitesseQix

            # Collision avec les chemins
            CollisionC=False
            for i in range(cx,cx+taille+1):
                if InChemin(chemins,i,cy+taille):
                    CollisionC=True
                if InChemin(chemins,i,cy):
                    CollisionC=True
            if CollisionC==False:
                for i in range(cy,cy+taille+1):
                    if InChemin(chemins,cx+taille,i):
                        CollisionC=True
                    if InChemin(chemins,cx,i):
                        CollisionC=True
            if CollisionC==True:
                cx=lastcx
                cy=lastcy
                RandomColor=randint(1,5)
                if RandomColor==1:
                    ColorQix="darkorchid"
                if RandomColor==2:
                    ColorQix="hotpink"
                if RandomColor==3:
                    ColorQix="orchid"
                if RandomColor==4:
                    ColorQix="mediumpurple"
                if RandomColor==5:
                    ColorQix="lightpink"
                Qixdep=randint(1,4)
            # Collision avec le tracet
            if DrawMode==True:
                CollisionT=False
                BuildingPathColl=[]
                BuildingPathColl.extend(BuildingPath)
                BuildingPathColl.append(((int(PlayerX),int(PlayerY)),(int(LastPointX),int(LastPointY))))
                for i in range(cx,cx+taille+1):
                    if InChemin(BuildingPathColl,i,cy+taille):
                        CollisionT=True
                    if InChemin(BuildingPathColl,i,cy):
                        CollisionT=True

                if CollisionT==False:
                    for i in range(cy,cy+taille+1):
                        if InChemin(BuildingPathColl,cx+taille,i):
                            CollisionT=True
                        if InChemin(BuildingPathColl,cx,i):
                            CollisionT=True

                if CollisionT==True:
                    if invincible==False:
                        Life-=1
                    if Life<=0:
                        perdu()
                        break

                    else: #Remettre à l'origine + 1sec cooldown
                        InPath = True
                        DrawMode = False
                        LastModewasDraw = False
                        BuildingPath = []
                        DrawPolygone = []
                        SpawnX, SpawnY = Respawn()
                        PlayerX=SpawnX
                        PlayerY=SpawnY
                        LastPlayerX=SpawnX
                        LastPlayerY=SpawnY
                        ListPlayer = [(PlayerX,PlayerY+10),(PlayerX-10,PlayerY),(PlayerX,PlayerY-10),(PlayerX+10,PlayerY)]
                        efface_tout()
                        rectangle(0,0,largeurfenetre,hauteurfenetre,"black","black",)
                        AfficheZone(EntirePolygone)
                        AfficheLignes(BuildingPath,"mediumblue")
                        AfficheLignes(chemins,"white")
                        AfficheLignes(oldchemins,"Gray")
                        AfficheLife(Life)
                        polygone(ListPlayer,"white",'',4)
                        Qix(cx, cy, taille)
                        for i in range(len(Sparxlst)):
                            x,y,jm,sd = Sparxlst[i]
                            Sparx(x,y,5)
                        mise_a_jour()
                        sleep(1)
                        continue

            ocx=cx
            ocy=cy

        if NbSparx!=0: # Sparx
            for i in range(len(Sparxlst)):
                Sx, Sy, JustMoved, SparxDir = Sparxlst[i]
                oSx=Sx
                oSy=Sy

                if SparxDir=="Down":
                    if InChemin(chemins,Sx-5,Sy)!=None and JustMoved==False:
                        Sx-=vitesseSparx
                        SparxDir="Left"
                        JustMoved=True
                    elif InChemin(chemins,Sx+5,Sy)!=None and JustMoved==False:
                        Sx+=vitesseSparx
                        SparxDir="Right"
                        JustMoved=True
                    elif InChemin(chemins,Sx,Sy)==None:
                        if InChemin(oldchemins,Sx-5,Sy)!=None and JustMoved==False:
                            Sx-=vitesseSparx
                            SparxDir="Left"
                            JustMoved=True
                        elif InChemin(oldchemins,Sx+5,Sy)!=None and JustMoved==False:
                            Sx+=vitesseSparx
                            SparxDir="Right"
                            JustMoved=True
                        else:
                            Sy+=vitesseSparx
                            JustMoved=False
                    else:
                        Sy+=vitesseSparx
                        JustMoved=False
                    
                elif SparxDir=="Up":
                    if InChemin(chemins,Sx+5,Sy)!=None and JustMoved==False:
                        Sx+=vitesseSparx
                        SparxDir="Right"
                        JustMoved=True
                    elif InChemin(chemins,Sx-5,Sy)!=None and JustMoved==False:
                        Sx-=vitesseSparx
                        SparxDir="Left"
                        JustMoved=True
                    elif InChemin(chemins,Sx,Sy)==None:
                        if InChemin(oldchemins,Sx+5,Sy)!=None and JustMoved==False:
                            Sx+=vitesseSparx
                            SparxDir="Right"
                            JustMoved=True
                        elif InChemin(oldchemins,Sx-5,Sy)!=None and JustMoved==False:
                            Sx-=vitesseSparx
                            SparxDir="Left"
                            JustMoved=True
                        else:
                            Sy-=vitesseSparx
                            JustMoved=False
                    else:
                        Sy-=vitesseSparx
                        JustMoved=False
                    
                elif SparxDir=="Right":
                    if InChemin(chemins,Sx,Sy-5)!=None and JustMoved==False:
                        Sy-=vitesseSparx
                        SparxDir="Up"
                        JustMoved=True
                    elif InChemin(chemins,Sx,Sy+5)!=None and JustMoved==False:
                        Sy+=vitesseSparx
                        SparxDir="Down"
                        JustMoved=True
                    elif InChemin(chemins,Sx,Sy)==None:
                        if InChemin(oldchemins,Sx,Sy-5)!=None and JustMoved==False:
                            Sy-=vitesseSparx
                            SparxDir="Up"
                            JustMoved=True
                        elif InChemin(oldchemins,Sx,Sy+5)!=None and JustMoved==False:
                            Sy+=vitesseSparx
                            SparxDir="Down"
                            JustMoved=True
                        else:
                            Sx+=vitesseSparx
                            JustMoved=False
                    else:
                        Sx+=vitesseSparx
                        JustMoved=False
                
                elif SparxDir=="Left":
                    if InChemin(chemins,Sx,Sy+5)!=None and JustMoved==False:
                        Sy+=vitesseSparx
                        SparxDir="Down"
                        JustMoved=True
                    elif InChemin(chemins,Sx,Sy-5)!=None and JustMoved==False:
                        Sy-=vitesseSparx
                        SparxDir="Up"
                        JustMoved=True
                    elif InChemin(chemins,Sx,Sy)==None:
                        if InChemin(oldchemins,Sx,Sy+5)!=None and JustMoved==False:
                            Sy+=vitesseSparx
                            SparxDir="Down"
                            JustMoved=True
                        elif InChemin(oldchemins,Sx,Sy-5)!=None and JustMoved==False:
                            Sy-=vitesseSparx
                            SparxDir="Up"
                            JustMoved=True
                        else:
                            Sx-=vitesseSparx
                            JustMoved=False
                    else:
                        Sx-=vitesseSparx
                        JustMoved=False

                if DrawMode==False:
                    CollisionS=False
                    for x in range(PlayerX-10,PlayerX+10):
                        if x==Sx and PlayerY==Sy:
                            CollisionS=True
                    if CollisionS==False:
                        for y in range(PlayerY-10,PlayerY+10):
                            if y==Sy and PlayerX==Sx:
                                CollisionS=True
                    if CollisionS==True:
                        if invincible==False:
                            Life-=1
                        if Life<=0:
                            perdu()
                            lostGame=True
                            break

                        else: #Remettre à l'origine + 1sec cooldown
                            InPath = True
                            DrawMode = False
                            LastModewasDraw = False
                            BuildingPath = []
                            DrawPolygone = []
                            SpawnX, SpawnY = Respawn()
                            PlayerX=SpawnX
                            PlayerY=SpawnY
                            LastPlayerX=SpawnX
                            LastPlayerY=SpawnY
                            ListPlayer = [(PlayerX,PlayerY+10),(PlayerX-10,PlayerY),(PlayerX,PlayerY-10),(PlayerX+10,PlayerY)]
                            efface_tout()
                            rectangle(0,0,largeurfenetre,hauteurfenetre,"black","black",)
                            AfficheZone(EntirePolygone)
                            AfficheLignes(BuildingPath,"mediumblue")
                            AfficheLignes(chemins,"white")
                            AfficheLignes(oldchemins,"Gray")
                            AfficheLife(Life)
                            polygone(ListPlayer,"white",'',4)
                            Qix(cx, cy, taille)
                            for i in range(len(Sparxlst)):
                                x,y,jm,sd = Sparxlst[i]
                                Sparx(x,y,5)
                            mise_a_jour()
                            sleep(1)
                            continue
                
                Sparxlst[i]=(Sx,Sy,JustMoved,SparxDir)
                Sparx(Sx,Sy,5) 

            if lostGame==True:break
        ### ### ### ### ###

        ###  Obstacles  ###
        if DrawMode == True:
            if obstacle==True:
                for i in range(len(ObstacleCos)):
                    CollisionO = False
                    ((Ox, Oy), (Ox2, Oy2), couleur) = ObstacleCos[i]
                    if Ox > Ox2 :
                        Ox,Ox2=Ox2,Ox
                    if Oy > Oy2:
                        Oy,Oy2=Oy2,Oy
                    if Ox < PlayerX < Ox2 and Oy < PlayerY < Oy2:
                        CollisionO = True
                        PlayerX = LastPlayerX
                        PlayerY = LastPlayerY

            ####   BONUS   ####
            if bonus1234==True:
                taille_pommes = len(bonus)
                pommes = mange_bonus(bonus,(PlayerX,PlayerY))
                if taille_pommes != len(bonus):
                    Time1 = time()
                    invincible = True

                if taille_pommes != len(bonus):
                    invincible = True
                    invincible_start_time = time()

                if invincible:
                    current_time = time()
                    if current_time - invincible_start_time > 5:
                        invincible = False
        ### ### ### ### ###
        ### ### ### ### ###
        if PlayerX<GameSpacex1 or PlayerX>GameSpacex2 or PlayerY<GameSpacey1 or PlayerY>GameSpacey2:
            PlayerX=LastPlayerX
            PlayerY=LastPlayerY

        if DrawMode == True :
            LastModewasDraw = True
        elif DrawMode == False :
            LastModewasDraw = False

        # Fermeture de la fenetre
        if touche_pressee("Escape"):
            ferme_fenetre()

        # sleep(0.01)
        mise_a_jour()
