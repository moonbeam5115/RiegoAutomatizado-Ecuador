# Riego Automatizado 

# Create and activate an environment:
conda create --prefix ./env python=3.8 -y

conda activate ./env

# Install requirements
pip install -r requirements.txt

# Sistema Inteligente Para Riego De Agua

El sistema puede ser inicializado por el programa `comenzar_riego_inteligente.py`

El programa contiene los siguientes pasos:

(1.) Importar funciones para utilizar en el programa
(2.) Definir el path a los datos meteorologicos - data_path
(3.) Calcular los valores tmax, tmin, hr, hr_min, hr_max dados la informacion meteorlogica
(4.) Calcular el volumen_de_riego dado los valores en (3.)
(5.) Calcular el volumen_optimzado
(6.) Calcular el tiempo de riego, dado el volumen_optimzado
(7.) Se define la funcion iniciar_riego para conectarse al arduino e implementar la logica dado los valores calculados anteriormente
(8.) Se define un "scheduler" para poner una hora que debe ejecutarse una funcion (con algun input) -> `schedule.every().day.at("23:35").do(determinar_riego, tiempo)`
(9.) Se crea un `while` loop para continuamente (cada 5 segundos) chequear la hora y determinar si se deberia ejecutar la funcion -> `schedule.run_pending()`
(10.) Se genera el resto de los datos para anadir a la base de datos junto a los datos coleccionados anteriormente
