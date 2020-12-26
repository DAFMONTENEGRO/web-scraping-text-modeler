# web-scraping-text-modeler

El proyecto es una propuesta de modelamiento del idioma español por medio de bases de datos relacionales, para la creación del modelo el programa es capaz de analizar el orden, composición y estructura de cualquier texto suministrado o conjunto de palabras. Esto quiere decir que el programa es capaz de construir un modelamiento sobre cualquier idioma en el que estén escritos los textos suministrados, sin embargo, por defecto se distribuye con una implementación en español y una biblioteca de textos en español obtenidos por la herramienta de web scraping integrada en el proyecto.

---

# Proyecto Bases de Datos

- Daniel Felipe Montenegro Herrera

---

## 1. Herramientas utilizadas

### 1.1. Librerías Python

Para su correcto funcionamiento el proyecto hace uso de cuatro librerías en Python, estas librerías son las que permiten la interconectividad de la herramienta. A continuación, se detalla el uso de cada librería:

* **Os:** Permite la lectura y escritura de archivos
* **Time:** Genera pequeños retardos para que la interfaz sea mas amigable
* **Requests:** Crea las solicitudes a las paginas web
* **Mysql.connector:** Es la librería oficial de Mysql para conectarse desde Python
* **BeautifulSoup:** Facilita el análisis de documentos html

La librería **Os** y la librería **Time** vienen por defecto distribuidas con Python, el resto se instaló por medio de pip.

### 1.2. Corpus de Referencia del Español Actual

El Corpus de Referencia del Español Actual (CREA) provee un [listado de frecuencias](http://corpus.rae.es/lfrecuencias.html) de todas palabras existentes en la lengua.

### 1.3. Web Scraping

Por defecto la base de datos se distribuirá con las primeras 121000 frecuencias del CREA, sin embargo, para poner a prueba la herramienta procesamos con ella 3276 textos (cuentos de diversos autores en el idioma español) que contenían 852302 frases los cuales fueron recolectados de la pagina web www.ciudadseva.com, esto gracias a que en su documento robots.txt especificaba al momento del raspado que era posible extraer este contenido.

Esta biblioteca se formo por medio de una aplicación que esta integrada en la librería  para hacer Web Scraping de cualquier pagina web.

### 1.4. MYSQL

Es el gestor de base de datos que utiliza el proyecto, los scripts de creación de la base de datos que se distribuyen están implementados especialmente para su uso en MYSQL.

---

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
El script de creacion permite la creacion de dos usuarios, el primero es el usuario por defecto **'root'** y el segundo es un usuario invitado llamado **'guest'**. 

---

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

---

## 4. Funcionalidades

### Resumen de las funcionalidades

El codigo puede desempeñar las siguientes funcionalidades, ya sea por medio del llamado a sus métodos o por medio de su interfaz de consola:

1. **Buscador de frases:** Dada una palabra o frase, busca todas las frases de la base de datos con esa frase o palabra, señalando en cada una el texto de su origen.
2. **Corrector de ortografía:** Dada una palabra o frase corrige su ortografía.
3. **Completar una frase:** A partir de una palabra o frase indica cual es la palabra mas probable a continuación.
4. **Entrenador corrector ortografico:** Funciona igual que el corrector ortografico, sin embargo, te indica las posibles correcciones y en caso de que no exista una correction guarda la palabra como un error (exclusiva del usuario 'root').

### 4.1. Buscador de frases

Creando una conexión con la base de datos es posible consultar la **vista phrases** y realizar una búsqueda sobre la misma, la sentencia a utilizar será SELECT LIKE para utilizar el comodín de  búsqueda “%”. Un ejemplo de la búsqueda para todas las frases que contienen “tu” en la base de datos seria la siguiente:
  
`SELECT Phrase, Text_name FROM phrases WHERE Phrase LIKE ‘%tu%' ;`

El resultado de esta búsqueda serán todas las tuplas frase-texto que contengan la palabra o frase indicada entre los porcentajes, de esta manera es como se implemento esta funcionalidad.

### 4.2. Corrector de ortográfica

Para verificar cada uno de los ejemplos que se presentaran a continuación por favor considere como corrección ortográfica para cada tipo de error a la palabra: `Montenegro`. Supongamos que al escribir la palabra de ejemplo cometemos un error, podemos clasificar cualquier posible error en alguno de estos tipos.

* **Error de omisión:** Es la falta de uno o mas caracteres. Ejemplo: `Mntenegro` se omite la primer letra o.
* **Error de posición:** Se intercambia uno o mas caracteres por uno diferente. Ejemplo: `Montenegzo` se intercambio la r por la z.
* **Error de adición:** Se agrega un carácter de mas a la palabra. Ejemplo: `Monttenegro` se escribe la palabra con dos t.

#### Corrección ortográfica: virde

La palabra virde es reamente la palabra verde mal escrita, para corregirla ortográficamente veamos los posible escenarios de acuerdo a los tipos de errores que presentamos anteriormente: 

* **-** ?irde v?rde vi?de vir?e vird?
* **=** !irde `v!rde` vi!de vir!e vird!
* **+** !virde v!irde vi!rde vir!de vird!e virde!

##### **Símbolos:** El símbolo ? representa la ausencia de un carácter en esa posición, la ! significa que existe un carácter cualquiera en esa posición, que es lo mismo que “_” al hacer una consulta en SQL. 

El caso `resaltado` es el que nos devolverá la corrección correcta de la palabra si intercambiamos ‘!’ por ‘e’, para obtener la palabra verde.

#### Resultado de la corrección

Para encontrar la corrección de una palabra buscaremos en la base de datos todos los posibles escenarios que nombramos anteriormente con la sentencia SELECT LIKE. En la diapositiva anterior indicamos que el caso resaltado es el que nos devolverá la corrección, es decir el caso `v!rde` que llevado a la sentencia SQL quedaría de la siguiente manera:

`SELECT * FROM " + table + " WHERE Word LIKE ‘v_rde' ;`

Esta sentencia la hacemos con cada uno de los posibles escenarios y eso nos dará como resultado todas las posibles correcciones, ahora simplemente **solo elegimos la palabra que mas repeticiones tenga** en la base de datos. Si estamos corrigiendo mas de una palabra podemos utilizar la **vista codings** que nos indicara cual es el conjunto de palabras que puede continuar luego de una frase solo realizamos la intersección de estos dos conjuntos para afinar la corrección.

### 4.3. Completar una frase

Para completar una frase solo tenemos que realizar una consulta sobre la vista codings,  pero antes es bueno explicar de que manera se almacenan los datos en esta vista.

##### Para hacerlo supongamos la siguiente frase del autor Abelardo Díaz Alfaro: “sombra imborrable del josco sobre la loma que domina el valle del toa”

1. El programa divide la frase, es decir genera el arreglo: [sombra, imborrable, del, josco, sobre, la, loma, que, domina, el, valle, del, toa].
2. Luego analiza cada una de estas palabras y las agrega a la tabla codings teniendo en cuenta de que palabra viene y a que palabra va (agrega el id de la palabra, la vista solo convierte este id en la palabra en cuestión).
3. Si la combinación de palabras ya existe solo le suma uno a la frecuencia (esto lo hace el procedimiento almacenado).

La tabla codings es una tabla que se relaciona consigo misma, sin embargo, esta tabla solo esta compuesta por números y la columna cod_come_from es el id de la ultima fila de esta misma tabla que contiene la combinación de palabras anterior a la palabra de la columna cod_wor_id.

##### Nota: Abordar el problema de esta manera nos asegura poder crear relaciones entre las entidades que decidimos construir con anterioridad, ya que este tipo de modelos normalmente es construido bajo un paradigma NOSQL; el reto propuesto en este proyecto era proponer una alternativa funcional desde el paradigma SQL.

### 4.4. Entrenador corrector ortográfico

Esta es la misma funcionalidad que el corrector ortográfico, sin embargo, esta variación no nos mostrara una única corrección como resultado sino todas las posibles correcciones de una palabra y nos permitirá elegir cual es la correcta para nosotros, de esta manera una vez elegida la corrección correcta le sumara una frecuencia a esa palabra en la base de datos. Si no existe una corrección para esa palabra la agregara como un error a la base de datos.

Esta función es **exclusiva** del usuario “root” de la base de datos quien es el que posee todos los permisos sobre la base de datos. En el menú del usuario “guest” no aparecerá esta funcionalidad.

---

## 5. Uso de la herramienta

Las funcionalidades se pueden usar de dos maneras, por medio del menú implementado en la librería o haciendo uso de los métodos, para llamar a los métodos primero hay que escribir **'import modeler'** en el script de Python en el que vayamos a utilizarlo, luego hacer uno de los siguientes llamados para la funcionalidad:

* **Buscador de frases:**	modeler. find_frase(phrase)
* **Corrector de ortografía:**	modeler.spell_checker (phrase, table)
* **Completar una frase:**	modeler.predictive_text(phrase)
* **Entrenador corrector ortografico:**	modeler.spell_checker_trainer(word, table)

La segunda alternativa es usar el menú integrado en la librería, para utilizar este menú existen dos maneras, la primera es ejecutar el script modeler.py, la segunda es ejecutar un “import modeler” y luego un “modeler.Menu()”. Al iniciar nos pedirá el usuario y contraseña de la base de datos, una vez ingresado y confirmada la conexión nos mostrara el menú.
