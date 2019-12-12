# METEO INFO

Autor: Sergio del Castillo Baranda

Módulo en python creado para resolver la práctica del módulo de python del máster Big Data & Blockchain de la Universidad Complutense de Madrid en 2019.

[Repositorio git](https://github.com/serCliff/meteo_info)

## MODO DE USO

Para asegurarse tener el mismo entorno de trabajo:

```bash
conda env create --file environment.yml
```

Ejecución de la práctica:

```bash
python3 meteo_info -h
```

Esto lanza el siguiente mensaje

```bash
usage: meteo_info [-h] [-mr] [-f FILE]

Ejecución de la práctica. Por defecto realiza la ejecución mediante el uso de la librería pandas con el fichero de ejemplo sample.txt

optional arguments:
  -h, --help            show this help message and exit
  -mr, --map-reduce     Ejecutar usando funcionalidad de map y reduce
  -f FILE, --file FILE  Ruta archivo tipo gsod.txt
```

## MODOS DE EJECUCIÓN

**Ejecución por defecto** lanza el script con el fichero de ejemplo empleando librería pandas.

```bash
python3 meteo_info
```

Ejecución mediante **uso de librería con map-reduce**

```bash
python3 meteo_info -mr
```

Ejecución **utilizando un fichero propio**, siempre tiene que tener el formato de los ficheros gsod.

```bash
python3 meteo_info -f /ruta/de/nuestro/fichero.txt
```

Podemos lanzar el script con **fichero propio** y utilizando la **librería map-reduce**:

```bash
python3 meteo_info -mr -f /ruta/de/nuestro/fichero.txt
```

## ARCHIVO LOG

Cuando ejecutemos el código en la propia ruta en la que nos encontremos dejará un fichero nombrado meteo_info.log donde nos informará en tiempo real de lo que se está ejecutando.

## CONCLUSIONES

La ejecución mediante el uso de las opciones que provee la librería pandas son muy fáciles de comprender y trabajar con ellas. Ofrecen un código limpio y rápido de realizar. Pero en su contra la penalización en la ejecución es muchísimo mayor respecto al uso de métodos como map, filter y reduce.