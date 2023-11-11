import customtkinter as ctk
import config
import openai

openai.api_key = config.api_key

#Constants
CONTEXT_FOR_ASSISTANT = """Eres un asistente amable que le va a ayudar a un usuario a crear Producto. 
            Los siguientes detalles tiene que estar incluidos, ni más ni menos: Nombre, Cantidad y Precio. 
            Solicita al usuario que ingrese esos atributos específicos. Cada vez que el usuario envíe un mensaje debes confirmar con él que esté correcta la información hasta que el usuario te dé una confirmación final que todo está bien. Luego, cuando el usuario de la confirmacion de que todo esta bien siempre incluye la frase exacta "Gracias por usar S" Tu discurso debe ser que estás intentando crear y hasta que él no te confirme no lo puedes hacer.
            """
MESSAGE_FOR_OUTPUT_CREATION = "Dame la informacion en forma de json de todos los Producto con los siguientes valores exactos Nombre, Cantidad y Precio para usar en un endpoint"

def sendInfo():
    userInput = inputText.get( "1.0", 'end-1c' )
    print(userInput)
    historyText.configure( state='normal' )
    if len( historyText.get( "1.0", 'end-1c' ) ) == 0: initializeAI( )
    historyText.insert( "end", "Usuario: ", tags="blue")
    historyText.insert( "end", userInput + "\n\n" )
    response = askAI( userInput )
    historyText.insert( "end", text="S: ", tags="orange")
    historyText.insert( "end", response + "\n\n" )

    if "Gracias por usar S" in response:
        #Este mensaje dependera de lo que se configure en Set up Actions
        array_messages.append({"role": "user", 
                               "content":MESSAGE_FOR_OUTPUT_CREATION })
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages = array_messages
        )
        response_text = response.choices[0].message.content
        historyText.insert( "end", text="Output: ", tags="yellow")
        historyText.insert( "end", response_text + "\n\n" )

    historyText.see( "end" )
    historyText.configure( state='disabled' )

def initializeAI( ):
    # Contexto del asistente
    context = CONTEXT_FOR_ASSISTANT
    global array_messages 
    array_messages = [{"role": "system", "content": context}] 
    
def askAI( userInput ):
    
    global array_messages
    array_messages.append({"role": "user", "content": userInput})

    

    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages= array_messages
    )
    response_text = response.choices[0].message.content
    array_messages.append({"role": "assistant", "content": response_text})

    return response_text


root = ctk.CTk()
topLabel = ctk.CTkLabel(root, text="Input Cliente", font=ctk.CTkFont(size=30, weight="bold"))
historyText = ctk.CTkTextbox(root, state = "disabled")
inputText = ctk.CTkTextbox( root, font= ctk.CTkFont( size = 15 ) )
button = ctk.CTkButton( root, text="Enviar informacion", command= sendInfo )
historyText.tag_config("blue", foreground="green" )
historyText.tag_config("orange", foreground="orange")
historyText.tag_config("yellow", foreground="yellow")


def main():   
    root.title("Input Merchants")
    root.geometry("750x550")
    ctk.set_appearance_mode("dark")
    topLabel.pack(padx=10, pady=(40,20))

    historyText.pack(fill="x", padx=100)

    
    inputText.pack( pady=10, fill="x", padx=100 )

    button.pack()


    root.mainloop()

if __name__ == '__main__':
    main()

