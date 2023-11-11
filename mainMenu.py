import customtkinter as ctk
import config
import openai

openai.api_key = config.api_key


#Set Up Actions attributes
radioButtons = ["Crear Órdenes","Crear Usuarios","Crear Productos"]
previousRadioButtonOption = -1

#Input Users Attributes


#Input Users Constants
CONTEXT_FOR_ASSISTANT = """Eres un asistente amable que le va a ayudar a un usuario a crear Producto. 
            Los siguientes detalles tiene que estar incluidos, ni más ni menos: Nombre, Cantidad y Precio. 
            Solicita al usuario que ingrese esos atributos específicos. Cada vez que el usuario envíe un mensaje debes confirmar con él que esté correcta la información hasta que el usuario te dé una confirmación final que todo está bien. Luego, cuando el usuario de la confirmacion de que todo esta bien siempre incluye la frase exacta "Gracias por usar S" Tu discurso debe ser que estás intentando crear y hasta que él no te confirme no lo puedes hacer.
            """
MESSAGE_FOR_OUTPUT_CREATION = "Dame la informacion en forma de json de todos los Producto con los siguientes valores exactos Nombre, Cantidad y Precio para usar en un endpoint"



def open_home( ):
    hideComponents( )
    lblWelcome = ctk.CTkLabel( main_frame, text= "Bienvenido a S", font=( "Bold", 40 ) )
    lblWelcome.pack( pady = 200 )

def open_setUpActions( ):
    hideComponents( )
    lblTitleOfSUA = ctk.CTkLabel( main_frame, text="Set-Up Actions", font=( "Bold", 40 ) )
    lblTitleOfSUA.pack( pady = 40 )

    value = 1
    for rb in radioButtons:
        rbn = ctk.CTkRadioButton( main_frame, text = rb, variable = radioButtonOption, value = value, command= lambda: clickRadiobuttons( ) )
        value=value+1
        rbn.pack( pady = 10 )
    lblOfRB.pack( pady = 20 )

def clickRadiobuttons( ):
    global previousRadioButtonOption
    msg = "Default"
    if radioButtonOption.get( ) == 1:
        msg = "Ingresa los parámetros de la orden que quieres crear"
    if radioButtonOption.get( ) == 2:
        msg = "Ingresa los parámetros de los usuarios que quieres crear"
    if radioButtonOption.get( ) == 3:
        msg = "Ingresa los parámetros de los productos que quieres crear"
    lblOfRB.configure( text = msg, font=( "Bold", 15 ) )
    if not textBox.winfo_ismapped( ):
        textBox.pack( )
        confirmationButton = ctk.CTkButton( main_frame, text="Confirmar", command = clickConfirmButton )
        confirmationButton.pack( pady = 20 )
    elif previousRadioButtonOption != -1:
        for lbl in dictOflblParameters[ previousRadioButtonOption ]:
            lbl.pack_forget( )
        for lbl in dictOflblParameters[ radioButtonOption.get( ) ]:
            lbl.pack( )
    previousRadioButtonOption = radioButtonOption.get( )

def clickConfirmButton( ):
    if textBox.get( ) != "":
        lbl = ctk.CTkLabel( main_frame, text = textBox.get( ) )
        dictOflblParameters[ radioButtonOption.get( ) ].append( lbl )
        lbl.pack( )
        textBox.delete(0, 'end')



def open_inputUser( ):
    hideComponents( )
    lblTitleOfIU = ctk.CTkLabel( main_frame, text="Input Cliente", font=( "Bold", 40 ) )
    lblTitleOfIU.pack( pady = 10 )
    historyText.pack(fill="x", padx=50 )
    inputText.pack( pady=10, fill="x", padx=50 )
    confirmationButtonIU.pack( )

def sendInfo( ):
    userInput = inputText.get( "1.0", 'end-1c' )
    historyText.configure( state='normal' )
    historyText.insert( "end", "Usuario: ", tags="blue")
    historyText.insert( "end", userInput + "\n\n" )
    if len( historyText.get( "1.0", 'end-1c' ) ) == 0: initializeAI( )
    response = askAI( userInput )
    historyText.insert( "end", text="S: ", tags="orange")
    historyText.insert( "end", response + "\n\n" )

    # if "Gracias por usar S" in response:
    #     #Este mensaje dependera de lo que se configure en Set up Actions
    #     array_messages.append({"role": "user", 
    #                            "content":MESSAGE_FOR_OUTPUT_CREATION })
    #     response = openai.chat.completions.create(
    #         model="gpt-3.5-turbo",
    #         messages = array_messages
    #     )
    #     response_text = response.choices[0].message.content
    #     historyText.insert( "end", text="Output: ", tags="yellow")
    #     historyText.insert( "end", response_text + "\n\n" )

    historyText.see( "end" )
    historyText.configure( state='disabled' )

def initializeAI( ):
    ( )

def askAI( userInput ):
    return "Falla en el sistema"

def hideComponents( ):
    for frame in main_frame.winfo_children( ):
        frame.pack_forget( )



root = ctk.CTk( )
root.geometry( "800x600" )
ctk.set_appearance_mode( "dark" )
root.title( "S Menú Principal" )



main_frame = ctk.CTkFrame( root )
main_frame.pack( side = ctk.RIGHT )
main_frame.pack_propagate( False )
main_frame.configure( width=640, height=900 )


options_frame = ctk.CTkFrame( root )
options_frame.pack( side=ctk.LEFT )
options_frame.pack_propagate( False )
options_frame.configure( width=150, height=900 )

home_btn = ctk.CTkButton( options_frame, text='Home', font=("Bold", 15), fg_color= "transparent", anchor="w", command=open_home )
home_btn.pack( pady=(40,20), fill="x" )

setupActions_btn = ctk.CTkButton( options_frame, text='Set Up Actions', font=("Bold", 15), fg_color= "transparent", anchor="w", command=open_setUpActions )
setupActions_btn.pack( pady=(0,20), fill="x" )

inputUsers_btn = ctk.CTkButton( options_frame, text='Input', font=("Bold", 15), fg_color= "transparent", anchor="w", command=open_inputUser )
inputUsers_btn.pack( pady=( 0, 20 ), fill="x"  )

#Set Up Actions
radioButtonOption = ctk.IntVar( )
lblOfRB = ctk.CTkLabel( main_frame, text = "" )
textBox = ctk.CTkEntry( main_frame )
dictOflblParameters = { 1: [ ], 2: [ ], 3: [ ] }

#Input Users
historyText = ctk.CTkTextbox( main_frame, state = "disabled", height = 375 )
inputText = ctk.CTkTextbox( main_frame, font= ctk.CTkFont( size = 15 ), height = 100 )
confirmationButtonIU = ctk.CTkButton( main_frame, text = "Enviar informacion", command = sendInfo )
historyText.tag_config( "blue", foreground = "green" )
historyText.tag_config( "orange", foreground = "orange" )
historyText.tag_config( "yellow", foreground = "yellow" )

root.mainloop( )
