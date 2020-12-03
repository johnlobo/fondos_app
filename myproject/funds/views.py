#-*- coding: utf-8 -*-
from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.template import loader
from .models import Fund
from bs4 import BeautifulSoup
import requests
import csv
import logging
#import pdb; pdb.set_trace()

logger = logging.getLogger(__name__)

def index(request):
    funds_list = Fund.objects.order_by('-pub_date')
    funds_list_processed = []
    for fund in funds_list:	
        url = "https://markets.ft.com/data/funds/tearsheet/summary?s="+fund.fund_ISIN
        urlHistorico = "https://markets.ft.com/data/funds/tearsheet/historical?s="+fund.fund_ISIN

        # Realizamos la petición a la web
        req = requests.get(url)

        # Comprobamos que la petición nos devuelve un Status Code = 200
        statusCode = req.status_code
        if statusCode == 200:
	    logger.debug(url+":"+str(statusCode))

            # Pasamos el contenido HTML de la web a un objeto BeautifulSoup()
            html = BeautifulSoup(req.text, "html.parser")

            # Obtenemos todos los span donde estan las entradas
	    cotizaciones = html.find_all('span', class_='mod-ui-data-list__value')
	    fechas = html.find_all('div', class_='mod-disclaimer')

	    # Si ha encontrado cotizaciones las pinta... 
	    if len(cotizaciones)>0:
		cifra = cotizaciones[0].get_text()
	        if len(fechas)>0:
		    fecha= fechas[0].get_text()
	        else:
	    	    fecha = "-"
	    else:
		cifra = "-"
		fecha = "-"
	    # Si ha encontrado la fecha la pinta... 

	    #construye la lista a mostrar en la página
	    funds_list_processed.append((fund.fund_name,fund.fund_ISIN,cifra,fecha,urlHistorico))

        # Imprimo el Título, Autor y Fecha de las entradas
        else:
            #print "Status Code %d" %statusCode
            logger.error("Status Code "+statusCode)
            logger.debug("Status Code "+statusCode)

    template = loader.get_template('funds/index.html')
    context = {
        'funds_list_processed': funds_list_processed,
    }
    return HttpResponse(template.render(context, request))
