#!/usr/bin/env python
# coding: utf8
print("===============================PyStars v.20191001==============================")
print("author of the program: Evgeniy Kosterev, Belarus, Gomel")
print("project home page: http://www.ekosterev.belastro.net/pystars.htm")
print("===============================================================================")
import os,sys,datetime
from datetime import timedelta
from math import *
from tkinter import *
import threading

POPRXY=10  #ZOOM CENTER !!!
if sys.platform != "win32" and sys.platform != "win64" and sys.platform != "darwin":
    import subprocess
    POPRXY=11
    
#sys.setrecursionlimit(10000)

font1="Arial 8" #little font
font2="Arial 10" #big font
font3="Arial 10" #font menu
font4="Arial 6" #very little font

#skycolor="darkblue"
skycolor="black"
gridcolor="darkgreen"
starcolor="lightyellow"
dsocolor="gray"
dsotextcolor="white"
textcolor="white"
horizcolor="olive"
constlincolor="royalblue"
constbuncolor="gray"
constlabcolor="gold"
planetcolor="darkkhaki"
planettextcolor="orangered"
cometcolor="lightblue"
menu_dcolor="black"
menu_lcolor="ghostwhite"
menu_selcolor="darkblue"
findcolor="red"
clickcolor="yellow"
eclcolor="goldenrod"
rclickcolor="silver"

#DSS
DSS_VER="all"
DSS_SZ1="30"
DSS_SZ2="30"

DSSLINK="http://archive.stsci.edu/"
ILINK="https://www.google.com/"

ZOOM=1 #mashtab
ZOOMOLD=ZOOM
ZOOMHIP=99999
ZOOMSAO=99999
ZOOMDSO2=10
ZOOMPLANET=100
rx=1000 #Razmer okna x potom budet perenaznaceno
ry=750 #Razmer okna y potom budet perenaznaceno
#RADIUS=1200 #Radius kruga pikseley
#RCANV=3600 #Razmer canvasa pikseley
#RCANVD2=RCANV/2
STARPOTOK=0  #stars potok ili net

#kr_on=0; risk=5  #vkl/vikl poisk ,riskatela gradkrugi

NOPRINT=0 #Print!
NOPAINT=0 #Paint!
HIDE=0 #hide buttons
MOVE=1  #insert press
NPOINTCLICK=0 #dla uglomera
RA1=0;DEC1=0;RA2=0;DEC2=0    #dla uglomera
RA_CANV2000=0    #RA CENTRA CANVASA
DEC_CANV2000=0   #DEC CENTRA CANVASA

SUMENTRY=0 #Dla proverki ismeneniy Entry

KPOL=1 #1=NORD -1=SOUTH
KPOL_OLD=1
MYLAT=52.42 #LAT
MYLON=-31 #LON -EAST
MYLATOLD=52.42
MYLONOLD=-31
CHLAT="N"
CHLON="E"
DELTAHOURS=3 #+3 HOUR

DSSYST=0 #Day Sun System
DELTAD=0 #Delta day Sun System dla trekov

UTCDTIME=""
DAY=0
MONTH=0
YEAR=0
HOUR=0
TIMEDELTA_=timedelta(hours=0)
LDTIME=""
LDAY=0
LMONTH=0
LYEAR=0
LHOUR=0
MJD=0
JD_=0
LMST=0
TIM_=0
DELTAT=0

TURN_ANGLE=0
LSUN=0
MAGN_LIMIT=10.5 # Asteroids and comets magnitude limit
    
pi2=2*pi
pid2=pi/2
pid180=pi/180
d180pi=180/pi
constlabdb=[]
asterdb=[]
cometdb=[]
stardb=[]
jsatdb=[]
ssatdb=[]

starhipdb = []
for i in range(0,24):
    starhipdb.append([])
    for j in range(0,17):
        starhipdb[i].append([])

starsaodb = []
for i in range(0,24):
    starsaodb.append([])
    for j in range(0,17):
        starsaodb[i].append([])

HIPSAO_IJ=[]  #dla Hipparcos i SAO
for i in range(0,24):
    HIPSAO_IJ.append([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])

dso1db=[]
dso2db=[]
planetdb=[]
clkoord=[]
constbun=[]
ini=[]
MPOV=[]
PMAT=[]
PMAT2=[]
PMAT1875=[]
TABLEPLNAME=[]
TABLEALT=[]

EPS = 23.4393*pid180 #Ekliptika
COSEPS=cos(EPS)
SINEPS=sin(EPS)
AU=149597870700 #au,m
re=6371 #sr radius zemli km



#======ConstBound_1875
RAL1875=[]
RAU1875=[]
DECL1875=[]
CONST1875=[]
f = open('constb_1875.dat', 'r')
for line in f:
    if line.strip!="" and line[0]!="#":
        spis=line.split()
        RAL1875.append(float(spis[0]))
        RAU1875.append(float(spis[1]))
        DECL1875.append(float(spis[2]))
        CONST1875.append(spis[3])
f.close()
#======Moon terms
Tmo_lr=[]
Tmo_b=[]
f = open('moon_terms.dat', 'r')
for line in f:
    if line.strip!="" and line[0]!="#":
        spis=line.split()
        for i in range(1,len(spis)): spis[i]=int(spis[i])
        if spis[0]=="lr": Tmo_lr.append(spis[1:len(spis)])
        elif spis[0]=="b": Tmo_b.append(spis[1:len(spis)])
f.close()
#==============================

TERMSL=[]; TERMSB=[]; TERMSR=[];
for i in range(0,10):
    TERMSL.append([]); TERMSB.append([]); TERMSR.append([])
#=======read terms file
def readterms(filename):
    T_l=[]; T_b=[]; T_r=[]
    for i in range(0,6): T_l.append([])
    for i in range(0,6): T_b.append([])
    for i in range(0,6): T_r.append([])
    f = open(filename, 'r')
    for line in f:
        if line.strip!="" and line[0]!="#":
            spis=line.split()
            spis[2]=int(spis[2])
            spis[3]=float(spis[3]); spis[4]=float(spis[4])
            j=int(spis[0][1])
            if spis[0][0]=="L": T_l[j].append(spis[2:len(spis)])
            elif spis[0][0]=="B": T_b[j].append(spis[2:len(spis)])
            elif spis[0][0]=="R": T_r[j].append(spis[2:len(spis)])
    f.close()
    return(T_l,T_b,T_r)
#======Terms
TERMSL[0],TERMSB[0],TERMSR[0]=readterms("earth_terms.dat")
TERMSL[2],TERMSB[2],TERMSR[2]=readterms("mercury_terms.dat")
TERMSL[3],TERMSB[3],TERMSR[3]=readterms("venus_terms.dat")
TERMSL[4],TERMSB[4],TERMSR[4]=readterms("mars_terms.dat")
TERMSL[5],TERMSB[5],TERMSR[5]=readterms("jupiter_terms.dat") 
TERMSL[6],TERMSB[6],TERMSR[6]=readterms("saturn_terms.dat")
TERMSL[7],TERMSB[7],TERMSR[7]=readterms("uranus_terms.dat")
TERMSL[8],TERMSB[8],TERMSR[8]=readterms("neptune_terms.dat") 
#===================

class constlab():
    name1=""
    name2=""
    pv=0
    sk=0
    pv2=0
    sk2=0
    x=0
    y=0
 
class star():
    num=0
    nam1=""
    nam2=""
    const=""
    m=99
    sp="?"
    x=0
    y=0
    ra2000=0
    dec2000=0
    ra=0
    dec=0
    dbldm=99
    dblsep=0
    varid=""
    b_v="?"
    cname=""
    mapname=""
    pmra=0
    pmdec=0
    hd=""
    sao=""

class starhip():
    num=0
    m=99
    sp=""
    x=0
    y=0
    ra2000=0
    dec2000=0
    ra=0
    dec=0
    dblcomp=""
    dblpa=-1
    dblsep=-1
    dbldm=99
    varcode=""
    varid=""
    varvmax=99
    varvmin=99
    varperiod=-1
    b_v=""
    pmra=0
    pmdec=0
    hd=""
    sao=""
    notes=""

class starsao():
    num=0
    m=99
    pmag=99
    sp=""
    x=0
    y=0
    ra2000=0
    dec2000=0
    ra=0
    dec=0
    pmra=0
    pmdec=0
    hd=""
      
class dso1():
    nam1=""
    prvh=0
    prvm=0
    prvs=0
    skl_sign=""
    sklg=0
    sklm=0
    skls=0
    m=""
    nam2=""
    inf=""
    br=""
    sz1=0
    sz2=0
    angle=0
    x=0
    y=0
    ra2000=0
    dec2000=0
    ra=0
    dec=0

class dso2():
    nam1=""
    prvh=0
    prvm=0
    prvs=0
    skl_sign=""
    sklg=0
    sklm=0
    skls=0
    m=""
    nam2=""
    inf=""
    br=""
    sz1=0
    sz2=0
    angle=0
    x=0
    y=0
    ra2000=0
    dec2000=0
    ra=0
    dec=0

class planet():
    str1=""
    str2=""
    str3=""
    str4=""
    x=0
    y=0
    ra=0
    dec=0
for i in range(0,10):planetdb.append(planet())

class jsat():
    name=""
    dx=0
    dy=0
    x=0
    y=0
for i in range(0,4):jsatdb.append(jsat())
jsatdb[0].name="Io"
jsatdb[1].name="Europa"
jsatdb[2].name="Ganymede"
jsatdb[3].name="Callisto"

class ssat():
    name=""
    dx=0
    dy=0
    x=0
    y=0
for i in range(0,8):ssatdb.append(ssat())
ssatdb[0].name="Mimas"
ssatdb[1].name="Enceladus"
ssatdb[2].name="Tethys"
ssatdb[3].name="Dione"
ssatdb[4].name="Rhea"
ssatdb[5].name="Titan"
ssatdb[6].name="Hyperion"
ssatdb[7].name="Iapetus"

class sring():
    pa=0
    b=0
    ring_magn=0
    
class asteroid():
    name=""
    num=""
    year1=0
    month1=0
    day1=0
    M1=0
    a=0
    e=0
    w=0
    N=0
    i=0
    H=0
    G=0
    str1=""
    str2=""
    str3=""
    str4=""
    x=0
    y=0
    ra=0
    dec=0
    magn=99
    
class comet():
    name=""
    year1=0
    month1=0
    day1=0
    q=0
    e=0
    w=0
    N=0
    i=0
    gg=0
    kk=0
    str1=""
    str2=""
    str3=""
    str4=""
    str5=""
    x=0
    y=0
    ra=0
    dec=0
    magn=99

print("Select star catalogue:")    
print("    1 Hipparcos")
print("    2 SAO")
cat=input()
if cat.strip()=="2": print("sao.dat will be loaded"); ZOOMSAO=10
else: print("hipparcos.dat will be loaded"); ZOOMHIP=10
print("===============================================================================")

#chtenie faila nastroiki
if os.path.isfile('program.ini'):
    print("program.ini"+" ... ",end="")
    f = open('program.ini', 'r')
    for line in f: ini.append(line)
    KPOL=float(ini[0])/abs(float(ini[0]))
    MYLAT=abs(float(ini[0]))
    MYLON=float(ini[1])
    DELTAHOURS=float(ini[2])
    f.close()
    print("OK")
else:
    f = open('program.ini', 'w')
    f.write(str(KPOL*MYLAT)+ '\n')
    f.write(str(MYLON)+ '\n')
    DELTAHOURS = 3
    f.write(str(DELTAHOURS)+ '\n')
    f.close()
#ZAPOLN BASY LABEL SOZWEZDIY
f = open('constlabel.dat', 'r')
print("constlabel.dat"+" ... ",end="")
i=0
for line in f:
    if line[0] != "#" and line[0] != ";" and line.strip()!="":
        constlabdb.append(constlab())
        constlabdb[i].name1=line[19:22]
        constlabdb[i].name2=line[25:44].strip()
        constlabdb[i].pv=float(line[0:6])
        constlabdb[i].sk=float(line[9:16])
        constlabdb[i].pv2=constlabdb[i].pv
        constlabdb[i].sk2=constlabdb[i].sk
        i=i+1
f.close()
print("OK")
#ZAPOLN BAZY ASTEROIDOV
f = open('asteroids.txt', 'r')
print("asteroids.txt"+" ... ",end="")
i=0
for line in f:
    if line[0] != "#" and line[0] != ";" and line.strip()!="":
        asterdb.append(asteroid())
        asterdb[i].name=line[9:46].strip()
        asterdb[i].num=line[0:7].strip()
        asterdb[i].year1=int(line[47:51])
        asterdb[i].month1=int(line[52:54])
        asterdb[i].day1=float(line[55:59])
        asterdb[i].M1=float(line[60:68])
        asterdb[i].a=float(line[69:78])
        asterdb[i].e=float(line[79:87])
        asterdb[i].w=float(line[88:96])
        asterdb[i].N=float(line[97:105])
        asterdb[i].i=float(line[106:114])
        asterdb[i].H=float(line[115:121])
        asterdb[i].G=float(line[122:127])
    
    i=i+1
                    
f.close()
print("OK")
#ZAPOLN BAZY KOMET
f = open('comets.txt', 'r')
print("comets.txt"+" ... ",end="")
i=0
for line in f:
    if line[0] != "#" and line[0] != ";" and line.strip()!="":
        cometdb.append(comet())
        cometdb[i].name=line[0:46].strip()
        cometdb[i].year1=int(line[47:51])
        cometdb[i].month1=int(line[52:54])
        cometdb[i].day1=float(line[55:62])
        cometdb[i].q=float(line[63:72])
        cometdb[i].e=float(line[79:87])
        cometdb[i].w=float(line[88:96])
        cometdb[i].N=float(line[97:105])
        cometdb[i].i=float(line[106:114])
        cometdb[i].gg=float(line[115:120])
        cometdb[i].kk=float(line[121:126])
    i=i+1
f.close()
print("OK")
#===========================================    
#ZAPOLN BAZY YARKIH ZWEZD
f = open('catalog.dat', 'r')
print("catalog.dat"+" ... ",end="")
i=0
for line in f:
    if line[102:107] != '     ' and line[0] != "#" and line[0] != ";" and line.strip()!="":
        stardb.append(star())
        stardb[i].num=int(line[0:4])
        stardb[i].nam1=line[4:7]
        stardb[i].nam2=line[7:11]
        stardb[i].const=line[11:14]
        prvh=int(line[75:77])
        prvm=int(line[77:79])
        prvs=float(line[79:83])
        skl_sign=line[83:84]
        sklg=int(line[84:86])
        sklm=int(line[86:88])
        skls=int(line[88:90])
        stardb[i].m=float(line[102:107])
        if line[127:147].strip()!="": stardb[i].sp=line[127:147]
        stardb[i].varid=line[51:60].strip()
        try:
            stardb[i].dbldm=float(line[180:184])
        except:
            stardb[i].dbldm=99
        try:
            stardb[i].dblsep=float(line[184:190])
        except:
            stardb[i].dblsep=0
        if line[109:114].strip()!="": stardb[i].b_v=line[109:114].strip()
        stardb[i].cname=line[199:].strip()
        stardb[i].pmra=float(line[148:154])
        stardb[i].pmdec=float(line[154:160])
        stardb[i].hd=line[25:31]
        stardb[i].sao=line[31:37]

        stardb[i].ra2000=(prvh+prvm/60+prvs/3600)
        if skl_sign!="-":
            stardb[i].dec2000=(sklg+sklm/60+skls/3600)
        else: stardb[i].dec2000=-(sklg+sklm/60+skls/3600)

        if stardb[i].nam2=="    ":strn=stardb[i].nam1.strip()
        else:
            strn=stardb[i].nam2
            if   strn[0:3]=="Alp": strn="α"+strn[3:4]
            elif strn[0:3]=="Bet": strn="β"+strn[3:4]
            elif strn[0:3]=="Gam": strn="γ"+strn[3:4]
            elif strn[0:3]=="Del": strn="δ"+strn[3:4]
            elif strn[0:3]=="Eps": strn="ε"+strn[3:4]
            elif strn[0:3]=="Zet": strn="ζ"+strn[3:4]
            elif strn[0:3]=="Eta": strn="η"+strn[3:4]
            elif strn[0:3]=="The": strn="θ"+strn[3:4]
            elif strn[0:3]=="Iot": strn="ι"+strn[3:4]
            elif strn[0:3]=="Kap": strn="κ"+strn[3:4]
            elif strn[0:3]=="Lam": strn="λ"+strn[3:4]
            elif strn[0:3]=="Mu ": strn="μ"+strn[3:4]
            elif strn[0:3]=="Nu ": strn="ν"+strn[3:4]
            elif strn[0:3]=="Xi ": strn="ξ"+strn[3:4]
            elif strn[0:3]=="Omi": strn="ο"+strn[3:4]
            elif strn[0:3]=="Pi ": strn="π"+strn[3:4]
            elif strn[0:3]=="Rho": strn="ρ"+strn[3:4]
            elif strn[0:3]=="Sig": strn="σ"+strn[3:4]
            elif strn[0:3]=="Tau": strn="τ"+strn[3:4]
            elif strn[0:3]=="Ups": strn="υ"+strn[3:4]
            elif strn[0:3]=="Phi": strn="φ"+strn[3:4]
            elif strn[0:3]=="Chi": strn="χ"+strn[3:4]
            elif strn[0:3]=="Psi": strn="ψ"+strn[3:4]
            elif strn[0:3]=="Ome": strn="ω"+strn[3:4]
        stardb[i].mapname=strn
        i=i+1
f.close()
print("OK")
#===========================================    
#ZAPOLN BAZY HYPPARCOS
def hipload():
    f = open('hipparcos.dat', 'r')
    #print("hipparcos.dat"+" ... ",end="")
    i=0
    for line in f:
        if line[0] != "#" and line[0] != ";" and line.strip()!="":
            i=int(line[12:14])
            skl_sign=line[25]
            if skl_sign=="-": j=-int(line[26:27])+8
            else: j=int(line[26:27])+8
            k=len(starhipdb[i][j])
            starhipdb[i][j].append(starhip())
            starhipdb[i][j][k].num=int(line[0:6])
            prvh=int(line[12:14])
            prvm=int(line[15:17])
            prvs=float(line[18:24])
            sklg=int(line[26:28])
            sklm=int(line[29:31])
            skls=float(line[32:37])
            starhipdb[i][j][k].m=float(line[54:60])
            starhipdb[i][j][k].sp=line[68:79]
            starhipdb[i][j][k].dblcomp=line[7:11].strip()
            starhipdb[i][j][k].ccdmcomp=line[117:119].strip()
            try:
                starhipdb[i][j][k].dblpa=int(line[120:123])
            except:
                starhipdb[i][j][k].dblpa=-1
            try:
                starhipdb[i][j][k].dblsep=float(line[124:130])
            except:
                starhipdb[i][j][k].dblsep=-1
            try:
                starhipdb[i][j][k].dbldm=float(line[131:135])
            except:
                starhipdb[i][j][k].dbldm=99
            starhipdb[i][j][k].varcode=line[52].strip()
            starhipdb[i][j][k].varid=line[86:95].strip()
            try:
                starhipdb[i][j][k].varvmax=float(line[107:111])
            except:
                starhipdb[i][j][k].varvmax=99
            try:
                starhipdb[i][j][k].varvmin=float(line[112:116])
            except:
                starhipdb[i][j][k].varvmin=99
            try:
                starhipdb[i][j][k].varperiod=float(line[100:106])
            except:
                starhipdb[i][j][k].varperiod=-1

            starhipdb[i][j][k].b_v=line[61:67].strip()
            try:
                starhipdb[i][j][k].pmra=float(line[38:44])
            except:
                starhipdb[i][j][k].pmra=0
            try:
                starhipdb[i][j][k].pmdec=float(line[45:51])
            except:
                starhipdb[i][j][k].pmdec=0
            starhipdb[i][j][k].hd=line[136:142].strip()
            starhipdb[i][j][k].sao=line[143:149].strip()
            starhipdb[i][j][k].notes=line[150]

            starhipdb[i][j][k].ra2000=(prvh+prvm/60+prvs/3600)
            if skl_sign!="-":
                starhipdb[i][j][k].dec2000=(sklg+sklm/60+skls/3600)
            else: starhipdb[i][j][k].dec2000=-(sklg+sklm/60+skls/3600)
            i=i+1
    f.close()
    #print("OK")
    #print()
    bhide.lift()
    hide()

    for i in range(0,24):
        for j in range(0,17):
            for k in range(0,len(starhipdb[i][j])):
                if i>9: ii=str(i)
                else: ii="0"+str(i)
                if j>9: jj=str(j)
                else: jj="0"+str(j)
                tag="starhip"+ii+jj+str(k)
                callback_starhip = lambda event, tag=tag: starhip_rightclick(event,tag)
                canvas.tag_bind(tag,"<Button-3>", callback_starhip)
#===========================================
#ZAPOLN BAZY SAO
def saoload():
    f = open('sao.dat', 'r')
    #print("sao.dat"+" ... ",end="")
    i=0
    for line in f:
        if line[0] != "#" and line[0] != ";" and line.strip()!="":
            i=int(line[28:30])
            skl_sign=line[49]
            if skl_sign=="-": j=-int(line[50:51])+8
            else: j=int(line[50:51])+8
            k=len(starsaodb[i][j])
            starsaodb[i][j].append(starsao())
            starsaodb[i][j][k].num=int(line[0:6])
            prvh=int(line[28:30])
            prvm=int(line[31:33])
            prvs=float(line[34:40])
            sklg=int(line[50:52])
            sklm=int(line[53:55])
            skls=float(line[56:61])
            try:
                starsaodb[i][j][k].pmag=float(line[7:11].strip())
            except:
                starsaodb[i][j][k].pmag=99
            try:
                starsaodb[i][j][k].m=float(line[12:16])
            except:
                starsaodb[i][j][k].m=99
            starsaodb[i][j][k].sp=line[17:20]
            try:
                starsaodb[i][j][k].pmra=15*float(line[41:48])
            except:
                starsaodb[i][j][k].pmra=0
            try:
                starsaodb[i][j][k].pmdec=float(line[62:68])
            except:
                starsaodb[i][j][k].pmdec=0
            starsaodb[i][j][k].hd=line[21:27].strip()

            starsaodb[i][j][k].ra2000=(prvh+prvm/60+prvs/3600)
            if skl_sign!="-":
                starsaodb[i][j][k].dec2000=(sklg+sklm/60+skls/3600)
            else: starsaodb[i][j][k].dec2000=-(sklg+sklm/60+skls/3600)
            i=i+1
    f.close()
    #print("OK")
    #print()
    bhide.lift()
    hide()
    
    for i in range(0,24):
        for j in range(0,17):
            for k in range(0,len(starsaodb[i][j])):
                if i>9: ii=str(i)
                else: ii="0"+str(i)
                if j>9: jj=str(j)
                else: jj="0"+str(j)
                tag="starsao"+ii+jj+str(k)
                callback_starsao = lambda event, tag=tag: starsao_rightclick(event,tag)
                canvas.tag_bind(tag,"<Button-3>", callback_starsao)
#===========================================                    
#ZAPOLN BAZY DSO1
f = open('dso1.dat', 'r')
print("dso1.dat"+" ... ",end="")
i=0
for line in f:
    if line[0] != "#" and line[0] != ";" and line.strip()!="":
        dso1db.append(dso1())
        spis=line.split(",")
        spis_nam=spis[8].split("/")                      
        dso1db[i].nam1=spis_nam[0]
        dso1db[i].prvh=int(spis[0])
        dso1db[i].prvm=int(spis[1])
        dso1db[i].prvs=float(spis[2])
        dso1db[i].skl_sign=spis[3]
        dso1db[i].sklg=int(spis[4])
        dso1db[i].sklm=int(spis[5])
        dso1db[i].skls=int(spis[6])
        dso1db[i].m=spis[7]
        dso1db[i].nam2=spis[8]
        dso1db[i].inf=spis[9]
        if len(spis)>=11:
            dso1db[i].br=spis[10]
        else: dso1db[i].br=""
        if len(spis)>=12 and spis[11]!="":
            dso1db[i].sz1=float(spis[11])
        else: dso1db[i].sz1=0
        if len(spis)>=13 and spis[12]!="":
            dso1db[i].sz2=float(spis[12])
        else: dso1db[i].sz2=0
        if len(spis)>=14 and spis[13]!="" and spis[13]!="\n":
            dso1db[i].angle=float(spis[13])
        else: dso1db[i].angle=0

        dso1db[i].ra2000=(dso1db[i].prvh+dso1db[i].prvm/60+dso1db[i].prvs/3600)
        if dso1db[i].skl_sign!="-":
            dso1db[i].dec2000=(dso1db[i].sklg+dso1db[i].sklm/60+dso1db[i].skls/3600)
        else: dso1db[i].dec2000=-(dso1db[i].sklg+dso1db[i].sklm/60+dso1db[i].skls/3600)
    i=i+1
f.close()
print("OK")
#===========================================    
#ZAPOLN BAZY DSO2
f = open('dso2.dat', 'r')
print("dso2.dat"+" ... ",end="")
i=0
for line in f:
    if line[0] != "#" and line[0] != ";" and line.strip()!="":
        dso2db.append(dso2())
        spis=line.split(",")
        spis_nam=spis[8].split("/")                      
        dso2db[i].nam1=spis_nam[0]
        dso2db[i].prvh=int(spis[0])
        dso2db[i].prvm=int(spis[1])
        dso2db[i].prvs=float(spis[2])
        dso2db[i].skl_sign=spis[3]
        dso2db[i].sklg=int(spis[4])
        dso2db[i].sklm=int(spis[5])
        dso2db[i].skls=int(spis[6])
        dso2db[i].m=spis[7]
        dso2db[i].nam2=spis[8]
        dso2db[i].inf=spis[9]
        if len(spis)>=11:
            dso2db[i].br=spis[10]
        else: dso2db[i].br=""
        if len(spis)>=12 and spis[11]!="":
            dso2db[i].sz1=float(spis[11])
        else: dso2db[i].sz1=0
        if len(spis)>=13 and spis[12]!="":
            dso2db[i].sz2=float(spis[12])
        else: dso2db[i].sz2=0
        if len(spis)>=14 and spis[13]!="" and spis[13]!="\n":
            dso2db[i].angle=float(spis[13])
        else: dso2db[i].angle=0

        dso2db[i].ra2000=(dso2db[i].prvh+dso2db[i].prvm/60+dso2db[i].prvs/3600)
        if dso2db[i].skl_sign!="-":
            dso2db[i].dec2000=(dso2db[i].sklg+dso2db[i].sklm/60+dso2db[i].skls/3600)
        else: dso2db[i].dec2000=-(dso2db[i].sklg+dso2db[i].sklm/60+dso2db[i].skls/3600)
    i=i+1
f.close()
print("OK")
#===================================
#ZAPOLN SPISKA KOORDINAT LINIY SOZWEZDIY
f = open('ConstLCoord.dat', 'r')
print("ConstLCoord.dat"+" ... ",end="")
for line in f:
    if line[0] != "#" and line[0] != ";" and line.strip()!="":
        clkoord.append(line)
f.close()
print("OK")
#======================================
#ZAPOLN SPISKA KOORDINAT GRANIC SOZWEZDIY
f = open('constb.dat', 'r')
print("constb.dat"+" ... ",end="")
for line in f:
    if line[0] != "#" and line[0] != ";" and line.strip()!="":
        constbun.append(line)
f.close()
print("OK")
print("===============================================================================")
#======================================

#RASCET PROEKCIY ORT PRIAMOUG KOORDINAT
def calcxyzpolm(prv,skl,prv1,m,kp):
    if skl>=90:skl=89.99999999
    elif skl<=-90:skl=-89.99999999

    if prv==6:prv=5.99999999
    elif prv==18:prv=17.99999999

    if prv1==6:prv1=5.99999999
    elif prv1==18:prv1=17.99999999

    sin_ugol1=sin(pid2-skl*pid180)
    ugol2=-prv1*15*pid180+(pid2)+prv*15*pid180
    x=m*kp*RADIUS*sin_ugol1*cos(ugol2)
    y=m*RADIUS*sin_ugol1*sin(ugol2)
    z=m*RADIUS*sin(skl*pid180)
    return(x,y,z)
#===========================

#Povorot sferi
def povorot(x,y,z,TURN_ANGLE):
    xx=MPOV[0]*x+MPOV[1]*y+MPOV[2]*z
    yy=MPOV[3]*x+MPOV[4]*y+MPOV[5]*z
    zz=MPOV[6]*x+MPOV[7]*y+MPOV[8]*z
    
    if xx==0:xx=0.00001;
    prvt=d180pi*(atan2(yy,xx)-pid2-TURN_ANGLE)/15
                
    sklt=-d180pi*(-pid2+acos(zz/sqrt(xx*xx+yy*yy+zz*zz)))
    return(prvt,sklt,zz)
#=========================
#RASCET KON KOORDINAT
def calcxycon(prv,skl,m):
    if sin(skl*pid180)==-1:skl=skl+0.00001
    x=m*RCANVD2+m*RADIUS * cos(pid2+prv*15*pid180) * cos(skl*pid180) / (sin(skl*pid180) + 1)
    y=m*RCANVD2+m*RADIUS * sin(pid2+prv*15*pid180) * cos(skl*pid180) / (sin(skl*pid180) + 1)
    return(x,y)
#===========================

#Gradusy c dolyami w grad min sec
def grms(hhh,ggg):
    signh=""; signg=""
    g1=abs(hhh)
    g=int(g1)
    g1=(g1-g)*60
    m=int(g1)
    s=(g1-m)*60

    if hhh<0: signh="-"
    
    s=round(s,1)
    if s==60: m=m+1; s=0
    if m==60: g=g+1; m=0
    if g==24: g=g-24
    if g==0 and m==0 and s==0: signh=""

    strgradh=signh+str(g)+"h "+str(m)+"m "+str(s)+"s"

    g1=abs(ggg)
    g=int(g1)
    g1=(g1-g)*60
    m=int(g1)
    s=(g1-m)*60
    
    if ggg<0: signg="-"
    
    s=round(s)
    if s==60: m=m+1; s=0
    if m==60: g=g+1; m=0
    if g==0 and m==0 and s==0: signg=""
    
    strgradg=signg+str(g)+"d "+str(m)+"m "+str(s)+"s"
    return(strgradh,strgradg)    

#=================================================================================================
#calc precess matrix
def pmatequ(t2,t1):
    dt=t2-t1
    zeta=((2306.2181+(1.39656-0.000139*t1)*t1)+((0.30188-0.000345*t1)+0.017998*dt)*dt)*dt/3600
    z=zeta+((0.79280+0.000411*t1)+0.000205*dt)*dt*dt/3600
    theta=((2004.3109-(0.85330+0.000217*t1)*t1)-((0.42665+0.000217*t1)+0.041833*dt)*dt)*dt/3600
    c1=cos(z*pid180);c2=cos(theta*pid180);c3=cos(zeta*pid180)
    s1=sin(z*pid180);s2=sin(theta*pid180);s3=sin(zeta*pid180)
    pmat=[]
    for jj in range(0,9):pmat.append([])
    pmat[0]=-s1*s3+c1*c2*c3;pmat[1]=-s1*c3-c1*c2*s3;pmat[2]=-c1*s2
    pmat[3]=c1*s3+s1*c2*c3; pmat[4]=c1*c3-s1*c2*s3; pmat[5]=-s1*s2
    pmat[6]=s2*c3;          pmat[7]=-s2*s3;         pmat[8]=c2
    return(pmat)
#=================================================================================================
#calc ECLIPTIC
def calcecl(d):
    eps = pid180*(23.4393 - 3.563E-7 * d)
    coseps=cos(eps)
    sineps=sin(eps)
    jde=d+2451543.5
    T=(jde-2451545)/36525
    L_=pid180*(218.3164477+481267.88123421*T-0.0015786*T*T+T**3/538841-T**4/65194000)
    OME=pid180*(125.04452-1934.136261*T+0.0020708*T*T+T**3/450000)
    L=pid180*(280.4665+36000.7698*T)
    dpsi=pid180/3600*(-17.20*sin(pid180*OME)-1.32*sin(pid180*2*L)-0.23*sin(pid180*2*L_)+0.21*sin(pid180*2*OME))
    deps=pid180/3600*(9.20*cos(pid180*OME)+0.57*cos(pid180*2*L)+0.1*cos(pid180*2*L_)-0.09*cos(pid180*2*OME))
    return(eps,coseps,sineps,dpsi,deps)
#=================================================================================================
#calc topocenrtic ra dec dist
def radectc(kpol,ragc,decgc,rgc,mylat,mylon,lmst):
    #calc tc distance
    x1,y1,z1=calcxyzpolm(ragc,decgc,lmst,ZOOM,kpol)
    x2,y2,z2=calcxyzpolm(lmst,mylat*kpol,lmst,ZOOM,kpol)
    modvekt=sqrt(x1*x1+y1*y1+z1*z1)
    cosalp=(x1*x2+y1*y2+z1*z2)/(modvekt*modvekt)
    rtc=sqrt(re*re+rgc*rgc-2*6371*rgc*cosalp)
    
    par = asin( 6371/rtc )
    gclat = kpol*mylat*pid180 - 0.1924*pid180 * sin(pid180*2*kpol*mylat)
    rho = 0.99833 + 0.00167 * cos(pid180*2*kpol*mylat)
    HA = pid180*15*pvminus(lmst,ragc)
    gu = atan2( tan(gclat) , cos(HA) )
    ratc   = pvminus(ragc, (par * rho * cos(gclat) * sin(HA) / cos(decgc*pid180))*d180pi/15)
    if gclat==0: ratc,dectc=sklplus(ratc,decgc,-d180pi*par * rho * sin(-decgc*pid180) * cos(HA)) 
    else: ratc,dectc=sklplus(ratc,decgc,-d180pi*par * rho * sin(gclat) * sin(gu - pid180*decgc) / sin(gu)) 
    return(ratc,dectc,rtc)
#=================================================================================================
def nutapl(pv,sk,dpsi,deps):
    if abs(sk)<85:
        cosalp=cos(pid180*pv); sinalp=sin(pid180*pv); tandel=tan(pid180*sk)
        dpvnut=d180pi/15*((COSEPS+SINEPS*sinalp*tandel)*dpsi-(cosalp*tandel)*deps)
        dsknut=d180pi*(SINEPS*cosalp*dpsi+sinalp*deps)
        pv_=pvplus(pv,dpvnut)
        pv_,sk_=sklplus(pv_,sk,dsknut)
    else: pv_=pv; sk_=sk
    return(pv_,sk_)

#=================================================================================================
def ekvtoconst1875(ra,dec):
    def step35(i):
        const=""
        while RAU1875[i]<=ra:
            i=i+1
        while RAL1875[i]>=ra:
            i=i+1
        if RAU1875[i]>ra:
            const=CONST1875[i]
        return(i,const)
               
    i=0; const=""
    while DECL1875[i]>=dec:
        i=i+1
    while const=="":
        i,const=step35(i)
    return(const)
#=================================================================================================
def ssystem(d,deltad,lmst,rcalc,objnum):
    global TABLEPLNAME,TABLEALT,EPS,COSEPS,SINEPS,LSUN
    TABLEPLNAME=[];TABLEALT=[]
    yy_,mm_,dd_,hh_=jdtodate(d-DELTAT/86400+2451543.5+DELTAHOURS/24)
    tracktext=(str(dd_)+"."+str(mm_)+"."+str(yy_)).ljust(11)
    dyplab=12; dxtrlab=37  #rasstoyanie text lab planet i lab track planet
    #d = deltad+367*year - int(7 * ( year + int((month+9)/12) ) / 4) + int(275*(month/9)) + day - 730530 + hour/24
    EPS,COSEPS,SINEPS,dpsi,deps=calcecl(d)

    if deltad==0 and NOPAINT==0:
        for i in range(0,10):
            planetdb[i].str1=""
            planetdb[i].str2=""
            planetdb[i].str3=""
            planetdb[i].str4=""
            planetdb[i].x=0
            planetdb[i].y=0

    Mjup=pid180*( 19.8950 + 0.0830853001 * d); Msat=pid180*(316.9670 + 0.0334442282 * d); Mur=pid180*(142.5905 + 0.011725806 * d)

    if NOPRINT==0:print()
    
    #=======Sun
    plname="Sun"
    plnum=0
    diam=1.392E9 #diametr Sun v metrax
    if NOPAINT==1:
        N = 0.0
        i = 0.0
        w = pid180*(282.9404 + 4.70935E-5 * d)
        a = 1.000000
        e = 0.016709 - 1.151E-9 * d
        M = pid180*(356.0470 + 0.9856002585 * d)
     
        
        Msun=M;wsun=w

        E_ = M + e * sin(M) * ( 1.0 + e * cos(M) )
        xv = cos(E_) - e
        yv = sqrt(1.0 - e*e) * sin(E_)

        r = sqrt( xv*xv + yv*yv )    
     
        v = atan2( yv, xv )
        lonsun = v + w 

        LSUN=M+w

        xs = r * cos(lonsun)
        ys = r * sin(lonsun) 

        xe = xs
        ye = ys * COSEPS
        ze = ys * SINEPS

        rsun=r  #rasstoyanie au
        rasun  = d180pi/15*atan2( ye, xe )
        if rasun<0:rasun=rasun+24
        decsun = d180pi*atan2( ze, sqrt(xe*xe+ye*ye) )

    else:
        jde=d+2451543.5
        t=(jde-2451545)/365250
        lonecl,latecl,rsun=lonlatr(plnum,t)
        tau=0.0057755183*rsun
        jde=jde-tau
        t=(jde-2451545)/365250
        lonecl,latecl,rsun=lonlatr(plnum,t)
        loneclgc=lonecl+pi+dpsi
        lateclgc=-latecl

        LSUN=loneclgc
        lonsun=loneclgc

        eps=EPS+deps
        coseps=cos(eps); sineps=sin(eps)

        rasun=d180pi*(atan2(sin(loneclgc)*coseps-tan(lateclgc)*sineps,cos(loneclgc)))/15
        if rasun<0: rasun=rasun+24
        if rasun>=24: rasun=rasun-24
        decsun=d180pi*asin(sin(lateclgc)*coseps+cos(lateclgc)*sineps*sin(loneclgc))        
        
    dpl=d180pi*2*atan((diam/2)/(rsun*AU))#Dpl grad
    
    if deltad==0: planetdb[plnum].ra=rasun; planetdb[plnum].dec=decsun;
    az,alt=calcaz(rasun,decsun,lmst)
    TABLEPLNAME.append(plname);TABLEALT.append(alt+0.583+dpl/2)

    strfind=zamenan(" ",efind.get().strip().lower())

    if NOPAINT==0:
        plname_=zamenan(" ",plname.strip().lower())
        if DELTAD==0 or (DELTAD!=0 and plname_.find(strfind)!=-1):
            if deltad==0:strtag="planet0"
            else:strtag="ddplanet0"
            x,y,rokr,ugv=ovalekv("Sun",rasun,decsun,dpl,0,"yellow","yellow",1,strtag)
            linexy(x-1.3*rokr,y-1.3*rokr,x+1.3*rokr,y+1.3*rokr,1,"yellow",strtag)
            linexy(x+1.3*rokr,y-1.3*rokr,x-1.3*rokr,y+1.3*rokr,1,"yellow",strtag)
            linexy(x,y-1.8*rokr,x,y+1.8*rokr,1,"yellow",strtag)
            linexy(x+1.8*rokr,y,x-1.8*rokr,y,1,"yellow",strtag)
            if DELTAD==0 and ZOOM<=2: stext(x,y,0,-1.8*rokr-dyplab,plname,planettextcolor,font1,strtag)
            if deltad!=0 and plname_.find(strfind)!=-1 and ctrackvar.get()==1:
                stext(x,y,1.8*rokr+dxtrlab,0,tracktext,planettextcolor,font1,"tracktext")


    if NOPRINT==0:
        rastr,decstr=grms(rasun,decsun)
        print("Sun:")
        print("RA="+rastr+" DEC="+decstr+" DIST="+str(round(rsun,4))+"au"+" DIAM="+str(round(dpl*60,1))+"'")
        print("AZ="+str(round(az,2))+"d"+" ALT="+str(round(alt,2))+"d")
 
    plnum=0
    
    if deltad==0 and NOPAINT==0:
        rastr,decstr=grms(rasun,decsun)
        planetdb[plnum].str1="Sun:"
        planetdb[plnum].str2="RA="+rastr+" DEC="+decstr+" DIST="+str(round(rsun,4))+"au"+" DIAM="+str(round(dpl*60,1))+"'"
        planetdb[plnum].str3="AZ="+str(round(az,2))+"d"+" ALT="+str(round(alt,2))+"d"
        planetdb[plnum].x=x
        planetdb[plnum].y=y

    if NOPRINT==0:print()

    #======Moon 
    if rcalc=="all" or (rcalc=="p" and (objnum==1 or objnum==-1)):
        N = pid180*(125.1228 - 0.0529538083 * d)
        i = pid180*5.1454
        w = pid180*(318.0634 + 0.1643573223 * d)
        a = 60.2666                       #(Earth radii)
        e = 0.054900
        M = pid180*(115.3654 + 13.0649929509 * d)

        plname="Moon"
        plnum=1

        if NOPAINT==0: moon_ra,moon_dec,rmoongc,lonmoon=moon_jm(d,dpsi,deps)
        else: moon_ra,moon_dec,rmoongc,lonmoon=calcmoon(plname,N,i,w,a,e,M,d,lonsun,rsun,Msun,wsun) 
                
        def angleto_0_2pi(angle):
            n=int(angle/pi2)
            angle=angle-n*pi2
            if angle<0: angle=angle+pi2
            return(angle)

        lonmoon=angleto_0_2pi(lonmoon)
        lonsun=angleto_0_2pi(lonsun)
        fmoon=(1-cos(lonmoon-lonsun))/2
        deltalon=lonsun-lonmoon
        deltalon=angleto_0_2pi(deltalon)
        if deltalon>=pi:fmoons="+"
        else: fmoons="-"

        # calc popravki za parallaks
        rmoongc=rmoongc*6371
        moon_ratc,moon_dectc,dist_tc=radectc(KPOL,moon_ra,moon_dec,rmoongc,MYLAT,MYLON,lmst)
        mpar = asin( 6371/dist_tc )
        
        radmoon=1738.14 #radius moon
        ugldmoon=2*asin(radmoon/(dist_tc))
        if deltad==0: planetdb[plnum].ra=moon_ratc; planetdb[plnum].dec=moon_dectc;
        az,alt=calcaz(moon_ratc,moon_dectc,lmst)
        TABLEPLNAME.append(plname);TABLEALT.append(alt+0.583+ugldmoon/2*d180pi)
        if NOPRINT==0:
            print("Moon:")
            rastr,decstr=grms(moon_ra,moon_dec)
            print("RAgc="+rastr+" DECgc="+decstr+" DISTgc="+str(round(rmoongc))+"km")
            rastr,decstr=grms(moon_ratc,moon_dectc)
            print("RAtc="+rastr+" DECtc="+decstr+" DISTtc="+str(round(dist_tc))+"km")
            print("AZ="+str(round(az,2))+"d"+" ALT="+str(round(alt,2))+"d")           
            print("DIAM="+str(round(ugldmoon*d180pi*60,2))+"'")
            print("PHASE="+fmoons+str(round(fmoon,2)))

        if deltad==0 and NOPAINT==0:
            rastrtc,decstrtc=grms(moon_ratc,moon_dectc)
            rastrgc,decstrgc=grms(moon_ra,moon_dec)
            planetdb[plnum].str1="Moon:"
            planetdb[plnum].str2="RAgc="+rastrgc+" DECgc="+decstrgc+" DISTgc="+str(round(rmoongc))+"km"
            planetdb[plnum].str3="RAtc="+rastrtc+" DECtc="+decstrtc+" DISTtc="+str(round(dist_tc))+"km"+" DIAM="+str(round(ugldmoon*d180pi*60,2))+"'"
            planetdb[plnum].str4="AZ="+str(round(az,2))+"d"+" ALT="+str(round(alt,2))+"d"+" PHASE="+fmoons+str(round(fmoon,2))

        ra_srad=rasun*15*pid180; ra_mrad=moon_ra*15*pid180
        dec_srad=decsun*pid180; dec_mrad=moon_dec*pid180;

        yy=cos(dec_srad)*sin(ra_srad-ra_mrad)
        #xx=cos(dec_mrad)*sin(dec_mrad)-sin(dec_srad)*cos(dec_srad)*cos(ra_srad-ra_mrad)
        xx=cos(dec_mrad)*sin(dec_srad)-sin(dec_mrad)*cos(dec_srad)*cos(ra_srad-ra_mrad)
        xi=atan2(yy,xx)

        if NOPAINT==0:
            plname_=zamenan(" ",plname.strip().lower())
            if DELTAD==0 or (DELTAD!=0 and plname_.find(strfind)!=-1):
                if deltad==0:strtag="planet1"
                else:strtag="ddplanet1"
                x,y,rokr,ugv=ovalekv("Moon",moon_ratc,moon_dectc,ugldmoon*d180pi,0,"gray","gray",1,strtag)
                #faza(x,y,int(rokr),fmoon,pid2+ugv+xi,"white",strtag) #risovanie Faza luni
                faza(x,y,int(rokr),fmoon,-pid2+ugv-xi,"white",strtag) #risovanie Faza luni 
                if deltad==0:
                    planetdb[plnum].x=x
                    planetdb[plnum].y=y
                textmoon=text="Moon "+fmoons+str(round(fmoon,2))
                if deltad==0:stext(x,y,0,-rokr-dyplab,textmoon,planettextcolor,font1,strtag)#canvas.create_text(x,(y-m*12/2)-10,text=textmoon,fill=textcolor)
                if deltad!=0 and plname_.find(strfind)!=-1 and ctrackvar.get()==1:
                    stext(x,y,rokr+dxtrlab,0,tracktext,planettextcolor,font1,"tracktext")
                if deltad!=0 and plname_.find(strfind)!=-1:
                    yystr=str(yy_).rjust(4,"0"); mmstr=str(mm_).rjust(2,"0"); ddstr=str(dd_).rjust(2,"0")

                    ra1875,dec1875=ekvtoekv1875(moon_ratc,moon_dectc)
                    const=ekvtoconst1875(ra1875,dec1875)
                    print("Moon: "+ddstr+"."+mmstr+"."+yystr+" PHASE="+fmoons+str(round(fmoon,2))+" in "+const)
                    print()
                          
        #==========shadow of the Earth
        if deltad==0 and NOPAINT==0:
            Rpt=mpar+0.27*pid180
            Rt=mpar-0.27*pid180
            rashad=pvplus(rasun,12)
            decshad=-decsun
            rashad_tc,decshad_tc,dist_tc=radectc(KPOL,rashad,decshad,rmoongc,MYLAT,MYLON,lmst)
       
            if abs(fmoon)>=0.9:
                x,y,rokr,ugv=ovalekv("Eshad",rashad_tc,decshad_tc,Rpt*2*d180pi,0,"plum",0,1,"eshadow")
                x,y,rokr,ugv=ovalekv("Eshad",rashad_tc,decshad_tc,Rt*2*d180pi,0,"plum",0,1,"eshadow")

        if NOPRINT==0:print()
        if NOPRINT==0:print("Planets:")

    #=======Mercury
    if rcalc=="all" or (rcalc=="p" and (objnum==2 or objnum==-1)):
        N = pid180* ( 48.3313 + 3.24587E-5 * d)
        i = pid180* (7.0047 + 5.00E-8 * d)
        w = pid180* ( 29.1241 + 1.01444E-5 * d)
        a = 0.387098
        e = 0.205635 + 5.59E-10 * d
        M = pid180* (168.6562 + 4.0923344368 * d)
        Af=1.918E-6
        diam=2*2439700
        plname="Mercury"
        plnum=2
        if NOPAINT==0: rapl,decpl,rpl,ugld,phase,m_=planet_jm(plname,d,deltad,lmst,diam,lonsun,rsun,Af,plnum,dpsi,deps)
        else: rapl,decpl,rpl,ugld,phase,m_=calcplanet(plname,N,i,w,a,e,M,d,deltad,lmst,diam,lonsun,rsun,Mjup,Msat,Mur,Af,plnum)

        if NOPAINT==0:
            plname_=zamenan(" ",plname.strip().lower())
            if DELTAD==0 or (DELTAD!=0 and plname_.find(strfind)!=-1):
                if deltad==0:strtag="planet2"
                else:strtag="ddplanet2"
                if ZOOM>=ZOOMPLANET: ugld_=ugld
                else: ugld_=0 #razmer po blesku
                x,y,rokr,ugv=ovalekv(plname,rapl,decpl,ugld_,m_,"darkgoldenrod","darkgoldenrod",1,strtag)
                if deltad==0:
                    planetdb[plnum].x=x
                    planetdb[plnum].y=y
                ra_plrad=rapl*15*pid180
                dec_plrad=decpl*pid180;
                yy=cos(dec_srad)*sin(ra_srad-ra_plrad)
                #xx=cos(dec_plrad)*sin(dec_plrad)-sin(dec_srad)*cos(dec_srad)*cos(ra_srad-ra_plrad)
                xx=cos(dec_plrad)*sin(dec_srad)-sin(dec_plrad)*cos(dec_srad)*cos(ra_srad-ra_plrad)
                xi=atan2(yy,xx)
                #faza(x,y,int(rokr),phase,pid2+ugv+xi,"white",strtag) #risovanie Fazy
                faza(x,y,int(rokr),phase,-pid2+ugv-xi,"white",strtag) #risovanie Fazy

                if deltad==0:stext(x,y,0,-rokr-dyplab,plname,planettextcolor,font1,strtag)#canvas.create_text(x,(y-m*10/2)-10,text=plname,fill=textcolor)
                if deltad!=0 and plname_.find(strfind)!=-1 and ctrackvar.get()==1:
                    stext(x,y,rokr+dxtrlab,0,tracktext,planettextcolor,font1,"tracktext")

    #=======Venus
    if rcalc=="all" or (rcalc=="p" and (objnum==3 or objnum==-1)):
        N = pid180* (76.6799 + 2.46590E-5 * d)
        i = pid180*(3.3946 + 2.75E-8 * d)
        w = pid180*(54.8910 + 1.38374E-5 * d)
        a = 0.723330
        e = 0.006773 - 1.302E-9 * d
        M = pid180*(48.0052 + 1.6021302244 * d)
        Af=1.721E-5
        diam=2*6051800
        plname="Venus"
        plnum=3
       
        if NOPAINT==0: rapl,decpl,rpl,ugld,phase,m_=planet_jm(plname,d,deltad,lmst,diam,lonsun,rsun,Af,plnum,dpsi,deps)
        else: rapl,decpl,rpl,ugld,phase,m_=calcplanet(plname,N,i,w,a,e,M,d,deltad,lmst,diam,lonsun,rsun,Mjup,Msat,Mur,Af,plnum)

        if NOPAINT==0:
            plname_=zamenan(" ",plname.strip().lower())
            if DELTAD==0 or (DELTAD!=0 and plname_.find(strfind)!=-1):
                if deltad==0:strtag="planet3"
                else:strtag="ddplanet3"
                if ZOOM>=ZOOMPLANET: ugld_=ugld
                else: ugld_=0 #razmer po blesku
                x,y,rokr,ugv=ovalekv(plname,rapl,decpl,ugld_,m_,"darkgoldenrod","darkgoldenrod",1,strtag)
                if deltad==0:
                    planetdb[plnum].x=x
                    planetdb[plnum].y=y
                ra_plrad=rapl*15*pid180
                dec_plrad=decpl*pid180;
                yy=cos(dec_srad)*sin(ra_srad-ra_plrad)
                #xx=cos(dec_plrad)*sin(dec_plrad)-sin(dec_srad)*cos(dec_srad)*cos(ra_srad-ra_plrad)
                xx=cos(dec_plrad)*sin(dec_srad)-sin(dec_plrad)*cos(dec_srad)*cos(ra_srad-ra_plrad)
                xi=atan2(yy,xx)
                #faza(x,y,int(rokr),phase,pid2+ugv+xi,"white",strtag) #risovanie Fazy
                faza(x,y,int(rokr),phase,-pid2+ugv-xi,"white",strtag) #risovanie Fazy

                if deltad==0:stext(x,y,0,-rokr-dyplab,plname,planettextcolor,font1,strtag)#canvas.create_text(x,(y-m*10/2)-10,text=plname,fill=textcolor)
                if deltad!=0 and plname_.find(strfind)!=-1 and ctrackvar.get()==1:
                    stext(x,y,rokr+dxtrlab,0,tracktext,planettextcolor,font1,"tracktext")

    #=======Mars
    if rcalc=="all" or (rcalc=="p" and (objnum==4 or objnum==-1)):
        N = pid180*( 49.5574 + 2.11081E-5 * d)
        i = pid180*(1.8497 - 1.78E-8 * d)
        w = pid180*(286.5016 + 2.92961E-5 * d)
        a = 1.523688
        e = 0.093405 + 2.516E-9 * d
        M = pid180*( 18.6021 + 0.5240207766 * d)
        Af=4.539E-6
        diam=2*3389500 
        plname="Mars"
        plnum=4
        
        if NOPAINT==0: rapl,decpl,rpl,ugld,phase,m_=planet_jm(plname,d,deltad,lmst,diam,lonsun,rsun,Af,plnum,dpsi,deps)
        else: rapl,decpl,rpl,ugld,phase,m_=calcplanet(plname,N,i,w,a,e,M,d,deltad,lmst,diam,lonsun,rsun,Mjup,Msat,Mur,Af,plnum)

        if NOPAINT==0:
            plname_=zamenan(" ",plname.strip().lower())
            if DELTAD==0 or (DELTAD!=0 and plname_.find(strfind)!=-1):
                if deltad==0:strtag="planet4"
                else:strtag="ddplanet4"
                if ZOOM>=ZOOMPLANET: ugld_=ugld
                else: ugld_=0 #razmer po blesku
                x,y,rokr,ugv=ovalekv(plname,rapl,decpl,ugld_,m_,"orangered","orangered",1,strtag)
                if deltad==0:
                    planetdb[plnum].x=x
                    planetdb[plnum].y=y
                    stext(x,y,0,-rokr-dyplab,plname,planettextcolor,font1,strtag)#canvas.create_text(x,(y-m*10/2)-10,text=plname,fill=textcolor)
                if deltad!=0 and plname_.find(strfind)!=-1 and ctrackvar.get()==1:
                    stext(x,y,rokr+dxtrlab,0,tracktext,planettextcolor,font1,"tracktext")

    #=======Jupiter
    if rcalc=="all" or (rcalc=="p" and (objnum==5 or objnum==-1)):
        N = pid180*( 100.4542 + 2.76854E-5 * d)
        i = pid180*( 1.3030 - 1.557E-7 * d)
        w = pid180*( 273.8777 + 1.64505E-5 * d)
        a = 5.20256
        e = 0.048498 + 4.469E-9 * d
        M = pid180*(  19.8950 + 0.0830853001 * d)
        Af=1.994E-4
        diam=2*69911000
        plname="Jupiter"
        plnum=5

        if NOPAINT==0: rapl,decpl,rpl,ugld,phase,m_=planet_jm(plname,d,deltad,lmst,diam,lonsun,rsun,Af,plnum,dpsi,deps)
        else: rapl,decpl,rpl,ugld,phase,m_=calcplanet(plname,N,i,w,a,e,M,d,deltad,lmst,diam,lonsun,rsun,Mjup,Msat,Mur,Af,plnum)

        if NOPAINT==0:
            plname_=zamenan(" ",plname.strip().lower())
            if DELTAD==0 or (DELTAD!=0 and plname_.find(strfind)!=-1):
                if deltad==0:strtag="planet5"
                else:strtag="ddplanet5"
                if ZOOM>=ZOOMPLANET: ugld_=ugld
                else: ugld_=0 #razmer po blesku
                x,y,rokr,ugv=ovalekv(plname,rapl,decpl,ugld_,m_,"khaki","khaki",1,strtag)
                for i in range(0,len(jsatdb)):
                    jsatdb[i].x=x; jsatdb[i].y=y

                if deltad==0 and ZOOM>=ZOOMPLANET and rokr>2:
                    t1=(d+2451543.5-2433282.5)/36525
                    alp0=(268+0.1061*t1)*pid180
                    del0=(64.5-0.0164*t1)*pid180
                    alp_=rapl*15*pid180; del_=decpl*pid180
                    yy=cos(del0)*sin(alp0-alp_)
                    xx=sin(del0)*cos(del_)-cos(del0)*sin(del_)*cos(alp0-alp_)
                    Pj=atan2(yy,xx)
                    for i in range(0,len(jsatdb)):
                        satpaint(plname,i,x,y,rokr*jsatdb[i].dx,rokr*jsatdb[i].dy,-Pj+pid2+ugv,2,"khaki","jsat"+str(i))
                
                if deltad==0:
                    planetdb[plnum].x=x
                    planetdb[plnum].y=y
                    stext(x,y,0,-rokr-dyplab,plname,planettextcolor,font1,strtag)#canvas.create_text(x,(y-m*10/2)-10,text=plname,fill=textcolor)
                if deltad!=0 and plname_.find(strfind)!=-1 and ctrackvar.get()==1:
                    stext(x,y,rokr+dxtrlab,0,tracktext,planettextcolor,font1,"tracktext")

    #=======Saturn
    if rcalc=="all" or (rcalc=="p" and (objnum==6 or objnum==-1)):
        N = pid180*(113.6634 + 2.38980E-5 * d)
        i = pid180*(2.4886 - 1.081E-7 * d)
        w = pid180*(339.3939 + 2.97661E-5 * d)
        a = 9.55475
        e = 0.055546 - 9.499E-9 * d
        M = pid180*(316.9670 + 0.0334442282 * d)
        Af=1.740E-4
        diam=2*58232000
        plname="Saturn"
        plnum=6

        if NOPAINT==0: rapl,decpl,rpl,ugld,phase,m_=planet_jm(plname,d,deltad,lmst,diam,lonsun,rsun,Af,plnum,dpsi,deps)
        else: rapl,decpl,rpl,ugld,phase,m_=calcplanet(plname,N,i,w,a,e,M,d,deltad,lmst,diam,lonsun,rsun,Mjup,Msat,Mur,Af,plnum)

        if NOPAINT==0:
            plname_=zamenan(" ",plname.strip().lower())
            if DELTAD==0 or (DELTAD!=0 and plname_.find(strfind)!=-1):
                if deltad==0:strtag="planet6"
                else:strtag="ddplanet6"
                if ZOOM>=ZOOMPLANET: ugld_=ugld
                else: ugld_=0 #razmer po blesku
                x,y,rokr,ugv=ovalekv(plname,rapl,decpl,ugld_,m_,planetcolor,planetcolor,1,strtag)
                for i in range(0,len(ssatdb)):
                    ssatdb[i].x=x; ssatdb[i].y=y

                if deltad==0 and ZOOM>=ZOOMPLANET and rokr>2:
                    for i in range(0,len(ssatdb)):
                        width=1
                        if i==5: width=2
                        satpaint(plname,i,x,y,rokr*ssatdb[i].dx,rokr*ssatdb[i].dy,-sring.pa+pid2+ugv,width,planetcolor,"ssat"+str(i))
                    
                if ZOOM>=ZOOMPLANET and rokr>2: ringsatpaint(x,y,int(rokr),ugv,planetcolor,strtag)
                if deltad==0:
                    planetdb[plnum].x=x
                    planetdb[plnum].y=y
                    stext(x,y,0,-rokr-dyplab,plname,planettextcolor,font1,strtag)#canvas.create_text(x,(y-m*10/2)-10,text=plname,fill=textcolor)
                if deltad!=0 and plname_.find(strfind)!=-1 and ctrackvar.get()==1:
                    stext(x,y,rokr+dxtrlab,0,tracktext,planettextcolor,font1,"tracktext")
    #=======Uranus
    if rcalc=="all" or (rcalc=="p" and (objnum==7 or objnum==-1)):
        N = pid180*( 74.0005 + 1.3978E-5 * d)
        i = pid180*(0.7733 + 1.9E-8 * d)
        w = pid180*( 96.6612 + 3.0565E-5 * d)
        a = 19.18171 - 1.55E-8 * d
        e = 0.047318 + 7.45E-9 * d
        M = pid180*(142.5905 + 0.011725806 * d)
        Af=7.768E-5
        diam=2*25362000 
        plname="Uranus"
        plnum=7

        if NOPAINT==0: rapl,decpl,rpl,ugld,phase,m_=planet_jm(plname,d,deltad,lmst,diam,lonsun,rsun,Af,plnum,dpsi,deps)
        else: rapl,decpl,rpl,ugld,phase,m_=calcplanet(plname,N,i,w,a,e,M,d,deltad,lmst,diam,lonsun,rsun,Mjup,Msat,Mur,Af,plnum)

        if NOPAINT==0:
            plname_=zamenan(" ",plname.strip().lower())
            if DELTAD==0 or (DELTAD!=0 and plname_.find(strfind)!=-1):
                if deltad==0:strtag="planet7"
                else:strtag="ddplanet7"
                if ZOOM>=ZOOMPLANET: ugld_=ugld
                else: ugld_=0 #razmer po blesku
                x,y,rokr,ugv=ovalekv(plname,rapl,decpl,ugld_,m_,"powderblue","powderblue",1,strtag)
                if deltad==0:
                    planetdb[plnum].x=x
                    planetdb[plnum].y=y
                    stext(x,y,0,-rokr-dyplab,plname,planettextcolor,font1,strtag)#canvas.create_text(x,(y-m*10/2)-10,text=plname,fill=textcolor)
                if deltad!=0 and plname_.find(strfind)!=-1 and ctrackvar.get()==1:
                    stext(x,y,rokr+dxtrlab,0,tracktext,planettextcolor,font1,"tracktext")
    #=======Neptune
    if rcalc=="all" or (rcalc=="p" and (objnum==8 or objnum==-1)):
        N = pid180*(131.7806 + 3.0173E-5 * d)
        i = pid180*(1.7700 - 2.55E-7 * d)
        w = pid180*(272.8461 - 6.027E-6 * d)
        a = 30.05826 + 3.313E-8 * d
        e = 0.008606 + 2.15E-9 * d
        M = pid180*(260.2471 + 0.005995147 * d)
        Af=7.597E-5
        diam=2*24622000
        plname="Neptune"
        plnum=8
        
        if NOPAINT==0: rapl,decpl,rpl,ugld,phase,m_=planet_jm(plname,d,deltad,lmst,diam,lonsun,rsun,Af,plnum,dpsi,deps)
        else: rapl,decpl,rpl,ugld,phase,m_=calcplanet(plname,N,i,w,a,e,M,d,deltad,lmst,diam,lonsun,rsun,Mjup,Msat,Mur,Af,plnum)

        if NOPAINT==0:
            plname_=zamenan(" ",plname.strip().lower())
            if DELTAD==0 or (DELTAD!=0 and plname_.find(strfind)!=-1):
                if deltad==0:strtag="planet8"
                else:strtag="ddplanet8"
                if ZOOM>=ZOOMPLANET: ugld_=ugld
                else: ugld_=0 #razmer po blesku
                x,y,rokr,ugv=ovalekv(plname,rapl,decpl,ugld_,m_,"royalblue","royalblue",1,strtag)
                if deltad==0:
                    planetdb[plnum].x=x
                    planetdb[plnum].y=y
                    stext(x,y,0,-rokr-dyplab,plname,planettextcolor,font1,strtag)#canvas.create_text(x,(y-m*10/2)-10,text=plname,fill=textcolor)
                if deltad!=0 and plname_.find(strfind)!=-1 and ctrackvar.get()==1:
                    stext(x,y,rokr+dxtrlab,0,tracktext,planettextcolor,font1,"tracktext")
    #=======Pluto
    if rcalc=="all" or (rcalc=="p" and (objnum==9 or objnum==-1)):
        J  = pid180*( 34.23  +  0.083091190 * d)
        S  = pid180*( 50.03  +  0.033459652 * d)
        P  = pid180*(238.95  +  0.003968789 * d)
        Af=4.073E-6
        diam=2*1187000
        plname="Pluto"
        plnum=9
        lonecl = pid180*(238.9508  +  0.00400703 * d)
        lonecl = lonecl - pid180*19.799 * sin(P)     + pid180*19.848 * cos(P)
        lonecl = lonecl +  pid180*0.897 * sin(2*P)   -  pid180*4.956 * cos(2*P)
        lonecl = lonecl +  pid180*0.610 * sin(3*P)   +  pid180*1.211 * cos(3*P)
        lonecl = lonecl -  pid180*0.341 * sin(4*P)   -  pid180*0.190 * cos(4*P)
        lonecl = lonecl +  pid180*0.128 * sin(5*P)   -  pid180*0.034 * cos(5*P)
        lonecl = lonecl -  pid180*0.038 * sin(6*P)   +  pid180*0.031 * cos(6*P)
        lonecl = lonecl +  pid180*0.020 * sin(S-P)   -  pid180*0.010 * cos(S-P)
        lonecl = lonecl -  pid180*0.004 * sin(S)     -  pid180*0.005 * cos(S)
        lonecl = lonecl -  pid180*0.006 * sin(S+P)   -  pid180*0.003 * cos(S+P)
        lonecl = lonecl +  pid180*0.007 * sin(J-P)   +  pid180*0.001 * cos(J-P)

        latecl = -pid180*3.9082
        latecl = latecl - pid180*5.453 * sin(P)      - pid180*14.975 * cos(P)
        latecl = latecl + pid180*3.527 * sin(2*P)    + pid180*1.673 * cos(2*P)
        latecl = latecl - pid180*1.051 * sin(3*P)    + pid180*0.328 * cos(3*P)
        latecl = latecl + pid180*0.179 * sin(4*P)    - pid180*0.292 * cos(4*P)
        latecl = latecl + pid180*0.019 * sin(5*P)    + pid180*0.100 * cos(5*P)
        latecl = latecl - pid180*0.031 * sin(6*P)    - pid180*0.026 * cos(6*P)
        latecl = latecl + pid180*0.005 * sin(S-P)    + pid180*0.011 * cos(S-P)
        
        r =  40.72
        r = r + 6.68 * sin(P)       + 6.90 * cos(P)
        r = r - 1.18 * sin(2*P)     - 0.03 * cos(2*P)
        r = r + 0.15 * sin(3*P)     - 0.14 * cos(3*P)
        r = r                       + 0.05 * cos(4*P)
        r = r - 0.01 * sin(5*P)     - 0.01 * cos(5*P)
        
        xh = r * cos(lonecl) * cos(latecl)
        yh = r * sin(lonecl) * cos(latecl)
        zh = r * sin(latecl) 

        xs = rsun * cos(lonsun)
        ys = rsun * sin(lonsun) 

        xg = xh + xs
        yg = yh + ys
        zg = zh 
        
        xe = xg
        ye = yg * COSEPS - zg * SINEPS
        ze = yg * SINEPS + zg * COSEPS

        rapl  = d180pi/15*atan2( ye, xe )
        if rapl<0:rapl=rapl+24
        decpl = d180pi*atan2( ze, sqrt(xe*xe+ye*ye) )
        if deltad==0: planetdb[plnum].ra=rapl; planetdb[plnum].dec=decpl;
        rapl,decpl=nutapl(rapl,decpl,dpsi,deps)

        rpl = sqrt(xg*xg+yg*yg+zg*zg)
        dpl=d180pi*2*atan((diam/2)/(rpl*AU))
        phase=1
        m_=5*log10(rpl*r/Af/sqrt(phase))-26.7    

        if NOPAINT==0:
            plname_=zamenan(" ",plname.strip().lower())
            if DELTAD==0 or (DELTAD!=0 and plname_.find(strfind)!=-1):
                if deltad==0:strtag="planet9"
                else:strtag="ddplanet9"
                if ZOOM>=ZOOMPLANET: ugld_=ugld
                else: ugld_=0 #razmer po blesku
                x,y,rokr,ugv=ovalekv(plname,rapl,decpl,ugld_,m_,planetcolor,planetcolor,1,strtag)
                if deltad==0:
                    planetdb[plnum].x=x
                    planetdb[plnum].y=y
                    stext(x,y,0,-rokr-dyplab,"Pluto",planettextcolor,font1,strtag)#canvas.create_text(x,(y-m*10/2)-10,text="Pluto",fill=textcolor)
                if deltad!=0 and plname_.find(strfind)!=-1 and ctrackvar.get()==1:
                    stext(x,y,rokr+dxtrlab,0,tracktext,planettextcolor,font1,"tracktext")
        az,alt=calcaz(rapl,decpl,lmst)
        TABLEPLNAME.append(plname);TABLEALT.append(alt+0.583)
        rastr,decstr=grms(rapl,decpl)
        if NOPRINT==0:
            print("Pluto   : RA="+rastr+" DEC="+decstr+" DIST="+str(round(rpl,4))+"au"+" DIAM="+str(round(dpl*3600,3))+'"')
            print("          AZ="+str(round(az,2))+"d"+" ALT="+str(round(alt,2))+"d"+" MAGN="+str(round(m_,2)))

        if deltad==0 and NOPAINT==0:
            rastr,decstr=grms(rapl,decpl)
            planetdb[plnum].str1=plname+":"
            planetdb[plnum].str2="RA="+rastr+" DEC="+decstr+" DIST="+str(round(rpl,4))+"au"+" DIAM="+str(round(dpl*3600,3))+'"'
            planetdb[plnum].str3="AZ="+str(round(az,2))+"d"+" ALT="+str(round(alt,2))+"d"+" MAGN="+str(round(m_,2))
#===================
    if NOPRINT==0:print()
    if rcalc=="all" or rcalc=="pa": calcasteroid(d,deltad,lmst,rsun,lonsun,dpsi,deps,MAGN_LIMIT,objnum)
    if NOPRINT==0:print()
    if rcalc=="all" or rcalc=="pc": calccomet(d,deltad,lmst,rsun,lonsun,dpsi,deps,MAGN_LIMIT,objnum)
    if NOPRINT==0:print()
#===========================================================================================================
#===============calc planets
def calcplanet(plname,N,i,w,a,e,M,d,deltad,lmst,diam,lonsun,rsun,Mjup,Msat,Mur,Af,plnum):
       
    E_ = M + e * sin(M) * ( 1.0 + e * cos(M) )
    E0=E_
    E1 = E0 - ( E0 - e * sin(E0) - M ) / ( 1 - e * cos(E0) )
    dE=1  
    while dE>0.0001*pid180:
        E1 = E0 - ( E0 - e * sin(E0) - M ) / ( 1 - e * cos(E0) )
        dE=abs(E0-E1); E0=E1
    E_=E1
    
    xv = a * ( cos(E_) - e )
    yv = a * ( sqrt(1.0 - e*e) * sin(E_) )

    r = sqrt( xv*xv + yv*yv )    
    v = atan2( yv, xv )

    xh = r * ( cos(N) * cos(v+w) - sin(N) * sin(v+w) * cos(i) )
    yh = r * ( sin(N) * cos(v+w) + cos(N) * sin(v+w) * cos(i) )
    zh = r * ( sin(v+w) * sin(i) )

    lonecl = atan2( yh, xh )
    if plname=="Jupiter":
        lonecl=lonecl-pid180*0.332 * sin(2*Mjup - 5*Msat - pid180*67.6)
        lonecl=lonecl-pid180*0.056 * sin(2*Mjup - 2*Msat + pid180*21) 
        lonecl=lonecl+pid180*0.042 * sin(3*Mjup - 5*Msat + pid180*21) 
        lonecl=lonecl-pid180*0.036 * sin(Mjup - 2*Msat)
        lonecl=lonecl+pid180*0.022 * cos(Mjup - Msat)
        lonecl=lonecl+pid180*0.023 * sin(2*Mjup - 3*Msat + pid180*52) 
        lonecl=lonecl-pid180*0.016 * sin(Mjup - 5*Msat - pid180*69) 
    if plname=="Saturn":
        lonecl=lonecl+pid180*0.812 * sin(2*Mjup - 5*Msat - pid180*67.6)
        lonecl=lonecl-pid180*0.229 * cos(2*Mjup - 4*Msat - pid180*2)
        lonecl=lonecl+pid180*0.119 * sin(Mjup - 2*Msat - pid180*3)
        lonecl=lonecl+pid180*0.046 * sin(2*Mjup - 6*Msat - pid180*69)
        lonecl=lonecl+pid180*0.014 * sin(Mjup - 3*Msat + pid180*32)
    if plname=="Uranus":
        lonecl=lonecl+pid180*0.040 * sin(Msat - 2*Mur + pid180*6)
        lonecl=lonecl+pid180*0.035 * sin(Msat - 3*Mur + pid180*33)
        lonecl=lonecl-pid180*0.015 * sin(Mjup - Mur + pid180*20)
         
    latecl = atan2( zh, sqrt(xh*xh+yh*yh) )
    if plname=="Saturn":
        latecl=latecl-pid180*0.020 * cos(2*Mjup - 4*Msat - pid180*2)
        latecl=latecl+pid180*0.018 * sin(2*Mjup - 6*Msat - pid180*49)
         
    xh = r * cos(lonecl) * cos(latecl)
    yh = r * sin(lonecl) * cos(latecl)
    zh = r * sin(latecl) 

    xs = rsun * cos(lonsun)
    ys = rsun * sin(lonsun) 

    xg = xh + xs
    yg = yh + ys
    zg = zh 
    
    xe = xg
    ye = yg * COSEPS - zg * SINEPS
    ze = yg * SINEPS + zg * COSEPS

    rapl  = d180pi/15*atan2( ye, xe )
    if rapl<0:rapl=rapl+24
    decpl = d180pi*atan2( ze, sqrt(xe*xe+ye*ye) )
    if deltad==0: planetdb[plnum].ra=rapl; planetdb[plnum].dec=decpl;
    az,alt=calcaz(rapl,decpl,lmst)
    TABLEPLNAME.append(plname);TABLEALT.append(alt+0.583)

    loneclgc = atan2( yg, xg )
    if lonecl<0:lonecl=lonecl+pi2
    if loneclgc<0:loneclgc=loneclgc+pi2
    phase=0.5*(1+cos(loneclgc-lonecl))
    if phase==0:phase=0.00001

    rpl = sqrt(xg*xg+yg*yg+zg*zg)

    lateclgc = asin(zg/rpl)
    if lateclgc<0:lateclgc=lateclgc+pi2
    
    m_=5*log10(rpl*r/Af/sqrt(phase))-26.7
    dpl=d180pi*2*atan((diam/2)/(rpl*AU))
    if plname=="Jupiter" and deltad==0 and NOPAINT==0:
        j_sat(d)
    if plname=="Saturn" and NOPAINT==0:
        s_ring(d,lateclgc,loneclgc,rapl,decpl)
        m_=m_+sring.ring_magn
        s_sat(d,rpl,lateclgc,loneclgc)
    rastr,decstr=grms(rapl,decpl)
    #print(plname,": RA=",rapl,"DEC=",decpl,"R=",round(rpl,4),"au")
    if NOPRINT==0:
        print(plname.ljust(7),": RA="+rastr+" DEC="+decstr+" DIST="+str(round(rpl,4))+"au"+" DIAM="+str(round(dpl*3600,1))+'"')
        if plname=="Mercury" or plname=="Venus" or plname=="Mars" or plname=="Jupiter":
            print("          AZ="+str(round(az,2))+"d"+" ALT="+str(round(alt,2))+"d"+" PHASE="+str(round(phase,2))+" MAGN="+str(round(m_,2)))
        else:
            print("          AZ="+str(round(az,2))+"d"+" ALT="+str(round(alt,2))+"d"+" MAGN="+str(round(m_,2)))

    if deltad==0 and NOPAINT==0:
        rastr,decstr=grms(rapl,decpl)
        planetdb[plnum].str1="planet "+plname+":"
        planetdb[plnum].str2="RA="+rastr+" DEC="+decstr+" DIST="+str(round(rpl,4))+"au"+" DIAM="+str(round(dpl*3600,1))+'"'
        if plname=="Mercury" or plname=="Venus" or plname=="Mars" or plname=="Jupiter":
            planetdb[plnum].str3="AZ="+str(round(az,2))+"d"+" ALT="+str(round(alt,2))+"d"+" PHASE="+str(round(phase,2))+" MAGN="+str(round(m_,2))
        else:
            planetdb[plnum].str3="AZ="+str(round(az,2))+"d"+" ALT="+str(round(alt,2))+"d"+" MAGN="+str(round(m_,2))
    return(rapl,decpl,rpl,dpl,phase,m_)
#==============================================
# For calc planets JM!!!
def lonlatr(plnum,t):
    Lsum=[]; Bsum=[]; Rsum=[]
    for lnum in range(0,len(TERMSL[plnum])):
        Lsum.append([]); Lsum[lnum]=0
        for i in range(0,len(TERMSL[plnum][lnum])):
            a=TERMSL[plnum][lnum][i][0]; b=TERMSL[plnum][lnum][i][1]; c=TERMSL[plnum][lnum][i][2]
            Lsum[lnum]=Lsum[lnum]+a*cos(b+c*t)
    L=0
    for lnum in range(0,len(Lsum)):
        L=L+Lsum[lnum]*(t**lnum)
    L=L/1E8

    for bnum in range(0,len(TERMSB[plnum])):
        Bsum.append([]); Bsum[bnum]=0
        for i in range(0,len(TERMSB[plnum][bnum])):
            a=TERMSB[plnum][bnum][i][0]; b=TERMSB[plnum][bnum][i][1]; c=TERMSB[plnum][bnum][i][2]
            Bsum[bnum]=Bsum[bnum]+a*cos(b+c*t)
    B=0
    for bnum in range(0,len(Bsum)):
        B=B+Bsum[bnum]*(t**bnum)
    B=B/1E8

    for rnum in range(0,len(TERMSR[plnum])):
        Rsum.append([]); Rsum[rnum]=0
        for i in range(0,len(TERMSR[plnum][rnum])):
            a=TERMSR[plnum][rnum][i][0]; b=TERMSR[plnum][rnum][i][1]; c=TERMSR[plnum][rnum][i][2]
            Rsum[rnum]=Rsum[rnum]+a*cos(b+c*t)
    R=0
    for rnum in range(0,len(Rsum)):
        R=R+Rsum[rnum]*(t**rnum)
    R=R/1E8
    return(L,B,R)
#============================
# Calc planets JM!!!
def planet_jm(plname,d,deltad,lmst,diam,lonsun,rsun,Af,plnum,dpsi,deps):
    def glc_to_gc(lonecl,latecl,r,rsun,lonsun,dpsi):
        xh = r * cos(lonecl) * cos(latecl)
        yh = r * sin(lonecl) * cos(latecl)
        zh = r * sin(latecl) 

        xs = rsun * cos(lonsun)
        ys = rsun * sin(lonsun) 

        xg = xh + xs
        yg = yh + ys
        zg = zh 
        rpl = sqrt(xg*xg+yg*yg+zg*zg)

        loneclgc = atan2( yg, xg )
        loneclgc=loneclgc+dpsi
        if loneclgc<0:loneclgc=loneclgc+pi2
        lateclgc = asin(zg/rpl)
        if lateclgc<0:lateclgc=lateclgc+pi2
        return(loneclgc,lateclgc,rpl)
    #=================
    jde=d+2451543.5
    t=(jde-2451545)/365250
    lonecl,latecl,r=lonlatr(plnum,t)
    loneclgc,lateclgc,rpl=glc_to_gc(lonecl,latecl,r,rsun,lonsun,dpsi)
    tau=0.0057755183*rpl
    jde=jde-tau
    t=(jde-2451545)/365250
    lonecl,latecl,r=lonlatr(plnum,t)
    loneclgc,lateclgc,rpl=glc_to_gc(lonecl,latecl,r,rsun,lonsun,dpsi)

    eps=EPS+deps
    coseps=cos(eps); sineps=sin(eps)

    rapl=d180pi*(atan2(sin(loneclgc)*coseps-tan(lateclgc)*sineps,cos(loneclgc)))/15
    if rapl<0: rapl=rapl+24
    if rapl>=24: rapl=rapl-24
    decpl=d180pi*asin(sin(lateclgc)*coseps+cos(lateclgc)*sineps*sin(loneclgc))

    if deltad==0: planetdb[plnum].ra=rapl; planetdb[plnum].dec=decpl;
    az,alt=calcaz(rapl,decpl,lmst)
    TABLEPLNAME.append(plname);TABLEALT.append(alt+0.583)

    phase=0.5*(1+cos(loneclgc-lonecl))
    if phase==0:phase=0.00001
    m_=5*log10(rpl*r/Af/sqrt(phase))-26.7
    dpl=d180pi*2*atan((diam/2)/(rpl*AU))
    if plname=="Jupiter" and deltad==0 and NOPAINT==0:
        j_sat(d)
    if plname=="Saturn" and NOPAINT==0:
        s_ring(d,lateclgc,loneclgc,rapl,decpl)
        m_=m_+sring.ring_magn
        s_sat(d,rpl,lateclgc,loneclgc)
    rastr,decstr=grms(rapl,decpl)
    if NOPRINT==0:
        print(plname.ljust(7),": RA="+rastr+" DEC="+decstr+" DIST="+str(round(rpl,4))+"au"+" DIAM="+str(round(dpl*3600,1))+'"')
        if plname=="Mercury" or plname=="Venus" or plname=="Mars" or plname=="Jupiter":
            print("          AZ="+str(round(az,2))+"d"+" ALT="+str(round(alt,2))+"d"+" PHASE="+str(round(phase,2))+" MAGN="+str(round(m_,2)))
        else:
            print("          AZ="+str(round(az,2))+"d"+" ALT="+str(round(alt,2))+"d"+" MAGN="+str(round(m_,2)))

    if deltad==0 and NOPAINT==0:
        rastr,decstr=grms(rapl,decpl)
        planetdb[plnum].str1="planet "+plname+":"
        planetdb[plnum].str2="RA="+rastr+" DEC="+decstr+" DIST="+str(round(rpl,4))+"au"+" DIAM="+str(round(dpl*3600,1))+'"'
        if plname=="Mercury" or plname=="Venus" or plname=="Mars" or plname=="Jupiter":
            planetdb[plnum].str3="AZ="+str(round(az,2))+"d"+" ALT="+str(round(alt,2))+"d"+" PHASE="+str(round(phase,2))+" MAGN="+str(round(m_,2))
        else:
            planetdb[plnum].str3="AZ="+str(round(az,2))+"d"+" ALT="+str(round(alt,2))+"d"+" MAGN="+str(round(m_,2))
    return(rapl,decpl,rpl,dpl,phase,m_)
#============================
#calc Jupiter satellites
def j_sat(d):
    #d=JD_-2451545
    d=d-1.5
    V=(172.74+0.00111588*d)*pid180
    M=(357.529+0.9856003*d)*pid180
    N=(20.020+0.0830853*d)*pid180
    J=(66.115+0.9025179*d)*pid180
    A=(1.915*sin(M)+0.020*sin(2*M))*pid180
    B=(5.555*sin(N)+0.168*sin(2*N))*pid180
    K=J+A-B
    R=1.00014-0.01671*cos(M)-0.00014*cos(2*M)
    r=5.20872-0.25208*cos(N)-0.00611*cos(2*N)
    delta=sqrt(r*r+R*R-2*r*R*cos(K))
    psi=asin(R*sin(K)/delta)
    lambd_=(34.35+0.083091*d+0.329*sin(V))*pid180+B
    Ds=pid180*3.12*sin(lambd_+42.8*pid180)
    De=Ds-pid180*(2.22*sin(psi)*cos(lambd_+22*pid180)-1.3*(r-delta)/delta*sin(lambd_-100.5*pid180))
    u1=(163.8067+203.4058643*(d-delta/173))*pid180+psi-B
    u2=(358.4108+101.2916334*(d-delta/173))*pid180+psi-B
    u3=(5.7129+50.2345179*(d-delta/173))*pid180+psi-B
    u4=(224.8151+21.4879801*(d-delta/173))*pid180+psi-B

    G=(331.18+50.310482*(d-delta/173))*pid180
    H=(87.4+21.569231*(d-delta/173))*pid180

    du1=0.473*sin(2*(u1-u2))*pid180
    du2=1.065*sin(2*(u2-u3))*pid180
    du3=0.165*sin(G)*pid180
    du4=0.841*sin(H)*pid180

    u1c=u1+du1
    u2c=u2+du2
    u3c=u3+du3
    u4c=u4+du4

    r1=5.9073-0.0244*cos(2*(u1-u2))
    r2=9.3991-0.0882*cos(2*(u2-u3))
    r3=14.9924-0.0216*cos(G)
    r4=26.3699-0.1935*cos(H)

    jsatdb[0].dx=r1*sin(u1c); jsatdb[0].dy=-r1*cos(u1c)*sin(De)
    jsatdb[1].dx=r2*sin(u2c); jsatdb[1].dy=-r2*cos(u2c)*sin(De)
    jsatdb[2].dx=r3*sin(u3c); jsatdb[2].dy=-r3*cos(u3c)*sin(De)
    jsatdb[3].dx=r4*sin(u4c); jsatdb[3].dy=-r4*cos(u4c)*sin(De)

#============================
#calc Saturn satellites    
def s_sat(d,rpl,bet0,lam0):
    #====subr
    def subr(lam_,p,e,a,OME,i,s1,c1):
        M=lam_-p
        C=(2*e-0.25*(e**3)+0.0520833333*(e**5))*sin(M)+(1.25*e*e-0.458333333*(e**4))*sin(2*M)+(1.083333333*(e**3)-0.671875*(e**5))*sin(3*M)+1.072917*(e**4)*sin(4*M)+1.142708*(e**5)*sin(5*M)
        r=a*(1-e*e)/(1+e*cos(M+C))
        g=OME-pid180*168.8112
        a1=sin(i)*sin(g)
        a2=c1*sin(i)*cos(g)-s1*cos(i)
        gam=asin(sqrt(a1*a1+a2*a2))
        u=atan2(a1,a2)
        ww=pid180*168.8112+u
        h=c1*sin(i)-s1*cos(i)*cos(g)
        psi=atan2(s1*sin(g),h)
        lam=lam_+C+u-g-psi
        OME=ww
        return(lam,OME,gam,r)
        #============
    def xyzcalc(lam,OME,gam,r,lam0,bet0,rpl,D,s1,c1,s2,c2):
        u=lam-OME; w=OME-pid180*168.8112
        X=r*(cos(u)*cos(w)-sin(u)*cos(gam)*sin(w))
        Y=r*(sin(u)*cos(w)*cos(gam)+cos(u)*sin(w))
        Z=r*sin(u)*sin(gam)
        A1=X
        B1=c1*Y-s1*Z
        C1=s1*Y+c1*Z
        A2=c2*A1-s2*B1
        B2=s2*A1+c2*B1
        C2=C1
        A3=A2*sin(lam0)-B2*cos(lam0)
        B3=A2*cos(lam0)+B2*sin(lam0)
        C3=C2
        A4=A3
        B4=B3*cos(bet0)+C3*sin(bet0)
        C4=C3*cos(bet0)-B3*sin(bet0)

        X=A4*cos(D)-C4*sin(D)
        Y=A4*sin(D)+C4*cos(D)
        Z=B4
        corr1=abs(Z)/53800*sqrt(1-(X/r)*(X/r))
        X=X+corr1
        corr2=rpl/(rpl+Z/2475)
        X=X*corr2; Y=Y*corr2
        return(X,Y,Z)
        #============        
    jde=d+2451543.5; jd0=2433282.4235
    T=(jd0-2451545)/36525; t=(jde-jd0)/36525
    hh=pid180/3600*((47.0029-0.06603*T+0.000598*T*T)*t+(-0.03302+0.000598*T)*t*t+0.00006*(t**3))
    P=pid180*(174.876384+3289.4789/3600*T+0.60622/3600*T*T-1/3600*(869.8089+0.50491*T)*t+1/3600*0.03536*t*t)
    pp=pid180/3600*((5029.0966+2.22226*T-0.000042*T*T)*t+(1.11113-0.000042*T)*t*t-0.000006*(t**3))
    A_=cos(hh)*cos(bet0)*sin(P-lam0)-sin(hh)*sin(bet0)
    B_=cos(bet0)*cos(P-lam0)
    C_=cos(hh)*sin(bet0)+sin(hh)*cos(bet0)*sin(P-lam0)
    lam0=-atan2(A_,B_)+pp+P; bet0=asin(C_)
    t1=jde-2411093; t2=t1/365.25; t3=(jde-2433282.423)/365.25+1950
    t4=jde-2411368; t5=t4/365.25; t6=jde-2415020; t7=t6/36525
    t8=t6/365.25; t9=(jde-2442000.5)/365.25; t10=jde-2409786; t11=t10/36525
    W0=pid180*(5.095*(t3-1866.39)); W1=pid180*(74.4+32.39*t2); W2=pid180*(134.3+92.62*t2)
    W3=pid180*(42-0.5118*t5); W4=pid180*(276.59+0.5118*t5); W5=pid180*(267.2635+1222.1136*t7)
    W6=pid180*(175.4762+1221.5515*t7); W7=pid180*(2.4891+0.002435*t7); W8=pid180*(113.35-0.2597*t7)
    s1=sin(28.0817*pid180); c1=cos(28.0817*pid180); s2=sin(168.8112*pid180); c2=cos(168.8112*pid180)
    e1=0.05589-0.000346*t7
    #calc D
    X9=0; Y9=0; Z9=1 #9 fict sat
    A19=X9
    B19=c1*Y9-s1*Z9
    C19=s1*Y9+c1*Z9
    A29=c2*A19-s2*B19
    B29=s2*A19+c2*B19
    C29=C19
    A39=A29*sin(lam0)-B29*cos(lam0)
    B39=A29*cos(lam0)+B29*sin(lam0)
    C39=C29
    A49=A39
    B49=B39*cos(bet0)+C39*sin(bet0)
    C49=C39*cos(bet0)-B39*sin(bet0)
    D=atan2(A49,C49)
    #==
    #Mimas
    L=pid180*(127.64+381.994497*t1-43.57*sin(W0)-0.720*sin(3*W0)-0.02144*sin(5*W0))
    p=pid180*(106.1+365.549*t2)
    M=L-p
    C=pid180*(2.18287*sin(M)+0.025988*sin(2*M)+0.00043*sin(3*M))
    lam=L+C
    r=3.06879/(1+0.01905*cos(M+C))
    gam=pid180*1.563
    OME=pid180*(54.5-365.072*t2)
    X,Y,Z=xyzcalc(lam,OME,gam,r,lam0,bet0,rpl,D,s1,c1,s2,c2)
    ssatdb[0].dx=X; ssatdb[0].dy=Y
    #Enceladus
    L=pid180*(200.317+262.7319002*t1+0.25667*sin(W1)+0.20883*sin(W2))
    p=pid180*(309.107+123.44121*t2)
    M=L-p
    C=pid180*(0.55577*sin(M)+0.00168*sin(2*M))
    lam=L+C
    r=3.94118/(1+0.00485*cos(M+C))
    gam=pid180*0.0262
    OME=pid180*(348-151.95*t2)
    X,Y,Z=xyzcalc(lam,OME,gam,r,lam0,bet0,rpl,D,s1,c1,s2,c2)
    ssatdb[1].dx=X; ssatdb[1].dy=Y
    #Tethys
    lam=pid180*(285.306+190.69791226*t1+2.063*sin(W0)+0.03409*sin(3*W0)+0.001015*sin(5*W0))
    r=4.880998
    gam=pid180*1.0976
    OME=pid180*(111.33-72.2441*t2)
    X,Y,Z=xyzcalc(lam,OME,gam,r,lam0,bet0,rpl,D,s1,c1,s2,c2)
    ssatdb[2].dx=X; ssatdb[2].dy=Y
    #Dione
    L=pid180*(254.712+131.53493193*t1-0.0215*sin(W1)-0.01733*sin(W2))
    p=pid180*(174.8+30.820*t2)
    M=L-p
    C=pid180*(0.24717*sin(M)+0.00033*sin(2*M))
    lam=L+C
    r=6.24871/(1+0.002157*cos(M+C))
    gam=pid180*0.0139
    OME=pid180*(232-30.27*t2)
    X,Y,Z=xyzcalc(lam,OME,gam,r,lam0,bet0,rpl,D,s1,c1,s2,c2)
    ssatdb[3].dx=X; ssatdb[3].dy=Y
    #Rhea
    p_=pid180*(342.7+10.057*t2)
    a1=0.000265*sin(p_)+0.01*sin(W4)
    a2=0.000265*cos(p_)+0.01*cos(W4)
    e=sqrt(a1*a1+a2*a2)
    p=atan2(a1,a2)
    N=pid180*(345-10.057*t2)
    lam_=pid180*(359.244+79.69004720*t1+0.086754*sin(N))
    i=pid180*(28.0362+0.346898*cos(N)+0.01930*cos(W3))
    OME=pid180*(168.8034+0.736936*sin(N)+0.041*sin(W3))
    a=8.725924
    lam,OME,gam,r=subr(lam_,p,e,a,OME,i,s1,c1)
    X,Y,Z=xyzcalc(lam,OME,gam,r,lam0,bet0,rpl,D,s1,c1,s2,c2)
    ssatdb[4].dx=X; ssatdb[4].dy=Y
    #Titan
    L=pid180*(261.1582+22.57697855*t4+0.074025*sin(W3))
    i_=pid180*(27.45141+0.295999*cos(W3))
    OME_=pid180*(168.66925+0.628808*sin(W3))
    a1=sin(W7)*sin(OME_-W8)
    a2=cos(W7)*sin(i_)-sin(W7)*cos(i_)*cos(OME_-W8)
    g0=pid180*102.8623
    psi=atan2(a1,a2)
    s=sqrt(a1*a1+a2*a2)
    g=W4-OME_-psi
    for count in range(0,3):
        w_=W4+pid180*0.37515*(sin(2*g)-sin(2*g0))
        g=w_-OME_-psi
    e_=0.029092+0.00019048*(cos(2*g)-cos(2*g0))
    q=2*(W5-w_)
    b1=sin(i_)*sin(OME_-W8)
    b2=cos(W7)*sin(i_)*cos(OME_)
    teta=atan2(0,b2)+W8
    e=e_+0.002778797*e_*cos(q)
    p=w_+pid180*0.159215*sin(q)
    u=2*W5-2*teta+psi
    h=0.9375*e_*e_*sin(q)+0.1875*s*s*sin(2*(W5-teta))
    lam_=L-pid180*0.254744*(e1*sin(W6)+0.75*e1*e1*sin(2*W6)+h)
    i=i_+pid180*0.031843*s*cos(u)
    OME=OME_+pid180*(0.031843*s*sin(u)/(sin(i_)*sin(i_)))
    a=20.216193
    lam,OME,gam,r=subr(lam_,p,e,a,OME,i,s1,c1)
    X,Y,Z=xyzcalc(lam,OME,gam,r,lam0,bet0,rpl,D,s1,c1,s2,c2)
    ssatdb[5].dx=X; ssatdb[5].dy=Y
    #Hyperion
    eta=pid180*(92.39+0.5621071*t6)
    dzeta=pid180*(148.19-19.18*t8)
    teta=pid180*(184.8-35.41*t9)
    teta_=teta-pid180*7.5
    a_s=pid180*(176+12.22*t8)
    b_s=pid180*(8+24.44*t8)
    c_s=b_s+pid180*5
    w_=pid180*(69.898-18.67088*t8)
    fi=2*(w_-W5)
    xi=pid180*(94.9-2.292*t8)
    a=24.50601-0.08686*cos(eta)-0.00166*cos(dzeta+eta)+0.00175*cos(dzeta-eta)
    e=0.103458-0.004099*cos(eta)-0.000167*cos(dzeta+eta)+0.000235*cos(dzeta-eta)+0.02303*cos(dzeta)-0.00212*cos(2*dzeta)+0.000151*cos(3*dzeta)+0.00013*cos(fi)
    p=pid180*(w_+0.15648*sin(xi)-0.4457*sin(eta)-0.2657*sin(dzeta+eta)-0.3573*sin(dzeta-eta)-12.872*sin(dzeta)+1.668*sin(2*dzeta)-0.2419*sin(3*dzeta)-0.07*sin(fi))
    lam_=pid180*(177.047+16.91993829*t6+0.15648*sin(xi)+9.142*sin(eta)+0.007*sin(2*eta)-0.014*sin(3*eta)+0.2275*sin(dzeta+eta)+0.2112*sin(dzeta-eta)-0.26*sin(dzeta)-0.0098*sin(2*dzeta)-0.013*sin(a_s)+0.017*sin(b_s)-0.0303*sin(fi))
    i=pid180*(27.3347+0.643486*cos(xi)+0.315*cos(W3)+0.018*cos(teta)-0.018*cos(c_s))
    OME=pid180*(168.6812+1.40136*cos(xi)+0.68599*sin(W3)-0.0392*sin(c_s)+0.0366*sin(teta_))
    lam,OME,gam,r=subr(lam_,p,e,a,OME,i,s1,c1)
    X,Y,Z=xyzcalc(lam,OME,gam,r,lam0,bet0,rpl,D,s1,c1,s2,c2)
    ssatdb[6].dx=X; ssatdb[6].dy=Y
    #Iapetus
    L=pid180*(261.1582+22.57697855*t4)
    w_s=pid180*(91.796+0.562*t7)
    psi=pid180*(4.367-0.195*t7)
    teta=pid180*(146.819-3.198*t7)
    fi=pid180*(60.470+1.521*t7)
    FI=pid180*(205.055-2.091*t7)
    e_=0.028298+0.001156*t11
    w_0=pid180*(352.91+11.71*t11)
    mu=pid180*(76.3852+4.53795125*t10)
    i_=pid180*(18.4602-0.9518*t11-0.072*t11*t11+0.0054*(t11**3))
    OME_=pid180*(143.198-3.919*t11+0.116*t11*t11+0.008*(t11**3))
    l=mu-w_0; g=w_0-OME_-psi; gl=w_0-OME_-fi; ls=W5-w_s; gs=w_s-teta; lt=L-W4; gt=W4-FI
    u1=2*(l+g-ls-gs); u2=l+gl-lt-gt; u3=l+2*(g-ls-gs); u4=lt+gt-gl; u5=2*(ls+gs)
    a=58.935028+0.004638*cos(u1)+0.058222*cos(u2)
    e=e_-0.0014097*cos(gl-gt)+0.0003733*cos(u5-2*g)+0.0001180*cos(u3)+0.0002408*cos(l)+0.0002849*cos(l+u2)+0.0006190*cos(u4)
    ww=pid180*(0.08077*sin(gl-gt)+0.02139*sin(u5-2*g)-0.00676*sin(u3)+0.01380*sin(l)+0.01632*sin(l+u2)+0.03547*sin(u4))
    p=w_0+ww/e_
    lam_=mu+pid180*(-0.04299*sin(u2)-0.00789*sin(u1)-0.06312*sin(ls)-0.00295*sin(2*ls)-0.02231*sin(u5)+0.00650*sin(u5+psi))
    i=i_+pid180*(0.04204*cos(u5+psi)+0.00235*cos(l+gl+lt+gt+fi)+0.00360*cos(u2+fi))
    ww_=pid180*(0.04204*sin(u5+psi)+0.00235*sin(l+gl+lt+gt+fi)+0.00358*sin(u2+fi))
    OME=OME_+ww_/sin(i_)
    lam,OME,gam,r=subr(lam_,p,e,a,OME,i,s1,c1)
    X,Y,Z=xyzcalc(lam,OME,gam,r,lam0,bet0,rpl,D,s1,c1,s2,c2)
    ssatdb[7].dx=X; ssatdb[7].dy=Y
#============================
#calc Saturn ring
def s_ring(d,las,los,rapl,decpl):
    alp_=rapl*15*pid180; del_=decpl*pid180
    tim=(d-1.5)/36525
    ir = 28.06*pid180
    Nr = 169.51*pid180 + 3.82E-5*pid180 * d
    sring.b = asin( sin(las) * cos(ir) - cos(las) * sin(ir) * sin(los-Nr) )
    sring.ring_magn = -2.6 * sin(abs(sring.b)) + 1.2 * (sin(sring.b))**2
    i=28.075216*pid180-0.012998*pid180*tim+0.000004*pid180*tim*tim
    ome=169.508470*pid180+1.394681*pid180*tim+0.000412*pid180*tim*tim
    lam0=ome-pid2; bet0=pid2-i
    alp0=atan2(sin(lam0)*COSEPS-tan(bet0)*SINEPS,cos(lam0))
    del0=asin(sin(bet0)*COSEPS+cos(bet0)*SINEPS*sin(lam0))
    yy=cos(del0)*sin(alp0-alp_)
    xx=sin(del0)*cos(del_)-cos(del0)*sin(del_)*cos(alp0-alp_)
    sring.pa=atan2(yy,xx)
#===============calc Moon
def calcmoon(plname,N,i,w,a,e,M,d,lonsun,rsun,Msun,wsun):
    Lsun=Msun+wsun
    Lm=M + w + N
    D = Lm - Lsun     
    F = Lm - N     
     
    E_ = M + e * sin(M) * ( 1.0 + e * cos(M) )
    E0=E_
    E1 = E0 - ( E0 - e * sin(E0) - M ) / ( 1 - e * cos(E0) )
    dE=1  
    while dE>0.0001*pid180:
        E1 = E0 - ( E0 - e * sin(E0) - M ) / ( 1 - e * cos(E0) )
        dE=abs(E0-E1); E0=E1
    E_=E1

    xv = a * ( cos(E_) - e )
    yv = a * ( sqrt(1.0 - e*e) * sin(E_) )

    r = sqrt( xv*xv + yv*yv )    
 
    v = atan2( yv, xv )

    xh = r * ( cos(N) * cos(v+w) - sin(N) * sin(v+w) * cos(i) )
    yh = r * ( sin(N) * cos(v+w) + cos(N) * sin(v+w) * cos(i) )
    zh = r * ( sin(v+w) * sin(i) )

    lonecl = atan2( yh, xh )
    lonecl=lonecl-pid180*1.274 * sin(M - 2*D)          
    lonecl=lonecl+pid180*0.658 * sin(2*D)               
    lonecl=lonecl-pid180*0.186 * sin(Msun)                
    lonecl=lonecl-pid180*0.059 * sin(2*M - 2*D)
    lonecl=lonecl-pid180*0.057 * sin(M - 2*D + Msun)
    lonecl=lonecl+pid180*0.053 * sin(M + 2*D)
    lonecl=lonecl+pid180*0.046 * sin(2*D - Msun)
    lonecl=lonecl+pid180*0.041 * sin(M - Msun)
    lonecl=lonecl-pid180*0.035 * sin(D)                 
    lonecl=lonecl-pid180*0.031 * sin(M + Msun)
    lonecl=lonecl-pid180*0.015 * sin(2*F - 2*D)
    lonecl=lonecl+pid180*0.011 * sin(M - 4*D)
    
    latecl = atan2( zh, sqrt(xh*xh+yh*yh) )
    latecl=latecl-pid180*0.173 * sin(F - 2*D)
    latecl=latecl-pid180*0.055 * sin(M - F - 2*D)
    latecl=latecl-pid180*0.046 * sin(M + F - 2*D)
    latecl=latecl+pid180*0.033 * sin(F + 2*D)
    latecl=latecl+pid180*0.017 * sin(2*M + F)

    lonmoon=lonecl
    
    xg = r * cos(lonecl) * cos(latecl)
    yg = r * sin(lonecl) * cos(latecl)
    zg = r * sin(latecl) 

    xe = xg
    ye = yg * COSEPS - zg * SINEPS
    ze = yg * SINEPS + zg * COSEPS

    rapl  = d180pi/15*atan2( ye, xe )
    if rapl<0:rapl=rapl+24
    decpl = d180pi*atan2( ze, sqrt(xe*xe+ye*ye) )
    
    rpl = sqrt(xg*xg+yg*yg+zg*zg)-0.58 * cos(M - 2*D)-0.46 * cos(2*D)  

    return(rapl,decpl,rpl,lonmoon)
#============================
#Moon calc JM
def moon_jm(d,dpsi,deps):
    jde=d+2451543.5
    T=(jde-2451545)/36525
    L_=pid180*(218.3164477+481267.88123421*T-0.0015786*T*T+T**3/538841-T**4/65194000)
    D=pid180*(297.8501921+445267.1114034*T-0.0018819*T*T+T**3/545868-T**4/113065000)
    M=pid180*(357.5291092+35999.0502909*T-0.0001536*T*T+T**3/24490000)
    M_=pid180*(134.9633964+477198.8675055*T+0.0087414*T*T+T**3/69699-T**4/14712000)
    F=pid180*(93.2720950+483202.0175233*T-0.0036539*T*T-T**3/3526000+T**4/863310000)
    A1=pid180*(119.75+131.849*T)
    A2=pid180*(53.09+479264.290*T)
    A3=pid180*(313.45+481266.484*T)
    E=1-0.002516*T-0.0000074*T*T

    sumL=0; sumR=0; sumB=0
    for i in range(0,len(Tmo_lr)):
        sumL=sumL+pid180*Tmo_lr[i][4]*sin(Tmo_lr[i][0]*D+Tmo_lr[i][1]*M+Tmo_lr[i][2]*M_+Tmo_lr[i][3]*F)
        sumR=sumR+Tmo_lr[i][5]*cos(Tmo_lr[i][0]*D+Tmo_lr[i][1]*M+Tmo_lr[i][2]*M_+Tmo_lr[i][3]*F)
    for i in range(0,len(Tmo_b)):
        sumB=sumB+pid180*Tmo_b[i][4]*sin(Tmo_b[i][0]*D+Tmo_b[i][1]*M+Tmo_b[i][2]*M_+Tmo_b[i][3]*F)

    sumL=E*sumL+pid180*(3958*sin(A1)+1962*sin(L_-F)+318*sin(A2))
    sumB=E*sumB-pid180*(2235*sin(L_)+382*sin(A3)+175*sin(A1-F)+175*sin(A1+F)+127*sin(L_-M_)-115*sin(L_+M_))
    
    lam=L_+sumL/1000000        
    bet=sumB/1000000           
    delta=385000.56+E*sumR/1000   #km
    pi_m=asin(6378.14/delta)
    
    lam=lam+dpsi
    eps=EPS+deps
    rapl=d180pi*(atan2(sin(lam)*cos(eps)-tan(bet)*sin(eps),cos(lam)))/15
    if rapl<0: rapl=rapl+24
    if rapl>=24: rapl=rapl-24
    decpl=d180pi*asin(sin(bet)*cos(eps)+cos(bet)*sin(eps)*sin(lam))
    rpl=delta/6371
    lonmoon=lam
    return(rapl,decpl,rpl,lonmoon)    

    #======Calc asteroid
def calcasteroid(d,deltad,lmst,rsun,lonsun,dpsi,deps,m_lim,objnum):

#      					        Moment M        M        a       e        Peri w  Node N    Incl i    H     G
#      1 Ceres                                 2010 01 04.0  70.4340  2.765723 0.079222  72.6927  80.3939  10.5863   3.34  0.12 
#      2 Pallas                                2010 01 04.0  53.3955  2.772749 0.230970 310.2064 173.1284  34.8404   4.13  0.11 
#      7 Iris                                  2010 01 04.0 311.1732  2.386586 0.230907 145.1424 259.6868   5.5231   5.51  0.15       

    if deltad==0 and NOPAINT==0:
        j=0
        for asteroid in asterdb:
            asterdb[j].str1=""
            asterdb[j].str2=""
            asterdb[j].str3=""
            asterdb[j].magn=99
            j=j+1

    foundtext="not available"
    if NOPRINT==0:print("Asteroids (MAGN<="+str(m_lim)+"):")
    yy_,mm_,dd_,hh_=jdtodate(d-DELTAT/86400+2451543.5+DELTAHOURS/24)
    tracktext=(str(dd_)+"."+str(mm_)+"."+str(yy_)).ljust(11)
    epoch_now=yy_+mm_/12+dd_/365.25
    
    k = 0.01720209895
    
    #j=0
    #for asteroid in asterdb:
    if objnum==-1: num1=0; num2=len(asterdb)
    else: num1=objnum; num2=objnum+1
    for j in range(num1,num2):
        plname=asterdb[j].name
        astnum=asterdb[j].num
        year1=asterdb[j].year1
        month1=asterdb[j].month1
        day1=int(asterdb[j].day1)
        hour1=24*(asterdb[j].day1-day1)
        M1=asterdb[j].M1*pid180
        a=asterdb[j].a
        e=asterdb[j].e
        w=asterdb[j].w*pid180
        N=asterdb[j].N*pid180
        i=asterdb[j].i*pid180
        H=asterdb[j].H
        G=asterdb[j].G

        epoch_orb=year1+month1/12+day1/365.25
        N = N + (0.013967 * ( epoch_orb - epoch_now ) + 3.82394E-5 * d)*pid180
        
        P = pi2 * sqrt(a*a*a) / k

        mjd_m = mjdf(day1,month1,year1,hour1)
        jd_m = mjd_m + 2400000.5
        dm = jd_m - 2451543.5
        #dm= 367*year1 - int(7 * ( year1 + int((month1+9)/12) ) / 4) + int(275*(month1/9)) + day1 - 730530 + hour1/24
        dt=dm-M1*P/pi2
        M = (d - dt) * k / sqrt(a*a*a)
 
        E_ = M + e * sin(M) * ( 1.0 + e * cos(M) )
        E0=E_
        E1 = E0 - ( E0 - e * sin(E0) - M ) / ( 1 - e * cos(E0) )
        dE=1  
        while dE>0.0001*pid180:
            E1 = E0 - ( E0 - e * sin(E0) - M ) / ( 1 - e * cos(E0) )
            dE=abs(E0-E1); E0=E1
        E_=E1
        
        xv = a * ( cos(E_) - e )
        yv = a * ( sqrt(1.0 - e*e) * sin(E_) )

        r = sqrt( xv*xv + yv*yv )    
 
        v = atan2( yv, xv )

        xh = r * ( cos(N) * cos(v+w) - sin(N) * sin(v+w) * cos(i) )
        yh = r * ( sin(N) * cos(v+w) + cos(N) * sin(v+w) * cos(i) )
        zh = r * ( sin(v+w) * sin(i) )

        lonecl = atan2( yh, xh ) 
        latecl = atan2( zh, sqrt(xh*xh+yh*yh) )
        
        xh = r * cos(lonecl) * cos(latecl)
        yh = r * sin(lonecl) * cos(latecl)
        zh = r * sin(latecl) 

        xs = rsun * cos(lonsun)
        ys = rsun * sin(lonsun) 

        xg = xh + xs
        yg = yh + ys
        zg = zh 
    
        xe = xg
        ye = yg * COSEPS - zg * SINEPS
        ze = yg * SINEPS + zg * COSEPS

        rapl  = d180pi/15*atan2( ye, xe )
        if rapl<0:rapl=rapl+24
        decpl = d180pi*atan2( ze, sqrt(xe*xe+ye*ye) )
        rapl,decpl=nutapl(rapl,decpl,dpsi,deps)
        rpl = sqrt(xg*xg+yg*yg+zg*zg)
        ra_tc,dec_tc,dist_tc=radectc(KPOL,rapl,decpl,rpl*AU/1000,MYLAT,MYLON,lmst)
        if deltad==0: asterdb[j].ra=ra_tc; asterdb[j].dec=dec_tc;
        az,alt=calcaz(ra_tc,dec_tc,lmst)        

        lona=lonecl;lons=lonsun
        if lona<0:lona=lonecl+pi2
        if lons<0:lons=lonsun+pi2
        #faz=(1-cos(lona-lons))/2

        ragcstr,decgcstr=grms(rapl,decpl)
        ratcstr,dectcstr=grms(ra_tc,dec_tc)
        try:
            m_ = H + 5*log10(rpl) + 5*log10(r) + G*abs(lona-lons)
        except:
            m_=100

        if deltad==0 and NOPAINT==0: asterdb[j].magn=m_

        if NOPRINT==0 and (asterdb[j].magn<=m_lim):
            print(asterdb[j].num+" "+plname)
            print("                       RAgc="+ragcstr+" DECgc="+decgcstr)
            print("                       RAtc="+ratcstr+" DECtc="+dectcstr+" DIST="+str(round(rpl,4))+"au")
            print("                       AZ="+str(round(az,2))+"d"+" ALT="+str(round(alt,2))+"d"+" MAGN="+str(round(m_,1)))
            foundtext=""
            
        if NOPAINT==0:
            strfind=zamenan(" ",efind.get().strip().lower())
            plname_=zamenan(" ",plname.strip().lower())
            if (deltad==0 or (deltad!=0 and plname_.find(strfind)!=-1)) and (asterdb[j].magn<=m_lim):
                if deltad==0:strtag="asteroid"+str(j)
                else:strtag="ddasteroid"+str(j)
                x,y,rokr,ugv=ovalekv(plname.strip(),ra_tc,dec_tc,0,m_,planetcolor,planetcolor,1,strtag)

                if deltad==0:
                    stext(x,y,0,-rokr-12,plname,planetcolor,font1,strtag)
                    asterdb[j].str1="asteroid "+asterdb[j].num+" "+plname.strip()+":"
                    asterdb[j].str2="RAgc="+ragcstr+" DECgc="+decgcstr
                    asterdb[j].str3="RAtc="+ratcstr+" DECtc="+dectcstr+" DIST="+str(round(rpl,4))+"au"
                    asterdb[j].str4="AZ="+str(round(az,2))+"d"+" ALT="+str(round(alt,2))+"d"+" MAGN="+str(round(m_,1))            
                    asterdb[j].x=x
                    asterdb[j].y=y
                if deltad!=0 and plname_.find(strfind)!=-1 and ctrackvar.get()==1:
                    stext(x,y,rokr+37,0,tracktext,planetcolor,font1,"tracktext")
        j=j+1
    if NOPRINT==0 and foundtext!="": print(foundtext)        
#====================================================================================
#======Calc comet
def calccomet(d,deltad,lmst,rsun,lonsun,dpsi,deps,m_lim,objnum):
#	nam				         t perig	  perig a e         e	     w      N	     i	     g      k
#C/1995 O1 Hale-Bopp                            1997 03 29.2897  0.938430       0.994913 130.8681 282.8606  89.2179  -2.0   4.0
#C/2016 R2 PANSTARRS                            2018 05 09.5805  2.602285       0.996533  33.1935  80.5703  58.2190   7.0   4.0
#C/2017 P2 PANSTARRS                            2017 12 06.6449  2.460014       1.000000 132.3124 165.5502  50.0834  15.0   4.0 
#C/2017 M5 TOTAS                                2018 06 02.3490  5.991384       1.002635  92.5808 216.2724  15.8857   6.5   4.0     
#2P Encke                                       2017 03 10.0884  0.335921       0.848308 186.5629 334.5602  11.7779  11.5   6.0

    if deltad==0 and NOPAINT==0:
        j=0
        for comet in cometdb:
            cometdb[j].str1=""
            cometdb[j].str2=""
            cometdb[j].str3=""
            cometdb[j].str4=""
            cometdb[j].magn=99
            j=j+1
     
    foundtext="not available"
    if NOPRINT==0:print("Comets (MAGN<="+str(m_lim)+"):")
    yy_,mm_,dd_,hh_=jdtodate(d-DELTAT/86400+2451543.5+DELTAHOURS/24)
    tracktext=(str(dd_)+"."+str(mm_)+"."+str(yy_)).ljust(11)
    epoch_now=yy_+mm_/12+dd_/365.25

    k = 0.01720209895

    #j=0
    #for comet in cometdb:
    if objnum==-1: num1=0; num2=len(cometdb)
    else: num1=objnum; num2=objnum+1
    for j in range(num1,num2):
        plname=cometdb[j].name
        year1=cometdb[j].year1
        month1=cometdb[j].month1
        day1=int(cometdb[j].day1)
        hour1=24*(cometdb[j].day1-day1)
        q=cometdb[j].q
        e=cometdb[j].e
        w=cometdb[j].w*pid180
        N=cometdb[j].N*pid180
        i=cometdb[j].i*pid180
        gg=cometdb[j].gg
        kk=cometdb[j].kk

        epoch_orb=year1+month1/12+day1/365.25
        N = N + (0.013967 * ( epoch_orb - epoch_now ) + 3.82394E-5 * d)*pid180
        
        mjd_P = mjdf(day1,month1,year1,hour1)
        jd_P = mjd_P + 2400000.5
        dP = jd_P - 2451543.5
        yyP,mmP,ddP,hhP=jdtodate(dP+2451543.5+DELTAHOURS/24)
        strperih="perihelion: "+str(ddP).rjust(2,"0")+"."+str(mmP).rjust(2,"0")+"."+str(yyP).rjust(4,"0")+" "+str(int(hhP)).rjust(2,"0")+":"+str(round(60*frac(hhP))).rjust(2,"0")

        #dP= 367*year1 - int(7 * ( year1 + int((month1+9)/12) ) / 4) + int(275*(month1/9)) + day1 - 730530 + hour1/24

        if e<0.98:
            a = q / (1.0 - e)
            P = pi2 * sqrt(a*a*a) / k
            M = pi2 * (d-dP)/P

            E_ = M + e * sin(M) * ( 1.0 + e * cos(M) )
            E0=E_
            E1 = E0 - ( E0 - e * sin(E0) - M ) / ( 1 - e * cos(E0) )
            dE=1  
            while dE>0.00001*pid180:
                E1 = E0 - ( E0 - e * sin(E0) - M ) / ( 1 - e * cos(E0) )
                dE=abs(E0-E1); E0=E1
            E_=E1
            
            xv = a * ( cos(E_) - e )
            yv = a * ( sqrt(1.0 - e*e) * sin(E_) )

            r = sqrt( xv*xv + yv*yv )    
            v = atan2( yv, xv )
        
        """if e==1:
            H_ = (d-dP) / (82.21168627 * sqrt(q*q*q))
            h = 1.5 * H_
            g = sqrt( 1.0 + h*h )
            #s = exp( log(g + h)/3.0) - exp( log(g - h)/3.0)
            s=(g + h)**(1/3)-(g-h)**(1/3)
    
            #v=2*asin(s*pid180/sqrt(1+s*pid180*s*pid180))
            v = 2.0 * atan(s)
            r = q * ( 1.0 + s*s )"""
        if e>=0.98:
            a = 0.75 * (d-dP) * k * sqrt( (1 + e) / (q*q*q) )
            b = sqrt( 1 + a*a )
            W_ = (b + a)**(1/3) - (b - a)**(1/3)
            f = (1 - e) / (1 + e)

            a1 = (2/3) + (2/5) * W_*W_
            a2 = (7/5) + (33/35) * W_*W_ + (37/175) * W_**4
            a3 = W_*W_ * ( (432/175) + (956/1125) * W_*W_ + (84/1575) * W_**4 )

            C = W_*W_ / (1 + W_*W_)
            g = f * C*C
            w2 = W_ * ( 1 + f * C * ( a1 + a2*g + a3*g*g ) )

            v = 2 * atan(w2)
            r = q * ( 1 + w2*w2 ) / ( 1 + w2*w2 * f )
        
        xh = r * ( cos(N) * cos(v+w) - sin(N) * sin(v+w) * cos(i) )
        yh = r * ( sin(N) * cos(v+w) + cos(N) * sin(v+w) * cos(i) )
        zh = r * ( sin(v+w) * sin(i) )

        lonecl = atan2( yh, xh )
        latecl = atan2( zh, sqrt(xh*xh+yh*yh) )
        
        xh = r * cos(lonecl) * cos(latecl)
        yh = r * sin(lonecl) * cos(latecl)
        zh = r * sin(latecl) 

        xs = rsun * cos(lonsun)
        ys = rsun * sin(lonsun) 

        xg = xh + xs
        yg = yh + ys
        zg = zh 
    
        xe = xg
        ye = yg * COSEPS - zg * SINEPS
        ze = yg * SINEPS + zg * COSEPS

        rapl  = d180pi/15*atan2( ye, xe )
        if rapl<0:rapl=rapl+24
        decpl = d180pi*atan2( ze, sqrt(xe*xe+ye*ye) )
        rapl,decpl=nutapl(rapl,decpl,dpsi,deps)
        rpl = sqrt(xg*xg+yg*yg+zg*zg)
        ra_tc,dec_tc,dist_tc=radectc(KPOL,rapl,decpl,rpl*AU/1000,MYLAT,MYLON,lmst)
        if deltad==0: cometdb[j].ra=ra_tc; cometdb[j].dec=dec_tc;
        az,alt=calcaz(ra_tc,dec_tc,lmst)      
        ragcstr,decgcstr=grms(rapl,decpl)
        ratcstr,dectcstr=grms(ra_tc,dec_tc)
        try:
            m_ = gg + 5*log10(rpl) + 2.5*kk*log10(r)
        except:
            m_=100

        if deltad==0 and NOPAINT==0: cometdb[j].magn=m_

        if NOPRINT==0 and (cometdb[j].magn<=m_lim):
            print(plname)
            print("                       RAgc="+ragcstr+" DECgc="+decgcstr)
            print("                       RAtc="+ratcstr+" DECtc="+dectcstr+" DIST="+str(round(rpl,4))+"au")
            print("                       AZ="+str(round(az,2))+"d"+" ALT="+str(round(alt,2))+"d"+" MAGN="+str(round(m_,1)))            
            print("                       "+strperih)
            foundtext=""
            
        if NOPAINT==0:
            strfind=zamenan(" ",efind.get().strip().lower())
            plname_=zamenan(" ",plname.strip().lower())
            if (deltad==0 or (deltad!=0 and plname_.find(strfind)!=-1)) and (cometdb[j].magn<=m_lim):
                x,y,z=calcxyzpolm(ra_tc,KPOL*dec_tc,LMST,ZOOM,KPOL)
                prvt,sklt,zz=povorot(x,y,z,TURN_ANGLE)
                x,y=calcxycon(prvt,sklt,ZOOM)
                if deltad==0:strtag="comet"+str(j)
                else:strtag="ddcomet"+str(j)
                ovalxy2(x,y,4,4,cometcolor,skycolor,1,strtag)
                #x,y,rokr,ugv=ovalekv(plname.strip(),rapl,decpl,0,m_,cometcolor,skycolor,1,strtag)
                if deltad==0:
                    stext(x,y,0,-4-12,plname,cometcolor,font1,strtag)
                    cometdb[j].str1="comet "+plname.strip()+":"
                    cometdb[j].str2="RAgc="+ragcstr+" DECgc="+decgcstr
                    cometdb[j].str3="RAtc="+ratcstr+" DECtc="+dectcstr+" DIST="+str(round(rpl,4))+"au"
                    cometdb[j].str4="AZ="+str(round(az,2))+"d"+" ALT="+str(round(alt,2))+"d"+" MAGN="+str(round(m_,1))
                    cometdb[j].str5=strperih   
                    cometdb[j].x=x
                    cometdb[j].y=y
                if deltad!=0 and plname_.find(strfind)!=-1:
                    yystr=str(yy_).rjust(4,"0"); mmstr=str(mm_).rjust(2,"0"); ddstr=str(dd_).rjust(2,"0")

                    ra1875,dec1875=ekvtoekv1875(ra_tc,dec_tc)
                    const=ekvtoconst1875(ra1875,dec1875)
                    
                    print("comet "+plname.strip()+": "+ddstr+"."+mmstr+"."+yystr+" MAGN="+str(round(m_,1))+" in "+const)
                    print()
                    if ctrackvar.get()==1:
                        stext(x,y,4+37,0,tracktext,cometcolor,font1,"tracktext")
                        #stext(x,y,-12,10,str(round(m_,1)),cometcolor,font4,"tracktext")

        j=j+1
    if NOPRINT==0 and foundtext!="": print(foundtext) 
#===================================================================
#Local to UTC for RiseSet and RiseSet2
def localtoutc(lday,lmonth,lyear,lh,lm,ls):
    
    ldtime=datetime.datetime(lyear, lmonth, lday , lh , lm , ls)
    utcdtime = ldtime - TIMEDELTA_
    utcdtime=utcdtime.strftime("%Y-%m-%d %H:%M:%S")
  
    day=int(utcdtime[8:10])
    month=int(utcdtime[5:7])
    year=int(utcdtime[0:4])
    hour=float(utcdtime[11:13])+float(utcdtime[14:16])/60+float(utcdtime[17:19])/3600
    return(day,month,year,hour)

# =============Rise Set
def riseset(*args):
    global NOPRINT,NOPAINT
    print("===============================================================================")
    print("LAT:",abs(MYLAT),CHLAT,"LON:",abs(MYLON),CHLON,"DATE:",LYEAR,"-",LMONTH,"-",LDAY)
    print("Sun, Moon and planets rising/set time:")
    NOPRINT=1
    NOPAINT=1
    foundtext="not available"
    hour2=0
    d = DSSYST - LHOUR/24 + hour2/24
    day,month,year,hour=localtoutc(LDAY,LMONTH,LYEAR,0,0,0)
    mjd_=mjdf(day,month,year,hour)
    lmst=lmstf(mjd_,MYLON)
    ssystem(d,0,lmst,"p",-1)
    tableplname_=TABLEPLNAME;tablealt_=TABLEALT
    while hour2<24-1/60:
        hour2=hour2+1/60
        lh=int(hour2);lm=int(hour2*60-lh*60)
        d=DSSYST - LHOUR/24 + hour2/24
        day,month,year,hour=localtoutc(LDAY,LMONTH,LYEAR,lh,lm,0)
        mjd_=mjdf(day,month,year,hour)
        lmst=lmstf(mjd_,MYLON)
        ssystem(d,0,lmst,"p",-1)
        i=0
        for line in TABLEPLNAME:
            if tablealt_[i]<0 and TABLEALT[i]>=0 and hour2>=1/60:
                hour2_=hour2-1/60
                if round((hour2_-int(hour2_))*60)==60:
                    hour2_=hour2_+1;min2=0
                else:min2=round((hour2_-int(hour2_))*60)
                print(TABLEPLNAME[i].ljust(14),"rise     :",int(hour2_),"h",min2,"m")
                foundtext=""
            if tablealt_[i]>=0 and TABLEALT[i]<0 and hour2>=1/60:
                hour2_=hour2-1/60
                if round((hour2_-int(hour2_))*60)==60:
                    hour2_=hour2_+1;min2=0
                else:min2=round((hour2_-int(hour2_))*60)
                print(TABLEPLNAME[i].ljust(14),"set      :",int(hour2_),"h",min2,"m")
                foundtext=""
        #sumerki
            if tablealt_[i]<-5.5 and TABLEALT[i]>=-5.5 and hour2>=1/60 and i==0:
                hour2_=hour2-1/60
                if round((hour2_-int(hour2_))*60)==60:
                    hour2_=hour2_+1;min2=0
                else:min2=round((hour2_-int(hour2_))*60)
                print("CIVIL          TWILIGHT :",int(hour2_),"h",min2,"m")
                foundtext=""
            if tablealt_[i]<-11.5 and TABLEALT[i]>=-11.5 and hour2>=1/60 and i==0:
                hour2_=hour2-1/60
                if round((hour2_-int(hour2_))*60)==60:
                    hour2_=hour2_+1;min2=0
                else:min2=round((hour2_-int(hour2_))*60)
                print("NAUTICAL       TWILIGHT :",int(hour2_),"h",min2,"m")
                foundtext=""
            if tablealt_[i]<-17.5 and TABLEALT[i]>=-17.5 and hour2>=1/60 and i==0:
                hour2_=hour2-1/60
                if round((hour2_-int(hour2_))*60)==60:
                    hour2_=hour2_+1;min2=0
                else:min2=round((hour2_-int(hour2_))*60)
                print("ASTRONOMICAL   TWILIGHT :",int(hour2_),"h",min2,"m")
                foundtext=""
            if tablealt_[i]>=-5.5 and TABLEALT[i]<-5.5 and hour2>=1/60 and i==0:
                hour2_=hour2-1/60
                if round((hour2_-int(hour2_))*60)==60:
                    hour2_=hour2_+1;min2=0
                else:min2=round((hour2_-int(hour2_))*60)
                print("NAUTICAL       TWILIGHT :",int(hour2_),"h",min2,"m")
                foundtext=""
            if tablealt_[i]>=-11.5 and TABLEALT[i]<-11.5 and hour2>=1/60 and i==0:
                hour2_=hour2-1/60
                if round((hour2_-int(hour2_))*60)==60:
                    hour2_=hour2_+1;min2=0
                else:min2=round((hour2_-int(hour2_))*60)
                print("ASTRONOMICAL   TWILIGHT :",int(hour2_),"h",min2,"m")
                foundtext=""
            if tablealt_[i]>=-17.5 and TABLEALT[i]<-17.5 and hour2>=1/60 and i==0:
                hour2_=hour2-1/60
                if round((hour2_-int(hour2_))*60)==60:
                    hour2_=hour2_+1;min2=0
                else:min2=round((hour2_-int(hour2_))*60)
                print("               NIGHT    :",int(hour2_),"h",min2,"m")
                foundtext=""
        #===========
            i=i+1
        tableplname_=TABLEPLNAME;tablealt_=TABLEALT

    # rising set 23:59!!!!
    hour2=24
    d = DSSYST - LHOUR/24 + 1
    timedelta_=timedelta(days=1)
    ldtime=datetime.datetime(LYEAR, LMONTH, LDAY , 0 , 0 , 0)
    ldtime=ldtime+timedelta_
    ldtime_=ldtime.strftime("%Y-%m-%d %H:%M:%S")
    lday=int(ldtime_[8:10])
    lmonth=int(ldtime_[5:7])
    lyear=int(ldtime_[0:4])
    day,month,year,hour=localtoutc(lday,lmonth,lyear,0,0,0)
    mjd_=mjdf(day,month,year,hour)
    lmst=lmstf(mjd_,MYLON)
    ssystem(d,0,lmst,"p",-1)
    i=0
    for line in TABLEPLNAME:
        if tablealt_[i]<0 and TABLEALT[i]>=0 and hour2>=1/60:
            print(TABLEPLNAME[i].ljust(14),"rise     :",23,"h",59,"m")
            foundtext=""            
        if tablealt_[i]>=0 and TABLEALT[i]<0 and hour2>=1/60:
            print(TABLEPLNAME[i].ljust(14),"set      :",23,"h",59,"m")
            foundtext=""
    #sumerki 23:59!
        if tablealt_[i]<-5.5 and TABLEALT[i]>=-5.5 and hour2>=1/60 and i==0:
            print("CIVIL          TWILIGHT :",23,"h",59,"m")
            foundtext=""                        
        if tablealt_[i]<-11.5 and TABLEALT[i]>=-11.5 and hour2>=1/60 and i==0:
            print("NAUTICAL       TWILIGHT :",23,"h",59,"m")
            foundtext=""                        
        if tablealt_[i]<-17.5 and TABLEALT[i]>=-17.5 and hour2>=1/60 and i==0:
            print("ASTRONOMICAL   TWILIGHT :",23,"h",59,"m")
            foundtext=""                        
        if tablealt_[i]>=-5.5 and TABLEALT[i]<-5.5 and hour2>=1/60 and i==0:
            print("NAUTICAL       TWILIGHT :",23,"h",59,"m")
            foundtext=""                        
        if tablealt_[i]>=-11.5 and TABLEALT[i]<-11.5 and hour2>=1/60 and i==0:
            print("ASTRONOMICAL   TWILIGHT :",23,"h",59,"m")
            foundtext=""                        
        if tablealt_[i]>=-17.5 and TABLEALT[i]<-17.5 and hour2>=1/60 and i==0:
            print("               NIGHT    :",23,"h",59,"m")
            foundtext=""                        
        #===========
        i=i+1
    NOPRINT=0
    NOPAINT=0
    if foundtext!="": print(foundtext)     
    print()
#====================================================================
# =============Rise Set 2
def riseset2(ra,dec,alt_,hh,mm,rcalc,objnum):
    def utctolocal(year,month,day,h,m,s):
        if m==60: m=0;h=h+1
        if h==24: h=0
        ldtime=datetime.datetime(year, month, day , h , m , s)
        ldtime=ldtime+TIMEDELTA_
        ldtime_=ldtime.strftime("%Y-%m-%d %H:%M:%S")
        lday=int(ldtime_[8:10])
        lmonth=int(ldtime_[5:7])
        lyear=int(ldtime_[0:4])
        lhour=int(ldtime_[11:13])
        lmin=int(ldtime_[14:16])
        lsek=int(ldtime_[17:19])
        return(lyear,lmonth,lday,lhour,lmin,lsek)

    def calckulm(ra):
        n=int(LSUN/pi2)
        LSUN_=LSUN-n*pi2
        gmst0=LSUN_*d180pi+180
        if gmst0<0: gmst0=gmst0+360
        if gmst0>=360: gmst0=gmst0-360
        ut_south = ( ra*15 - gmst0 + MYLON ) / 15.0
        if ut_south<0:
            while(ut_south<0):
                ut_south=ut_south+24
        if ut_south>=24:
            while(ut_south>=24):
                ut_south=ut_south-24
        kulmh=int(ut_south);kulmm=int(round(frac(ut_south)*60,0))
        lyear,lmonth,lday,lhour,lmin,lsek=utctolocal(LYEAR,LMONTH,LDAY,kulmh,kulmm,0)
        return(lhour,lmin,ut_south)
        
    global NOPRINT, NOPAINT
    NOPRINT=1; NOPAINT=1

    rish="-";rism="-";kulmh="-";kulmm="-";seth="-";setm="-"

    kulmh,kulmm,ut_south0=calckulm(ra)
    ssystem(-1+DSSYST - LHOUR/24 + kulmh/24 + kulmm/1440,0,0,"p",0) #for calc LSUN for d-1
    kulmh,kulmm,ut_south0=calckulm(ra)

    kulmh,kulmm,ut_south2=calckulm(ra)
    ssystem(1+DSSYST - LHOUR/24 + kulmh/24 + kulmm/1440,0,0,"p",0) #for calc LSUN for d+1
    kulmh,kulmm,ut_south2=calckulm(ra)

    kulmh,kulmm,ut_south=calckulm(ra)
    ssystem(DSSYST - LHOUR/24 + kulmh/24 + kulmm/1440,0,0,"p",0) #for calc LSUN for d
    kulmh,kulmm,ut_south=calckulm(ra)
    kulmtime=kulmh+kulmm/60
    kulmh=str(kulmh);kulmm=str(kulmm)
    
    day,month,year,hour=localtoutc(LDAY,LMONTH,LYEAR,hh,mm,0)
    mjd_=mjdf(day,month,year,hour)
    lmst=lmstf(mjd_,MYLON)
    d = DSSYST - LHOUR/24 + hh/24 + mm/1440
    #d=DSSYST-LHOUR/24+0.5
    ssystem(d,0,lmst,rcalc,objnum)

    coslha=(sin(alt_*pid180)-sin(KPOL*MYLAT*pid180)*sin(dec*pid180))/(cos(KPOL*MYLAT*pid180)*cos(dec*pid180))

    if abs(coslha)<=1:
        lha=acos(coslha)

        ris_=pvminus(ut_south,lha*d180pi/15.04107)      #15.04107
        rish=int(ris_);rism=int(round(frac(ris_)*60,0))
        lyear,lmonth,lday,lhour,lmin,lsek=utctolocal(LYEAR,LMONTH,LDAY,rish,rism,0)
        rish=str(lhour);rism=str(lmin)
        ristime=lhour+lmin/60

        set_=pvplus(ut_south,lha*d180pi/15.04107)   #15.04107
        seth=int(set_);setm=int(round(frac(set_)*60,0))
        lyear,lmonth,lday,lhour,lmin,lsek=utctolocal(LYEAR,LMONTH,LDAY,seth,setm,0)
        seth=str(lhour);setm=str(lmin)
        settime=lhour+lmin/60
        
        if ristime>settime and ristime<kulmtime:
            set_=pvplus(ut_south0,lha*d180pi/15.04107)   #15.04107
            seth=int(set_);setm=int(round(frac(set_)*60,0))
            lyear,lmonth,lday,lhour,lmin,lsek=utctolocal(LYEAR,LMONTH,LDAY,seth,setm,0)
            seth=str(lhour);setm=str(lmin)

        if settime>kulmtime and settime<ristime:
            ris_=pvminus(ut_south2,lha*d180pi/15.04107)      #15.04107
            rish=int(ris_);rism=int(round(frac(ris_)*60,0))
            lyear,lmonth,lday,lhour,lmin,lsek=utctolocal(LYEAR,LMONTH,LDAY,rish,rism,0)
            rish=str(lhour);rism=str(lmin)

    NOPRINT=0; NOPAINT=0
    return(rish,rism,kulmh,kulmm,seth,setm)
#==============================================================================
def riseset_iter(i,rcalc):
    def radecdb(rcalc):
        if rcalc=="p":ra=planetdb[i].ra; dec=planetdb[i].dec
        elif rcalc=="pa":ra=asterdb[i].ra; dec=asterdb[i].dec
        elif rcalc=="pc":ra=cometdb[i].ra; dec=cometdb[i].dec
        return(ra,dec)
    global NOPRINT, NOPAINT
    NOPRINT=1; NOPAINT=1

    alt_=-0.583
    if (i==0 or i==1) and rcalc=="p": alt_=alt_-0.25
    kulmh2="-"; kulmh3="-"; kulmh4="-"; kulmh5="-";

    hh=12; mm=0
    day,month,year,hour=localtoutc(LDAY,LMONTH,LYEAR,hh,mm,0)
    mjd_=mjdf(day,month,year,hour)
    lmst=lmstf(mjd_,MYLON)
    d = DSSYST - LHOUR/24 + hh/24 + mm/1440
    ssystem(d,0,lmst,rcalc,i)
    
    ra,dec=radecdb(rcalc)
    ra1=ra; dec1=dec
    rish,rism,kulmh1,kulmm1,seth,setm=riseset2(ra,dec,alt_,hh,mm,rcalc,i)
    if kulmh1!="-":
        ra,dec=radecdb(rcalc)
        hh=int(kulmh1) ;mm=int(kulmm1)
        rish,rism,kulmh2,kulmm2,seth,setm=riseset2(ra,dec,alt_,hh,mm,rcalc,i)
    if kulmh2!="-":
        if abs(int(kulmh2)-int(kulmh1))<12:
            ra,dec=radecdb(rcalc)
            hh=int(kulmh2); mm=int(kulmm2)
            rish,rism,kulmh3,kulmm3,seth,setm=riseset2(ra,dec,alt_,hh,mm,rcalc,i)
    if kulmh3!="-":
        if abs(int(kulmh3)-int(kulmh2))<12:
            ra,dec=radecdb(rcalc)
            hh==int(kulmh3); mm=int(kulmm3)
            rish,rism,kulmh4,kulmm4,seth,setm=riseset2(ra,dec,alt_,hh,mm,rcalc,i)
    if kulmh4!="-":
        if abs(int(kulmh4)-int(kulmh3))<12:
            ra,dec=radecdb(rcalc)
            hh==int(kulmh4); mm=int(kulmm4)
            rish,rism,kulmh5,kulmm5,seth,setm=riseset2(ra,dec,alt_,hh,mm,rcalc,i)
    if kulmh5!="-":
        if abs(int(kulmh5)-int(kulmh4))<12:
            kulmh_=kulmh5; kulmm_=kulmm5
        else: kulmh_="-"; kulmm_="-"
    else: kulmh_="-"; kulmm_="-"

    rish2="-"; rish3="-"; rish4="-"; rish5="-";
    hh=12;mm=0
    ra=ra1; dec=dec1
    rish1,rism1,kulmh,kulmm,seth,setm=riseset2(ra,dec,alt_,hh,mm,rcalc,i)
    if rish1!="-":
        ra,dec=radecdb(rcalc)
        hh=int(rish1); mm=int(rism1)
        rish2,rism2,kulmh,kulmm,seth,setm=riseset2(ra,dec,alt_,hh,mm,rcalc,i)
    if rish2!="-":
        if abs(int(rish2)-int(rish1))<12:
            ra,dec=radecdb(rcalc)
            hh=int(rish2); mm=int(rism2)
            rish3,rism3,kulmh,kulmm,seth,setm=riseset2(ra,dec,alt_,hh,mm,rcalc,i)
    if rish3!="-":
        if abs(int(rish3)-int(rish2))<12:
            ra,dec=radecdb(rcalc)
            hh=int(rish3); mm=int(rism3)
            rish4,rism4,kulmh,kulmm,seth,setm=riseset2(ra,dec,alt_,hh,mm,rcalc,i)
    if rish4!="-":
        if abs(int(rish4)-int(rish3))<12:
            ra,dec=radecdb(rcalc)
            hh=int(rish4); mm=int(rism4)
            rish5,rism5,kulmh,kulmm,seth,setm=riseset2(ra,dec,alt_,hh,mm,rcalc,i)
    if rish5!="-":
        if abs(int(rish5)-int(rish4))<12:
            rish_=rish5; rism_=rism5
        else: rish_="-"; rism_="-"
    else: rish_="-"; rism_="-"

    seth2="-"; seth3="-"; seth4="-"; seth5="-"
    hh=12;mm=0
    ra=ra1; dec=dec1
    rish,rism,kulmh,kulmm,seth1,setm1=riseset2(ra,dec,alt_,hh,mm,rcalc,i)
    if seth1!="-":
        ra,dec=radecdb(rcalc)
        hh=int(seth1); mm=int(setm1)
        rish,rism,kulmh,kulmm,seth2,setm2=riseset2(ra,dec,alt_,hh,mm,rcalc,i)
    if seth2!="-":
        if abs(int(seth2)-int(seth1))<12:
            ra,dec=radecdb(rcalc)
            hh=int(seth2); mm=int(setm2)
            rish,rism,kulmh,kulmm,seth3,setm3=riseset2(ra,dec,alt_,hh,mm,rcalc,i)
    if seth3!="-":
        if abs(int(seth3)-int(seth2))<12:
            ra,dec=radecdb(rcalc)
            hh=int(seth3); mm=int(setm3)
            rish,rism,kulmh,kulmm,seth4,setm4=riseset2(ra,dec,alt_,hh,mm,rcalc,i)
    if seth4!="-":
        if abs(int(seth4)-int(seth3))<12:
            ra,dec=radecdb(rcalc)
            hh=int(seth4); mm=int(setm4)
            rish,rism,kulmh,kulmm,seth5,setm5=riseset2(ra,dec,alt_,hh,mm,rcalc,i)
    if seth5!="-":
        if abs(int(seth5)-int(seth4))<12:
            seth_=seth5; setm_=setm5
        else:  seth_="-"; setm_="-"
    else: seth_="-"; setm_="-"

    if rish_=="-":strrise="-"
    else: strrise=rish_+"h "+rism_+"m"
    if kulmh_=="-":strkulm="-"
    else: strkulm=kulmh_+"h "+kulmm_+"m"
    if seth_=="-":strset="-"
    else: strset=seth_+"h "+setm_+"m"
    print("RISE: "+strrise+"  CULM: "+strkulm+"  SET: "+strset)
    NOPRINT=0; NOPAINT=0
#==============================================================================
# Coord precess
def ekv2000toekv(ra,dec):
    x = cos(ra*15*pid180) * cos(dec*pid180)
    y = sin(ra*15*pid180) * cos(dec*pid180)
    z = sin(dec*pid180)
    u=PMAT[0]*x+PMAT[1]*y+PMAT[2]*z
    v=PMAT[3]*x+PMAT[4]*y+PMAT[5]*z
    w=PMAT[6]*x+PMAT[7]*y+PMAT[8]*z
    x=u;y=v;z=w
    if x==0:x=0.00001
    r = atan(y/x)
    if x < 0 : ra_ = r + pi
    if x > 0 : ra_ = r + pi2
    ra_=ra_*d180pi/15
    if ra_>=24:ra_=ra_-24
    dec_ = d180pi*asin(z)
    return(ra_,dec_)
#==============================================================================
def ekvtoekv2000(ra,dec):
    x = cos(ra*15*pid180) * cos(dec*pid180)
    y = sin(ra*15*pid180) * cos(dec*pid180)
    z = sin(dec*pid180)
    u=PMAT2[0]*x+PMAT2[1]*y+PMAT2[2]*z
    v=PMAT2[3]*x+PMAT2[4]*y+PMAT2[5]*z
    w=PMAT2[6]*x+PMAT2[7]*y+PMAT2[8]*z
    x=u;y=v;z=w
    if x==0:x=0.00001
    r = atan(y/x)
    if x < 0 : ra_ = r + pi
    if x > 0 : ra_ = r + pi2
    ra_=ra_*d180pi/15
    if ra_>=24:ra_=ra_-24
    dec_ = d180pi*asin(z)
    return(ra_,dec_)
#==============================================================================
def ekvtoekv1875(ra,dec):
    x = cos(ra*15*pid180) * cos(dec*pid180)
    y = sin(ra*15*pid180) * cos(dec*pid180)
    z = sin(dec*pid180)
    u=PMAT1875[0]*x+PMAT1875[1]*y+PMAT1875[2]*z
    v=PMAT1875[3]*x+PMAT1875[4]*y+PMAT1875[5]*z
    w=PMAT1875[6]*x+PMAT1875[7]*y+PMAT1875[8]*z
    x=u;y=v;z=w
    if x==0:x=0.00001
    r = atan(y/x)
    if x < 0 : ra_ = r + pi
    if x > 0 : ra_ = r + pi2
    ra_=ra_*d180pi/15
    if ra_>=24:ra_=ra_-24
    dec_ = d180pi*asin(z)
    return(ra_,dec_)
#==============================================================================
def pmot(pv,sk,dpv,dsk,d_year):
    dpv_=d_year*dpv/3600/15
    dsk_=d_year*dsk/3600
    pv_=pvplus(pv,dpv_)
    pv_,sk_=sklplus(pv_,sk,dsk_)
    return(pv_,sk_)
def nuta(pv,sk):
    if abs(sk)<85:
        cosalp=cos(pid180*pv); sinalp=sin(pid180*pv); tandel=tan(pid180*sk)
        dpvnut=d180pi/15*((SCOSEPS+SSINEPS*sinalp*tandel)*SDPSI-(cosalp*tandel)*SDEPS)
        dsknut=d180pi*(SSINEPS*cosalp*SDPSI+sinalp*SDEPS)
        pv_=pvplus(pv,dpvnut)
        pv_,sk_=sklplus(pv_,sk,dsknut)
    else: pv_=pv; sk_=sk
    return(pv_,sk_)
#==============================================================================
#KARTA V KONICESKOY PROEKCII
def smap(d):
    global SEPS,SCOSEPS,SSINEPS,SDPSI,SDEPS
    SEPS,SCOSEPS,SSINEPS,SDPSI,SDEPS=calcecl(d)
    d_year=YEAR+MONTH/12+DAY/365.25-2000
    #===Constellation boundaries
    #if NOPRINT==0:print("Constellation boundaries")
    for i in range(0,6575-1):
        line1=constbun[i]
        pv1=float(line1[0:10])
        sk1=float(line1[11:22])
        pv1,sk1=ekv2000toekv(pv1,sk1)
        constnum1=line1[23:26]
        line2=constbun[i+1]
        pv2=float(line2[0:10])
        sk2=float(line2[11:22])
        pv2,sk2=ekv2000toekv(pv2,sk2)
        constnum2=line2[23:26]
        if constnum1==constnum2:
            lineekv(pv1,sk1,pv2,sk2,1,constbuncolor,0)

    #===Deep sky objects 1
    #if NOPRINT==0:print("Deep sky objects")
    if ZOOM<ZOOMDSO2:
        i=0
        for dso1 in dso1db:
            dso1db[i].ra,dso1db[i].dec=ekv2000toekv(dso1db[i].ra2000,dso1db[i].dec2000)
            dso1db[i].ra,dso1db[i].dec=nuta(dso1db[i].ra,dso1db[i].dec)
            if dso1db[i].sz1==0 and dso1db[i].sz1==0: size=0.25
            elif dso1db[i].sz1==0 or (dso1db[i].sz1<dso1db[i].sz2 and dso1db[i].sz2!=0): size=dso1db[i].sz2/60
            elif dso1db[i].sz2==0 or (dso1db[i].sz2<dso1db[i].sz1 and dso1db[i].sz1!=0): size=dso1db[i].sz1/60
            #else: size=(dso1db[i].sz1+dso1db[i].sz2)/2/60
            strtag="dso1_"+str(i)
            x,y,rokr,ugv=ovalekv(dso1db[i].nam1,dso1db[i].ra,dso1db[i].dec,size,0,dsocolor,0,1,strtag)
            dso1db[i].x=x
            dso1db[i].y=y
            if dso1db[i].m=="": m=0
            else: m=float(dso1db[i].m)
            ky=-1
            if dso1db[i].nam1[len(dso1db[i].nam1)-1]=="B": ky=1
            if ZOOM>=2 and ZOOM<5 and m<=7: stext(x,y,0,ky*(rokr+10),dso1db[i].nam1,dsotextcolor,font1,strtag)
            elif ZOOM>=5: stext(x,y,0,ky*(rokr+10),dso1db[i].nam1,dsotextcolor,font1,strtag)
            i=i+1
          
    #===Deep sky objects 2
    #if NOPRINT==0:print("Deep sky objects")
    if ZOOM>=ZOOMDSO2:
        i=0
        for dso2 in dso2db:
            dso2db[i].ra,dso2db[i].dec=ekv2000toekv(dso2db[i].ra2000,dso2db[i].dec2000)
            dso2db[i].ra,dso2db[i].dec=nuta(dso2db[i].ra,dso2db[i].dec)
            if dso2db[i].sz1==0 and dso2db[i].sz1==0: size=1/60
            elif dso2db[i].sz1==0 or (dso2db[i].sz1<dso2db[i].sz2 and dso2db[i].sz2!=0): size=dso2db[i].sz2/60
            elif dso2db[i].sz2==0 or (dso2db[i].sz2<dso2db[i].sz1 and dso2db[i].sz1!=0): size=dso2db[i].sz1/60
            #else: size=(dso2db[i].sz1+dso2db[i].sz2)/2/60
            strtag="dso2_"+str(i)
            x,y,rokr,ugv=ovalekv(dso2db[i].nam1,dso2db[i].ra,dso2db[i].dec,size,0,dsocolor,0,1,strtag)
            dso2db[i].x=x
            dso2db[i].y=y
            if dso2db[i].m=="": m=0
            else: m=float(dso2db[i].m)
            ky=-1
            if dso2db[i].nam1[len(dso2db[i].nam1)-1]=="B": ky=1
            if (ZOOM>=ZOOMDSO2 and ZOOM<ZOOMDSO2+10 and m<=12) or (ZOOM>=ZOOMDSO2+10 and ZOOM<ZOOMDSO2+20 and m<=13.5): stext(x,y,0,ky*(rokr+10),dso2db[i].nam1,dsotextcolor,font1,strtag)
            elif ZOOM>=ZOOMDSO2+20: stext(x,y,0,ky*(rokr+10),dso2db[i].nam1,dsotextcolor,font1,strtag)
            i=i+1

    #===Constellation lines
    #if NOPRINT==0:print("Constellation lines")
    for line in clkoord:
        pv1=float(line[0:8])
        sk1=float(line[9:17])
        pv1,sk1=pmot(pv1,sk1,float(line[36:42]),float(line[43:49]),d_year)
        pv1,sk1=ekv2000toekv(pv1,sk1)
        pv1,sk1=nuta(pv1,sk1)
        pv2=float(line[18:26])
        sk2=float(line[27:35])
        pv2,sk2=pmot(pv2,sk2,float(line[50:56]),float(line[57:63]),d_year)
        pv2,sk2=ekv2000toekv(pv2,sk2)
        pv2,sk2=nuta(pv2,sk2)
        lineekv(pv1,sk1,pv2,sk2,1,constlincolor,0)

    #===Constellation labels
    #if NOPRINT==0:print("Constellation labels")
    i=0
    for constlab in constlabdb:
        ra,dec=ekv2000toekv(constlabdb[i].pv,constlabdb[i].sk)
        ra,dec=nuta(ra,dec)
        constlabdb[i].pv2=ra
        constlabdb[i].sk2=dec
        x,y,z=calcxyzpolm(ra,KPOL*dec,LMST,ZOOM,KPOL)
        prvt,sklt,zz=povorot(x,y,z,TURN_ANGLE)
        x,y=calcxycon(prvt,sklt,ZOOM)
        constlabdb[i].x=x
        constlabdb[i].y=y
        strtag="constellation"+str(i)
        stext(x,y,0,0,constlabdb[i].name2,constlabcolor,font2,strtag)
        i=i+1
        
    def stars():
        #===BSC stars
        #if NOPRINT==0:print("Bright Star Catalogue")    
        #i=0
        root.update()
        i=int(len(stardb)/24*pvminus(RA_CANV2000,6))
        for star in stardb:
            if stardb[i].m<8:

                ra2000_,dec2000_=pmot(stardb[i].ra2000,stardb[i].dec2000,stardb[i].pmra,stardb[i].pmdec,d_year)
                prv,skl=ekv2000toekv(ra2000_,dec2000_)
                prv,skl=nuta(prv,skl)
                
                stardb[i].ra=prv; stardb[i].dec=skl;
                x,y,z=calcxyzpolm(prv,KPOL*skl,LMST,ZOOM,KPOL)
                prvt,sklt,zz=povorot(x,y,z,TURN_ANGLE) 
                x,y=calcxycon(prvt,sklt,ZOOM)            
                stardb[i].x=x; stardb[i].y=y;
                #if zz>=0:  #Рисовать только звезды над горизонтом
                #if zz!=9999999:   #Рисовать все звезды
                if x>-10 and y>-10 and x<ZOOM*RCANV+10 and y<ZOOM*RCANV+10:
                    w=8-round(stardb[i].m,0)
                    if ZOOM>=ZOOMHIP or ZOOM>=ZOOMSAO:w=w+2
                    if ZOOM<3:w=w-1
                    if stardb[i].sp[2]=="W" or stardb[i].sp[2]=="O":starcolor1="deepskyblue"
                    elif stardb[i].sp[2]=="B":starcolor1="lightblue"
                    elif stardb[i].sp[2]=="A":starcolor1="white"
                    elif stardb[i].sp[2]=="F":starcolor1="yellow"
                    elif stardb[i].sp[2]=="G":starcolor1="gold"
                    elif stardb[i].sp[2]=="K":starcolor1="orange"
                    elif stardb[i].sp[2]=="M":starcolor1="red"
                    elif stardb[i].sp[2]=="L" or stardb[i].sp[2]=="T":starcolor1="darkred"
                    else: starcolor1=starcolor
                    strtag="bstar"+str(i)
                    if (ZOOM<ZOOMHIP and ZOOM<ZOOMSAO) or abs(d_year)<100:
                        if w>2:
                            ovalxy2(x,y,w/2,w/2,starcolor1,starcolor1,1,strtag)
                            if stardb[i].dbldm!=99:
                                linexy2(x,y,-w,0,w,0,1,starcolor1,strtag)
                            #canvas.create_oval([x-w/2,y-w/2],[x+w/2,y+w/2],outline=starcolor1,fill=starcolor1,tag="bstar"+str(i))
                        elif w==2:
                            linexy2(x,y,-1,0,1,0,2,starcolor1,strtag)
                            #canvas.create_line(x-1,y,x+1,y,width=2,fill=starcolor1,tag="bstar"+str(i))
                        else:
                            linexy2(x,y,0,0,1,0,1,starcolor1,strtag)
                            #canvas.create_line(x,y,x+1,y,width=1,fill=starcolor1,tag="bstar"+str(i))
                    else: stext(x,y,0,0,"b",textcolor,"Arial 6",strtag)
                    if float(stardb[i].m)<3.75+ZOOM/4:
                        stext(x,y,0,-12,stardb[i].mapname,textcolor,font1,strtag)#canvas.create_text(x,y-12,text=strn,fill=textcolor)
            i=i+1
            if i==len(stardb): i=0
    
    #===============
    if STARPOTOK==1:
        thread_smap = threading.Thread(target=stars, name="smap")
        thread_smap.start()
    else: stars()

    #===Stars HIPPARCOS
    if ZOOM>=ZOOMHIP: hippaint(0)
    if ZOOM>=ZOOMSAO: saopaint(0)
#=========================================================
#===Stars HIPPARCOS
def hippaint(event):
    global HIPSAO_IJ
    if ZOOM>=ZOOMHIP:
        d_year=YEAR+MONTH/12+DAY/365.25-2000
        qx=canvas.xview()
        qy=canvas.yview()
        az,alt=calcaz_xycanv((qx[0]+qx[1])/2*ZOOM*RCANV+POPRXY,(qy[0]+qy[1])/2*ZOOM*RCANV+POPRXY)
        ra_canv,dec_canv=calcekv(az,alt,LMST)
        ra_canv,dec_canv=ekvtoekv2000(ra_canv,dec_canv) # ra_canv,dec_canv to 2000 !!!

        if abs(dec_canv)>=60:
            ra1=0; ra2=23; ra0=0
        else:
            ra1=0
            ra2=5
            ra0=pvminus(int(ra_canv),3)

        dec1=dec_canv-20
        dec2=dec_canv+20
        if dec1<=-90: dec1=-89
        if dec2>=90: dec2=89
    
        for i_ in range(ra1,ra2+1):
            i=pvplus(ra0,i_)
            for j in range(int(dec1/10)+8,int(dec2/10)+8+1):
                if HIPSAO_IJ[i][j]==0:
                    HIPSAO_IJ[i][j]=1
                    for k in range(0,len(starhipdb[i][j])):

                        if starhipdb[i][j][k].m<99:

                            ra2000_,dec2000_=pmot(starhipdb[i][j][k].ra2000,starhipdb[i][j][k].dec2000,starhipdb[i][j][k].pmra,starhipdb[i][j][k].pmdec,d_year)
                            prv,skl=ekv2000toekv(ra2000_,dec2000_)
                            prv,skl=nuta(prv,skl)
                            
                            starhipdb[i][j][k].ra=prv; starhipdb[i][j][k].dec=skl
                            x,y,z=calcxyzpolm(prv,KPOL*skl,LMST,ZOOM,KPOL)
                            prvt,sklt,zz=povorot(x,y,z,TURN_ANGLE) 
                            x,y=calcxycon(prvt,sklt,ZOOM)            
                            starhipdb[i][j][k].x=x; starhipdb[i][j][k].y=y;
                            if x>-10 and y>-10 and x<ZOOM*RCANV+10 and y<ZOOM*RCANV+10:
                                w=10-round(starhipdb[i][j][k].m,0)
                                if starhipdb[i][j][k].sp[0]=="W" or starhipdb[i][j][k].sp[0]=="O":starcolor1="deepskyblue"
                                elif starhipdb[i][j][k].sp[0]=="B":starcolor1="lightblue"
                                elif starhipdb[i][j][k].sp[0]=="A":starcolor1="white"
                                elif starhipdb[i][j][k].sp[0]=="F":starcolor1="yellow"
                                elif starhipdb[i][j][k].sp[0]=="G":starcolor1="gold"
                                elif starhipdb[i][j][k].sp[0]=="K":starcolor1="orange"
                                elif starhipdb[i][j][k].sp[0]=="M":starcolor1="red"
                                elif starhipdb[i][j][k].sp[0]=="L" or starhipdb[i][j][k].sp[0]=="T":starcolor1="darkred"
                                else: starcolor1=starcolor
                                if i>9: ii=str(i)
                                else: ii="0"+str(i)
                                if j>9: jj=str(j)
                                else: jj="0"+str(j)
                                strtag="starhip"+ii+jj+str(k)
                                if w>2:
                                    ovalxy2(x,y,w/2,w/2,starcolor1,starcolor1,1,strtag)
                                    if starhipdb[i][j][k].dblcomp!="":
                                        linexy2(x,y,-w,0,w,0,1,starcolor1,strtag)
                                elif w==2:
                                    linexy2(x,y,-1,0,1,0,2,starcolor1,strtag)
                                else:
                                    linexy2(x,y,0,0,1,0,1,starcolor1,strtag)
#===============================================================================
#===Stars SAO
def saopaint(event):
    global HIPSAO_IJ
    if ZOOM>=ZOOMSAO:
        d_year=YEAR+MONTH/12+DAY/365.25-2000
        qx=canvas.xview()
        qy=canvas.yview()
        az,alt=calcaz_xycanv((qx[0]+qx[1])/2*ZOOM*RCANV+POPRXY,(qy[0]+qy[1])/2*ZOOM*RCANV+POPRXY)
        ra_canv,dec_canv=calcekv(az,alt,LMST)
        ra_canv,dec_canv=ekvtoekv2000(ra_canv,dec_canv) # ra_canv,dec_canv to 2000 !!!

        if abs(dec_canv)>=60:
            ra1=0; ra2=23; ra0=0
        else:
            ra1=0
            ra2=5
            ra0=pvminus(int(ra_canv),3)

        dec1=dec_canv-20
        dec2=dec_canv+20
        if dec1<=-90: dec1=-89
        if dec2>=90: dec2=89
    
        for i_ in range(ra1,ra2+1):
            i=pvplus(ra0,i_)
            for j in range(int(dec1/10)+8,int(dec2/10)+8+1):
                if HIPSAO_IJ[i][j]==0:
                    HIPSAO_IJ[i][j]=1
                    for k in range(0,len(starsaodb[i][j])):
                        if starsaodb[i][j][k].m<99: starmagn=starsaodb[i][j][k].m
                        else: starmagn=starsaodb[i][j][k].pmag
                        #if starmagn<99:
                        ra2000_,dec2000_=pmot(starsaodb[i][j][k].ra2000,starsaodb[i][j][k].dec2000,starsaodb[i][j][k].pmra,starsaodb[i][j][k].pmdec,d_year)
                        prv,skl=ekv2000toekv(ra2000_,dec2000_)
                        prv,skl=nuta(prv,skl)

                        starsaodb[i][j][k].ra=prv; starsaodb[i][j][k].dec=skl
                        x,y,z=calcxyzpolm(prv,KPOL*skl,LMST,ZOOM,KPOL)
                        prvt,sklt,zz=povorot(x,y,z,TURN_ANGLE) 
                        x,y=calcxycon(prvt,sklt,ZOOM)            
                        starsaodb[i][j][k].x=x; starsaodb[i][j][k].y=y;
                        if x>-10 and y>-10 and x<ZOOM*RCANV+10 and y<ZOOM*RCANV+10:
                            w=10-round(starmagn,0)
                            if starsaodb[i][j][k].sp[0]=="W" or starsaodb[i][j][k].sp[0]=="O":starcolor1="deepskyblue"
                            elif starsaodb[i][j][k].sp[0]=="B":starcolor1="lightblue"
                            elif starsaodb[i][j][k].sp[0]=="A":starcolor1="white"
                            elif starsaodb[i][j][k].sp[0]=="F":starcolor1="yellow"
                            elif starsaodb[i][j][k].sp[0]=="G":starcolor1="gold"
                            elif starsaodb[i][j][k].sp[0]=="K":starcolor1="orange"
                            elif starsaodb[i][j][k].sp[0]=="M":starcolor1="red"
                            elif starsaodb[i][j][k].sp[0]=="L" or starsaodb[i][j][k].sp[0]=="T":starcolor1="darkred"
                            else: starcolor1=starcolor
                            if i>9: ii=str(i)
                            else: ii="0"+str(i)
                            if j>9: jj=str(j)
                            else: jj="0"+str(j)
                            strtag="starsao"+ii+jj+str(k)
                            if w>2:
                                ovalxy2(x,y,w/2,w/2,starcolor1,starcolor1,1,strtag)
                                #if starhipdb[i][j][k].dblcomp!="":
                                #    linexy2(x,y,-w,0,w,0,1,starcolor1,strtag)
                            elif w==2:
                                linexy2(x,y,-1,0,1,0,2,starcolor1,strtag)
                            else:
                                linexy2(x,y,0,0,1,0,1,starcolor1,strtag)
#=========================================================
# рисование азимутальной сетки в конической проекции  AZ SETKA V KONICESKOY
def risgridconaz():
    #if NOPRINT==0:print("Azimuthal grid")
    
    prvpol=-(pi-TURN_ANGLE)/pi*12
    if prvpol==24: prvpol=0
    if KPOL==-1:prvpol=pvplus(prvpol,12)
    
    fl2=0
    for dprv in range(0,144):
        fl=0
        prv=dprv/6
        for skl in range(0,85,5):
            x1,y1=calcxycon(pvplus(prv,prvpol),skl,ZOOM)
            x1=ZOOM*RCANV-x1

            x2,y2=calcxycon(pvplus(pvplus(prv,0.1666666667),prvpol),skl,ZOOM)
            x2=ZOOM*RCANV-x2
            fl=not fl
            if fl==1:
                linexy(x1,y1,x2,y2,1,gridcolor,"azgrid")

            x2,y2=calcxycon(pvplus(prv,prvpol),skl+5,ZOOM)
            x2=ZOOM*RCANV-x2

            if fl2==0 and skl<=75: linexy(x1,y1,x2,y2,1,gridcolor,"azgrid")

        fl2=fl2+1
        if fl2==4: fl2=0
        
    if ZOOM>=10: steppv=1;sk1=5; sk2=85;stepsk=10
    elif ZOOM>=5: steppv=2;sk1=5; sk2=85;stepsk=10
    else:       steppv=3;sk1=15;sk2=95;stepsk=20;
    for prv in range(0,36,steppv):
        prv_=prv*0.6666667
        for skl in range(sk1,sk2,stepsk):
            x,y=calcxycon(pvplus(prv_,prvpol),skl,ZOOM)
            x=ZOOM*RCANV-x
            ovalxy2(x,y,12,12,skycolor,skycolor,1,"azgrid")
            stext(x,y,0,0,int(prv_*15),gridcolor,font1,"azgrid")
            if (skl+5)<80:
                x,y=calcxycon(pvplus(pvplus(prv_,1),prvpol),skl+5,ZOOM)
                x=ZOOM*RCANV-x
                ovalxy2(x,y,12,12,skycolor,skycolor,1,"azgrid")
                stext(x,y,0,0,skl+5,gridcolor,font1,"azgrid")

        
#=========================================================

# рисование экваториальной сетки в конической проекции EKV SETKA V KONICESKOY
def risgridconekv():
    #if NOPRINT==0:print("Equatorial grid")
    
    fl2=0
    for dprv in range(0,96):
        prv=dprv/4
        for skl in range(-80,85,5):

            if frac(skl/10)==0:
                x1,y1,x2,y2=lineekv(prv,skl,pvplus(prv,0.25),skl,1,gridcolor,0)
                
            if fl2==0 and skl<=75:
                x1,y1,x2,y2=lineekv(prv,skl,prv,skl+5,1,gridcolor,0) 
            
        fl2=fl2+1
        if fl2==4: fl2=0

    if ZOOM>=5: steppv=1; stepsk=10
    else:       steppv=2; stepsk=20;
    for prv in range(0,24,steppv):
        for skl in range(0,80,stepsk):
            x,y,z=calcxyzpolm(prv,KPOL*(skl+5),LMST,ZOOM,KPOL)
            prvt,sklt,zz=povorot(x,y,z,TURN_ANGLE)
            x,y=calcxycon(prvt,sklt,ZOOM)            
            ovalxy2(x,y,12,12,skycolor,skycolor,1,"eqgrid")
            stext(x,y,0,0,prv,gridcolor,font1,"eqgrid")

            x,y,z=calcxyzpolm(prv,-KPOL*(skl+5),LMST,ZOOM,KPOL)
            prvt,sklt,zz=povorot(x,y,z,TURN_ANGLE)
            x,y=calcxycon(prvt,sklt,ZOOM)            
            ovalxy2(x,y,12,12,skycolor,skycolor,1,"eqgrid")
            stext(x,y,0,0,prv,gridcolor,font1,"eqgrid")

            x,y,z=calcxyzpolm(prv+0.5,skl*KPOL,LMST,ZOOM,KPOL)
            prvt,sklt,zz=povorot(x,y,z,TURN_ANGLE)
            x,y=calcxycon(prvt,sklt,ZOOM)            
            ovalxy2(x,y,12,12,skycolor,skycolor,1,"eqgrid")
            stext(x,y,0,0,skl,gridcolor,font1,"eqgrid")

            x,y,z=calcxyzpolm(prv+0.5,-skl*KPOL,LMST,ZOOM,KPOL)
            prvt,sklt,zz=povorot(x,y,z,TURN_ANGLE)
            x,y=calcxycon(prvt,sklt,ZOOM)            
            ovalxy2(x,y,12,12,skycolor,skycolor,1,"eqgrid")
            stext(x,y,0,0,-skl,gridcolor,font1,"eqgrid")

#=========================================================

#рисование горизонта  RISOVANIE HORIZONTA
def rishoriz():
    #if NOPRINT==0:print("Horizon")
    
    prvpol=-(pi-TURN_ANGLE)/pi*12
    if prvpol==24: prvpol=0
    if KPOL==-1:prvpol=pvplus(prvpol,12)
    
    sklr=-0.583
    for dprv in range(0,96):
        prv=dprv/4
        x1r,y1r=calcxycon(pvplus(prv,prvpol),sklr,ZOOM)
        x2r,y2r=calcxycon(pvplus(pvplus(prv,0.25),prvpol),sklr,ZOOM)
        x1r=ZOOM*RCANV-x1r
        x2r=ZOOM*RCANV-x2r
        linexy(x1r,y1r,x2r,y2r,3,horizcolor,"horizon")

        skl=0
        x1,y1=calcxycon(pvplus(prv,prvpol),skl,ZOOM)
        x2,y2=calcxycon(pvplus(pvplus(prv,0.25),prvpol),skl,ZOOM)
        x1=ZOOM*RCANV-x1
        x2=ZOOM*RCANV-x2
        linexy(x1,y1,x2,y2,1,horizcolor,"horizon")

    skl=-0.583
    for prv in range(0,72):
        prv_=prv*0.6666667/2
        x,y=calcxycon(pvplus(prv_,prvpol),skl,ZOOM)
        x=ZOOM*RCANV-x
        if frac(round(prv_*15,0)/10)==0:
            ovalxy2(x,y,12,12,skycolor,skycolor,1,"horizon")
            stext(x,y,0,0,int(prv_*15),gridcolor,font1,"horizon")
        aznesw=int(prv_*15)
        if aznesw==0 or aznesw==45 or aznesw==90 or aznesw==135 or aznesw==180 or aznesw==225 or aznesw==270 or aznesw==315: 
            dx=0;dy=0;
            if round(y,0)<ZOOM*RCANVD2:dy=-24
            if round(y,0)>ZOOM*RCANVD2:dy=24
            if round(x,0)<ZOOM*RCANVD2:dx=-24
            if round(x,0)>ZOOM*RCANVD2:dx=24
            if aznesw==0:poltext="N"
            elif aznesw==45:poltext="NE"
            elif aznesw==90:poltext="E"
            elif aznesw==135:poltext="SE"
            elif aznesw==180:poltext="S"
            elif aznesw==225:poltext="SW"
            elif aznesw==270:poltext="W"
            elif aznesw==315:poltext="NW"
            stext(x,y,dx,dy,poltext,"red",font2,"horizon")                

    sz=90-2/ZOOM
    lineekv(0,KPOL*sz,12,KPOL*sz,1,gridcolor,0)
    lineekv(6,KPOL*sz,18,KPOL*sz,1,gridcolor,0)

    pv1,sk1=calcekv(0,sz,LMST)
    pv2,sk2=calcekv(180,sz,LMST)
    pv3,sk3=calcekv(90,sz,LMST)
    pv4,sk4=calcekv(270,sz,LMST)
    lineekv(pv1,sk1,pv2,sk2,1,gridcolor,0)
    lineekv(pv3,sk3,pv4,sk4,1,gridcolor,0)
#=================================
#====Risovanie Legenda
def legpaint():
    canvasL.delete("all")
    if ZOOM<ZOOMHIP and ZOOM<ZOOMSAO: mmax=8; canvasL.config(height=110)
    else: mmax=10; canvasL.config(height=135)
    for m in range(0,mmax):
        x=8; y=10+m*13
        w=8-round(m,0)
        if ZOOM>=ZOOMHIP or ZOOM>=ZOOMSAO: w=w+2
        if ZOOM<3:w=w-1
        if w>2:
            canvasL.create_oval([x-w/2,y-w/2],[x+w/2,y+w/2],outline=starcolor,fill=starcolor,width=1)
        elif w==2:
            canvasL.create_line(x-1,y,x+1,y,width=2,fill=starcolor)
        else:
            canvasL.create_line(x,y,x+1,y,width=1,fill=starcolor)
        canvasL.create_text(x+12,y,text=str(m),fill=textcolor,font=font4)
#=========================
#====Risovanie Ecliptika
def eclpaint(d):
    global NOPRINT, NOPAINT
    noprint=NOPRINT; nopaint=NOPAINT
    NOPRINT=1; NOPAINT=1
    masra=[]; masdec=[]
    for i in range (int(d),int(d)+366):
        ssystem(i,0,LMST,"p",0)
        masra.append(planetdb[0].ra)
        masdec.append(planetdb[0].dec)
    NOPAINT=0
    for i in range(0,len(masra)-1):
        lineekv(masra[i],masdec[i],masra[i+1],masdec[i+1],1,eclcolor,1)
    lineekv(masra[0],masdec[0],masra[len(masra)-1],masdec[len(masdec)-1],1,eclcolor,1)
    NOPRINT=noprint; NOPAINT=nopaint
    masra=[]; masdec=[]
#=========================        
# Frac !
def frac(x):
    x=x-int(x)
    if x<0:
        x=x+1
    fr=x
    return(fr)
#======Line pv skl
def lineekv(pv1,sk1,pv2,sk2,wid,col,p):
    x,y,z=calcxyzpolm(pv1,KPOL*sk1,LMST,ZOOM,KPOL)
    prvt,sklt,zz=povorot(x,y,z,TURN_ANGLE)
    x1,y1=calcxycon(prvt,sklt,ZOOM)
    x,y,z=calcxyzpolm(pv2,KPOL*sk2,LMST,ZOOM,KPOL)
    prvt,sklt,zz=povorot(x,y,z,TURN_ANGLE)
    x2,y2=calcxycon(prvt,sklt,ZOOM)
    l=sqrt((x2-x1)*(x2-x1)+(y2-y1)*(y2-y1))
    if p==0 and l<2*RADIUS*ZOOM and NOPAINT==0:
        canvas.create_line(x1,y1,x2,y2,width=wid,fill=col)
    if p==1 and l<2*RADIUS*ZOOM and NOPAINT==0:
        canvas.create_line(x1,y1,x2,y2,width=wid,fill=col,dash=(4,4))
    return(x1,y1,x2,y2)

#======Line xy
def linexy(x1,y1,x2,y2,wid,col,strtag):
    l=sqrt((x2-x1)*(x2-x1)+(y2-y1)*(y2-y1))
    if l<2*RADIUS*ZOOM and NOPAINT==0:
        canvas.create_line(x1,y1,x2,y2,width=wid,fill=col,tag=strtag)

#======Line xy2
def linexy2(x,y,dx1,dy1,dx2,dy2,wid,col,strtag):
    if NOPAINT==0:canvas.create_line(x+dx1,y+dy1,x+dx2,y+dy2,width=wid,fill=col,tag=strtag)

#=======Text canvas
def stext(x,y,dx,dy,txt,col,font_,strtag):
    if NOPAINT==0:canvas.create_text(x+dx,y+dy,text=txt,fill=col,font=font_,tag=strtag)

#=======Oval mashtabiruemiy
def ovalxy(x1,y1,x2,y2,outcol,col,wid):
    if col==0:
        if NOPAINT==0:canvas.create_oval([x1,y1],[x2,y2],outline=outcol,width=wid)
        #canvas2.create_oval([x1*m2,y1*m2],[x2*m2,y2*m2],outline=outcol,width=wid)
    else:
        if NOPAINT==0:canvas.create_oval([x1,y1],[x2,y2],outline=outcol,fill=col,width=wid)
        #canvas2.create_oval([x1*m2,y1*m2],[x2*m2,y2*m2],outline=outcol,fill=col,width=wid)

#=======Oval PRV SKL R
def ovalekv(plname,pvpl,skpl,ugld,m_,outcol,col,wid,strtag):

    """if ugld==0: ugld_=0.083
    else: ugld_=ugld
    azpl,altpl=calcaz(pvpl,skpl,LMST)
    az1=azpl;az2=azpl
    alt1=altpl-ugld_/2
    alt2=altpl+ugld_/2
    if alt2>90:
        alt2==90-(alt2-90)
        az2=ugplus(azpl,180)

    pv1,sk1=calcekv(az1,alt1)
    pv2,sk2=calcekv(az2,alt2)"""
    
    x,y,z=calcxyzpolm(pvpl,KPOL*skpl,LMST,ZOOM,KPOL)
    prvt,sklt,zz=povorot(x,y,z,TURN_ANGLE)
    xc,yc=calcxycon(prvt,sklt,ZOOM)

    if ugld==0: ugld_=0.083
    else: ugld_=ugld
    sk1=skpl-ugld_/2
    sk2=skpl+ugld_/2

    x,y,z=calcxyzpolm(pvpl,KPOL*sk1,LMST,ZOOM,KPOL)
    prvt,sklt,zz=povorot(x,y,z,TURN_ANGLE)
    x1,y1=calcxycon(prvt,sklt,ZOOM)

    x,y,z=calcxyzpolm(pvpl,KPOL*sk2,LMST,ZOOM,KPOL)
    prvt,sklt,zz=povorot(x,y,z,TURN_ANGLE)
    x2,y2=calcxycon(prvt,sklt,ZOOM)
        
    if ugld!=0:
        rokr=int(round(0.5*sqrt((x2-x1)**2+(y2-y1)**2)))    
    else:
        if ZOOM>=2:rokr=(8-round(m_,0))/2
        else: rokr=(7-round(m_,0))/2
        if ZOOM>=ZOOMHIP or ZOOM>=ZOOMSAO:rokr=rokr+1

    ugv=atan2((y2-y1),(x2-x1))  #+pid2
    if rokr<2: rokr=2
    
    x1ok=xc-rokr;x2ok=xc+rokr
    y1ok=yc-rokr;y2ok=yc+rokr
    if col==0:
        if NOPAINT==0:
            canvas.create_oval([x1ok,y1ok],[x2ok,y2ok],outline=outcol,width=wid,tag=strtag)
            #canvas2.create_oval([x1ok*m2,y1ok*m2],[x2ok*m2,y2ok*m2],outline=outcol,width=wid)
    else:
        if NOPAINT==0:
            canvas.create_oval([x1ok,y1ok],[x2ok,y2ok],outline=outcol,fill=col,width=wid,tag=strtag)
            #canvas2.create_oval([x1ok*m2,y1ok*m2],[x2ok*m2,y2ok*m2],outline=outcol,fill=col,width=wid)
    return(xc,yc,rokr,ugv)
        
#=======Oval2
def ovalxy2(x,y,dx,dy,outcol,col,wid,strtag):
    if col==0:
        if NOPAINT==0:canvas.create_oval([x-dx,y-dy],[x+dx,y+dy],outline=outcol,width=wid,tag=strtag)
        #canvas2.create_oval([x*m2-dx,y*m2-dy],[x*m2+dx,y*m2+dy],outline=outcol,width=wid)
    else:
        if NOPAINT==0:canvas.create_oval([x-dx,y-dy],[x+dx,y+dy],outline=outcol,fill=col,width=wid,tag=strtag)
        #canvas2.create_oval([x*m2-dx,y*m2-dy],[x*m2+dx,y*m2+dy],outline=outcol,fill=col,width=wid)
#================

#=============Risovanie FAZY
def faza(xc,yc,rokr,fz,pugol,fcolor,strtag):
    #fug=fz*pi
    #fug=(0.5+(1/2/(3**0.5))*tan((2*fz-1)*pi/3))*pi
    fug=acos(1-2*fz)
    mpovx=[]
    mpovz=[]
    for i in range(0,9):
        mpovx.append([])
        mpovz.append([])
    masx=[];masy=[]
    masx2=[];masy2=[]

    masx_=[];masy_=[]
    masx2_=[];masy2_=[]
    
    mpovx[0]=1;mpovx[1]=0;mpovx[2]=0
    mpovx[3]=0;mpovx[4]=cos(fug);mpovx[5]=-sin(fug)
    mpovx[6]=0;mpovx[7]=sin(fug);mpovx[8]=cos(fug)

    mpovz[0]=cos(pugol);mpovz[1]=-sin(pugol);mpovz[2]=0
    mpovz[3]=sin(pugol);mpovz[4]=cos(pugol);mpovz[5]=0
    mpovz[6]=0;mpovz[7]=0;mpovz[8]=1

    for x in range(-rokr,rokr+1):
        y=sqrt(rokr*rokr-x*x)
        masx.append(x)
        masy.append(y)
    z=0
    i=0
    for x in masx:
        y=masy[i]
        xx=mpovx[0]*x+mpovx[1]*y+mpovx[2]*z
        yy=mpovx[3]*x+mpovx[4]*y+mpovx[5]*z
        #z=mpovx[6]*x+mpovx[7]*y+mpovx[8]*z
        masx2.append(xx)
        masy2.append(yy)        
        i=i+1
    i=0
    for x in masx:
        y=masy[i]
        xx=mpovz[0]*x+mpovz[1]*y+mpovz[2]*z
        yy=mpovz[3]*x+mpovz[4]*y+mpovz[5]*z
        masx_.append(xx)
        masy_.append(yy)        
        i=i+1
    i=0
    for x in masx2:
        y=masy2[i]
        xx=mpovz[0]*x+mpovz[1]*y+mpovz[2]*z
        yy=mpovz[3]*x+mpovz[4]*y+mpovz[5]*z
        masx2_.append(xx)
        masy2_.append(yy)        
        i=i+1
    i=0
    for x in masx_:
        y=masy_[i]
        xx=masx2_[i]
        yy=masy2_[i]
        canvas.create_line(x+xc,y+yc,xx+xc,yy+yc,width=2,fill=fcolor,tag=strtag)
        i=i+1
#=============Risovanie Ring Saturn
def ringsatpaint(xc,yc,rokr,ugv,ringcolor,strtag):
    pugol=-sring.pa+pid2+ugv
    rokr1=int(round(1.28*rokr,0))
    rokr2=int(round(2.41*rokr,0))
    rokr_cassini=int(round(2.06*rokr,0))
    naklon=pid2-sring.b
    mpovx=[]
    mpovz=[]
    for i in range(0,9):
        mpovx.append([])
        mpovz.append([])
    masx=[];masy=[]
    masx2=[];masy2=[]

    mpovx[0]=1;mpovx[1]=0;mpovx[2]=0
    mpovx[3]=0;mpovx[4]=cos(naklon);mpovx[5]=-sin(naklon)
    mpovx[6]=0;mpovx[7]=sin(naklon);mpovx[8]=cos(naklon)

    mpovz[0]=cos(pugol);mpovz[1]=-sin(pugol);mpovz[2]=0
    mpovz[3]=sin(pugol);mpovz[4]=cos(pugol);mpovz[5]=0
    mpovz[6]=0;mpovz[7]=0;mpovz[8]=1

    for x in range(-rokr1,rokr1+1):
        y=sqrt(rokr1*rokr1-x*x)
        masx.append(x)
        masy.append(y)
        masx.append(x)
        masy.append(-y)
    for x in range(-rokr2,rokr2+1):
        y=sqrt(rokr2*rokr2-x*x)
        masx.append(x)
        masy.append(y)
        masx.append(x)
        masy.append(-y)
    for x in range(-rokr_cassini,rokr_cassini+1):
        y=sqrt(rokr_cassini*rokr_cassini-x*x)
        masx.append(x)
        masy.append(y)
        masx.append(x)
        masy.append(-y)
    z=0
    i=0
    for x in masx:
        y=masy[i]
        xx=mpovx[0]*x+mpovx[1]*y+mpovx[2]*z
        yy=mpovx[3]*x+mpovx[4]*y+mpovx[5]*z
        #z=mpovx[6]*x+mpovx[7]*y+mpovx[8]*z
        masx2.append(xx)
        masy2.append(yy)        
        i=i+1
    i=0
    for x in masx2:
        y=masy2[i]
        xx=mpovz[0]*x+mpovz[1]*y+mpovz[2]*z
        yy=mpovz[3]*x+mpovz[4]*y+mpovz[5]*z
        canvas.create_line(xx+xc,yy+yc,xx+xc+1,yy+yc,width=2,fill=ringcolor,tag=strtag)
        i=i+1
#=============Risovanie SATELLITE
def satpaint(plname,numsat,xc,yc,dx,dy,pugol,d,color,strtag):
    mpovz=[]
    for i in range(0,9):
        mpovz.append([])
    mpovz[0]=cos(pugol);mpovz[1]=-sin(pugol)
    mpovz[3]=sin(pugol);mpovz[4]=cos(pugol)
    #dx=-dx
    dy=-dy
    xsat=(mpovz[0]*dx+mpovz[1]*dy)+xc
    ysat=(mpovz[3]*dx+mpovz[4]*dy)+yc
    if plname=="Jupiter": jsatdb[numsat].x=xsat; jsatdb[numsat].y=ysat;
    if plname=="Saturn": ssatdb[numsat].x=xsat; ssatdb[numsat].y=ysat;
    #d=2
    if d>2:
        ovalxy2(xsat,ysat,d/2,d/2,color,color,1,strtag)
    elif d==2:
        linexy2(xsat,ysat,-1,0,1,0,2,color,strtag)
    else:
        linexy2(xsat,ysat,0,0,1,0,1,color,strtag)
#======Pramoe Voshozdenie plus
def pvplus(pv,dpv):
    if (pv+dpv)>=24: pv=pv+dpv-24
    else: pv=pv+dpv
    return(pv)
#======Pramoe Voshozdenie minus
def pvminus(pv,dpv):
    if (pv-dpv)<0: pv=pv-dpv+24
    else: pv=pv-dpv
    return(pv)
#=============================
#======Sklonenie plus
def sklplus(pv,sk,dsk):
    if (sk+dsk)>90: sk=180-sk-dsk; pv=pvplus(pv,12)
    elif (sk+dsk)<-90: sk=-180+sk+dsk; pv=pvplus(pv,12)
    else: sk=sk+dsk
    return(pv,sk)
#=============================
#Ugol plus
def ugplus(ug,dug):
    if (ug+dug)>=360: ug=ug+dug-360
    else: ug=ug+dug
    return(ug)
#Ugol minus
def ugminus(ug,dug):
    if (ug-dug)<0: ug=ug-dug+360
    else: ug=ug-dug
    return(ug)
#=============================

#======Calc AZ coord
def calcaz(pv,sk,lmst):
    mylat2=MYLAT
    if mylat2==90:mylat2=89.999999
    if mylat2==-90:mylat2=-89.999999
    pvrad=pv*15*pid180
    skrad=sk*pid180
    h=15*pid180*pvminus(lmst,pv)
    mylatrad=KPOL*mylat2*pid180
    a_=asin(sin(skrad)*sin(mylatrad)+cos(skrad)*cos(mylatrad)*cos(h))
    if a_==90:a_=89.999999
    if a_==-90:a_=-89.999999
    cosA1=(sin(skrad)-sin(mylatrad)*sin(a_))/(cos(mylatrad)*cos(a_))
    if cosA1>1:cosA1=1
    if cosA1<-1:cosA1=-1
    A1=acos(cosA1)
    if (sin(h)<0): az_=A1
    else: az_=pi2-A1
    az_=az_*d180pi;a_=a_*d180pi
    return(az_,a_)
#=============================

#======Calc EKV coord
def calcekv(azimuth,alt,lmst):
    mylat2=MYLAT
    if mylat2==90:mylat2=89.999999
    if mylat2==-90:mylat2=-89.999999
    altrad=alt*pid180
    azimuthrad=azimuth*pid180
    mylatrad=KPOL*mylat2*pid180
    dec=asin(sin(altrad)*sin(mylatrad)+cos(altrad)*cos(mylatrad)*cos(azimuthrad))
    dec=dec*d180pi
    if dec==90:dec=89.999999
    if dec==-90:dec=-89.999999
    cosh_=(sin(altrad)-sin(mylatrad)*sin(dec*pid180))/(cos(mylatrad)*cos(dec*pid180))
    if cosh_>1:cosh_=1
    if cosh_<-1:cosh_=-1
    h_=acos(cosh_)
    if (sin(azimuthrad)<0): h=h_
    else: h=pi2-h_
    h=h*d180pi/15
    ra=pvminus(lmst,h)
    return(ra,dec)
#==============Nasatie knopki start
def start():
    global TURN_ANGLE,EPS,COSEPS,SINEPS,MPOV,PMAT,PMAT2,PMAT1875
    global ZOOM,ZOOMOLD,NOPRINT,SUMENTRY
    global DELTAD,DSSYST,KPOL,KPOL_OLD,CHLAT,CHLON,MYLAT,MYLON,MYLATOLD,MYLONOLD,DELTAHOURS
    global UTCDTIME,DAY,MONTH,YEAR,HOUR,TIMEDELTA_,LDTIME,LDAY,LMONTH,LYEAR,LHOUR
    global MJD,JD_,LMST,TIM_,RA_CANV2000,DEC_CANV2000,HIPSAO_IJ,MAGN_LIMIT,DELTAT

    HIPSAO_IJ=[]  #dla Hipparcos
    for i in range(0,24):
        HIPSAO_IJ.append([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])

    MAGN_LIMIT=float(emagn.get())

    canvas.delete("all")

    qx=canvas.xview()
    qy=canvas.yview()
    azimuth_old,alt_old=calcaz_xycanv((qx[0]+qx[1])/2*ZOOMOLD*RCANV+POPRXY,(qy[0]+qy[1])/2*ZOOMOLD*RCANV+POPRXY)
    #ra_canv,dec_canv=calcekv(azimuth_old,alt_old,LMST)

    MYLAT=float(str(elat.get()))
    if clatvar.get()==1:KPOL=1
    if clatvar.get()==0:KPOL=-1
    MYLON=float(str(elon.get()))
    if clonvar.get()==1:MYLON=-MYLON
    DELTAHOURS=float(edt.get())
    TIMEDELTA_=timedelta(hours=DELTAHOURS)

    f = open('program.ini', 'w')
    f.write(str(KPOL*MYLAT)+ '\n')
    f.write(str(MYLON)+ '\n')
    f.write(str(DELTAHOURS)+ '\n')
    f.close()

    DELTAD=0
    NOPRINT=0
    sumentry2=KPOL+float(elat.get())+float(elon.get())+float(eyy.get())+float(emm.get())+float(edd.get())
    sumentry2=sumentry2+float(ehh.get())+float(emin.get())+float(ess.get())+float(edt.get())+clatvar.get()+clonvar.get()+float(emagn.get())
    if SUMENTRY==sumentry2: NOPRINT=1
    else: SUMENTRY=sumentry2

    if NOPRINT==0:
        print("===============================================================================")
    
    if KPOL==1:CHLAT='N'
    else:CHLAT='S'
    if MYLON<0:CHLON='E'
    elif MYLON>0:CHLON='W'
    else: CHLON=''

    if NOPRINT==0:print("Latitude="+str(MYLAT)+" "+CHLAT)
    if NOPRINT==0:print("Longitude="+str(abs(MYLON))+" "+CHLON)

    LDAY=int(edd.get())
    LMONTH=int(emm.get())
    LYEAR=int(eyy.get())
    LHOUR=float(ehh.get())+float(emin.get())/60+float(ess.get())/3600
    LDTIME=datetime.datetime(LYEAR, LMONTH, LDAY , int(ehh.get()) , int(emin.get()) , int(ess.get()))
    UTCDTIME = LDTIME - TIMEDELTA_

    UTCDTIME=UTCDTIME.strftime("%Y-%m-%d %H:%M:%S")
    LDTIME=LDTIME.strftime("%Y-%m-%d %H:%M:%S")
    if NOPRINT==0:print("UTCDateTime="+UTCDTIME)
    if NOPRINT==0:print("LocalDateTime="+LDTIME)
   
    DAY=int(UTCDTIME[8:10])
    MONTH=int(UTCDTIME[5:7])
    YEAR=int(UTCDTIME[0:4])
    HOUR=float(UTCDTIME[11:13])+float(UTCDTIME[14:16])/60+float(UTCDTIME[17:19])/3600

    MJD=mjdf(DAY,MONTH,YEAR,HOUR)
    JD_=MJD+2400000.5
    LMST=lmstf(MJD,MYLON)
    DELTAT=calcdeltat(YEAR,MONTH)
    TIM_=(JD_+DELTAT/86400-2451545)/36525
    if NOPRINT==0:
        print("MJD="+str(round(MJD,6)))
        print("JD="+str(round(JD_,6)))
        rastr,decstr=grms(LMST,0)
        print("LMST="+rastr+" ("+str(round(LMST,6))+"h)")
        print("DELTA_T="+str(round(DELTAT,2))+"s")
        
    if oturnvar.get()=="S":TURN_ANGLE=0
    elif oturnvar.get()=="SE":TURN_ANGLE=pi/4
    elif oturnvar.get()=="E":TURN_ANGLE=pi/2
    elif oturnvar.get()=="NE":TURN_ANGLE=3*pi/4
    elif oturnvar.get()=="N":TURN_ANGLE=pi
    elif oturnvar.get()=="NW":TURN_ANGLE=5*pi/4
    elif oturnvar.get()=="W":TURN_ANGLE=3*pi/2
    elif oturnvar.get()=="SW":TURN_ANGLE=7*pi/4
    if KPOL==-1: TURN_ANGLE=TURN_ANGLE+pi

    fi=pid2-MYLAT*pid180

    MPOV[0]=1;MPOV[1]=0;MPOV[2]=0
    MPOV[3]=0;MPOV[4]=cos(fi);MPOV[5]=-sin(fi)
    MPOV[6]=0;MPOV[7]=sin(fi);MPOV[8]=cos(fi)

    ZOOM=float(ozoomvar.get())

    rx2=root.winfo_width()
    ry2=root.winfo_height()
    
    ra_canv,dec_canv=calcekv(azimuth_old,alt_old,LMST)

    x,y,z=calcxyzpolm(ra_canv,KPOL*dec_canv,LMST,ZOOM,KPOL)
    prvt,sklt,zz=povorot(x,y,z,TURN_ANGLE)
    xc,yc=calcxycon(prvt,sklt,ZOOM)
    #xc=xc+10;yc=yc+10

    if ZOOM!=ZOOMOLD:
        canvas.config(scrollregion=(0,0,ZOOM*RCANV,ZOOM*RCANV))

    if ZOOM>2 or ZOOMOLD>2 or ZOOM!=ZOOMOLD:
        canvas.xview_moveto((xc/RCANV/ZOOM)-rx2/(ZOOM*2*RCANV))
        canvas.yview_moveto((yc/RCANV/ZOOM)-ry2/(ZOOM*2*RCANV))

    qx=canvas.xview()
    qy=canvas.yview()

    if KPOL!=KPOL_OLD or MYLAT!=MYLATOLD or MYLON!=MYLONOLD:
        canvas.xview_moveto(1/2-rx2/(ZOOM*2*RCANV))
        canvas.yview_moveto(1/2-ry2/(ZOOM*2*RCANV))
    KPOL_OLD=KPOL;MYLATOLD=MYLAT;MYLONOLD=MYLON
    
    ZOOMOLD=ZOOM

    PMAT=pmatequ(TIM_,0)
    PMAT2=pmatequ(0,TIM_)
    PMAT1875=pmatequ((2405890-2451545)/36525,TIM_)

    azimuth,alt=calcaz_xycanv((qx[0]+qx[1])/2*ZOOM*RCANV+POPRXY,(qy[0]+qy[1])/2*ZOOM*RCANV+POPRXY)
    ra_canv,dec_canv=calcekv(azimuth,alt,LMST) #dla otobrajeniya zvezd
    RA_CANV2000,DEC_CANV2000=ekvtoekv2000(ra_canv,dec_canv) #2000!

    #EPS=(23.43929111-46.8150*TIM_/3600-0.00059*TIM_/3600*TIM_+0.001813*TIM_**3/3600)*pid180

    if ogridvar.get()=="EQ":risgridconekv()
    if ogridvar.get()=="AZ":risgridconaz()
    if ogridvar.get()=="EQ&AZ":
        risgridconekv()
        risgridconaz()
    rishoriz()
    legpaint()
    DSSYST=JD_-2451543.5+DELTAT/86400
    eclpaint(DSSYST)
    smap(DSSYST)
    #DSSYST = 367*YEAR - int(7 * ( YEAR + int((MONTH+9)/12) ) / 4) + int(275*(MONTH/9)) + DAY - 730530 + HOUR/24
    #for y in range (2100,9100,100):
    #    if ((YEAR==y and MONTH>=3) or (YEAR>y)) and frac(y/400)!=0:DSSYST=DSSYST-1
    #for y in range (1900,1500,-100):
    #    if ((YEAR==y and MONTH<3) or (YEAR<y)) and frac(y/400)!=0:DSSYST=DSSYST+1
    ssystem(DSSYST,DELTAD,LMST,"all",-1)
    #NOPRINT=0
#===============================
# hide buttons
def hide(*args):
    global HIDE
    if HIDE==0:HIDE=1
    elif HIDE==1:HIDE=0
    if HIDE==1:
        bstart.lower(); bfind.lower();btrack.lower();brisset.lower();bnow.lower();btminus.lower();btplus.lower();bdss.lower();bisearch.lower()
        ogrid.lower();oturn.lower();ozoom.lower()
        etrack.lower();efind.lower();emagn.lower()
        lgrid.lower();lturn.lower();lzoom.lower();lmagn.lower()
        ctrack.lower()
        #root.attributes('-fullscreen', True)
    if HIDE==0:
        bstart.lift();bfind.lift();btrack.lift();brisset.lift();bnow.lift();btminus.lift();btplus.lift();bdss.lift();bisearch.lift()
        ogrid.lift();oturn.lift();ozoom.lift()
        etrack.lift();efind.lift();emagn.lift()
        lgrid.lift();lturn.lift();lzoom.lift();lmagn.lift()
        ctrack.lift()
        #root.attributes('-fullscreen', False)
#============================
# Sun System track
def sstrack(*args):
    global NOPRINT,DELTAD
    err=0
    new_v=etrack.get().strip()
    try:
        float(new_v)
    except:
        err=1
    if err==0:
        if float(new_v)<-3660 or float(new_v)>3660: err=1

    if err==0:
        if float(new_v)==0: DELTAD=0
        if float(new_v)!=0:
            NOPRINT=1
            DELTAD=DELTAD+float(new_v)
            timedelta_d=timedelta(days=int(abs(DELTAD)))
            timedelta_s=timedelta(seconds=int(86400*frac(abs(DELTAD))))
            utcdtime=datetime.datetime(YEAR, MONTH, DAY , int(UTCDTIME[11:13]) , int(UTCDTIME[14:16]) , int(UTCDTIME[17:19]))
            if DELTAD>=0: utcdtime = utcdtime + timedelta_d + timedelta_s
            else: utcdtime = utcdtime - timedelta_d - timedelta_s
            udtime_s=utcdtime.strftime("%Y-%m-%d %H:%M:%S")
            day=int(udtime_s[8:10])
            month=int(udtime_s[5:7])
            year=int(udtime_s[0:4])
            hour=float(udtime_s[11:13])+float(udtime_s[14:16])/60+float(udtime_s[17:19])/3600
            mjd_=mjdf(day,month,year,hour)
            lmst=lmstf(mjd_,MYLON)

            ssystem(DSSYST+DELTAD,DELTAD,lmst,"all",-1)
            NOPRINT=0
    else:
        etrack.delete(0,END)
        etrack.insert(0,"E")
#============================
#Striranie povtor simvolov        
def zamenan(char,s):
    while char*2 in s:
        s=s.replace(char*2,char)
    return s
#============================
#Find
def objfind(*args):
    #podprogramma dla poiska hipparcos star
    def hipfind(i,j,k,ffind):                            
        d_year=YEAR+MONTH/12+DAY/365.25-2000
        dpv=d_year*starhipdb[i][j][k].pmra/3600/15
        dsk=d_year*starhipdb[i][j][k].pmdec/3600
        ra2000_=pvplus(starhipdb[i][j][k].ra2000,dpv)
        ra2000_,dec2000_=sklplus(ra2000_,starhipdb[i][j][k].dec2000,dsk)
        prv,skl=ekv2000toekv(ra2000_,dec2000_)
        starhipdb[i][j][k].ra=prv; starhipdb[i][j][k].dec=skl;
        x,y,z=calcxyzpolm(prv,KPOL*skl,LMST,ZOOM,KPOL)
        prvt,sklt,zz=povorot(x,y,z,TURN_ANGLE) 
        x,y=calcxycon(prvt,sklt,ZOOM)            
        starhipdb[i][j][k].x=x; starhipdb[i][j][k].y=y
        ffind=""
        if x>=0 and y>=0 and x<=RCANV*ZOOM and y<=RCANV*ZOOM:
            canvas.xview_moveto(x/RCANV/ZOOM-rx2/(ZOOM*2*RCANV))
            canvas.yview_moveto(y/RCANV/ZOOM-ry2/(ZOOM*2*RCANV))
            hipstarprint(i,j,k)
            linexy(x-10,y,x-30,y,1,findcolor,"find")
            linexy(x,y+10,x,y+30,1,findcolor,"find")
        elif x<0 or y<0 or x>RCANV*ZOOM or y>RCANV*ZOOM:
            print("star HIP "+str(starhipdb[i][j][k].num)+" is outside of map")
            print()
        return(ffind)
    #===============
    #podprogramma dla poiska SAO star
    def saofind(i,j,k,ffind):                            
        d_year=YEAR+MONTH/12+DAY/365.25-2000
        dpv=d_year*starsaodb[i][j][k].pmra/3600/15
        dsk=d_year*starsaodb[i][j][k].pmdec/3600
        ra2000_=pvplus(starsaodb[i][j][k].ra2000,dpv)
        ra2000_,dec2000_=sklplus(ra2000_,starsaodb[i][j][k].dec2000,dsk)
        prv,skl=ekv2000toekv(ra2000_,dec2000_)
        starsaodb[i][j][k].ra=prv; starsaodb[i][j][k].dec=skl;
        x,y,z=calcxyzpolm(prv,KPOL*skl,LMST,ZOOM,KPOL)
        prvt,sklt,zz=povorot(x,y,z,TURN_ANGLE) 
        x,y=calcxycon(prvt,sklt,ZOOM)            
        starsaodb[i][j][k].x=x; starsaodb[i][j][k].y=y
        ffind=""
        if x>=0 and y>=0 and x<=RCANV*ZOOM and y<=RCANV*ZOOM:
            canvas.xview_moveto(x/RCANV/ZOOM-rx2/(ZOOM*2*RCANV))
            canvas.yview_moveto(y/RCANV/ZOOM-ry2/(ZOOM*2*RCANV))
            saostarprint(i,j,k)
            linexy(x-10,y,x-30,y,1,findcolor,"find")
            linexy(x,y+10,x,y+30,1,findcolor,"find")
        elif x<0 or y<0 or x>RCANV*ZOOM or y>RCANV*ZOOM:
            print("star SAO "+str(starsaodb[i][j][k].num)+" is outside of map")
            print()
        return(ffind)
    #===============
    #podprogramma dla poiska Bright Star
    def bstarfind(i,ffind):
        ffind=""
        if stardb[i].x>=0 and stardb[i].y>=0 and stardb[i].x<=RCANV*ZOOM and stardb[i].y<=RCANV*ZOOM:
            canvas.xview_moveto((stardb[i].x/RCANV/ZOOM)-rx2/(ZOOM*2*RCANV))
            canvas.yview_moveto((stardb[i].y/RCANV/ZOOM)-ry2/(ZOOM*2*RCANV))
            bscstarprint(i)
            linexy(stardb[i].x-10,stardb[i].y,stardb[i].x-30,stardb[i].y,1,findcolor,"find")
            linexy(stardb[i].x,stardb[i].y+10,stardb[i].x,stardb[i].y+30,1,findcolor,"find")
        if stardb[i].x<0 or stardb[i].y<0 or stardb[i].x>RCANV*ZOOM or stardb[i].y>RCANV*ZOOM:
            print("star HR "+str(stardb[i].num)+" is outside of map")
            print()
        return(ffind)
    #===============                    

    if ''.join(efind.get().split()).lower()!="":

        rx2=root.winfo_width()
        ry2=root.winfo_height()
        i=0;ffind="not found"
        #strfind=''.join(efind.get().split()).lower()
        strfind=zamenan(" ",efind.get().strip().lower())

#find hr(bsc) star po common name
        #line=efind.get().strip().lower()
        line=zamenan(" ",efind.get().strip().lower())
        for i in range (0,len(stardb)):
            #cname=stardb[i].cname.lower()
            cname=zamenan(" ",stardb[i].cname.lower())
            if cname.find(line)!=-1 and stardb[i].x>=0 and stardb[i].y>=0 and stardb[i].x<=RCANV*ZOOM and stardb[i].y<=RCANV*ZOOM:
                canvas.xview_moveto((stardb[i].x/RCANV/ZOOM)-rx2/(ZOOM*2*RCANV))
                canvas.yview_moveto((stardb[i].y/RCANV/ZOOM)-ry2/(ZOOM*2*RCANV))
                bscstarprint(i)
                linexy(stardb[i].x-10,stardb[i].y,stardb[i].x-30,stardb[i].y,1,findcolor,"find")
                linexy(stardb[i].x,stardb[i].y+10,stardb[i].x,stardb[i].y+30,1,findcolor,"find")
                ffind=""
            elif cname.find(line)!=-1 and (stardb[i].x<0 or stardb[i].y<0 or stardb[i].x>RCANV*ZOOM or stardb[i].y>RCANV*ZOOM):
                print("star "+stardb[i].cname+" is outside of map")
                print()
                ffind=""

#find constellation
        for i in range (0,len(constlabdb)):
            constname=constlabdb[i].name1+";"+constlabdb[i].name2
            #constname=''.join(constname.split()).lower()
            constname=zamenan(" ",constname.strip().lower())
            if strfind!="" and constname.find(strfind)!=-1 and constlabdb[i].x>=0 and constlabdb[i].y>=0 and constlabdb[i].x<=RCANV*ZOOM and constlabdb[i].y<=RCANV*ZOOM:
                canvas.xview_moveto((constlabdb[i].x/RCANV/ZOOM)-rx2/(ZOOM*2*RCANV))
                canvas.yview_moveto((constlabdb[i].y/RCANV/ZOOM)-ry2/(ZOOM*2*RCANV))
                constellationprint(i)
                ffind=""
            elif strfind!="" and constname.find(strfind)!=-1 and (constlabdb[i].x<0 or constlabdb[i].y<0 or constlabdb[i].x>RCANV*ZOOM or constlabdb[i].y>RCANV*ZOOM):
                print("constellation",constlabdb[i].name2,"("+constlabdb[i].name1+")"+" is outside of map")
                print()
                ffind=""

#find hr(bsc) star po hr
        findspis=efind.get().split()
        strfindhr=''.join(efind.get().split()).lower()
        if len(findspis)==2 and (strfindhr.find("hr")!=-1 or strfindhr.find("bsc")!=-1):
            sfind_ = strfindhr.replace("hr","")
            sfind_ = sfind_.replace("bsc","")
            if sfind_.isdigit()==True:
                for i in range (0,len(stardb)):
                    if stardb[i].num==int(sfind_): ffind=bstarfind(i,ffind)

#find hr(bsc) star po VarID
        #strfindvar=''.join(efind.get().split()).lower()
        strfindvar=zamenan(" ",efind.get().strip().lower())
        if strfindvar[0:4]=="var ":
            sfind_ = strfindvar[4:]
            if sfind_!="":
                for i in range (0,len(stardb)):
                    #varname=''.join(stardb[i].varid.split()).lower()
                    varname=zamenan(" ",stardb[i].varid.strip().lower())
                    if varname.find(sfind_)!=-1: ffind=bstarfind(i,ffind)

#find hr(bsc) star po HD
        strfindhd=''.join(efind.get().split()).lower()
        if len(findspis)==2 and strfindhd[0:2]=="hd":
            sfind_ = strfindhd[2:]
            if sfind_.isdigit()==True:
                for i in range (0,len(stardb)):
                    hdnum=stardb[i].hd.strip()
                    if hdnum==sfind_: ffind=bstarfind(i,ffind)
                    
#find hr(bsc) star po SAO
        strfindsao=''.join(efind.get().split()).lower()
        if len(findspis)==2 and strfindsao[0:3]=="sao":
            sfind_ = strfindsao[3:]
            if sfind_.isdigit()==True:
                for i in range (0,len(stardb)):
                    saonum=stardb[i].sao.strip()
                    if saonum==sfind_: ffind=bstarfind(i,ffind)
                            
#find (bsc) star po alp And
        line=efind.get()
        line=line.lower()
        findspis=line.split()
        if len(findspis)==3: findspis[1]=findspis[1]+findspis[2]
        if (len(findspis)==2 or len(findspis)==3) and len(findspis[1])>2:
            constel=[]
            f=0
            for i in range (0,len(constlabdb)):
                line=constlabdb[i].name1
                line=line.lower()
                if findspis[1]==line:
                    f=1
                    constel.append(line)
            if f==0:
                for i in range (0,len(constlabdb)):
                    line=constlabdb[i].name2
                    line=''.join(line.split())
                    line=line.lower()
                    if line.find(findspis[1])!=-1:
                        line_=constlabdb[i].name1
                        line_=line_.lower()
                        constel.append(line_)
            if len(constel)>1:
                for line in constel:
                    if constel.count(line)>1:
                        constel.remove(line)
            if len(constel)>0:
                sfind_=findspis[0]
                for cnamef in constel:
                    for i in range (0,len(stardb)):
                        snam1=stardb[i].nam1.strip().lower()
                        snam2=stardb[i].nam2.lower(); snam2=''.join(snam2.split())
                        cname=stardb[i].const.strip().lower()
                        if (sfind_==snam1 or (sfind_.isdigit()==False and snam2.find(sfind_)!=-1)) and (cnamef==cname) and stardb[i].x>=0 and stardb[i].y>=0 and stardb[i].x<=RCANV*ZOOM and stardb[i].y<=RCANV*ZOOM:
                            canvas.xview_moveto((stardb[i].x/RCANV/ZOOM)-rx2/(ZOOM*2*RCANV))
                            canvas.yview_moveto((stardb[i].y/RCANV/ZOOM)-ry2/(ZOOM*2*RCANV))
                            bscstarprint(i)
                            linexy(stardb[i].x-10,stardb[i].y,stardb[i].x-30,stardb[i].y,1,findcolor,"find")
                            linexy(stardb[i].x,stardb[i].y+10,stardb[i].x,stardb[i].y+30,1,findcolor,"find")
                            ffind=""
                        elif (sfind_==snam1 or (sfind_.isdigit()==False and snam2.find(sfind_)!=-1)) and (cnamef==cname) and (stardb[i].x<0 or stardb[i].y<0 or stardb[i].x>RCANV*ZOOM or stardb[i].y>RCANV*ZOOM):
                            if stardb[i].nam2.strip()!="": strn=stardb[i].nam1.strip()+" "+''.join(stardb[i].nam2.split())+" "+stardb[i].const
                            else: strn=stardb[i].nam1.strip()+" "+stardb[i].const
                            strn=strn.strip()
                            print("star "+strn+" is outside of map")
                            print()
                            ffind=""

#find HIPPARCOS star
        #po HIC                            
        line=efind.get()
        line=line.lower()
        findspis=line.split()
        if ZOOM>=ZOOMHIP and len(findspis)==2 and (findspis[0].find("hip")!=-1 or findspis[0].find("hic")!=-1 or findspis[0].find("hipparcos")!=-1) and findspis[1].isdigit()==True:
            sfind_ = int(findspis[1])
            for i in range(0,24):
                for j in range(0,17):
                    for k in range(0,len(starhipdb[i][j])):
                        if starhipdb[i][j][k].num==sfind_:
                            ffind=hipfind(i,j,k,ffind)
        #po HD                            
        if ZOOM>=ZOOMHIP and len(findspis)==2 and findspis[0].find("hd")!=-1 and findspis[1].isdigit()==True:
            sfind_ = findspis[1]
            for i in range(0,24):
                for j in range(0,17):
                    for k in range(0,len(starhipdb[i][j])):
                        if starhipdb[i][j][k].hd==sfind_:
                            ffind=hipfind(i,j,k,ffind)
        #po SAO                            
        if ZOOM>=ZOOMHIP and len(findspis)==2 and findspis[0].find("sao")!=-1 and findspis[1].isdigit()==True:
            sfind_ = findspis[1]
            for i in range(0,24):
                for j in range(0,17):
                    for k in range(0,len(starhipdb[i][j])):
                        if starhipdb[i][j][k].sao==sfind_:
                            ffind=hipfind(i,j,k,ffind)
        #po VarID
        if ZOOM>=ZOOMHIP:                            
            #strfindvar=''.join(efind.get().split()).lower()
            strfindvar=zamenan(" ",efind.get().strip().lower())
            if strfindvar[0:4]=="var ":
                sfind_ = strfindvar[4:]
                if sfind_!="":
                    for i in range(0,24):
                        for j in range(0,17):
                            for k in range(0,len(starhipdb[i][j])):
                                #varname=''.join(starhipdb[i][j][k].varid.split()).lower()
                                varname=zamenan(" ",starhipdb[i][j][k].varid.strip().lower())
                                if varname.find(sfind_)!=-1:
                                    ffind=hipfind(i,j,k,ffind)
#find SAO star
        #po SAO                            
        line=efind.get()
        line=line.lower()
        findspis=line.split()
        if ZOOM>=ZOOMSAO and len(findspis)==2 and findspis[0].find("sao")!=-1 and findspis[1].isdigit()==True:
            sfind_ = int(findspis[1])
            for i in range(0,24):
                for j in range(0,17):
                    for k in range(0,len(starsaodb[i][j])):
                        if starsaodb[i][j][k].num==sfind_:
                            ffind=saofind(i,j,k,ffind)
        #po HD                            
        if ZOOM>=ZOOMSAO and len(findspis)==2 and findspis[0].find("hd")!=-1 and findspis[1].isdigit()==True:
            sfind_ = findspis[1]
            for i in range(0,24):
                for j in range(0,17):
                    for k in range(0,len(starsaodb[i][j])):
                        if starsaodb[i][j][k].hd==sfind_:
                            ffind=saofind(i,j,k,ffind)                                    

#find dso1 m ngc ic
        strfinddso=''.join(efind.get().split()).lower()
        line=efind.get()
        line=line.lower()
        findspis=line.split()
        if ZOOM<ZOOMDSO2 and len(findspis)==2:
            for i in range (0,len(dso1db)):
                line_=dso1db[i].nam2
                sfind = line_.split("/")
                for j in range (0,len(sfind)):
                    line=sfind[j].lower()
                    if line==strfinddso and dso1db[i].x>=0 and dso1db[i].y>=0 and dso1db[i].x<=RCANV*ZOOM and dso1db[i].y<=RCANV*ZOOM:
                        canvas.xview_moveto((dso1db[i].x/RCANV/ZOOM)-rx2/(ZOOM*2*RCANV))
                        canvas.yview_moveto((dso1db[i].y/RCANV/ZOOM)-ry2/(ZOOM*2*RCANV))
                        dso1print(i)
                        linexy(dso1db[i].x-10,dso1db[i].y,dso1db[i].x-30,dso1db[i].y,1,findcolor,"find")
                        linexy(dso1db[i].x,dso1db[i].y+10,dso1db[i].x,dso1db[i].y+30,1,findcolor,"find")
                        ffind=""
                    elif line==strfinddso and (dso1db[i].x<0 or dso1db[i].y<0 or dso1db[i].x>RCANV*ZOOM or dso1db[i].y>RCANV*ZOOM):
                        print("deep sky object "+dso1db[i].nam2+" is outside of map")
                        print()
                        ffind=""

#find dso1 name
        line=efind.get()
        line=line.lower()
        findspis=line.split()
        if ZOOM<ZOOMDSO2 and len(findspis)==2 and findspis[0].find("dso")!=-1:
            sfind1 = findspis[1]
            for i in range (0,len(dso1db)):
                line=dso1db[i].nam2.lower()
                if line.find(sfind1)!=-1 and dso1db[i].x>=0 and dso1db[i].y>=0 and dso1db[i].x<=RCANV*ZOOM and dso1db[i].y<=RCANV*ZOOM:
                    canvas.xview_moveto((dso1db[i].x/RCANV/ZOOM)-rx2/(ZOOM*2*RCANV))
                    canvas.yview_moveto((dso1db[i].y/RCANV/ZOOM)-ry2/(ZOOM*2*RCANV))
                    dso1print(i)
                    linexy(dso1db[i].x-10,dso1db[i].y,dso1db[i].x-30,dso1db[i].y,1,findcolor,"find")
                    linexy(dso1db[i].x,dso1db[i].y+10,dso1db[i].x,dso1db[i].y+30,1,findcolor,"find")
                    ffind=""
                elif line.find(sfind1)!=-1 and (dso1db[i].x<0 or dso1db[i].y<0 or dso1db[i].x>RCANV*ZOOM or dso1db[i].y>RCANV*ZOOM):
                    print("deep sky object "+dso1db[i].nam2+" is outside of map")
                    print()
                    ffind=""

#find dso2 m ngc ic
        strfinddso=''.join(efind.get().split()).lower()
        line=efind.get()
        line=line.lower()
        findspis=line.split()
        if ZOOM>=ZOOMDSO2 and len(findspis)==2:
            for i in range (0,len(dso2db)):
                line_=dso2db[i].nam2
                sfind = line_.split("/")
                for j in range (0,len(sfind)):
                    line=sfind[j].lower()
                    if line==strfinddso and dso2db[i].x>=0 and dso2db[i].y>=0 and dso2db[i].x<=RCANV*ZOOM and dso2db[i].y<=RCANV*ZOOM:
                        canvas.xview_moveto((dso2db[i].x/RCANV/ZOOM)-rx2/(ZOOM*2*RCANV))
                        canvas.yview_moveto((dso2db[i].y/RCANV/ZOOM)-ry2/(ZOOM*2*RCANV))
                        dso2print(i)
                        linexy(dso2db[i].x-10,dso2db[i].y,dso2db[i].x-30,dso2db[i].y,1,findcolor,"find")
                        linexy(dso2db[i].x,dso2db[i].y+10,dso2db[i].x,dso2db[i].y+30,1,findcolor,"find")
                        ffind=""
                    elif line==strfinddso and (dso2db[i].x<0 or dso2db[i].y<0 or dso2db[i].x>RCANV*ZOOM or dso2db[i].y>RCANV*ZOOM):
                        print("deep sky object "+dso2db[i].nam2+" is outside of map")
                        print()
                        ffind=""

#find dso2 name
        line=efind.get()
        line=line.lower()
        findspis=line.split()
        if ZOOM>=ZOOMDSO2 and len(findspis)==2 and findspis[0].find("dso")!=-1:
            sfind1 = findspis[1]
            for i in range (0,len(dso2db)):
                line=dso2db[i].nam2.lower()
                if line.find(sfind1)!=-1 and dso2db[i].x>=0 and dso2db[i].y>=0 and dso2db[i].x<=RCANV*ZOOM and dso2db[i].y<=RCANV*ZOOM:
                    canvas.xview_moveto((dso2db[i].x/RCANV/ZOOM)-rx2/(ZOOM*2*RCANV))
                    canvas.yview_moveto((dso2db[i].y/RCANV/ZOOM)-ry2/(ZOOM*2*RCANV))
                    dso2print(i)
                    linexy(dso2db[i].x-10,dso2db[i].y,dso2db[i].x-30,dso2db[i].y,1,findcolor,"find")
                    linexy(dso2db[i].x,dso2db[i].y+10,dso2db[i].x,dso2db[i].y+30,1,findcolor,"find")
                    ffind=""
                elif line.find(sfind1)!=-1 and (dso2db[i].x<0 or dso2db[i].y<0 or dso2db[i].x>RCANV*ZOOM or dso2db[i].y>RCANV*ZOOM):
                    print("deep sky object "+dso2db[i].nam2+" is outside of map")
                    print()
                    ffind=""

#find coord
        line=efind.get()
        findspis=line.split()
        if len(findspis)==2:
            err=0
            try:
                ra=float(findspis[0])
            except:
                err=1
            try:
                dec=float(findspis[1])
            except:
                err=1
            if err==0:
                if ra>=0 and ra<24 and dec>=-90 and dec<=90:
                    x,y,z=calcxyzpolm(ra,KPOL*dec,LMST,ZOOM,KPOL)
                    prvt,sklt,zz=povorot(x,y,z,TURN_ANGLE) 
                    x,y=calcxycon(prvt,sklt,ZOOM)            
                    if x>=0 and y>=0 and x<=RCANV*ZOOM and y<=RCANV*ZOOM:
                        canvas.xview_moveto(x/RCANV/ZOOM-rx2/(ZOOM*2*RCANV))
                        canvas.yview_moveto(y/RCANV/ZOOM-ry2/(ZOOM*2*RCANV))
                        linexy(x-10,y,x-30,y,1,findcolor,"find")
                        linexy(x,y+10,x,y+30,1,findcolor,"find")
                        ffind=""
                        dsssave(ra,dec)
                    elif x<0 or y<0 or x>RCANV*ZOOM or y>RCANV*ZOOM:
                        print(efind.get().strip()+" is outside of map")
                        print()
                        ffind=""

#find asteroid
        for i in range (0,len(asterdb)):
            astername1=asterdb[i].str1.strip(":")
            astername2=astername1.replace("asteroid ","").lower()
            #astername2=''.join(astername2.split())
            astername2=zamenan(" ",astername2.strip())
            if strfind!="" and astername2.find(strfind)!=-1 and asterdb[i].x>=0 and asterdb[i].y>=0 and asterdb[i].x<=RCANV*ZOOM and asterdb[i].y<=RCANV*ZOOM:
                canvas.xview_moveto((asterdb[i].x/RCANV/ZOOM)-rx2/(ZOOM*2*RCANV))
                canvas.yview_moveto((asterdb[i].y/RCANV/ZOOM)-ry2/(ZOOM*2*RCANV))
                x=asterdb[i].x; y=asterdb[i].y
                linexy(x-10,y,x-30,y,1,findcolor,"find")
                linexy(x,y+10,x,y+30,1,findcolor,"find")
                asteroidprint(i)
                ffind=""
            elif strfind!="" and astername2.find(strfind)!=-1 and (asterdb[i].x<0 or asterdb[i].y<0 or asterdb[i].x>RCANV*ZOOM or asterdb[i].y>RCANV*ZOOM):
                print(astername1+" is outside of map")
                print()
                ffind=""
#find comet
        for i in range (0,len(cometdb)):
            cometname1=cometdb[i].str1.strip(":")
            cometname2=cometname1.replace("comet ","").lower()
            #cometname2=''.join(cometname2.split())
            cometname2=zamenan(" ",cometname2.strip())
            if strfind!="" and cometname2.find(strfind)!=-1 and cometdb[i].x>=0 and cometdb[i].y>=0 and cometdb[i].x<=RCANV*ZOOM and cometdb[i].y<=RCANV*ZOOM:
                canvas.xview_moveto((cometdb[i].x/RCANV/ZOOM)-rx2/(ZOOM*2*RCANV))
                canvas.yview_moveto((cometdb[i].y/RCANV/ZOOM)-ry2/(ZOOM*2*RCANV))
                x=cometdb[i].x; y=cometdb[i].y
                linexy(x-10,y,x-30,y,1,findcolor,"find")
                linexy(x,y+10,x,y+30,1,findcolor,"find")
                cometprint(i)
                ffind=""
            elif strfind!="" and cometname2.find(strfind)!=-1 and (cometdb[i].x<0 or cometdb[i].y<0 or cometdb[i].x>RCANV*ZOOM or cometdb[i].y>RCANV*ZOOM):
                print(cometname1+" is outside of map")
                print()
                ffind=""                    

#find Jupiter satellites
        jsatfind=efind.get().strip().lower()
        for i in range (0,len(jsatdb)):
            if jsatfind!="" and jsatdb[i].name.lower().find(jsatfind)!=-1 and jsatdb[i].x>=0 and jsatdb[i].y>=0 and jsatdb[i].x<=RCANV*ZOOM and jsatdb[i].y<=RCANV*ZOOM:
                canvas.xview_moveto((jsatdb[i].x/RCANV/ZOOM)-rx2/(ZOOM*2*RCANV))
                canvas.yview_moveto((jsatdb[i].y/RCANV/ZOOM)-ry2/(ZOOM*2*RCANV))
                x=jsatdb[i].x; y=jsatdb[i].y
                linexy(x-10,y,x-30,y,1,findcolor,"find")
                linexy(x,y+10,x,y+30,1,findcolor,"find")
                print(jsatdb[i].name+" (Jupiter's satellite)")
                print()
                ffind=""
            elif jsatfind!="" and jsatdb[i].name.lower().find(jsatfind)!=-1 and (jsatdb[i].x<0 or jsatdb[i].y<0 or jsatdb[i].x>RCANV*ZOOM or jsatdb[i].y>RCANV*ZOOM):
                print(jsatdb[i].name+" (Jupiter's satellite)"+" is outside of map")
                print()
                ffind=""

#find Saturn satellites
        ssatfind=efind.get().strip().lower()
        for i in range (0,len(ssatdb)):
            if ssatfind!="" and ssatdb[i].name.lower().find(ssatfind)!=-1 and ssatdb[i].x>=0 and ssatdb[i].y>=0 and ssatdb[i].x<=RCANV*ZOOM and ssatdb[i].y<=RCANV*ZOOM:
                canvas.xview_moveto((ssatdb[i].x/RCANV/ZOOM)-rx2/(ZOOM*2*RCANV))
                canvas.yview_moveto((ssatdb[i].y/RCANV/ZOOM)-ry2/(ZOOM*2*RCANV))
                x=ssatdb[i].x; y=ssatdb[i].y
                linexy(x-10,y,x-30,y,1,findcolor,"find")
                linexy(x,y+10,x,y+30,1,findcolor,"find")
                print(ssatdb[i].name+" (Saturn's satellite)")
                print()
                ffind=""
            elif ssatfind!="" and ssatdb[i].name.lower().find(ssatfind)!=-1 and (ssatdb[i].x<0 or ssatdb[i].y<0 or ssatdb[i].x>RCANV*ZOOM or ssatdb[i].y>RCANV*ZOOM):
                print(ssatdb[i].name+" (Saturn's satellite)"+" is outside of map")
                print()
                ffind=""
                
#find planet Sun Moon Pluto
        for i in range (0,10):
            plname1=planetdb[i].str1.strip(":")
            plname2=plname1.replace("planet ","").lower()
            #plname2=''.join(plname2.split())
            plname2=zamenan(" ",plname2.strip())
            if strfind!="" and plname2.find(strfind)!=-1 and planetdb[i].x>=0 and planetdb[i].y>=0 and planetdb[i].x<=RCANV*ZOOM and planetdb[i].y<=RCANV*ZOOM:
                canvas.xview_moveto((planetdb[i].x/RCANV/ZOOM)-rx2/(ZOOM*2*RCANV))
                canvas.yview_moveto((planetdb[i].y/RCANV/ZOOM)-ry2/(ZOOM*2*RCANV))
                if ZOOM<3:
                    x=planetdb[i].x; y=planetdb[i].y
                    linexy(x-10,y,x-30,y,1,findcolor,"find")
                    linexy(x,y+10,x,y+30,1,findcolor,"find")
                planetprint(i)
                ffind=""
            elif strfind!="" and plname2.find(strfind)!=-1 and (planetdb[i].x<0 or planetdb[i].y<0 or planetdb[i].x>RCANV*ZOOM or planetdb[i].y>RCANV*ZOOM):
                print(plname1+" is outside of map")
                print()
                ffind=""
                    
        if ZOOM>=ZOOMHIP: hippaint(0)
        if ZOOM>=ZOOMSAO: saopaint(0)

        if ffind=="not found":
            print(efind.get().strip(),"not found")
            print()
#====================================================================
#print bsc star
def bscstarprint(i):
    if stardb[i].nam2.strip()!="": strn=stardb[i].nam1.strip()+" "+''.join(stardb[i].nam2.split())+" "+stardb[i].const
    else: strn=stardb[i].nam1.strip()+" "+stardb[i].const
    strn=strn.strip()
    if strn!="":strn=strn+"/"
    hdstr=""; saostr=""
    if stardb[i].hd.strip()!="": hdstr="HD "+stardb[i].hd.strip()+"/"
    if stardb[i].sao.strip()!="": saostr="SAO "+stardb[i].sao.strip()+"/"
    line1="HR "+str(stardb[i].num)+"/"+strn+hdstr+saostr
    line1=line1.strip("/")
    rastr,decstr=grms(stardb[i].ra2000,stardb[i].dec2000)
    line2="RA(2000)="+rastr+" "
    line2=line2+"DEC(2000)="+decstr+" MAGN="+str(stardb[i].m)+" SP="+stardb[i].sp.strip()+" B-V="+stardb[i].b_v
    rastr,decstr=grms(stardb[i].ra,stardb[i].dec)
    az,alt=calcaz(stardb[i].ra,stardb[i].dec,LMST)
    line3="RA="+rastr+" DEC="+decstr+" AZ="+str(round(az,2))+"d"+" ALT="+str(round(alt,2))+"d"
    line4=""; strdouble=""
    if stardb[i].dbldm!=99:
        if stardb[i].dblsep!=0:
            strdouble=" (DeltaMAGN="+str(stardb[i].dbldm)+" SEP="+str(stardb[i].dblsep)+'")'
        line4="double"+strdouble
    line5=""
    if stardb[i].varid!="":
        line5="variable (VarID="+stardb[i].varid+")"
    print("star "+line1+" (Bright Star Catalogue):")
    if stardb[i].cname!="": print("common name(s): "+stardb[i].cname)
    print(line2)
    print(line3)
    if line4!="": print(line4)
    if line5!="": print(line5)
    rish,rism,kulmh,kulmm,seth,setm=riseset2(stardb[i].ra,stardb[i].dec,-0.583,12,0,"p",0)
    if rish=="-":strrise="-"
    else: strrise=rish+"h "+rism+"m"
    if kulmh=="-":strkulm="-"
    else: strkulm=kulmh+"h "+kulmm+"m"
    if seth=="-":strset="-"
    else: strset=seth+"h "+setm+"m"
    print("RISE: "+strrise+"  CULM: "+strkulm+"  SET: "+strset)
    print()
    cname=stardb[i].cname.split(";")[0]
    dsssave(stardb[i].ra,stardb[i].dec)
    isearchsave("star "+line1.strip().replace("/"," ")+" "+cname)

#print HIPPARCOS star
def hipstarprint(i,j,k):
    line1="HIC "+str(starhipdb[i][j][k].num)+"/"
    if starhipdb[i][j][k].hd!="": line1=line1+"HD "+starhipdb[i][j][k].hd+"/"
    if starhipdb[i][j][k].sao!="": line1=line1+"SAO "+starhipdb[i][j][k].sao+"/"
    line1=line1.strip("/")
    rastr,decstr=grms(starhipdb[i][j][k].ra2000,starhipdb[i][j][k].dec2000)
    line2="RA(2000)="+rastr
    if starhipdb[i][j][k].sp.strip()!="":strsp=" SP="+starhipdb[i][j][k].sp.strip()
    else:strsp=""
    if starhipdb[i][j][k].b_v!="":strbv=" B-V="+starhipdb[i][j][k].b_v
    else:strbv=""
    line2=line2+" DEC(2000)="+decstr+" MAGN="+str(starhipdb[i][j][k].m)+strsp+strbv
    rastr,decstr=grms(starhipdb[i][j][k].ra,starhipdb[i][j][k].dec)
    az,alt=calcaz(starhipdb[i][j][k].ra,starhipdb[i][j][k].dec,LMST)
    line3="RA="+rastr+" DEC="+decstr+" AZ="+str(round(az,2))+"d"+" ALT="+str(round(alt,2))+"d"
    line4=""; strdouble=""
    if starhipdb[i][j][k].ccdmcomp!="":
        strdouble=" ("+"COMP="+starhipdb[i][j][k].ccdmcomp
        if starhipdb[i][j][k].dbldm!=99:
            strdouble=strdouble+" DeltaMAGN="+str(starhipdb[i][j][k].dbldm)
        if starhipdb[i][j][k].dblsep!=-1:
            strdouble=strdouble+" SEP="+str(starhipdb[i][j][k].dblsep)+'"'
        if starhipdb[i][j][k].dblpa!=-1:
            strdouble=strdouble+" PA="+str(starhipdb[i][j][k].dblpa)+"d"
        strdouble=strdouble+")"
    if starhipdb[i][j][k].dblcomp!="":
        line4="double"+strdouble
    line5=""
    if starhipdb[i][j][k].varcode!="":
        if starhipdb[i][j][k].varcode=="1":varcodetext="suspected variable, with a suspected amplitude variation smaller than 2 mag"
        elif starhipdb[i][j][k].varcode=="2":varcodetext="suspected variable, with a suspected amplitude variation larger than 2 mag"
        elif starhipdb[i][j][k].varcode=="3":varcodetext="known variable, with an amplitude variation larger than 0.2 mag"
        elif starhipdb[i][j][k].varcode=="4":varcodetext="known variable, with large amplitude (> 2 mag), for which an ephemeris was necessary"
        elif starhipdb[i][j][k].varcode=="5":varcodetext="known variable, with an amplitude variation smaller than 0.2 mag"
        line5="VarCODE="+starhipdb[i][j][k].varcode+": "+varcodetext
    line6=""
    if starhipdb[i][j][k].varid!="": line6=line6+"VarID="+starhipdb[i][j][k].varid+" "
    if starhipdb[i][j][k].varvmax!=99:
        line6=line6+"MagnMAX="+str(starhipdb[i][j][k].varvmax)+" MagnMIN="+str(starhipdb[i][j][k].varvmin)
    if starhipdb[i][j][k].varperiod!=-1:
        line6=line6+" VarPERIOD="+str(starhipdb[i][j][k].varperiod)+"d"
    print("star "+line1+" (Hipparcos Catalogue):")
    print(line2)
    print(line3)
    if line4!="":
        print(line4)
        f = open('hip_double.dat', 'r')
        flag=0
        for line in f:
            if line[0]=="#": print(line.strip())
            if (line[0:6].strip()!=str(starhipdb[i][j][k].num) and line[0:6].strip()!="") and flag==1:
                break
            if (line[0:6].strip()==str(starhipdb[i][j][k].num) or line[0:6].strip()=="") and flag==1:
                print(line.strip("\n"))
            if line[0:6].strip()==str(starhipdb[i][j][k].num) and flag==0:
                print(line.strip("\n"))
                flag=1
        f.close()

    if line5!="": print(line5)
    if line6!="": print(line6)
    if starhipdb[i][j][k].notes.strip()!="":
        f = open('hip_notes.dat', 'r')
        for line in f:
            if line[0:6].strip()==str(starhipdb[i][j][k].num):
                print(line[8:].strip("\n"))            
        f.close()

    rish,rism,kulmh,kulmm,seth,setm=riseset2(starhipdb[i][j][k].ra,starhipdb[i][j][k].dec,-0.583,12,0,"p",0)
    if rish=="-":strrise="-"
    else: strrise=rish+"h "+rism+"m"
    if kulmh=="-":strkulm="-"
    else: strkulm=kulmh+"h "+kulmm+"m"
    if seth=="-":strset="-"
    else: strset=seth+"h "+setm+"m"
    print("RISE: "+strrise+"  CULM: "+strkulm+"  SET: "+strset)
    print()
    dsssave(starhipdb[i][j][k].ra,starhipdb[i][j][k].dec)
    isearchsave(line1.replace("/"," ")+" star")

#print SAO star
def saostarprint(i,j,k):
    line1="SAO "+str(starsaodb[i][j][k].num)+"/"
    if starsaodb[i][j][k].hd!="": line1=line1+"HD "+starsaodb[i][j][k].hd+"/"
    line1=line1.strip("/")
    rastr,decstr=grms(starsaodb[i][j][k].ra2000,starsaodb[i][j][k].dec2000)
    line2="RA(2000)="+rastr+" "
    if starsaodb[i][j][k].sp.strip()!="": strsp=" SP="+starsaodb[i][j][k].sp.strip()
    else:strsp=""
    if starsaodb[i][j][k].m!=99: strmag=" Magn="+str(starsaodb[i][j][k].m)
    else:strmag=""
    if starsaodb[i][j][k].pmag!=99: strpmag=" PMagn="+str(starsaodb[i][j][k].pmag)
    else:strpmag=""
    line2=line2+"DEC(2000)="+decstr+strmag+strpmag+strsp
    rastr,decstr=grms(starsaodb[i][j][k].ra,starsaodb[i][j][k].dec)
    az,alt=calcaz(starsaodb[i][j][k].ra,starsaodb[i][j][k].dec,LMST)
    line3="RA="+rastr+" DEC="+decstr+" AZ="+str(round(az,2))+"d"+" ALT="+str(round(alt,2))+"d"
    #line4=""
    #line5=""
    #line6=""
    print("star "+line1+" (SAO Catalogue):")
    print(line2)
    print(line3)
    #if line5!="": print(line5)
    #if line6!="": print(line6)
    rish,rism,kulmh,kulmm,seth,setm=riseset2(starsaodb[i][j][k].ra,starsaodb[i][j][k].dec,-0.583,12,0,"p",0)
    if rish=="-":strrise="-"
    else: strrise=rish+"h "+rism+"m"
    if kulmh=="-":strkulm="-"
    else: strkulm=kulmh+"h "+kulmm+"m"
    if seth=="-":strset="-"
    else: strset=seth+"h "+setm+"m"
    print("RISE: "+strrise+"  CULM: "+strkulm+"  SET: "+strset)
    print()
    dsssave(starsaodb[i][j][k].ra,starsaodb[i][j][k].dec)
    isearchsave(line1.replace("/"," ")+" star")

#print dso1
def dso1print(i):
    line1=dso1db[i].nam2+" ("+dso1db[i].inf+")"
    if dso1db[i].sz1!=0:strsize=" SIZE="+str(dso1db[i].sz1)+"'"
    elif dso1db[i].sz2!=0:strsize=" SIZE="+str(dso1db[i].sz2)+"'"
    else: strsize=""
    if dso1db[i].m!="": strmagn=" MAGN="+dso1db[i].m
    else: strmagn=""
    if dso1db[i].br!="": strbr=" BRIGHТ="+dso1db[i].br
    else: strbr=""
    line2="RA(2000)="+str(dso1db[i].prvh)+"h "+str(dso1db[i].prvm)+"m "+str(dso1db[i].prvs)+"s "
    line2=line2+"DEC(2000)="+str(dso1db[i].sklg)+"d "+str(dso1db[i].sklm)+"m "+str(dso1db[i].skls)+"s"+strmagn+strbr+strsize
    rastr,decstr=grms(dso1db[i].ra,dso1db[i].dec)
    az,alt=calcaz(dso1db[i].ra,dso1db[i].dec,LMST)
    line3="RA="+rastr+" DEC="+decstr+" AZ="+str(round(az,2))+"d"+" ALT="+str(round(alt,2))+"d"
    print("deep sky object "+line1+":")
    print(line2)
    print(line3)
    rish,rism,kulmh,kulmm,seth,setm=riseset2(dso1db[i].ra,dso1db[i].dec,-0.583,12,0,"p",0)
    if rish=="-":strrise="-"
    else: strrise=rish+"h "+rism+"m"
    if kulmh=="-":strkulm="-"
    else: strkulm=kulmh+"h "+kulmm+"m"
    if seth=="-":strset="-"
    else: strset=seth+"h "+setm+"m"
    print("RISE: "+strrise+"  CULM: "+strkulm+"  SET: "+strset)
    print()
    dsssave(dso1db[i].ra,dso1db[i].dec)
    isearchsave(dso1db[i].nam2.replace("/"," ")+" deep sky")

#print dso2
def dso2print(i):
    line1=dso2db[i].nam2+" ("+dso2db[i].inf+")"
    if dso2db[i].sz1!=0:strsize=" SIZE="+str(dso2db[i].sz1)+"'"
    elif dso2db[i].sz2!=0:strsize=" SIZE="+str(dso2db[i].sz2)+"'"
    else: strsize=""
    if dso2db[i].m!="": strmagn=" MAGN="+dso2db[i].m
    else: strmagn=""
    if dso2db[i].br!="": strbr=" BRIGHТ="+dso2db[i].br
    else: strbr=""
    line2="RA(2000)="+str(dso2db[i].prvh)+"h "+str(dso2db[i].prvm)+"m "+str(dso2db[i].prvs)+"s "
    line2=line2+"DEC(2000)="+str(dso2db[i].sklg)+"d "+str(dso2db[i].sklm)+"m "+str(dso2db[i].skls)+"s"+strmagn+strbr+strsize
    rastr,decstr=grms(dso2db[i].ra,dso2db[i].dec)
    az,alt=calcaz(dso2db[i].ra,dso2db[i].dec,LMST)
    line3="RA="+rastr+" DEC="+decstr+" AZ="+str(round(az,2))+"d"+" ALT="+str(round(alt,2))+"d"
    print("deep sky object "+line1+":")
    print(line2)
    print(line3)
    rish,rism,kulmh,kulmm,seth,setm=riseset2(dso2db[i].ra,dso2db[i].dec,-0.583,12,0,"p",0)
    if rish=="-":strrise="-"
    else: strrise=rish+"h "+rism+"m"
    if kulmh=="-":strkulm="-"
    else: strkulm=kulmh+"h "+kulmm+"m"
    if seth=="-":strset="-"
    else: strset=seth+"h "+setm+"m"
    print("RISE: "+strrise+"  CULM: "+strkulm+"  SET: "+strset)
    print()
    dsssave(dso2db[i].ra,dso2db[i].dec)
    isearchsave(dso2db[i].nam2.replace("/"," ")+" deep sky")

#planet print
def planetprint(i):
    print(planetdb[i].str1)
    print(planetdb[i].str2)
    print(planetdb[i].str3)
    if planetdb[i].str1=="Moon:": print(planetdb[i].str4)
    riseset_iter(i,"p")
    print()
    dsssave(planetdb[i].ra,planetdb[i].dec)
    isearchsave(planetdb[i].str1.strip(":"))
#comet  print
def cometprint(j):
    print(cometdb[j].str1)
    print(cometdb[j].str2)
    print(cometdb[j].str3)
    print(cometdb[j].str4)
    print(cometdb[j].str5)
    riseset_iter(j,"pc")
    print()
    dsssave(cometdb[j].ra,cometdb[j].dec)
    isearchsave(cometdb[j].str1.strip(":"))
#asteroid  print
def asteroidprint(j):
    print(asterdb[j].str1)
    print(asterdb[j].str2)
    print(asterdb[j].str3)
    print(asterdb[j].str4)
    riseset_iter(j,"pa")
    print()
    dsssave(asterdb[j].ra,asterdb[j].dec)
    isearchsave(asterdb[j].str1.strip(":"))
#constellation  print
def constellationprint(i):
    print("constellation "+constlabdb[i].name2+" ("+constlabdb[i].name1+")")
    print()
    azimuth,alt=calcaz_xycanv(constlabdb[i].x,constlabdb[i].y)
    ra,dec=calcekv(azimuth,alt,LMST)
    dsssave(ra,dec)
    isearchsave("constellation "+constlabdb[i].name2+" "+constlabdb[i].name1)
#====================================================================
    #===Time
#====================================================================
def mjdf(day_,month_,year_,hour_): #calc MJD
    a=10000*year_+100*month_+day_
    if month_<=2:
        month_=month_+12
        year_=year_-1
    if a<=15821004.1:
        b=-2+int((year_+4716)/4)-1179
    else:
        b=int(year_/400)-int(year_/100)+int(year_/4)
    a=365*year_-679004
    mjd_=a+b+int(30.6001*(month_+1))+day_+hour_/24
    return(mjd_)

def lmstf(mjd_,mylon_): #calc LMST srednee mestnoe zvezdnoe vremia
    mjd0=int(mjd_)
    ut_=(mjd_-mjd0)*24
    t_=(mjd0-51544.5)/36525
    gmst_=6.697374558+1.0027379093*ut_+(8640184.812866+(0.093104-6.2E-6*t_)*t_)*t_/3600
    lmst_=24*frac((gmst_-mylon_/15)/24)
    return(lmst_)
#=======JD to DateTime
def jdtodate(jd):
    jd_=jd+0.5
    Z=int(jd_); F=jd_-Z
    if Z>=2299161:
        alp = int((Z - 1867216.25) / 36524.25)
        A = Z + 1 + alp - int(alp / 4)
    else:
        A = Z
    B = A + 1524
    C = int((B - 122.1) / 365.25)
    D = int(365.25 * C)
    E = int((B - D) / 30.6001)

    day=int(B - D - int(30.6001 * E) + F)
    
    if E < 14:
        month = E -  1
    else:
        month = E - 13
        
    if month > 2:
        year = C - 4716
    else:
        year = C - 4715

    hour=24*(jd_-int(jd_))

    return(year,month,day,hour)

#=========================================
def calcdeltat(year,month):
    #dt=62.92+0.32217*(year-2000)+0.005589*(year-2000)*(year-2000)
    y = year + (month - 0.5)/12
    if year<-500:
        u = (y-1820)/100
        dt = -20 + 32 * u^2
    elif -500<=year and year<500:
        u = y/100
        dt = 10583.6 - 1014.41 * u + 33.78311 * (u**2) - 5.952053 * (u**3) - 0.1798452 * (u**4) + 0.022174192 * (u**5) + 0.0090316521 * (u**6) 
    elif 500<=year and year<1600:
        u = (y-1000)/100
        dt = 1574.2 - 556.01 * u + 71.23472 * (u**2) + 0.319781 * (u**3) - 0.8503463 * (u**4) - 0.005050998 * (u**5) + 0.0083572073 * (u**6)
    elif 1600<=year and year<1700:
        t = y - 1600
        dt = 120 - 0.9808 * t - 0.01532 * (t**2) + (t**3) / 7129
    elif 1700<=year and year<1800:        
        t = y - 1700
        dt = 8.83 + 0.1603 * t - 0.0059285 * (t**2) + 0.00013336 * (t**3) - (t**4) / 1174000
    elif 1800<=year and year<1860:        
        t = y - 1800
        dt = 13.72 - 0.332447 * t + 0.0068612 * (t**2) + 0.0041116 * (t**3) - 0.00037436 * (t**4) + 0.0000121272 * (t**5) - 0.0000001699 * (t**6) + 0.000000000875 * (t**7)
    elif 1860<=year and year<1900:        
        t = y - 1860
        dt = 7.62 + 0.5737 * t - 0.251754 * (t**2) + 0.01680668 * (t**3) - 0.0004473624 * (t**4) + (t**5) / 233174
    elif 1900<=year and year<1920:        
        t = y - 1900
        dt = -2.79 + 1.494119 * t - 0.0598939 * (t**2) + 0.0061966 * (t**3) - 0.000197 * (t**4)
    elif 1920<=year and year<1941:        
        t = y - 1920
        dt = 21.20 + 0.84493*t - 0.076100 * (t**2) + 0.0020936 * (t**3)
    elif 1941<=year and year<1961:        
        t = y - 1950
        dt = 29.07 + 0.407*t - (t**2)/233 + (t**3) / 2547
    elif 1961<=year and year<1986:        
        t = y - 1975
        dt = 45.45 + 1.067*t - (t**2)/260 - (t**3) / 718
    elif 1986<=year and year<2005:        
        t = y - 2000
        dt = 63.86 + 0.3345 * t - 0.060374 * (t**2) + 0.0017275 * (t**3) + 0.000651814 * (t**4)	+ 0.00002373599 * (t**5)
    elif 2005<=year and year<2050:        
        t = y - 2000
        dt = 62.92 + 0.32217 * t + 0.005589 * (t**2)
    elif 2050<=year and year<2150:        
        dt = -20 + 32 * (((y-1820)/100)**2) - 0.5628 * (2150 - y)
    elif 2150<=year:        
        u = (y-1820)/100
        dt = -20 + 32 * (u**2)
    if 1955>year or year>2005:
        c = -0.000012932 * ((y - 1955) ** 2)
        dt=dt+c
    return(dt)
#=========================================
def dtnow(*args): # DateTime NOW in Entry
    deltahours=int(edt.get())
    timedelta_=timedelta(hours=DELTAHOURS)

    utcdtime=datetime.datetime.utcnow()
    ldtime=utcdtime+timedelta_
    ldtime=ldtime.strftime("%Y-%m-%d %H:%M:%S")
    lday=int(ldtime[8:10])
    lmonth=int(ldtime[5:7])
    lyear=int(ldtime[0:4])
    lhour=float(ldtime[11:13])+float(ldtime[14:16])/60+float(ldtime[17:19])/3600

    eyy.delete(0,END)
    emm.delete(0,END)
    edd.delete(0,END)
    ehh.delete(0,END)
    emin.delete(0,END)
    ess.delete(0,END)

    eyy.insert(0,lyear)
    emm.insert(0,lmonth)
    edd.insert(0,lday)
    ehh.insert(0,ldtime[11:13])
    emin.insert(0,ldtime[14:16])
    ess.insert(0,ldtime[17:19])
#============================================
def timeminus(*args): # button timeminus
    deltamin=-15
    timenew(deltamin)
def timeplus(*args): #button timeplus
    deltamin=15
    timenew(deltamin)
def timenew(deltamin):
    timedelta_=timedelta(minutes=deltamin)
    #lday=int(edd.get())
    #lmonth=int(emm.get())
    #lyear=int(eyy.get())
    #lhour=float(ehh.get())+float(emin.get())/60+float(ess.get())/3600
    #ldtime=datetime.datetime(lyear, lmonth, lday , int(ehh.get()) , int(emin.get()) , int(ess.get()))
    ldtime=datetime.datetime(LYEAR, LMONTH, LDAY , int(LDTIME[11:13]) , int(LDTIME[14:16]) , int(LDTIME[17:19]))
    ldtime=ldtime+timedelta_

    ldtime=ldtime.strftime("%Y-%m-%d %H:%M:%S")
    lday=int(ldtime[8:10])
    lmonth=int(ldtime[5:7])
    lyear=int(ldtime[0:4])
    lhour=float(ldtime[11:13])+float(ldtime[14:16])/60+float(ldtime[17:19])/3600

    eyy.delete(0,END)
    emm.delete(0,END)
    edd.delete(0,END)
    ehh.delete(0,END)
    emin.delete(0,END)
    ess.delete(0,END)

    eyy.insert(0,lyear)
    emm.insert(0,lmonth)
    edd.insert(0,lday)
    ehh.insert(0,ldtime[11:13])
    emin.insert(0,ldtime[14:16])
    ess.insert(0,ldtime[17:19])
    start()
#==========================================================================
#==========================================================================
# calc az,alt po x,y canv
def calcaz_xycanv(xclick,yclick):
    azimuth=d180pi*atan2(yclick-ZOOM*RCANV/2,xclick-ZOOM*RCANV/2)

    y_=yclick-ZOOM*RCANV/2
    x_=xclick-ZOOM*RCANV/2
    if y_==0 and x_==0:alt=pid2
    else:
        if abs(y_)>abs(x_):
            ky=ZOOM*RADIUS * sin(azimuth*pid180)
            alt=2*atan((-y_/ky+1)/(y_/ky+1))
        else:
            kx=ZOOM*RADIUS * cos(azimuth*pid180)
            alt=2*atan((-x_/kx+1)/(x_/kx+1))
            
    #alt=2*atan((y_/k-1)/(y_/k+1))
    alt=alt*d180pi

    if azimuth>0:azimuth=360-azimuth
    if azimuth<0:azimuth=-azimuth
    azimuth=ugminus(azimuth,TURN_ANGLE*d180pi+90)
    if KPOL==-1:azimuth=ugminus(azimuth,180)

    return(azimuth,alt)
#==========================================================
#canvas click
def click1(event):
    xclick = canvas.canvasx(event.x)
    yclick = canvas.canvasy(event.y)
    ctrl=0
    canv_click(xclick,yclick,ctrl)

def click2(event):
    xclick = canvas.canvasx(event.x)
    yclick = canvas.canvasy(event.y)
    ctrl=1
    canv_click(xclick,yclick,ctrl)
    
def canv_click(xclick,yclick,ctrl):
    global NPOINTCLICK,RA1,DEC1,RA2,DEC2
    nclick=1
    if NPOINTCLICK==0: NPOINTCLICK=1;nclick=0
    elif NPOINTCLICK==1: NPOINTCLICK=2
    elif NPOINTCLICK==2: NPOINTCLICK=1
    rx2=root.winfo_width()
    ry2=root.winfo_height()
    if MOVE==1 and ctrl==0:
        canvas.xview_moveto((xclick/RCANV/ZOOM)-rx2/(ZOOM*2*RCANV))
        canvas.yview_moveto((yclick/RCANV/ZOOM)-ry2/(ZOOM*2*RCANV))

    canvas.delete("click")
    linexy(xclick-10,yclick,xclick-30,yclick,1,clickcolor,"click")
    linexy(xclick,yclick+10,xclick,yclick+30,1,clickcolor,"click")

    azimuth,alt=calcaz_xycanv(xclick,yclick)
    
    ra,dec=calcekv(azimuth,alt,LMST)

    if ctrl==1:
        efind.delete(0,END)
        efind.insert(0,str(round(ra,4))+" "+str(round(dec,3)))

    rastr,decstr=grms(ra,dec)
    print("point <"+str(NPOINTCLICK)+">:"+" RA="+rastr+" DEC="+decstr+" AZ="+str(round(azimuth,2))+"d"+" ALT="+str(round(alt,2))+"d")
#Rise Set
    rish,rism,kulmh,kulmm,seth,setm=riseset2(ra,dec,-0.583,12,0,"p",0)
    if rish=="-":strrise="-"
    else: strrise=rish+"h "+rism+"m"
    if kulmh=="-":strkulm="-"
    else: strkulm=kulmh+"h "+kulmm+"m"
    if seth=="-":strset="-"
    else: strset=seth+"h "+setm+"m"
    print("RISE: "+strrise+"  CULM: "+strkulm+"  SET: "+strset)
#Uglomer
    if NPOINTCLICK==1:RA1=ra*15*pid180;DEC1=dec*pid180
    if NPOINTCLICK==2:RA2=ra*15*pid180;DEC2=dec*pid180
    if nclick==1: cosd=sin(DEC1)*sin(DEC2)+cos(DEC1)*cos(DEC2)*cos(RA1-RA2)
    if nclick==1 and cosd<=1 and cosd>=-1 and NPOINTCLICK==1:
        angle=round(d180pi*acos(cosd),4)
        rastr,decstr=grms(0,d180pi*acos(cosd))
        print("angle with <2>: "+decstr+" ("+str(angle)+"d)")
    if nclick==1 and cosd<=1 and cosd>=-1 and NPOINTCLICK==2:
        angle=round(d180pi*acos(cosd),4)
        rastr,decstr=grms(0,d180pi*acos(cosd))
        print("angle with <1>: "+decstr+" ("+str(angle)+"d)")
    if ZOOM>=ZOOMHIP: hippaint(0)
    if ZOOM>=ZOOMSAO: saopaint(0)

    dsssave(ra,dec)
    print()
#=====================OPEN FILE
def openfile(filename):
    if filename=="DSS.url": link=DSSLINK
    else: link=ILINK
    
    if sys.platform == "win32" or sys.platform == "win64":
        os.startfile(filename)
    else:
        if sys.platform == "darwin":
            opener ="open"
            os.system(opener+" "+filename)
        else:
            opener ="xdg-open"
            subprocess.call(["xdg-open", link])
            #os.system(opener+" "+filename)
            
#=====================DSS save
def dsssave(ra,dec):
    global DSSLINK
    ra_,dec_=ekvtoekv2000(ra,dec)
    #save DSS link
    line="URL=http://archive.stsci.edu/cgi-bin/dss_search?v="+DSS_VER+"&r="+str(round(ra_,5))+"%2000"+"&d="+str(round(dec_,5))+"&e=J2000"+"&h="+DSS_SZ1+"&w="+DSS_SZ2+"&f=gif&c=none&fov=NONE&v3="
    DSSLINK="http://archive.stsci.edu/cgi-bin/dss_search?v="+DSS_VER+"&r="+str(round(ra_,5))+"%2000"+"&d="+str(round(dec_,5))+"&e=J2000"+"&h="+DSS_SZ1+"&w="+DSS_SZ2+"&f=gif&c=none&fov=NONE&v3="
    f = open('DSS.url', 'w')
    f.write("[InternetShortcut]"+ "\n")
    f.write(line+ "\n")
    f.close()
#=====================SEARCH link save
def isearchsave(str):
    global ILINK
    line="URL=https://www.google.by/search?ie=UTF-8&hl=ru&q="+str
    #line="URL=https://yandex.by/search/?text="+str
    ILINK="https://www.google.by/search?ie=UTF-8&hl=ru&q="+str
    f = open('ISEARCH.url', 'w')
    f.write("[InternetShortcut]"+ "\n")
    f.write(line+ "\n")
    f.close()
#=============Mouse button2
def canv_but2(event):
    xclick = canvas.canvasx(event.x)
    yclick = canvas.canvasy(event.y)
    stext(xclick,yclick,0,0,efind.get(),textcolor,font1,"but2text")
    line=efind.get().strip()
    if line=="del" or line=="DEL" or line=="Del" or line=="delete" or line=="DELETE" or line=="Delete": canvas.delete("but2text")
#=================
    
def rclick_paint(x,y):
    canvas.delete("rclick")
    linexy(x-10,y,x-30,y,1,rclickcolor,"rclick")
    linexy(x,y+10,x,y+30,1,rclickcolor,"rclick")
   
#bstar rightclick
def bstar_rightclick(event,tag):
    xclick = canvas.canvasx(event.x);yclick = canvas.canvasy(event.y)
    rclick_paint(xclick,yclick)
    i=int(tag[5:])
    bscstarprint(i)
#starhip rightclick
def starhip_rightclick(event,tag):
    xclick = canvas.canvasx(event.x);yclick = canvas.canvasy(event.y)
    rclick_paint(xclick,yclick)
    i=int(tag[7:9])
    j=int(tag[9:11])
    k=int(tag[11:])
    hipstarprint(i,j,k)
#starsao rightclick
def starsao_rightclick(event,tag):
    xclick = canvas.canvasx(event.x);yclick = canvas.canvasy(event.y)
    rclick_paint(xclick,yclick)
    i=int(tag[7:9])
    j=int(tag[9:11])
    k=int(tag[11:])
    saostarprint(i,j,k)
#dso1 rightclick
def dso1_rightclick(event,tag):
    xclick = canvas.canvasx(event.x);yclick = canvas.canvasy(event.y)
    rclick_paint(xclick,yclick)
    i=int(tag[5:])
    dso1print(i)
#dso2 rightclick
def dso2_rightclick(event,tag):
    xclick = canvas.canvasx(event.x);yclick = canvas.canvasy(event.y)
    rclick_paint(xclick,yclick)
    i=int(tag[5:])
    dso2print(i)
#planet rightclick
def planet_rightclick(event,tag):
    xclick = canvas.canvasx(event.x);yclick = canvas.canvasy(event.y)
    rclick_paint(xclick,yclick)
    i=int(tag[6:])
    planetprint(i)
#Jupiter satellites rightclick
def jsat_rightclick(event,tag):
    xclick = canvas.canvasx(event.x);yclick = canvas.canvasy(event.y)
    rclick_paint(xclick,yclick)
    i=int(tag[4:])
    print(jsatdb[i].name+" (Jupiter's satellite)")
    print()
#Saturn satellites rightclick
def ssat_rightclick(event,tag):
    xclick = canvas.canvasx(event.x);yclick = canvas.canvasy(event.y)
    rclick_paint(xclick,yclick)
    i=int(tag[4:])
    print(ssatdb[i].name+" (Saturn's satellite)")
    print()
#comet  rightclick
def comet_rightclick(event,tag):
    xclick = canvas.canvasx(event.x);yclick = canvas.canvasy(event.y)
    rclick_paint(xclick,yclick)
    j=int(tag[5:])
    cometprint(j)
#asteroid  rightclick
def asteroid_rightclick(event,tag):
    xclick = canvas.canvasx(event.x);yclick = canvas.canvasy(event.y)
    rclick_paint(xclick,yclick)
    j=int(tag[8:])
    asteroidprint(j)
#constellation  rightclick    
def constellation_rightclick(event,tag):
    xclick = canvas.canvasx(event.x);yclick = canvas.canvasy(event.y)
    rclick_paint(xclick,yclick)
    i=int(tag[13:])
    constellationprint(i)
#=========================================================================
#insert press
def insert_press(event):
    global MOVE
    if MOVE==0: MOVE=1
    else: MOVE=0

#left press
def left_press(event):
    bstart.focus()
    qx=canvas.xview()
    rx2=root.winfo_width()
    canvas.xview_moveto((qx[0]+qx[1])/2-0.05/ZOOM-rx2/(ZOOM*2*RCANV))
    if ZOOM>=ZOOMHIP: hippaint(event)
    if ZOOM>=ZOOMSAO: saopaint(event)    
#right press
def right_press(event):
    bstart.focus()
    qx=canvas.xview()
    rx2=root.winfo_width()
    canvas.xview_moveto((qx[0]+qx[1])/2+0.05/ZOOM-rx2/(ZOOM*2*RCANV))
    if ZOOM>=ZOOMHIP: hippaint(event)
    if ZOOM>=ZOOMSAO: saopaint(event)    
#up press
def up_press(event):
    bstart.focus()
    qy=canvas.yview()
    ry2=root.winfo_height()
    canvas.yview_moveto((qy[0]+qy[1])/2-0.05/ZOOM-ry2/(ZOOM*2*RCANV))
    if ZOOM>=ZOOMHIP: hippaint(event)
    if ZOOM>=ZOOMSAO: saopaint(event)    
#down press
def down_press(event):
    bstart.focus()
    qy=canvas.yview()
    ry2=root.winfo_height()
    canvas.yview_moveto((qy[0]+qy[1])/2+0.05/ZOOM-ry2/(ZOOM*2*RCANV))
    if ZOOM>=ZOOMHIP: hippaint(event)
    if ZOOM>=ZOOMSAO: saopaint(event)    
#Alt+f press
def altf_press(event):
    root.attributes('-fullscreen', True)
#Esc press
def esc_press(event):
    root.attributes('-fullscreen', False)

def entry_control(*args):
    def check_int(new_v,v1,v2):
        err=0
        try:
            int(new_v)
        except:
            err=1
        if err==0:
            if int(new_v)<v1 or int(new_v)>v2: err=1
        return(err)

    def check_float(new_v,v1,v2):
        err=0
        try:
            float(new_v)
        except:
            err=1
        if err==0:
            if float(new_v)<v1 or float(new_v)>v2: err=1
        return(err)

    fstart=0; 
    if check_float(elat.get().strip(),0,90)==1:
        elat.delete(0,END)
        elat.insert(0,"E")
        fstart=1
    if check_float(elon.get().strip(),0,180)==1:
        elon.delete(0,END)
        elon.insert(0,"E")
        fstart=1
    if check_int(eyy.get().strip(),1,9999)==1:
        eyy.delete(0,END)
        eyy.insert(0,"E")
        fstart=1
    if check_int(emm.get().strip(),1,12)==1:
        emm.delete(0,END)
        emm.insert(0,"E")
        fstart=1
    if check_float(emagn.get().strip(),-99,99)==1:
        emagn.delete(0,END)
        emagn.insert(0,"E")
        fstart=1
        
    if fstart==0:
        mm=int(emm.get().strip()); yy=int(eyy.get().strip())
        if mm==1 or mm==3 or mm==5 or mm==7 or mm==8 or mm==10 or mm==12: ndays=31
        elif mm==4 or mm==6 or mm==9 or mm==11: ndays=30
        elif mm==2 and frac(yy/400)==0: ndays=29
        elif mm==2 and frac(yy/400)!=0 and frac(yy/100)==0: ndays=28
        elif mm==2 and frac(yy/400)!=0 and frac(yy/100)!=0 and frac(yy/4)==0: ndays=29
        elif mm==2 and frac(yy/4)!=0: ndays=28
    else: ndays=31
        
    if check_int(edd.get().strip(),1,ndays)==1:
        edd.delete(0,END)
        edd.insert(0,"E")
        fstart=1
    if check_int(ehh.get().strip(),0,23)==1:
        ehh.delete(0,END)
        ehh.insert(0,"E")
        fstart=1
    if check_int(emin.get().strip(),0,59)==1:
        emin.delete(0,END)
        emin.insert(0,"E")
        fstart=1
    if check_int(ess.get().strip(),0,59)==1:
        ess.delete(0,END)
        ess.insert(0,"E")
        fstart=1
    if check_float(edt.get().strip(),-12,14)==1:
        edt.delete(0,END)
        edt.insert(0,"E")
        fstart=1

    if fstart==0:
        start()

#==========canvas1 create
root=Tk()
root.title("PyStars")
#=======IKONKA
#root.iconbitmap("PyStars16.ico")

imgicon = PhotoImage(file="PyStars.png")
root.tk.call("wm", "iconphoto", root._w, imgicon)
#===============
rx=root.winfo_screenwidth()-120 #razmer ekrana x
ry=root.winfo_screenheight()-140 #razmer ekrana y
strgeometry=str(rx)+"x"+str(ry)+"+50+50"
root.wm_geometry(strgeometry) #razmer+verhniy leviy ugol
root.resizable(width=True, height=True)
root.config(highlightbackground=skycolor,highlightthickness=0)

#RADIUS=root.winfo_screenwidth()/2 #Radius kruga pikseley
RADIUS=root.winfo_screenheight()*2/3 #Radius kruga pikseley
RCANV=root.winfo_screenwidth()*1.2 #Razmer canvasa pikseley
RCANVD2=RCANV/2

frame=Frame(root,width=rx,height=ry,bd=-1)
frame.grid(row=20,column=10)
frame.config(highlightbackground=skycolor,highlightthickness=0)
frame.pack(side=BOTTOM)

#root.tk_setPalette(background=menu_dcolor,foreground=menu_lcolor)

#panel=Canvas(root,width=1000,height=40)
#panel.place(x=5,y=5)
yy1=3
yy2=27
yy3=25

llat = Label(root, text="LAT:")
llat.config(width=4,height=1)
llat.config(highlightbackground=skycolor,highlightthickness=0,background=skycolor,foreground=menu_lcolor,font=font3,bd=1)
llat.place(x=7,y=yy1)

llon = Label(root, text="LON:")
llon.config(width=4,height=1)
llon.config(highlightbackground=skycolor,highlightthickness=0,background=skycolor,foreground=menu_lcolor,font=font3,bd=1)
llon.place(x=124,y=yy1)

ldat = Label(root, text="DATE:")
ldat.config(width=5,height=1)
ldat.config(highlightbackground=skycolor,highlightthickness=0,background=skycolor,foreground=menu_lcolor,font=font3,bd=1)
ldat.place(x=242,y=yy1)

ltim = Label(root, text="TIME:")
ltim.config(width=5,height=1)
ltim.config(highlightbackground=skycolor,highlightthickness=0,background=skycolor,foreground=menu_lcolor,font=font3,bd=1)
ltim.place(x=332,y=yy1)

lgrid = Label(root, text="GRID:")
lgrid.config(width=5,height=1)
lgrid.config(highlightbackground=skycolor,highlightthickness=0,background=skycolor,foreground=menu_lcolor,font=font3,bd=1)
lgrid.place(x=450,y=yy1)

lturnvar="DIR:"
lturn = Label(root,text=lturnvar)
lturn.config(width=4,height=1)
lturn.config(highlightbackground=skycolor,highlightthickness=0,background=skycolor,foreground=menu_lcolor,font=font3,bd=1)
lturn.place(x=550,y=yy1)

lzoom = Label(root, text="ZOOM:")
lzoom.config(width=6,height=1)
lzoom.config(highlightbackground=skycolor,highlightthickness=0,background=skycolor,foreground=menu_lcolor,font=font3,bd=1)
lzoom.place(x=615,y=yy1)

ldt = Label(root, text="dT:")
ldt.config(width=3,height=1)
ldt.config(highlightbackground=skycolor,highlightthickness=0,background=skycolor,foreground=menu_lcolor,font=font3,bd=1)
ldt.place(x=118,y=yy3+27)

lmagn = Label(root, text="mLIM:")
lmagn.config(width=5,height=1)
lmagn.config(highlightbackground=skycolor,highlightthickness=0,background=skycolor,foreground=menu_lcolor,font=font3,bd=1)
lmagn.place(x=7,y=yy3+25+27+27+20+30)

elat = Entry(root)
elat.config(width=7,font=font3)
elat.config(highlightbackground=skycolor,highlightthickness=0,bg=menu_lcolor,fg=menu_dcolor,selectbackground=menu_selcolor,selectforeground=menu_lcolor,justify="left",insertbackground=menu_dcolor,bd=1)
elat.place(x=7,y=yy2)

clatvar=IntVar()
clatvar.set(0)
clat=Checkbutton(root, text="NORTH", variable=clatvar,onvalue=1,offvalue=0)
clat.config(highlightbackground=skycolor,highlightthickness=0,background=skycolor,foreground=menu_lcolor,selectcolor=skycolor,activebackground=skycolor,activeforeground=menu_lcolor,bd=1)
clat.config(font=font3)
clat.place(x=53,y=yy2)
#clat.select()

elon = Entry(root)
elon.config(width=7,font=font3)
elon.config(highlightbackground=skycolor,highlightthickness=0,bg=menu_lcolor,fg=menu_dcolor,selectbackground=menu_selcolor,selectforeground=menu_lcolor,justify="left",insertbackground=menu_dcolor,bd=1)
elon.place(x=124,y=yy2)

clonvar=IntVar()
clonvar.set(0)
clon=Checkbutton(root, text="EAST", variable=clonvar,onvalue=1,offvalue=0)
clon.config(highlightbackground=skycolor,highlightthickness=0,background=skycolor,foreground=menu_lcolor,selectcolor=skycolor,activebackground=skycolor,activeforeground=menu_lcolor,bd=1)
clon.config(font=font3)
clon.place(x=172,y=yy2)
#clon.select()

ctrackvar=IntVar()
ctrackvar.set(0)
ctrack=Checkbutton(root, text="LABELS", variable=ctrackvar,onvalue=1,offvalue=0)
ctrack.config(highlightbackground=skycolor,highlightthickness=0,background=skycolor,foreground=menu_lcolor,selectcolor=skycolor,activebackground=skycolor,activeforeground=menu_lcolor,bd=1)
ctrack.config(font=font3)
ctrack.place(x=101,y=yy3+25+27+27+13)

eyy = Entry(root)
eyy.config(width=4,font=font3)
eyy.config(highlightbackground=skycolor,highlightthickness=0,bg=menu_lcolor,fg=menu_dcolor,selectbackground=menu_selcolor,selectforeground=menu_lcolor,justify="left",insertbackground=menu_dcolor,bd=1)
eyy.place(x=242,y=yy2)

emm = Entry(root)
emm.config(width=2,font=font3)
emm.config(highlightbackground=skycolor,highlightthickness=0,bg=menu_lcolor,fg=menu_dcolor,selectbackground=menu_selcolor,selectforeground=menu_lcolor,justify="left",insertbackground=menu_dcolor,bd=1)
emm.place(x=276,y=yy2)

edd = Entry(root)
edd.config(width=2,font=font3)
edd.config(highlightbackground=skycolor,highlightthickness=0,bg=menu_lcolor,fg=menu_dcolor,selectbackground=menu_selcolor,selectforeground=menu_lcolor,justify="left",insertbackground=menu_dcolor,bd=1)
edd.place(x=296,y=yy2)

ehh = Entry(root)
ehh.config(width=2,font=font3)
ehh.config(highlightbackground=skycolor,highlightthickness=0,bg=menu_lcolor,fg=menu_dcolor,selectbackground=menu_selcolor,selectforeground=menu_lcolor,justify="left",insertbackground=menu_dcolor,bd=1)
ehh.place(x=332,y=yy2)

emin = Entry(root)
emin.config(width=2,font=font3)
emin.config(highlightbackground=skycolor,highlightthickness=0,bg=menu_lcolor,fg=menu_dcolor,selectbackground=menu_selcolor,selectforeground=menu_lcolor,justify="left",insertbackground=menu_dcolor,bd=1)
emin.place(x=352,y=yy2)

ess = Entry(root)
ess.config(width=2,font=font3)
ess.config(highlightbackground=skycolor,highlightthickness=0,bg=menu_lcolor,fg=menu_dcolor,selectbackground=menu_selcolor,selectforeground=menu_lcolor,justify="left",insertbackground=menu_dcolor,bd=1)
ess.place(x=372,y=yy2)

edt = Entry(root)
edt.config(width=3,font=font3)
edt.config(highlightbackground=skycolor,highlightthickness=0,bg=menu_lcolor,fg=menu_dcolor,selectbackground=menu_selcolor,selectforeground=menu_lcolor,justify="left",insertbackground=menu_dcolor,bd=1)
edt.place(x=147,y=yy3+27)

etrack = Entry(root)
etrack.config(width=6,font=font3)
etrack.config(highlightbackground=skycolor,highlightthickness=0,bg=menu_lcolor,fg=menu_dcolor,selectbackground=menu_selcolor,selectforeground=menu_lcolor,justify="left",insertbackground=menu_dcolor,bd=1)
etrack.place(x=55,y=yy3+25+27+27+13)

efind = Entry(root)
efind.config(width=15,font=font3)
efind.config(highlightbackground=skycolor,highlightthickness=0,bg=menu_lcolor,fg=menu_dcolor,selectbackground=menu_selcolor,selectforeground=menu_lcolor,justify="left",insertbackground=menu_dcolor,bd=1)
efind.place(x=55,y=yy3+25+25+13)

emagn = Entry(root)
emagn.config(width=4,font=font3)
emagn.config(highlightbackground=skycolor,highlightthickness=0,bg=menu_lcolor,fg=menu_dcolor,selectbackground=menu_selcolor,selectforeground=menu_lcolor,justify="left",insertbackground=menu_dcolor,bd=1)
emagn.place(x=53,y=yy3+25+27+27+20+30)

bfind = Button(root)
bfind.config(width=5,text="Find",command=objfind,padx=0,pady=0,font=font3)
bfind.config(highlightbackground=skycolor,highlightthickness=0,bg=menu_lcolor,fg=menu_dcolor,justify="center",activebackground=menu_lcolor,activeforeground=menu_dcolor,bd=1)
bfind.place(x=7,y=yy3+25+25+13)

btrack = Button(root)
btrack.config(width=5,text="+days",command=sstrack,padx=0,pady=0,font=font3)
btrack.config(highlightbackground=skycolor,highlightthickness=0,bg=menu_lcolor,fg=menu_dcolor,justify="center",activebackground=menu_lcolor,activeforeground=menu_dcolor,bd=1)
btrack.place(x=7,y=yy3+25+27+27+13)

brisset = Button(root)
brisset.config(width=9,text="RiseSet",command=riseset,padx=0,pady=0,font=font3)
brisset.config(highlightbackground=skycolor,highlightthickness=0,bg=menu_lcolor,fg=menu_dcolor,justify="center",activebackground=menu_lcolor,activeforeground=menu_dcolor,bd=1)
brisset.place(x=7,y=yy3+25+25+30+30+30+15)

bhide = Button(root)
bhide.config(width=1,text="h",command=hide,padx=0,pady=0,font=font3)
bhide.config(highlightbackground=skycolor,highlightthickness=0,bg=menu_lcolor,fg=menu_dcolor,justify="center",activebackground=menu_lcolor,activeforeground=menu_dcolor,bd=1)
bhide.place(x=7,y=yy3+25+25+30+30+30+30+15)

def dssstart(*args): openfile("DSS.url")
bdss = Button(root)
bdss.config(width=1,text="d",command=dssstart,padx=0,pady=0,font=font3)
bdss.config(highlightbackground=skycolor,highlightthickness=0,bg=menu_lcolor,fg=menu_dcolor,justify="center",activebackground=menu_lcolor,activeforeground=menu_dcolor,bd=1)
bdss.place(x=7,y=yy3+25+25+30+30+30+30+30+15)

def isearchstart(*args): openfile("ISEARCH.url")
bisearch = Button(root)
bisearch.config(width=1,text="i",command=isearchstart,padx=0,pady=0,font=font3)
bisearch.config(highlightbackground=skycolor,highlightthickness=0,bg=menu_lcolor,fg=menu_dcolor,justify="center",activebackground=menu_lcolor,activeforeground=menu_dcolor,bd=1)
bisearch.place(x=7,y=yy3+25+25+30+30+30+30+30+30+15)

bnow = Button(root)
bnow.config(width=4,text="Now",command=dtnow,padx=0,pady=0,font=font3)
bnow.config(highlightbackground=skycolor,highlightthickness=0,bg=menu_lcolor,fg=menu_dcolor,justify="center",activebackground=menu_lcolor,activeforeground=menu_dcolor,bd=1)
bnow.place(x=242,y=yy3+25)

btminus = Button(root)
btminus.config(width=2,text="<",command=timeminus,padx=0,pady=0,font=font3)
btminus.config(highlightbackground=skycolor,highlightthickness=0,bg=menu_lcolor,fg=menu_dcolor,justify="center",activebackground=menu_lcolor,activeforeground=menu_dcolor,bd=1)
btminus.place(x=332,y=yy3+25)

btplus = Button(root)
btplus.config(width=2,text=">",command=timeplus,padx=0,pady=0,font=font3)
btplus.config(highlightbackground=skycolor,highlightthickness=0,bg=menu_lcolor,fg=menu_dcolor,justify="center",activebackground=menu_lcolor,activeforeground=menu_dcolor,bd=1)
btplus.place(x=355,y=yy3+25)

bstart = Button(root)
bstart.config(width=10,text="Apply",command=entry_control,padx=0,pady=0,font=font3)
bstart.config(highlightbackground=skycolor,highlightthickness=0,bg=menu_lcolor,fg=menu_dcolor,justify="center",activebackground=menu_lcolor,activeforeground=menu_dcolor,bd=1)
bstart.place(x=715,y=yy3+1)

ogridvar=StringVar()
ogridvar.set("EQ")
ogrid=OptionMenu(root,ogridvar,*["EQ","AZ","EQ&AZ","NO GRID"])
ogrid.config(width=8,padx=0,pady=0,font=font3)
ogrid.config(highlightbackground=skycolor,highlightthickness=0,bg=menu_lcolor,fg=menu_dcolor,justify="left",activebackground=menu_lcolor,activeforeground=menu_dcolor,bd=2)
ogrid.nametowidget(ogrid.menuname).config(bg=menu_lcolor,fg=menu_dcolor,activebackground=menu_selcolor,activeforeground=menu_lcolor,bd=1)
ogrid.nametowidget(ogrid.menuname).config(font=font3)
ogrid.place(x=450,y=yy3+2)

oturnvar=StringVar()
oturnvar.set("S")
oturn=OptionMenu(root,oturnvar,*["S","SE","E","NE","N","NW","W","SW"])
oturn.config(width=3,padx=0,pady=0,font=font3)
oturn.config(highlightbackground=skycolor,highlightthickness=0,bg=menu_lcolor,fg=menu_dcolor,justify="left",activebackground=menu_lcolor,activeforeground=menu_dcolor,bd=2)
oturn.nametowidget(oturn.menuname).config(bg=menu_lcolor,fg=menu_dcolor,activebackground=menu_selcolor,activeforeground=menu_lcolor,bd=1)
oturn.nametowidget(oturn.menuname).config(font=font3)
oturn.place(x=550,y=yy3+2)

ozoomvar=StringVar()
ozoomvar.set("1")
ozoom=OptionMenu(root,ozoomvar,*["1","2","3","5","10","20","50","100","200"])
ozoom.config(width=3,padx=0,pady=0,font=font3)
ozoom.config(highlightbackground=skycolor,highlightthickness=0,bg=menu_lcolor,fg=menu_dcolor,justify="left",activebackground=menu_lcolor,activeforeground=menu_dcolor,bd=2)
ozoom.nametowidget(ozoom.menuname).config(bg=menu_lcolor,fg=menu_dcolor,activebackground=menu_selcolor,activeforeground=menu_lcolor,bd=1)
ozoom.nametowidget(ozoom.menuname).config(font=font3)
ozoom.place(x=615,y=yy3+2)

bhide.lower()
hide()

#=====
canvas=Canvas(frame,bg=skycolor,width=root.winfo_screenwidth(),height=root.winfo_screenheight(),scrollregion=(0,0,ZOOM*RCANV,ZOOM*RCANV))
canvasL=Canvas(frame,bg=skycolor,width=25,height=150,bd=-1,relief="sunken")
#canvasL.config(highlightbackground=menu_lcolor)
canvasL.config(highlightbackground=skycolor,highlightthickness=0)
canvasL.place(anchor="sw",relx=0.01,rely=0.95)
hbar=Scrollbar(frame,orient=HORIZONTAL)
hbar.pack(side=BOTTOM,fill=X)
hbar.config(command=canvas.xview,width=16,elementborderwidth=-1,bd=1,highlightbackground=skycolor,highlightthickness=0)
vbar=Scrollbar(frame,orient=VERTICAL)
vbar.pack(side=RIGHT,fill=Y)
vbar.config(command=canvas.yview,width=16,elementborderwidth=-1,bd=1,highlightbackground=skycolor,highlightthickness=0)
canvas.config(highlightbackground=skycolor,highlightthickness=2,xscrollcommand=hbar.set, yscrollcommand=vbar.set,bd=0)
canvas.pack(side=LEFT,expand=True,fill=BOTH)
canvas.xview_moveto(1/2-rx/(ZOOM*2*RCANV))
canvas.yview_moveto(1/2-ry/(ZOOM*2*RCANV))

canvas.bind("<Button-1>", click1)
canvas.bind("<Button-2>", canv_but2)
canvas.bind("<Control-Button-1>", click2)
root.bind("<Insert>", insert_press)
root.bind("<Alt-Left>", left_press)
root.bind("<Alt-Right>", right_press)
root.bind("<Control-Left>", timeminus)
root.bind("<Control-Right>", timeplus)
root.bind("<Alt-Up>", up_press)
root.bind("<Alt-Down>", down_press)
root.bind("<Alt-f>", altf_press)
root.bind("<Alt-F>", altf_press)
root.bind("<Alt-n>", dtnow)
root.bind("<Alt-N>", dtnow)
root.bind("<Alt-h>", hide)
root.bind("<Alt-H>", hide)
root.bind("<Alt-r>", riseset)
root.bind("<Alt-R>", riseset)
root.bind("<Alt-d>", dssstart)
root.bind("<Alt-D>", dssstart)
root.bind("<Alt-i>", isearchstart)
root.bind("<Alt-I>", isearchstart)
root.bind("<Escape>", esc_press)
if ZOOMHIP<9999:
    hbar.bind("<ButtonRelease>", hippaint)
    vbar.bind("<ButtonRelease>", hippaint)
if ZOOMSAO<9999:
    hbar.bind("<ButtonRelease>", saopaint)
    vbar.bind("<ButtonRelease>", saopaint)
efind.bind("<Return>", objfind)
etrack.bind("<Return>", sstrack)
eyy.bind("<Return>", entry_control)
emm.bind("<Return>", entry_control)
edd.bind("<Return>", entry_control)
ehh.bind("<Return>", entry_control)
emin.bind("<Return>", entry_control)
ess.bind("<Return>", entry_control)
edt.bind("<Return>", entry_control)
elat.bind("<Return>", entry_control)
elon.bind("<Return>", entry_control)
bstart.bind("<Return>", entry_control)
emagn.bind("<Return>", entry_control)

#==================================SAVE MAP
def savemap(*args):
    x1=root.winfo_rootx(); y1=root.winfo_rooty()
    x2=x1+root.winfo_width()-20; y2=y1+root.winfo_height()-20
    if x2>root.winfo_screenwidth(): x2=root.winfo_screenwidth();
    if y2>root.winfo_screenheight(): y2=root.winfo_screenheight();
    img = ImageGrab.grab(bbox=(x1, y1, x2, y2))
    for i in range(0, img.size[0]-1):
        for j in range(0, img.size[1]-1):
            pixelColorVals = img.getpixel((i,j));
            redPixel    = 255 - pixelColorVals[0]; # Negate red pixel
            greenPixel  = 255 - pixelColorVals[1]; # Negate green pixel
            bluePixel   = 255 - pixelColorVals[2]; # Negate blue pixel
            img.putpixel((i,j),(redPixel, greenPixel, bluePixel));
    img=img.convert("L")
    img.save("map.gif", "GIF")

PILLOW="OK"
try:
    if sys.platform != "win32" and sys.platform != "win64" and sys.platform != "darwin":    
        from PIL import Image, ImageFilter
        import pyscreenshot as ImageGrab
    else:
        from PIL import Image, ImageGrab,ImageFilter    
except:
    PILLOW="NO"

if PILLOW=="OK":
    root.bind("<Alt-s>", savemap)
    root.bind("<Alt-S>", savemap)
#==================================
    
for i in range(0,len(stardb)):
    tag = "bstar" + str(i)
    callback_bstar = lambda event, tag=tag: bstar_rightclick(event,tag)
    canvas.tag_bind(tag,"<Button-3>", callback_bstar)

for i in range(0,len(dso1db)):
    tag = "dso1_" + str(i)
    callback_dso1 = lambda event, tag=tag: dso1_rightclick(event,tag)
    canvas.tag_bind(tag,"<Button-3>", callback_dso1)

for i in range(0,len(dso2db)):
    tag = "dso2_" + str(i)
    callback_dso2 = lambda event, tag=tag: dso2_rightclick(event,tag)
    canvas.tag_bind(tag,"<Button-3>", callback_dso2)

for i in range(0,10):
    tag = "planet" + str(i)
    callback_planet = lambda event, tag=tag: planet_rightclick(event,tag)
    canvas.tag_bind(tag,"<Button-3>", callback_planet)

for i in range(0,4):
    tag = "jsat" + str(i)
    callback_jsat = lambda event, tag=tag: jsat_rightclick(event,tag)
    canvas.tag_bind(tag,"<Button-3>", callback_jsat)

for i in range(0,8):
    tag = "ssat" + str(i)
    callback_ssat = lambda event, tag=tag: ssat_rightclick(event,tag)
    canvas.tag_bind(tag,"<Button-3>", callback_ssat)

for i in range(0,len(cometdb)):
    tag = "comet" + str(i)
    callback_comet = lambda event, tag=tag: comet_rightclick(event,tag)
    canvas.tag_bind(tag,"<Button-3>", callback_comet)

for i in range(0,len(asterdb)):
    tag = "asteroid" + str(i)
    callback_asteroid = lambda event, tag=tag: asteroid_rightclick(event,tag)
    canvas.tag_bind(tag,"<Button-3>", callback_asteroid)

for i in range(0,len(constlabdb)):
    tag = "constellation" + str(i)
    callback_constellation = lambda event, tag=tag: constellation_rightclick(event,tag)
    canvas.tag_bind(tag,"<Button-3>", callback_constellation)

#root.attributes("-toolwindow", True)
#===============================================



#===============================================

if KPOL==1:CHLAT='N'
else:CHLAT='S'
if MYLON<0:CHLON='E'
elif MYLON>0:CHLON='W'
else: CHLON=''

print("Latitude="+str(MYLAT)+" "+CHLAT)
print("Longitude="+str(abs(MYLON))+" "+CHLON)


UTCDTIME=datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
print("UTCDateTime="+UTCDTIME)
DAY=int(UTCDTIME[8:10])
MONTH=int(UTCDTIME[5:7])
YEAR=int(UTCDTIME[0:4])
HOUR=float(UTCDTIME[11:13])+float(UTCDTIME[14:16])/60+float(UTCDTIME[17:19])/3600

#ldtime=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
TIMEDELTA_=timedelta(hours=DELTAHOURS)
LDTIME=(datetime.datetime.utcnow()+TIMEDELTA_).strftime("%Y-%m-%d %H:%M:%S")
print("LocalDateTime="+LDTIME)
LDAY=int(LDTIME[8:10])
LMONTH=int(LDTIME[5:7])
LYEAR=int(LDTIME[0:4])
LHOUR=float(LDTIME[11:13])+float(LDTIME[14:16])/60+float(LDTIME[17:19])/3600

#timedelta_ = datetime.datetime.utcnow() - datetime.datetime.now()

elat.insert(0,str(MYLAT))
if KPOL==1:clat.select()
KPOL_OLD=KPOL;MYLATOLD=MYLAT

elon.insert(0,str(abs(MYLON)))
if MYLON<0:clon.select()
MYLONOLD=MYLON

eyy.insert(0,LYEAR)
emm.insert(0,LMONTH)
edd.insert(0,LDAY)
ehh.insert(0,LDTIME[11:13])
emin.insert(0,LDTIME[14:16])
ess.insert(0,LDTIME[17:19])
if int(DELTAHOURS)==float(DELTAHOURS): str_dt=str(int(DELTAHOURS))
else: str_dt=str(DELTAHOURS)
edt.insert(0,str_dt)
emagn.insert(0,MAGN_LIMIT)

MJD=mjdf(DAY,MONTH,YEAR,HOUR)
print("MJD="+str(round(MJD,6)))
JD_=MJD+2400000.5
print("JD="+str(round(JD_,6)))
LMST=lmstf(MJD,MYLON)
rastr,decstr=grms(LMST,0)
print("LMST="+rastr+" ("+str(round(LMST,6))+"h)")
DELTAT=calcdeltat(YEAR,MONTH)
print("DELTA_T="+str(round(DELTAT,2))+"s")
TIM_=(JD_+DELTAT/86400-2451545)/36525

if oturnvar.get()=="S":TURN_ANGLE=0
elif oturnvar.get()=="SE":TURN_ANGLE=pi/4
elif oturnvar.get()=="E":TURN_ANGLE=pi/2
elif oturnvar.get()=="NE":TURN_ANGLE=3*pi/4
elif oturnvar.get()=="N":TURN_ANGLE=pi
elif oturnvar.get()=="NW":TURN_ANGLE=5*pi/4
elif oturnvar.get()=="W":TURN_ANGLE=3*pi/2
elif oturnvar.get()=="SW":TURN_ANGLE=7*pi/4
if KPOL==-1: TURN_ANGLE=TURN_ANGLE+pi

fi=pid2-MYLAT*pid180

for jj in range(0,9):MPOV.append([])
MPOV[0]=1;MPOV[1]=0;MPOV[2]=0
MPOV[3]=0;MPOV[4]=cos(fi);MPOV[5]=-sin(fi)
MPOV[6]=0;MPOV[7]=sin(fi);MPOV[8]=cos(fi)

PMAT=pmatequ(TIM_,0)
PMAT2=pmatequ(0,TIM_)
PMAT1875=pmatequ((2405890-2451545)/36525,TIM_)

azimuth,alt=calcaz_xycanv(0.5*ZOOM*RCANV,0.5*ZOOM*RCANV)
ra_canv,dec_canv=calcekv(azimuth,alt,LMST)
RA_CANV2000,DEC_CANV2000=ekvtoekv2000(ra_canv,dec_canv) #2000!

#EPS=(23.43929111-46.8150*TIM_/3600-0.00059*TIM_/3600*TIM_+0.001813*TIM_**3/3600)*pid180

SUMENTRY=KPOL+float(elat.get())+float(elon.get())+float(eyy.get())+float(emm.get())+float(edd.get())
SUMENTRY=SUMENTRY+float(ehh.get())+float(emin.get())+float(ess.get())+float(edt.get())+clatvar.get()+clonvar.get()+float(emagn.get())

DELTAD=0
etrack.insert(0,0)
#risgridconaz()
risgridconekv()
rishoriz()
legpaint()
#DSSYST = 367*YEAR - int(7 * ( YEAR + int((MONTH+9)/12) ) / 4) + int(275*(MONTH/9)) + DAY - 730530 + HOUR/24
#for y in range (2100,9100,100):
#    if ((YEAR==y and MONTH>=3) or (YEAR>y)) and frac(y/400)!=0:DSSYST=DSSYST-1
#for y in range (1900,1500,-100):
#    if ((YEAR==y and MONTH<3) or (YEAR<y)) and frac(y/400)!=0:DSSYST=DSSYST+1
DSSYST=JD_-2451543.5+DELTAT/86400
eclpaint(DSSYST)
smap(DSSYST)
ssystem(DSSYST,DELTAD,LMST,"all",-1)

if ZOOMHIP<9999:
    thread_hipload = threading.Thread(target=hipload, name="hipload")
    thread_hipload.start()

if ZOOMSAO<9999:
    thread_saoload = threading.Thread(target=saoload, name="saoload")
    thread_saoload.start()
     
root.mainloop()

