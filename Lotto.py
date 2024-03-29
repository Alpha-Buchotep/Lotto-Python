# ---------------------------------------
#|  Python - Egyszerű lottó sorsoló      |
#|---------------------------------------|
#|  Tesztelve: Python 3.10.106 verzióval |
# ---------------------------------------

#------------------------------------
# Importok
#------------------------------------

# SYS modul import
import sys

# OS modul import (képernyőtörlés, ablak fejlécének szövege stb.)
import os

# JSON modul import (JSON adatok kezeléséhez)
import json

# Dátum / idő modul import
import datetime

# time modul import - time.sleep(x)
import time

# Math modul random import > véletlenszám generáláshoz
import random

# Beállítjuk az ablak fejlécét
os.system("title Python Lottó - Készenlétben")

#-------------------------------------------------------------------
# Lottó típusok adatai > JSON
#-------------------------------------------------------------------

lottoOtos = '{ "nev":"Ötös lottó", "jatekMezokSzama":1, "minSzam":1, "maxSzam":90, "huzandoSzamok":5 }'
lottoHatos = '{ "nev":"Hatos lottó", "jatekMezokSzama":1, "minSzam":1, "maxSzam":45, "huzandoSzamok":6 }'
lottoHetes = '{ "nev":"Hetes lottó", "jatekMezokSzama":2, "minSzam":1, "maxSzam":35, "huzandoSzamok":7, "minSzamB":1, "maxSzamB":35, "huzandoSzamokB":7 }'
lottoEuroJ = '{ "nev":"EuroJackpot", "jatekMezokSzama":2, "minSzam":1, "maxSzam":50, "huzandoSzamok":5, "minSzamB":1, "maxSzamB":12, "huzandoSzamokB":2 }'

#-------------------------------------------------------------------
# Egyéb globális változók
#-------------------------------------------------------------------

szelvenyekSzama = int(2)
fajlMentes = str("n")
elvalasztoJel = str(";")

#-------------------------------------
# Képernyő törlése
#-------------------------------------

os.system("cls")

#----------------------------------------------------
# Adatok bekérése függvény
#----------------------------------------------------

def adatokBekerese():

	#-------------------------------------
	# Globális változók inicializálása
	#-------------------------------------

	global szelvenyekSzama
	global fajlMentes
	global elvalasztoJel
	
	#------------------------------------------
	# Lokális változók > alapértékek > lottó 5
	#------------------------------------------

	lottoValasztas = str("1")
	huzandoSzelvenyekSzama = str("2")

	#-------------------------------------
	# Lottó típusok kiírása
	#-------------------------------------

	print("")
	print(" ██╗      ██████╗ ████████╗████████╗ ██████╗  ")
	print(" ██║     ██╔═══██╗╚══██╔══╝╚══██╔══╝██╔═══██╗ ")
	print(" ██║     ██║   ██║   ██║      ██║   ██║   ██║ ")
	print(" ██║     ██║   ██║   ██║      ██║   ██║   ██║ ")
	print(" ███████╗╚██████╔╝   ██║      ██║   ╚██████╔╝ ")
	print(" ╚══════╝ ╚═════╝    ╚═╝      ╚═╝    ╚═════╝  ")
	print("")
	print("  ------------------------------------------ ")
	print(" | 1 | Ötös lottó   | 1 mezős               |")
	print(" |------------------------------------------|")
	print(" | 2 | Hatos lottó  | 1 mezős               |")
	print(" |------------------------------------------|")
	print(" | 3 | Hetes lottó  | 1 mezős (kézi/gépi)   |")
	print(" |------------------------------------------|")
	print(" | 4 | EuroJackpot  | 2 mezős (A/B mező)    |")
	print(" |------------------------------------------|")
	print(" | S | Szabályok    |                       |")
	print(" |------------------------------------------|")
	print(" | X | Kilépés      |                       |")
	print("  ------------------------------------------ ")
	print("")

	#-------------------------------------------------------------
	# Felhasználói választás bekérése a lottó típusáról,
	# ez alapján hívjuk majd meg a sorsoló függvényt
	#-------------------------------------------------------------

	print("")
	lottoValasztas = str(input(" Melyik lottót húzzam? (1/2/3/4, alap: 1) | "))

	# Csak Enter-t nyomtunk, 5-s lottó
	if lottoValasztas == "":
		lottoValasztas = 1

	# S-t nyomtunk, jatekSzabalyok() függvény meghívása
	elif lottoValasztas.lower() == "s":
		jatekSzabalyok()
		input(" Nyomj Enter-t a folytatáshoz")
		adatokBekerese()

	# X-t nyomtunk, viszlat() függvény meghívása
	elif lottoValasztas.lower() == "x":
		viszlat()

	else:
		#-----------------------------------------------------------------
		# Megpróbáljuk egész számmá alakítani a kapott értéket
		# Ha nem sikerül, akkor alapértelmezetten az 1 típust választjuk
		#-----------------------------------------------------------------
		try:
			lottoValasztas = int(lottoValasztas)

			# Ha a megadott típus 4-nél nagyobb, akkor az 1 típust sorsoljuk
			if lottoValasztas > 4:
				lottoValasztas = 1

			# Ha a típus 1-nél kisebb, akkor az 1 típust sorsoljuk
			elif lottoValasztas < 1:
				lottoValasztas = 1

		# Nem sikerült a megadott értéket egész számmá alakítani
		except:
			lottoValasztas = 0
		
		#---------------------------------------------------------------
		# Megadott típus vizsgálata
		#---------------------------------------------------------------

	if lottoValasztas > 4 or lottoValasztas < 1:
		# Nem létező lottót választottunk, kilépünk
		print("")
		print(" Nem megfelelő lottót választottál!")
		print("")
		sys.exit()

	#---------------------------------------------------------------
	# Megkérdezzük a felhasználót, hány szelvényt szeretne sorsolni
	#---------------------------------------------------------------

	print("")
	huzandoSzelvenyekSzama = str(input(" Hány darab szelvényt húzzak? (max. 3600 db, alap: 2) | "))
	
	#-------------------------------------------------------------------
	# Ha Enter-t nyomtunk, akkor alapértlmezetten 2 db szelvényt húzunk
	#-------------------------------------------------------------------
	
	if huzandoSzelvenyekSzama == "":
		huzandoSzelvenyekSzama = 2

	#-------------------------------------------------------------
	# Sorsolandó szelvények számának ellenőrzáse / konverzió
	#-------------------------------------------------------------
	# Megpróbáljuk egész számmá alakítani a megadott értéket
	# Ha nem sikerül, akkor alapértelmezetten 2 db szelvényt húzunk
	#-------------------------------------------------------------
	try:
		huzandoSzelvenyekSzama = int(huzandoSzelvenyekSzama)
		szelvenyekSzama = int(huzandoSzelvenyekSzama)
		# Ha 3600 szelvénynél többet adtunk meg, akkor is csak 3600 db szelvényt húzunk
		if huzandoSzelvenyekSzama > 3600:
			szelvenyekSzama = 3600

		# Ha 1 szelvénynél kevesebbet adtunk meg, akkor legalább 1 db szelvényt sorsolunk
		elif huzandoSzelvenyekSzama < 1:
			szelvenyekSzama = 1

	# Nem sikerült a megadott értéket egész számmá alakítani, ezért
	# 2 db szelvényt sorsolunk ki
	except:
		szelvenyekSzama = 2

	#---------------------------------------------------------------
	# Felhasználói választás > mentsük-e fájlba a kisorsolt számokat
	#---------------------------------------------------------------

	print("")
	fajlMentes = str(input(" Mentsük fájlba a kisorsolt számokat? (I/i = van mentés, bármi más érték vagy Enter esetén nincs, alap: nincs) | "))

	#-------------------------------------------------
	# Ha mentjük fájlba a számokat, akkor bekérjük
	# a felhasználótól az elválasztó karaktert
	#-------------------------------------------------

	if fajlMentes.lower() == "i":

		#-------------------------------------------------------------
		# Elválasztó karakter bekérése
		#-------------------------------------------------------------
		print("")
		elvalasztoJel = str(input(" Elválasztó karakter a fájlban (max. 1 karakter lehet, alap: pontosvessző) | "))

		#-------------------------------------------------
		# Ha nem adunk meg elválaszó jelet, akkor az 
		# alapértelmezett pontosvesszőt ( ; ) használjuk
		#-------------------------------------------------

		if elvalasztoJel == "":
			elvalasztoJel = ";"

		#------------------------------------------------------
		# Ha több, mint egy karakter hosszú az elválasztó jel,
		# akkor csak az első karektert vesszük figyelembe
		#------------------------------------------------------
		
		if len(elvalasztoJel) > 1:
			elvalasztoJel = elvalasztoJel[0]

		#------------------------------------------------------
		# Ha nem I vagy i betűt írtunk be, szamokMentese = "n"
		#------------------------------------------------------

	else:
		fajlMentes = "n"

	#-------------------------------------------------------------------
	# Felhasználói választás > legyen-e várakozás a számsorolások között
	#-------------------------------------------------------------------

	print("")
	varakozas = str(input(" Legyen minimális várakozás a sorsolások között? (I/i = igen, bármi más érték vagy Enter esetén nincs, alap: nincs) | "))

	if varakozas.lower() == "i":

		varakozas = "i"

		#-------------------------------------------------------------------------
		# Felhasználói választás a várakozás idejéről (0.1 - 5.0 másodperc között
		#-------------------------------------------------------------------------

		print("")
		varakozasiIdo = str(input(" Mennyi időt várjunk a számok sorsolása között? (min.: 0.1 mp, max.: 5 mp, alap: 0.5 mp) | "))

		if varakozasiIdo == "":
			varakozasiIdo = float(0.5)
		else:
			try:
				varakozasiIdo = float(varakozasiIdo)
			except:
				varakozasiIdo = float(0.5)
	
	else:
		varakozas = "n"
		varakozasiIdo = 0

	#-------------------------------------------------------------
	# A kapott adatok alapján meghívjuk a lottoSorsolas függvényt
	#-------------------------------------------------------------

	lottoSorsolas(lottoValasztas, varakozas, varakozasiIdo)

#-------------------------------------------------------------
# Adatok bekérése függvény vége
#-------------------------------------------------------------

#-------------------------------------------------------------
# Sorsolás függvény > alapértelmezett értékekkel megadva
#-------------------------------------------------------------

def lottoSorsolas(lottoTipus = 1, varakozas = "n", varakozasiIdo = 0.5):

	# Beállítjuk az ablak fejlécét
	os.system("title Python Lottó - Sorsolás folyamatban")

	#----------------------------------------------------------------------------
	# Globális változók inicializálása
	#----------------------------------------------------------------------------

	global szelvenyekSzama
	global fajlMentes
	global elvalasztoJel

	#----------------------------------------------------------------------------
	# Lokális, csak ebben a függvényben elérhető változók
	#----------------------------------------------------------------------------

	fajlMentesHiba = 0
	fajlNev = ""
	szamlalo = 0
	aktualisanKihuzottSzam = 0
	kihuzottSzamok = []
	szamokFajlba = ""
	tmpLottoAdatok = ""
	lottoNev = ""
	kezdoSzam = 0
	vegeSzam = 0
	sorsolandoSzamok = 0
	kezdoSzamB = 0
	vegeSzamB = 0
	sorsolandoSzamokB = 0
	jatekMezok = 0

	#----------------------------------------------------------------------------
	# Az alábbi vizsgálattal döntjük el, melyik lottó JSON adatait kell betölteni
	# a lottoSorsolas függvény lottoTipus paramétere alapján
	#----------------------------------------------------------------------------

	# Ötös lottó
	if lottoTipus == 1:
		tmpLottoAdatok = json.loads(lottoOtos)
		lottoNev = tmpLottoAdatok["nev"]
		jatekMezok = tmpLottoAdatok["jatekMezokSzama"]
		kezdoSzam = tmpLottoAdatok["minSzam"]
		vegeSzam = tmpLottoAdatok["maxSzam"]
		sorsolandoSzamok = tmpLottoAdatok["huzandoSzamok"]

	# Hatos lottó
	elif lottoTipus == 2:
		tmpLottoAdatok = json.loads(lottoHatos)
		lottoNev = tmpLottoAdatok["nev"]
		jatekMezok = tmpLottoAdatok["jatekMezokSzama"]
		kezdoSzam = tmpLottoAdatok["minSzam"]
		vegeSzam = tmpLottoAdatok["maxSzam"]
		sorsolandoSzamok = tmpLottoAdatok["huzandoSzamok"]

	# Hetes (Skandináv) lottó
	elif lottoTipus == 3:
		tmpLottoAdatok = json.loads(lottoHetes)
		lottoNev = tmpLottoAdatok["nev"]
		jatekMezok = tmpLottoAdatok["jatekMezokSzama"]
		kezdoSzam = tmpLottoAdatok["minSzam"]
		vegeSzam = tmpLottoAdatok["maxSzam"]
		sorsolandoSzamok = tmpLottoAdatok["huzandoSzamok"]
		#-----------------------------------------------
		kezdoSzamB = tmpLottoAdatok["minSzamB"]
		vegeSzamB = tmpLottoAdatok["maxSzamB"]
		sorsolandoSzamokB = tmpLottoAdatok["huzandoSzamokB"]

	# EuroJackpot
	elif lottoTipus == 4:
		tmpLottoAdatok = json.loads(lottoEuroJ)
		lottoNev = tmpLottoAdatok["nev"]
		jatekMezok = tmpLottoAdatok["jatekMezokSzama"]
		kezdoSzam = tmpLottoAdatok["minSzam"]
		vegeSzam = tmpLottoAdatok["maxSzam"]
		sorsolandoSzamok = tmpLottoAdatok["huzandoSzamok"]
		#-----------------------------------------------
		kezdoSzamB = tmpLottoAdatok["minSzamB"]
		vegeSzamB = tmpLottoAdatok["maxSzamB"]
		sorsolandoSzamokB = tmpLottoAdatok["huzandoSzamokB"]

	# A lehetséges lottók közül egyik sem
	else:
		print(" -------------------------------------------")
		print(" Nem megfelelő lottő típus! ")
		print(" -------------------------------------------")
		print("")
		sys.exit()

	# -------------------------------------
	# Jelenlegi dátum / idő beszippantása
	# -------------------------------------

	datum = datetime.datetime.now()

	#------------------------------------
	# Kiírjuk a sorsolás kezdetét
	#------------------------------------

	print("")
	print(" A(z) " + lottoNev + " sorsolás elindult: " + str(datum.strftime("%Y.%m.%d %H:%M:%S")) + " - " + str(szelvenyekSzama) + " db szelvény lesz kisorsolva.")
	print("")

	#------------------------------------
	# Kiírjuk a választott lottó nevét
	#------------------------------------

	print(" -------------------------------------------")
	print(" A(z) " + lottoNev + " nyerőszámai")
	print(" -------------------------------------------")
	print("")

	#--------------------------------------------------------------------
	# Ciklussal a megadott mennyiségű lottószelvényt sorsoljuk ki
	#--------------------------------------------------------------------

	for n in range(0, szelvenyekSzama):

		szamlalo = 0
		aktualisanKihuzottSzam = 0
		kihuzottSzamok = []
		szamokFajlba = ""

		#--------------------------------------------------------------------
		# Összesen 36x húznánk számot, de amint elérjük a
		# húzandó számok mennyiségét, kilépünk a ciklusból
		# Ezt azért csináljuk, ha esetleg valamelyik szám többször kerülne
		# kihúzásra és nem tudnánk elég számot sorsolni a ciklussal
		#--------------------------------------------------------------------

		#----------------------------
		# Számsorsolás - #1 mező
		#----------------------------

		for x in range(0, 37):

			# Húzunk kegy számot a lottó típusának megfelelően
			aktualisanKihuzottSzam = random.randrange(kezdoSzam, vegeSzam)

			# Ha a most húzott szám már szerepel a kihuzottSzamok tömbben, akkor újra húzunk
			if aktualisanKihuzottSzam in kihuzottSzamok:
				continue

			# Ha a most húzott szám nem szerepel a kihuzottSzamok tömbben, akkor vizsgálunk
			else:

				# Ha a szamlalo = a húzandó számok mennyiségével (kisorsoltuk a kellő mennyiségű számot),
				# akkor kilépünk a ciklusból
				if szamlalo == sorsolandoSzamok:
					break

				# Ha a szamlalo nem = a húzandó számok mennyiségével, akkor beírjuk a tömbbe
				# a most kihúzott számot és a szamlalo értékét növeljük eggyel.
				else:
					kihuzottSzamok.append(aktualisanKihuzottSzam)
					szamlalo += 1

		# Emelkedő sorrendbe rendezzük a kihuzottSzamok tömb (lista) elemeit
		kihuzottSzamok.sort()
		
		# Egy karakterrel beljebb írjuk ki a konzolon számokat (szóköz van az elején)
		print(" ", end = "")

		# Ciklussal kiírjuk a kisorsolt számokat
		for y in kihuzottSzamok:

			# egy sorba írjuk a számokat, az y változót string típusta konvertáljuk str(y)
			print(str(y), flush=True, end = " ")

			#--------------------------------------------------------------------------
			# Amennyiben kértünk várakozást, várunk a számok kiiratása között 500 ms-t
			#--------------------------------------------------------------------------

			if varakozas.lower() == "i":
				time.sleep(varakozasiIdo)

			# Összetesszük a sorsolás számait egy string típusú változóba,
			# ezt írjuk majd be a fájlba, a megadott vagy alapértelmezett
			# elválasztó jellel
			szamokFajlba += str(y) + elvalasztoJel
			
		#--------------------------------------------------
		# Számsorsolás #2 mező (Hetes illetve EuroJackpot)
		#--------------------------------------------------

		if jatekMezok > 1:
			print("")
			szamlaloB = 0
			aktualisanKihuzottSzamB = 0
			kihuzottSzamokB = []
			szamokFajlbaB = ""

			#--------------------------------------------------------------------
			# Összesen 36x húznánk számot, de amint elérjük a
			# húzandó számok mennyiségét, kilépünk a ciklusból
			# Ezt azért csináljuk, ha esetleg valamelyik szám többször kerülne
			# kihúzásra és nem tudnánk elég számot sorsolni a ciklussal
			#--------------------------------------------------------------------

			for x in range(0, 37):

				# Húzunk egy számot a lottó típusának megfelelően
				aktualisanKihuzottSzamB = random.randrange(kezdoSzamB, vegeSzamB)

				# Ha a most húzott szám már szerepel a kihuzottSzamok tömbben, akkor újra húzunk
				if aktualisanKihuzottSzamB in kihuzottSzamokB:
					continue

				# Ha a most húzott szám nem szerepel a kihuzottSzamok tömbben, akkor vizsgálunk
				else:

					# Ha a szamlalo = a húzandó számok mennyiségével (kisorsoltuk a kellő mennyiségű számot),
					# akkor kilépünk a ciklusból
					if szamlaloB == sorsolandoSzamokB:
						break

					# Ha a szamlalo nem = a húzandó számok mennyiségével, akkor beírjuk a tömbbe
					# a most kihúzott számot és a szamlalo értékét növeljük eggyel.
					else:
						kihuzottSzamokB.append(aktualisanKihuzottSzamB)
						szamlaloB += 1

			# Emelkedő sorrendbe rendezzük a kihuzottSzamok tömb (lista) elemeit
			kihuzottSzamokB.sort()
			
			# Egy karakterrel beljebb írjuk ki a konzolon számokat (szóköz van az elején)
			print(" ", end = "")

			# Ciklussal kiírjuk a kisorsolt számokat
			for y in kihuzottSzamokB:

				# egy sorba írjuk a számokat, az y változót string típusta konvertáljuk str(y)
				print(str(y), flush=True, end = " ")

				#--------------------------------------------------------------------------
				# Amennyiben kértünk várakozást, várunk a számok kiiratása között 500 ms-t
				#--------------------------------------------------------------------------

				if varakozas.lower() == "i":
					time.sleep(varakozasiIdo)
				
				# Összetesszük a sorsolás számait egy string típusú változóba,
				# ezt írjuk majd be a fájlba, a megadott vagy alapértelmezett
				# elválasztó jellel
				szamokFajlbaB += str(y) + elvalasztoJel
				
		print("")

		# Ha kértük a számok fájlba mentését, akkor legeneráljuk a
		# mentendő fájl nevét a felhasználó home könyvtárába
		if fajlMentes.lower() == "i":

			# Az utolsó delimiter karaktert eltávolítjuk minden sor végéről
			tmpLen = len(szamokFajlba) - 1
			szamokFajlba = szamokFajlba[:tmpLen]
			
			# #2 mező - Az utolsó delimiter karaktert eltávolítjuk minden sor végéről
			if jatekMezok > 1:
				tmpLen = len(szamokFajlbaB) - 1
				szamokFajlbaB = szamokFajlbaB[:tmpLen]

			try:
				# A fájlnév pl. így nézhet ki: C:\Users\FELHASZÁLÓNÉV\Hatos lottó__2023-02-05_180924.txt
				fajlNev = os.path.expanduser("~") + "/" + lottoNev + "__" + str(datum.strftime("%Y-%m-%d_%H%M%S")) + ".txt"

				# Megpróbáljuk megnyitni vagy létrehozni a fájlt,
				# az adatokat hozzáfűzzük nem felülírjuk (a)
				f = open(fajlNev, "a")

				# Beírjuk a számokat, majd teszünk egy sortörést (\n)
				f.write(szamokFajlba + "\n")

				# Ha van 2. mező, azok számait is beírjuk, majd teszünk egy sortörést (\n)
				if jatekMezok > 1:
					f.write(szamokFajlbaB + "\n")

				# Bezárjuk a fájl
				f.close()

			# Hiba a fájl mentésekor
			except:
				# Hibajelző változó növelése +1-el = van hiba
				fajlMentesHiba += 1

		print("")

	#-------------------------------------------------------------
	# Ha mentettük a fájlt, csekkoljuk, hogy nem
	# történt-e hiba a mentés során
	#-------------------------------------------------------------
	
	if fajlMentes.lower() == "i":

		#-------------------------------------------------------------
		# Ha a fajlMentesHiba változó nagyobb 1-nél, az azt jelenti,
		# hogy a mentési folyamat során hiba történt
		#-------------------------------------------------------------

		if fajlMentesHiba > 0:
			print("")
			print(" ------------------------------")
			print("  Nem sikerült a fájl mentése! ")
			print(" ------------------------------")

		# Ha a fajlMentesHiba változó = 0, az azt jelenti,
		# hogy a mentési folyamat sikeres volt

		else:
			print("")
			print(" ------------------------------")
			print("  Fájl mentése sikeres!")
			print(" ------------------------------")

	datum = datetime.datetime.now()

	print("")
	print(" A sorsolás véget ért: " + str(datum.strftime("%Y.%m.%d %H:%M:%S")))

	# Beállítjuk az ablak fejlécét
	os.system("title Python Lottó - Készenlétben")

	#-------------------------------------------------------------
	# Akarunk még sorsolni?
	#-------------------------------------------------------------

	print("")
	sorolasUjra = str(input(" Akarsz újra sorsolni? (I/i = igen, bármi egyéb = nem) | "))
	print("")

	if sorolasUjra.lower() == "i":
		adatokBekerese()
	else:
		viszlat()

#-------------------------------------------------------------
# Sorsolás függvény vége
#-------------------------------------------------------------

#-------------------------------------------------------------
# Kilépés függvény - elköszönés + kilépés a programból
#-------------------------------------------------------------

def viszlat():
	print("")
	print("                                         ██               ")
	print("                                        ██╝               ")
	print(" ██╗   ██╗██╗███████╗███████╗██╗      █████╗ ████████╗██╗ ")
	print(" ██║   ██║██║██╔════╝╚══███╔╝██║     ██╔══██╗╚══██╔══╝██║ ")
	print(" ██║   ██║██║███████╗  ███╔╝ ██║     ███████║   ██║   ██║ ")
	print(" ╚██╗ ██╔╝██║╚════██║ ███╔╝  ██║     ██╔══██║   ██║   ╚═╝ ")
	print("  ╚████╔╝ ██║███████║███████╗███████╗██║  ██║   ██║   ██╗ ")
	print("   ╚═══╝  ╚═╝╚══════╝╚══════╝╚══════╝╚═╝  ╚═╝   ╚═╝   ╚═╝ ")
	print("")
	input("")
	sys.exit()

#-------------------------------------------------------------
# Kilépés függvény vége
#-------------------------------------------------------------


#-------------------------------------------------------------
# Játékszabályok függvény
#-------------------------------------------------------------

def jatekSzabalyok():

	#-------------------------------------
	# Képernyő törlése
	#-------------------------------------

	os.system("cls")

	print("")
	print(" ----------------")
	print(" Ötös lottó")
	print(" ----------------")
	print("")
	print(" Egy mezős játék, 5 számot kell sorsolni 1-90 közötti tartományból.")
	print("")
	print(" ----------------")
	print(" Hatos lottó")
	print(" ----------------")
	print("")
	print(" Egy mezős játék, 6 számot kell sorsolni 1-45 közötti tartományból.")
	print("")
	print(" ----------------")
	print(" Hetes lottó")
	print(" ----------------")
	print("")
	print(" Egy mezős játék, de kézi és gépi sorsolás is van.")
	print(" 7 számot kell sorsolni 1-35 közötti tartományból.")
	print("")
	print(" ----------------")
	print(" EuroJackpot")
	print(" ----------------")
	print("")
	print(" Két mezős játék, A és B mező.")
	print(" Az A mezőben 5 számot kell sorsolni 1-50 közötti tartományból, a B mezőben pedig 2 számot kell sorsolni 1-12 közötti tartományból.")
	print("")

#-------------------------------------------------------------
# Játékszabályok függvény vége
#-------------------------------------------------------------

#-------------------------------------------------------------
# Adatok bekérése függvény meghívása > program indítása
#-------------------------------------------------------------

adatokBekerese()

#-------------------------------------------------
