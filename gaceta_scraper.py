import requests
from bs4 import BeautifulSoup
from datetime import datetime

def scraping_gaceta_medio_oriente():
    url = "https://www.lagaceta.com.ar/tags/275683/guerra-medio-oriente"
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Obtenemos la fecha de hoy en el formato que suele usar el sitio
        hoy = datetime.now().strftime("%d/%m/%Y")
        noticias_del_dia = []

        # Buscamos los contenedores de las notas
        # Nota: Estas clases pueden variar levemente, pero suelen ser 'card' o 'story'
        for articulo in soup.find_all('div', class_='card'):
            titulo_tag = articulo.find('h2') or articulo.find('h3')
            link_tag = articulo.find('a', href=True)
            resumen_tag = articulo.find('p', class_='card-text') # O la clase que use la bajada
            
            if titulo_tag and link_tag:
                titulo = titulo_tag.get_text(strip=True)
                link = "https://www.lagaceta.com.ar" + link_tag['href']
                resumen = resumen_tag.get_text(strip=True) if resumen_tag else "Sin bajada disponible."
                
                # En muchos sitios de noticias, la fecha está en un span o time
                fecha_tag = articulo.find('span', class_='date')
                fecha_texto = fecha_tag.get_text(strip=True) if fecha_tag else hoy # Default a hoy si no hay tag
                
                # Agregamos si es de hoy (o simplemente las primeras 5 si queremos lo más reciente)
                noticias_del_dia.append(f"TÍTULO: {titulo}\nRESUMEN: {resumen}\nLINK: {link}\n")

        if not noticias_del_dia:
            return "No se encontraron noticias publicadas hoy en esta sección."

        return "\n---\n".join(noticias_del_dia[:10]) # Retornamos las 10 más recientes

    except Exception as e:
        return f"Error al acceder al sitio: {e}"

# Ejecución para la Gem
contexto_noticias = scraping_gaceta_medio_oriente()
print(contexto_noticias)
