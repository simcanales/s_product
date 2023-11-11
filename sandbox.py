import config
import openai

openai.api_key = config.api_key

# Contexto del asistente
array_messages = [{"role": "system", "content": "Crea una tabla para un pedido con las siguientes columnas: usuario que pide, producto, cantidad"}]

# Usuario digita pregunta y se guarda en el arreglo de mensajes
# content = input("Escribe tu pregunta!")
# messages.append({"role": "user",
#              "content:": content})

sample_text =  "Simón quiere pedir 3 doritos, 2 gatorades y 4 bombillas. Camilo necesita 4 teclados, 3 ratones y tal vez 90 notebooks. Sebastián encarga 10 papeles, 4 guitarras y 60 CPU, Sonia necesita 3 pelotas de tenis"
array_messages.append({"role": "user", "content": sample_text})

# Chatgpt responde y se guarda respuesta en el arreglo de mensajes

response = openai.chat.completions.create(
    model="gpt-3.5-turbo-1106",
    messages=array_messages
)
# messages.append({"role": "assistant",
#              "content:": response)

# Imprimir respuesta
print(response.choices[0].message.content)





