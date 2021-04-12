
import sys
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time
import csv
from datetime import datetime

options = Options()
options.add_argument('--headless') #background task; don't open a window
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')#I copied this, so IDK?
options.add_argument('--disable-dev-shm-usage')#this too

seccionSeleccionada = ""
SECCIONESMANGO = ['/es/mujer','/es/hombre','/es/nina','/es/nino']
#SECCIONESMANGO = ['/es/hombre','/es/nina','/es/nino']
#SECCIONESMANGO = ['/es/nina','/es/nino']

SECCIONESMANGOROPA = ['vestidos','camisas','camisetas','cardigans'
,'sudaderas','chaquetas','abrigos','pantalones','vaqueros'
,'faldas','shorts']

urlListMangoSecciones = []
urlListMangoSeccionesRopa = []
urlMangoPageBasic = "https://shop.mango.com"
urlMangoPage = "https://shop.mango.com/es"
Mango = "MANGO"



"""
Change te colon character to hyphens character
Args : (object: str) : line candidate to change colon to hyphens
Returns : (object: ) line with change accomplished
"""
def changeColonTogion(lineToCleam):##### ha que tratar esto aqui hay muchas casuisticas (darle una vuelta)
	if(lineToCleam != None):
		return lineToCleam.replace(",","-")
	else:
		return "NULL"

"""
Change get the information  in div elemente with the  class product-info-text
Args : (object: str) : Al elements with class product-info-text , the listo to write on file.
Returns : (object: ) line with change accomplished
"""


def getProductInfoExtra(elementosInfo,lineToWrite):
	if(elementosInfo != None):
		for info in elementosInfo:
			if(info.get_text().count("Composi") > 0 ):
				lineToWrite.append(changeColonTogion(info.get_text()))
			else:
				lineToWrite.append("NULL")


"""
transform the sizes of a vector to a line
Args : (object: str) : Al elements span with class size-available , the listo to write on file.
Returns : (object: ) line with change accomplished
"""

def transforTeSizeListToLine(elementosInfo ,lineToWrite):
	lineSizes = ""
	if(elementosInfo != None):
		for sizes in elementosInfo:
			lineSizes += sizes.get_text()
			lineSizes+="-"
		lineToWrite.append(lineSizes)


"""
function to write in a file
Args : (object: List) : the line of file to write
Returns : (object: ) line with change accomplished
"""

def writeInFile(InfoToWrite):

	with open('C:\\Users\\sarab\\OneDrive\\Desktop\\Master\\Tipologia y ciclo de vida de datos\\Practica1\\datasetMango_4_test.csv', 'a') as f:
		csv_write = csv.writer(f)
		#for row in InfoToWrite:
		csv_write.writerow(InfoToWrite)


"""
Get the group for sex of  the clots
Args : (object: List) : url of the clothes to analyze
Returns : (object: ) the group of clots
"""

def getGroupRopa(linkOfClotePage):
	for group in SECCIONESMANGO:
		if(linkOfClotePage.find(group) > 0 ):
			return group.replace("es/","").replace("/","")
		else:
			return "NULL"

"""
Get the Category for sex of  the clots
Args : (object: List) : url of the clothes to analyze
Returns : (object: ) the Category of clots
"""

def getCategoryRopa(linkOfClotePage):
	for group in SECCIONESMANGOROPA:
		if(linkOfClotePage.count(group) > 0 ):
			return group
	return "NULL"

"""
Count the number of images in the web site to promotion the clothes
Args : (object: List) : the elements in div  stament with id=app
Returns : (object: ) the number of image in div  stament with id=app
"""
def countImg(elements):
	imagenesElementos  = elements.find_all('div',class_='image-btn')
	numeroDeImagenes = 0
	if(elements.find_all('div',class_='image-btn') != None):
		for imagenes in imagenesElementos:
			numeroDeImagenes+= 1
		return str(numeroDeImagenes)
	return "NULL"

"""
GET the discount  in the web site to  clothes
Args : (object: List) : the elements in div  stament with id=app
Returns : (object: ) the discount aplicate to clothes
"""

def getDiscount(elementos):
	if(elementos.find('span',class_="product-discount") != None):
		return elementos.find('span',class_="product-discount").get_text()
	else:
		return str(0)

"""
GET the clothes care rocmenden of the shop in a line 
Args : (object: List) : the elements in div  stament with id=app
Returns : (object: ) return clothes care in a line. 
"""

def getCaracteristicasLavado(elementos):
	if(elementos.find('div',class_="product-info-icons") != None):
		elementosInfo = elementos.find('div',class_="product-info-icons")
		insturccionesLavado =""
		for lavado in elementosInfo.find_all('img', alt=True):
			insturccionesLavado += " - "
			insturccionesLavado += lavado['alt']
	return insturccionesLavado


"""
GET the  seasons clothes
Args : (object: List) : 
Returns : (object: ) return the seasons. 
"""
def get_season():
    try:
        date = datetime.now()
        if date.month < 7:
            season = 'Primavera-Verano'
        else:
            season = 'Otoño-Invierno'
        return season
    except:
        return 'NULL'


"""
GET the Atributhes of cloths in web site for write in file. 
Args : (object: List) : link of webpage to analyze
Returns : (object: ) NULL
"""
# realizar bucle de esto para que tire todo lo que pille.
def getAtributtersOfClots(linkOfClotePage):
	##if():
	#if(isNotClotePage(linkOfClotePage)):
		lineToWrite =[]
		driver = webdriver.Chrome(options=options)
		driver.get(linkOfClotePage)# set browser to use this page
		time.sleep(3) # let the scripts load
		html = driver.page_source #copy from chrome process to your python instance
		driver.quit()
		soupMango = BeautifulSoup(html,features="html.parser")
		elementos = soupMango.find('div',id="app")

		
		if(elementos != None):
			#Referencia (id): cadena de caracteres alfanumérico que utiliza cada página para identificar el producto.
			if(elementos.find('span',class_="product-reference") != None):
				lineToWrite.append(changeColonTogion(elementos.find('span',class_="product-reference").get_text()))## escribimos en fichero
			else:
				lineToWrite.append("NULL")
			#Grupo (group): conjunto del que forma parte el producto. Las posibilidades son Hombre, Mujer o Niños.
			lineToWrite.append( getGroupRopa(linkOfClotePage))

			#Categoría (category): tipo de prenda a la que pertenece. Por ejemplo, camisa, blusa, pantalones, vaqueros, etc.
			lineToWrite.append(getCategoryRopa(linkOfClotePage))

			# Imágenes (images): cantidad de imágenes proporcionadas.
			lineToWrite.append( countImg(elementos) )

			#  Tallas (size): Rango de tallas disponible. Seguir la estructura: ‘talla mínima’–‘talla máxima’. Por ejemplo, XS-XL.
			transforTeSizeListToLine( elementos.find_all( 'span',class_="size-available"),lineToWrite)## escribimos en fichero

			#Variedad de colores (colour): número de colores distintos disponibles por el producto
			if(elementos.find( 'span',class_="colors-info-name") != None):
				lineToWrite.append(changeColonTogion(elementos.find( 'span',class_="colors-info-name").get_text()))
			else:
				lineToWrite.append("NULL")

			# Temporada (season): la moda se distribuye por distintas temporadas acorde a la estación en la que nos encontramos. Se podrán definir cuatro temporadas: primavera, verano, otoño e invierno.
			lineToWrite.append(get_season())

			#Oferta (sales): porcentaje de descuento disponible por el producto.
			#lineToWrite.append(getDiscount(elementos))

			#   Precio (price): coste del producto.
			if(elementos.find('span',class_="product-sale") != None):
				lineToWrite.append( changeColonTogion( elementos.find('span',class_="product-sale").get_text()))## escribimos en fichero
			else:
				lineToWrite.append("NULL")
			# Valoración_clientes
			lineToWrite.append("NULL")

			# (opinion):
			lineToWrite.append("NULL")


			# Materia_prima (raw_material): ¿¿¿

			#getProductInfoExtra(elementos.find_all( 'p',class_="product-info-text"),lineToWrite)

			# made_inn
			lineToWrite.append("NULL")

			#caracteristicas de lavado.
			lineToWrite.append(getCaracteristicasLavado(elementos))
			
			lineToWrite.append(Mango)
			#print( elementos.find( 'span',class_="product-sale").get_text())## pintamos
			
			writeInFile( lineToWrite)

		

"""
GET the html text of Main page and parsing with BeautifulSoup class. 
Args : (object: List) : url MAIN PAGE OF MANGO, URL mango Page Basics, Seccions of Mango page 
Returns : (object: ) NULL
"""


def getMangoMainPage(urlMangoPage,urlMangoPageBasic,SECCIONESMANGO): # Funcion que pilla la pagina principal

	mangoPage = requests.get(urlMangoPage)
	soupMango = BeautifulSoup(mangoPage.content,features="html.parser")
	soupMango.find_all('a')
	
	for link in soupMango.find_all('a'): # pillamos los tipo a y los links
		for seccion in SECCIONESMANGO:   
			if(link.get('href') == seccion): 
				urlListMangoSecciones.append(urlMangoPageBasic + link.get('href')) # Construimos los enlaces a las secciones

	#print(urlListMangoSecciones);


#getMangoMainPage(urlMangoPage,urlMangoPageBasic,SECCIONESMANGO)

"""
GET the html text of  Seccions mango page  and parsing with BeautifulSoup class. 
Args : (object: List) : urls Mango Seccions , URL mango Page Basics, Seccions of Mango clothes 
Returns : (object: ) NULL
"""

def getMangoSeccionesRopa(urlListMangoSecciones,urlMangoPageBasic,SECCIONESMANGOROPA): # pillamos las secciones!!

	global urlListMangoSeccionesRopa 
	for urlSecciones in urlListMangoSecciones:

		mangoPage = requests.get(urlSecciones)
		soupMango = BeautifulSoup(mangoPage.content,features="html.parser")
		for link in soupMango.find_all('a'):
			for ropa in SECCIONESMANGOROPA: # pillamos todas las secciones
				if( link.get('href') is not None):
					if(link.get('href').count(ropa) > 0): # 
						#print("numero de bucles "  + str(numeroDeBucles))
						#print("este es el contenido de la raiable link.get(`href) " + link.get('href'))
						#print("este es el contenido de la variable ropa " + ropa)
						urlListMangoSeccionesRopa.append(urlMangoPageBasic + link.get('href'))
	urlListMangoSeccionesRopa = (dict.fromkeys(urlListMangoSeccionesRopa))# quitamos los repetidos que se encuentran en la propia pagina web.
	print(len(urlListMangoSeccionesRopa))

#getMangoSeccionesRopa(urlListMangoSecciones,urlMangoPageBasic,SECCIONESMANGOROPA)


"""
get the urls and build the urls to get the attributes
Args : (object: List) : List of urls mango Seccions. 
Returns : (object: ) NULL
"""

def getMangoClots(urlListMangoSeccionesRopa): ## por aqui pasamos las urls de la ropa

#mangoPage = requests.get();
	global seccionSeleccionada 
	numeroDePaginasMax = 32536
	numeroDePaginasleidas = 0
	numeroMaximoDeGruposLeidos = numeroDePaginasMax / len(urlListMangoSeccionesRopa)
	numeroDeGruposLeidos =0
	for urlClotes in urlListMangoSeccionesRopa: ## iteramos sobre la url de la ropa
		seccionSeleccionada = urlClotes
		print("numero de paginas fuera del for ")
		print(numeroDePaginasleidas)
		#if(numeroDePaginasleidas >= numeroDePaginasMax):
		#	break
		driver = webdriver.Chrome(options=options)
		driver.get(urlClotes)# set browser to use this page
		time.sleep(4) # let the scripts load
		html = driver.page_source #copy from chrome process to your python instance
		driver.quit()
		soupMango = BeautifulSoup(html,features="html.parser")
		#print(soupMango.find('div',id="app").get_text()); ## pillamos el div con id "app" (div que contiene la ropa)
		elementos = soupMango.find('div',id="app")
		for aTag in elementos.find_all('a'): #iteramos sobre los links. 

			links = aTag.get('href')
			if(links.find(".html") > 0 ):# tiene que acabar en .html para que sea una pagina de ropa no un menu
				numeroDeGruposLeidos += 1
				numeroDePaginasleidas += 1
				print("numero de paginas liedas actualmente")
				print(numeroDePaginasleidas)
				print(urlMangoPageBasic + links)
				getAtributtersOfClots(urlMangoPageBasic + links) ## creamos el link de la pagina de los atributos de la ropa"""
			
			if(numeroDeGruposLeidos > numeroMaximoDeGruposLeidos):
				numeroDeGruposLeidos = 0
				break
#getMangoClots(urlListMangoSeccionesRopa)

"""
Main function execute the runtime
Args :NULL
Returns : NULL
"""


def main ():

	getMangoMainPage(urlMangoPage,urlMangoPageBasic,SECCIONESMANGO)
	getMangoSeccionesRopa(urlListMangoSecciones,urlMangoPageBasic,SECCIONESMANGOROPA)
	getMangoClots(urlListMangoSeccionesRopa)




if __name__ == "__main__":
	main()

