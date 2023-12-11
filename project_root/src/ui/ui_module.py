import customtkinter as ctk
from ai.ai_module import AIAssistant
import time

class UIManager( ):
    #Set Up Actions attributes
    radioButtons = ["Crear Órdenes","Crear Usuarios","Crear Productos"]
    previousRadioButtonOption = -1
    isAIInitialized = False
    aIAssistant = None
    

    WELCOME_MESSAGE = "Bienvenido! Que quieres pedir hoy?\n\n"
    def __init__( self ):
        self.root = ctk.CTk( )
        self.root.geometry( "800x600" )
        ctk.set_appearance_mode( "dark" )
        self.root.title( "S Menú Principal" )



        self.main_frame = ctk.CTkFrame( self.root )
        self.main_frame.pack( side = ctk.RIGHT )
        self.main_frame.pack_propagate( False )
        self.main_frame.configure( width=640, height=900 )


        self.options_frame = ctk.CTkFrame( self.root )
        self.options_frame.pack( side=ctk.LEFT )
        self.options_frame.pack_propagate( False )
        self.options_frame.configure( width=150, height=900 )

        self.home_btn = ctk.CTkButton( self.options_frame, text='Home', font=("Bold", 15), fg_color= "transparent", anchor="w", command= self.open_home )
        self.home_btn.pack( pady=(40,20), fill="x" )

        self.setupActions_btn = ctk.CTkButton( self.options_frame, text='Set Up Actions', font=("Bold", 15), fg_color= "transparent", anchor="w", command= self.open_setUpActions )
        self.setupActions_btn.pack( pady=(0,20), fill="x" )

        self.inputUsers_btn = ctk.CTkButton( self.options_frame, text='Input', font=("Bold", 15), fg_color= "transparent", anchor="w", command= self.open_inputUser )
        self.inputUsers_btn.pack( pady=( 0, 20 ), fill="x"  )

        #Set Up Actions
        self.radioButtonOption = ctk.IntVar( )
        self.lblOfRB = ctk.CTkLabel( self.main_frame, text = "" )
        self.textBox = ctk.CTkEntry( self.main_frame )
        self.dictOflblParameters = { 1: [ ], 2: [ ], 3: [ ] } 

        #Input Users
        self.historyText = ctk.CTkTextbox( self.main_frame, state = "disabled", height = 375 )
        self.inputText = ctk.CTkTextbox( self.main_frame, font= ctk.CTkFont( size = 15 ), height = 100 )
        self.confirmationButtonIU = ctk.CTkButton( self.main_frame, text = "Enviar informacion", command = self.sendInfo )
        self.historyText.tag_config( "blue", foreground = "green" )
        self.historyText.tag_config( "orange", foreground = "orange" )
        self.historyText.tag_config( "yellow", foreground = "yellow" )

        self.root.mainloop( )

    def open_home( self ):
        self.hideComponents( )
        lblWelcome = ctk.CTkLabel( self.main_frame, text= "Bienvenido a S", font=( "Bold", 40 ) )
        lblWelcome.pack( pady = 200 )

    def open_setUpActions( self ):
        self.hideComponents( )
        lblTitleOfSUA = ctk.CTkLabel( self.main_frame, text="Set-Up Actions", font=( "Bold", 40 ) )
        lblTitleOfSUA.pack( pady = 40 )

        value = 1
        for rb in self.radioButtons:
            rbn = ctk.CTkRadioButton( self.main_frame, text = rb, variable = self.radioButtonOption, value = value, command= self.clickRadiobuttons )
            value=value+1
            rbn.pack( pady = 10 )
        self.lblOfRB.pack( pady = 20 )

    def clickRadiobuttons( self ):
        global previousRadioButtonOption
        msg = "Default"
        if self.radioButtonOption.get( ) == 1:
            msg = "Ingresa los parámetros de la orden que quieres crear"
        if self.radioButtonOption.get( ) == 2:
            msg = "Ingresa los parámetros de los usuarios que quieres crear"
        if self.radioButtonOption.get( ) == 3:
            msg = "Ingresa los parámetros de los productos que quieres crear"
        self.lblOfRB.configure( text = msg, font=( "Bold", 15 ) )
        if not self.textBox.winfo_ismapped( ):
            self.textBox.pack( )
            confirmationButton = ctk.CTkButton( self.main_frame, text="Confirmar", command = self.clickConfirmButton )
            confirmationButton.pack( pady = 20 )
        elif previousRadioButtonOption != -1:
            for lbl in self.dictOflblParameters[ previousRadioButtonOption ]:
                lbl.pack_forget( )
            for lbl in self.dictOflblParameters[ self.radioButtonOption.get( ) ]:
                lbl.pack( )
        previousRadioButtonOption = self.radioButtonOption.get( )

    def clickConfirmButton( self ):
        if self.textBox.get( ) != "":
            lbl = ctk.CTkLabel( self.main_frame, text = self.textBox.get( ) )
            self.dictOflblParameters[ self.radioButtonOption.get( ) ].append( lbl )
            lbl.pack( )
            self.textBox.delete(0, 'end')

    def open_inputUser( self ):
        self.hideComponents( )
        lblTitleOfIU = ctk.CTkLabel( self.main_frame, text="Input Cliente", font=( "Bold", 40 ) )
        lblTitleOfIU.pack( pady = 10 )
        self.historyText.pack(fill="x", padx=50 )
        self.inputText.pack( pady=10, fill="x", padx=50 )
        self.confirmationButtonIU.pack( )
        if len( self.historyText.get( "1.0", 'end-1c' ) ) == 0: 
            self.historyText.configure( state='normal' )
            self.historyText.insert( "end", text="S: ", tags="orange")
            self.historyText.insert( "end", self.WELCOME_MESSAGE )

    def sendInfo( self ):
        if self.isAIInitialized is not True: self.initializeAIandProducts( )
        userInput = self.inputText.get( "1.0", 'end-1c' )
        self.inputText.delete('1.0', 'end')
        self.historyText.configure( state='normal' )
        self.historyText.insert( "end", "Usuario: ", tags="blue")
        self.historyText.insert( "end", userInput + "\n\n" )
        response = self.askAI( userInput )
        self.historyText.insert( "end", text="S: ", tags="orange")
        self.historyText.insert( "end", response + "\n\n" )
        self.historyText.see( "end" )
        self.historyText.configure( state='disabled' )

    def initializeAIandProducts( self ):
        self.aIAssistant = AIAssistant( )
        self.isAIInitialized = True

    def askAI( self, userInput ):
        start_time = time.time()
        response = self.aIAssistant.askAI( userInput )
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Execution time: {execution_time} seconds")
        return response

    def hideComponents( self):
        for frame in self.main_frame.winfo_children( ):
            frame.pack_forget( )