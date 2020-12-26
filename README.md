# web-scraping-text-modeler

Antes de empezar te recomiendo leer la informacion de cada una de las carpetas que se distribuyen con este proyecto.

## Informacion del directorio:

* DATA WEB SCRAPING: Posee todos los textos que se utilizaron para contruir la base de datos sustentada con en el proyecto, son documentos de texto (.txt) los cuales son transcripciones de cuentos extraidos de la web. Son mas de 3000 asi que por eso pesan un poco.

* DOCUMENT: Te brindara un poco de informacion del proyecto, sin embargo, hay algunas cosas que es mas faciles visualizar por eso te recomiendo ver la presentacion que tiene informacion mas visual y completa sobre el proyecto.

* PRESENTATION: Esta es la documentacion grafica oficial del proyecto, casi todo esta explicado ahi de una manera divertida; asi que espero sea de utilidad

* SQL: Esta carpeta tiene todo lo que respecta a la construccion de la base de datos con la que se sutento el proyecto, la carpeta tiene en su interior dos carpetas.
  * SYSTEM: Es la principal en ella encontraras tres carpetas
    * CREATION SCRIPTS: Contiene dos scripts en SQL que son modeler_database.sql y modeler_initialization.sql, el primero crea el esquema y las tablas, el segundo los procedimientos almacenados, vistas, triggers,usuarios... etc. Ademas de agregar por defecto 121000 palabras para poder hacer uso de la libreria.
     * DIAGRAM: Es la imagen del modelo de la base de datos
     * MODEL WORKBENCH: Es el archivo Workbench de la base de datos
  * VALUES: Tiene el script correspondiente a los mas de 3000 cuentos alojados en la carpeta DATA WEB SCRAPING
* CODE: Aqui esta alojado el script 'modeler.py' del proyecto escrito en python.
