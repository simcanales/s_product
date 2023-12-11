import csv
import json
from typing import Dict, List
import os

current_dir = os.path.dirname(os.path.abspath(__file__))

PATH_TO_PRODUCTS = os.path.join(current_dir, 'Catalogo Home Burger - Productos.csv')
PATH_TO_EXTRAS = os.path.join(current_dir, 'Catalogo Home Burger - Adiciones.csv')



class Catalog( ):
    product_array = []
    def __init__( self ):
        # Create the product table
        global product_array
        product_array = self.read_product_file( PATH_TO_PRODUCTS, PATH_TO_EXTRAS )


    def read_product_file( self, product_path, extra_path):
        print(f"Absolute path to extras file: {os.path.abspath(PATH_TO_EXTRAS)}")

        extras_dict = {extra.extra_id: extra for extra in self.read_extra_file( extra_path )}

        with open( product_path, 'r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file, fieldnames=['id Producto', 'Nombre', 'Descripcion', 'Precio', 'Extras Disponibles', 'Categoria', 'Esta Disponible'], skipinitialspace=True)
            next(reader)  # Saltar la primera fila (encabezados)
            productos = []
            for row in reader:
                try:
                    extras_disponibles = [int(extra_id) for extra_id in row.get('Extras Disponibles', '').split(',') if extra_id.strip()]
                except ValueError:
                    print(f"Error: No se puede convertir a entero. Fila con Extras Disponibles: {row}")
                    continue

                extras = [extras_dict[extra_id] for extra_id in extras_disponibles]
                productos.append(Product(int(row['id Producto']), row['Nombre'], row['Descripcion'], float(row['Precio']), extras, row['Categoria'], row['Esta Disponible'] == 'Si'))
        return productos
    
    def read_extra_file( self, extra_path ):
        with open( extra_path, 'r', newline='', encoding='utf-8' ) as file:
            reader = csv.DictReader(file, fieldnames=['ID Extra', 'Nombre', 'Opciones Disponibles y Precio', 'Cantidad Máxima Total Seleccionable', 'Es Obligatoria', 'Cantidad Máxima por Opción'], skipinitialspace=True)
        
            # Omitir la primera fila que contiene encabezados
            next(reader, None)
        
            extras = []
            for row in reader:
                options_and_price_str = row['Opciones Disponibles y Precio']
                options_and_price = {}
                if options_and_price_str:
                    options_and_price_list = [option_price.split(':') for option_price in options_and_price_str.split(',')]
                    options_and_price = {option.strip(): (float(price) if price else None) for option, price in options_and_price_list}

                extras.append(Extra(
                    int(row['ID Extra']),
                    row['Nombre'],
                    options_and_price,
                    int(row['Cantidad Máxima Total Seleccionable']),
                    row['Es Obligatoria'] == 'Si',
                    int(row['Cantidad Máxima por Opción'])
                ))
        return extras
    
    def products_to_json( self ):
        global product_array
        products_json = []
        for product in product_array:
            product_json = {
                "name": product.name,
                "description": product.description,
                "price": product.price,
                "extras": []
            }

            for extra in product.extras:
                extra_json = {
                    "name": extra.name,
                    "optionsAndPrice": extra.optionsAndPrice
                }
                product_json["extras"].append(extra_json)

            products_json.append(product_json)

        return json.dumps(products_json, ensure_ascii=False,separators=(',', ':'))


class Extra:
    def __init__(self, extra_id: int, name: str, optionsAndPrice: Dict[str, float], maxQuantityTotal: int, isMandatory: bool, quantityPerOption: int):
        self.extra_id = extra_id
        self.name = name
        self.optionsAndPrice = optionsAndPrice
        self.maxQuantityTotal = maxQuantityTotal
        self.isMandatory = isMandatory
        self.quantityPerOption = quantityPerOption
    def __str__(self):
        options_and_price_str = ", ".join(f"{option}: {price}" for option, price in self.optionsAndPrice.items())
        return f"Extra ID: {self.extra_id}, Nombre: {self.name}, Opciones y Precio: {{{options_and_price_str}}}, Máxima Cantidad Total: {self.maxQuantityTotal}, Obligatoria: {self.isMandatory}, Cantidad Máxima por Opción: {self.quantityPerOption}"

class Product:
    def __init__(self, product_id: int, name: str, description: str, price: float, extras: List[Extra], category: str, isAvailable: bool):
        self.product_id = product_id
        self.name = name
        self.description = description
        self.price = price
        self.extras = extras
        self.category = category
        self.isAvailable = isAvailable

        # Agregar un diccionario para almacenar los extras por nombre
        self.extras_dict = {extra.name: extra for extra in extras}

    def get_extra_by_name(self, extra_name: str) -> Extra:
        return self.extras_dict.get(extra_name)
    def __str__(self):
        return f"Producto ID: {self.product_id}, Nombre: {self.name}, Disponible: {self.isAvailable}\n  " + "\n  ".join(str(extra) for extra in self.extras)

    
