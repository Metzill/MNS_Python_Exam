class Vehicle:

    nbVehicles = 0

    def __init__(self, data):
        self.vehicleType = data.get('vehicleType')
        self.name = data.get('name')
        self.brand = data.get('brand')
        self.maxSpeed = data.get('maxSpeed')
        self.kms = data.get('kms')
        Vehicle.nbVehicles += 1

    def save(self, datalake):
        datalake.append(self)
