from fastapi import Request, FastAPI

from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from vehicule import Vehicle

app = FastAPI()

datalake = []


# 1ère route
@app.get('/')
def testFnct():
    return {'API Status': 'ON'}


# 2ᵉ route
@app.post('/createVehicle')
def createVehicle(request: Request):
    for i in request.query_params:
        if i not in {'Avion', 'Bateau', 'Moto', 'Voiture'}:
            return JSONResponse({'ERROR': 'le type de véhicule ne peut être que : Avion, Bateau, Moto ou Voiture'},
                                400)
        if i == '':
            return JSONResponse(
                {'error': 'impossible de rechercher un champ vide'}, 400)
    data = {
        'vehicleType': request.query_params['vehicleType'],
        'name': request.query_params['name'],
        'brand': request.query_params['brand'],
        'maxSpeed': request.query_params['maxSpeed'],
        'kms': request.query_params['kms']
    }

    newVehicle = Vehicle(data)
    newVehicle.save(datalake)

    return JSONResponse({
        newVehicle.name: newVehicle.__dict__
    })


# 3ᵉ route
@app.get('/getVehicles')
def getVehicles():
    return JSONResponse({'nbVehicle': Vehicle.nbVehicles})


# 4ᵉ route
@app.get('/nbof/{vType}')
def nbOfType(vType: str):
    if vType in {'Avion', 'Bateau', 'Moto', 'Voiture'}:
        count = 0
        for i in datalake:
            if i.vehicleType == vType:
                count += 1

        return JSONResponse({
            'Number of ' + vType: count
        })
    else:
        return JSONResponse({'ERROR': 'le type de véhicule ne peut être que : Avion, Bateau, Moto ou Voiture'}, 400)


# 5ᵉ route
@app.get('/searchVehicle')
def searchVehicle(request: Request):
    for i in request.query_params:
        if i == '':
            return JSONResponse(
                {'error': 'impossible de rechercher un champ vide'}, 400)
        if i not in {'vehicleType', 'name', 'brand', 'maxSpeed', 'kms'}:
            return JSONResponse(
                {'error': 'les seuls champs autorisés pour une recherche sont : vehicleType, name, brand, '
                          'maxSpeed et kms '}, 400)
    searchResult = []
    for vehicle in datalake:
        vehicleDict = vehicle.__dict__
        for param in vehicleDict:
            if request.query_params[param] == vehicleDict[param]:
                searchResult.append(vehicleDict)

    return JSONResponse(searchResult)


@app.exception_handler(StarletteHTTPException)
def http_exception_handler(request: Request, exc: StarletteHTTPException):
    return JSONResponse({'error': 'route does not exist'}, 404)
