# survey-demo

## REST API

Server code generated by [Swagger codegen](https://swagger.io/tools/swagger-codegen/) from OpenAPI 3 definition yaml, with a sqlite3 database persisting state, and business logic implemented into the controller.

### Usage

To run the server, execute the following from the **python-flask-server-generated directory**:
```
pip3 install -r requirements.txt
python3 db_init.py
python3 -m swagger_server
```

and open your browser to here:
```
http://localhost:5000/ui/
```

## Vue.js App Front-end

Single page app, mostly single component (Polls.vue) interface. 

### Usage

Derived from client/README.md, execute the following from the **client** directory:

### Project Setup
```
npm install
```

### Compiles and hot-reloads for development
```
npm run serve
```
