# Copyright 2015 IBM Corp. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os, json, logging, data
from flask import Flask, jsonify
from pymongo import MongoClient
from flask import render_template

app = Flask(__name__)

# Conexion con el servidor
vcap_config = os.environ.get('VCAP_SERVICES')
decoded_config = json.loads(vcap_config)
for key, value in decoded_config.iteritems():
     if key.startswith('mongodb'):
         mongo_creds = decoded_config[key][0]['credentials']
mongo_url = str(mongo_creds['url'])

client = MongoClient(mongo_url)

logging.warn('carga de datos')
# Cargamos los datos
data.loadData(client)
logging.warn('fin de carga de datos')


@app.route('/')
def Welcome():
    return app.send_static_file('index.html')

@app.route('/listar')
def listar():

    logging.warn('Inicio Consulta')
    db = client.db
    listado = db.listado
    lista = listado.find().sort('nombre',1)
    logging.warn('Fin Consulta')

    return render_template('listado.html',lista = lista)

@app.route('/listarFiltro')
def listarFiltro():

    db = client.db
    listado = db.listado

    logging.warn('Inicio Consulta')
    lista = listado.find({"pais":"China","sexo":"Male"}).sort('nombre',1)
    logging.warn('Fin Consulta')

    return render_template('listado.html',lista = lista)


@app.route('/error')
def generarerror():

   x = client.database_names()
   logging.warn(x)

   return x


port = os.getenv('PORT', '5000')
if __name__ == "__main__":
	app.run(host='0.0.0.0', port=int(port))