class Car:
    def __init__(self, car_data):
        self.production_date = car_data.get('productionDate')
        self.description = car_data.get('description')
        self.url = car_data.get('url')
        self.known_vehicle_damages = car_data.get('knownVehicleDamages')
        self.model = car_data.get('model')
        self.mileage = car_data['mileageFromOdometer'].get('value') if 'mileageFromOdometer' in car_data else None
        self.vehicle_transmission = car_data.get('vehicleTransmission')
        self.color = car_data.get('color')
        self.brand = car_data['brand'].get('name') if 'brand' in car_data else None
        self.name = car_data.get('name')
        self.image = car_data.get('image')
        self.category = car_data.get('category')
        self.price_currency = car_data['offers'].get('priceCurrency') if 'offers' in car_data else None
        self.city = car_data['web_info'].get('city_persian') if 'web_info' in car_data else None
        self.title = car_data['web_info'].get('title') if 'web_info' in car_data else None
        self.category_slug = car_data['web_info'].get('category_slug_persian') if 'web_info' in car_data else None
        self.district = car_data['web_info'].get('district_persian') if 'web_info' in car_data else None

        self.price = car_data['offers'].get('price') if 'offers' in car_data else None
        # Remove trailing zeros
        if self.price is not None:
            self.price = float(self.price)
            if self.price.is_integer():
                self.price = int(self.price) / 10000000

    def __str__(self):
        return f"{self.name}\nرنگ: {self.color}\nکارکرد: {self.mileage} کیلومتر\nقیمت: {self.price} میلیون تومان\n{self.city}-{self.district}\n{self.url}\n\n{self.image}"
