# Flujo y Costo
Proyecto para el Control de Flujo y Costo en la Empresa de Tabaco Torcido Villa Clara (ETTVC)

#Iniciar proyecto

- Clonar el repositorio

$git clone https://github.com/vivianromero/FlujoCosto.git

$git clone git@gitlab.azcuba.cu:python/control-de-flujo-y-costos.git

- Moverse a la carpera creada

$cd FlujoCosto

- Hacer que el fichero de config de las variables de entorno local .env.local no sea rastreado por el Git

$git rm --cached config/.env.local

-Correr las migraciones:
python manage.py migrate

-Cargar los datos iniciales
python manage.py populatedb
