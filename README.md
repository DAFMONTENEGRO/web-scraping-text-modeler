# web-scraping-text-modeler

El proyecto es una propuesta de modelamiento del idioma español por medio de bases de datos relacionales, para la creación del modelo el programa es capaz de analizar el orden, composición y estructura de cualquier texto suministrado o conjunto de palabras. Esto quiere decir que el programa es capaz de construir un modelamiento sobre cualquier idioma en el que estén escritos los textos suministrados, sin embargo, por defecto se distribuye con una implementación en español y una biblioteca de textos en español obtenidos por la herramienta de web scraping integrada en el proyecto.

# Proyecto Bases de Datos

- Daniel Felipe Montenegro Herrera

## 1. Herramientas utilizadas

### 1.1. Librerías Python

Para su correcto funcionamiento el proyecto hace uso de cuatro librerías en Python, estas librerías son las que permiten la interconectividad de la herramienta. A continuación, se detalla el uso de cada librería:

* **Os:** Permite la lectura y escritura de archivos
* **Time:** Genera pequeños retardos para que la interfaz sea mas amigable
* **Requests:** Crea las solicitudes a las paginas web
* **Mysql.connector:** Es la librería oficial de Mysql para conectarse desde Python
* **BeautifulSoup:** Facilita el análisis de documentos html

La librería Os y la librería Time vienen por defecto distribuidas con Python, el resto se instaló por medio de pip.

### 1.2. Corpus de Referencia del Español Actual

El Corpus de Referencia del Español Actual (CREA) provee un [listado de frecuencias](http://corpus.rae.es/lfrecuencias.html) de todas palabras existentes en la lengua.

### 1.3. Web Scraping

Por defecto la base de datos se distribuirá con las primeras 121000 frecuencias del CREA, sin embargo, para poner a prueba la herramienta procesamos con ella 3276 textos (cuentos de diversos autores en el idioma español) que contenían 852302 frases los cuales fueron recolectados de la pagina web www.ciudadseva.com, esto gracias a que en su documento robots.txt especificaba al momento del raspado que era posible extraer este contenido.

Esta biblioteca se formo por medio de una aplicación que esta integrada en la librería  para hacer Web Scraping de cualquier pagina web.

### 1.4. MYSQL

Es el gestor de base de datos que utiliza el proyecto, los scripts de creación de la base de datos que se distribuyen están implementados especialmente para su uso en MYSQL.

## 2. Estructura de la base de datos

### 2.1. Modelo de la base de datos

La base de datos que se distribuye por defecto es modificable, sin embargo, el script de creación incluido solo plantea la necesidad de cinco entidades para su correcto funcionamiento. Las entidades son las siguientes:

![modelo](https://raw.githubusercontent.com/DAFMONTENEGRO/web-scraping-text-modeler/master/SQL/SYSTEM/DIAGRAM/modeler_diagram.png)

### 2.2. Resumen de la base de datos

* **Entidades (5):** word, coding, phrase, mistake y text
* **Triggers (1):** frequent_mistake
* **Views (7):** crea, scripts, total_words, mistakes, codings, texts y phrases
* **Stored Procedures (7):** insert_crea, insert_word, insert_mistake, insert_coding, insert_text, insert_phrase y id_word
* **Users (2):** root y guest
* **Values (121000):** Las 121.000 primeras frecuencias del CREA

### 2.3. Usuarios
El script de creacion permite la creacion de dos usuarios, el primero es el usuario por defecto “root” y el segundo es un usuario invitado llamado “guest”. 

## 3. Contenido del proyecto

Este es el detalle del contenido de cada una de las carpetas que se distribuyen con este proyecto:

* **/DATA WEB SCRAPING:** Posee todos los textos que se utilizaron para contruir la base de datos sustentada con en el proyecto, son documentos de texto (.txt) los cuales son transcripciones de cuentos extraidos de la web. Son mas de 3000 por lo que pesan un poco, asi que para poder distribuirlos los encontraras comprimidos en el archivo 'data_web_scraping.rar'.

* **/DOCUMENT:** Te brindara un poco de informacion del proyecto, sin embargo, hay algunas cosas que es mas faciles visualizar por eso te recomiendo ver la presentacion que tiene informacion mas visual y completa sobre el proyecto.

* **/PRESENTATION:** Esta es la documentacion grafica oficial del proyecto, casi todo esta explicado ahi de una manera divertida; asi que espero sea de utilidad. [¡Se puede ver online en GitHub!](https://github.com/DAFMONTENEGRO/web-scraping-text-modeler/blob/master/PRESENTATION/official%20presentation.pdf)

* **/SQL:** Esta carpeta tiene todo lo que respecta a la construccion de la base de datos con la que se sutento el proyecto, la carpeta tiene en su interior dos carpetas.
  * **/SQL/SYSTEM:** Es la principal en ella encontraras tres carpetas.
    * **/SQL/SYSTEM/CREATION SCRIPTS:** Contiene dos scripts en SQL que son 'modeler_database.sql' y 'modeler_initialization.sql', el primero crea el esquema y las tablas, el segundo los procedimientos almacenados, vistas, triggers,usuarios... etc. Ademas de agregar por defecto 121000 palabras para poder hacer uso de la libreria.
     * **/SQL/SYSTEM/DIAGRAM:** Es la imagen del modelo de la base de datos.
     * **/SQL/SYSTEM/MODEL WORKBENCH:** Es el archivo Workbench de la base de datos.
  * **/SQL/VALUES:** Tiene el script en SQL comprimido en rar para poder agregar los mas de 3000 cuentos alojados en la carpeta 'DATA WEB SCRAPING'
* **/CODE:** Aqui esta alojado el script [modeler.py](https://github.com/DAFMONTENEGRO/web-scraping-text-modeler/blob/master/CODE/modeler.py) del proyecto escrito en python.
