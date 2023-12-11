from data_processing.data_module import Catalog
import openai
import json
import config
from decimal import Decimal
import os

from config.api_keys import API_KEY
openai.api_key = API_KEY

class AIAssistant( ):
    array_messages = []
    def __init__( self ):
        current_dir = os.path.dirname( os.path.abspath(__file__) )

        json_file_path = os.path.join( current_dir, 'estructura_pedido.json' )
        with open( json_file_path, 'r', encoding='utf-8' ) as o:
            json_file = json.loads( o.read( ) )
            order_format = json.dumps( json_file ,ensure_ascii=False, separators=(',', ':') )

        catalog = Catalog( )
        products = catalog.products_to_json( )

        first_part_file_path = os.path.join(current_dir, 'first_part_context_for_assistant.txt')
        second_part_file_path = os.path.join(current_dir, 'second_part_context_for_assistant.txt')

        with open(first_part_file_path, 'r', encoding='utf-8') as c:
            firstpart_txt = c.readlines()
            firstpart_txt_context_for_assistant_minified_text = "".join(line.strip( ) for line in firstpart_txt if line.strip())

        with open(second_part_file_path, 'r', encoding='utf-8') as c:
            secondpart_txt = c.readlines()
            secondpart_txt_context_for_assistant_minified_text = "".join(line.strip( ) for line in secondpart_txt if line.strip())
    
        context = firstpart_txt_context_for_assistant_minified_text + order_format + secondpart_txt_context_for_assistant_minified_text + "Catalogo de productos y adiciones:" + products
        print(context)
        self.array_messages = [{"role": "system", "content": context}]
    
    def askAI( self, userInput ):
        self.array_messages.append({"role": "user", "content": userInput})
        response = openai.chat.completions.create(
            model="gpt-4-1106-preview",
            messages= self.array_messages,
            response_format={"type": "json_object"},
            max_tokens=1000
        )
        response_json = response.choices[0].message.content
        print("Assistant: " + response_json )
        data = json.loads( response_json )
        response_text = data["mensaje"]
        self.array_messages.append({"role": "assistant", "content": response_text})
        if "pedido" in data:
            if len( data["pedido"] ) > 0:
                orderFormated = self.format_pedido( data )
                response_text += "\n\nTu pedido\n"+orderFormated
        if "pedido_confirmado" in data:
            if data["pedido_confirmado"]: response_text +="\nPEDIDO CONFIRMADO"
        return response_text
    
    def format_pedido( self, jsonOrder ):
        formatted_order = ""

        for index, item in enumerate(jsonOrder["pedido"], start=1):
            product_price = Decimal(item['precio_base'])
            formatted_order += f"{index}. {item['nombre']} (x{item['cantidad']}). ${'{:,.0f}'.format(product_price)}\n"

            if item.get("extras"):
                for extra_group in item["extras"]:
                    for extra in extra_group["seleccion"]:
                        formatted_order += f" - {extra['extra']}"
                        if extra['precio'] != "0.0":
                            product_price += Decimal(extra['precio'])
                            price_str = f"${'{:,.0f}'.format(Decimal(extra['precio']))}"
                            formatted_order += f" {price_str}\n"
                        else:
                            formatted_order += "\n"
            else:
                formatted_order += "\n"

        total_order_price = sum(
            Decimal(item['precio_base']) + sum(
                Decimal(extra['precio']) for extra_group in item["extras"] for extra in extra_group["seleccion"]
                if extra['precio'] != "0.0"
            ) for item in jsonOrder["pedido"]
        )

        formatted_order += f"Total a pagar: ${'{:,.0f}'.format(total_order_price)}\n"

        return formatted_order