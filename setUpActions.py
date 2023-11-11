import tkinter as tk


root = tk.Tk()
lblOfRB = tk.Label(root)
radioButtonOption = tk.IntVar()
textBox = tk.Entry(root)
confirmationButton = None
dictOflblParameters = {1: [], 2: [], 3: []}
previousRadioButtonOption = -1


#Methods
def createRadioButtons():
    radioButtons = ["Crear Órdenes","Crear Usuarios","Crear Productos"]
    value = 1
    for rb in radioButtons:
        rbn = tk.Radiobutton(root, text=rb, variable=radioButtonOption, value=value, command= lambda: clickRadiobuttons() )
        value=value+1
        rbn.pack()
    
def clickRadiobuttons( ):
    global previousRadioButtonOption
    msg = "Default"
    if radioButtonOption.get( ) == 1:
        msg = "Ingresa los parámetros de la orden que quieres crear"
    if radioButtonOption.get( ) == 2:
        msg = "Ingresa los parámetros de los usuarios que quieres crear"
    if radioButtonOption.get( ) == 3:
        msg = "Ingresa los parámetros de los productos que quieres crear"
    lblOfRB["text"]= msg
    if not textBox.winfo_ismapped( ):
        textBox.pack( )
        confirmationButton = tk.Button( root, text="Confirmar", command = clickButton )
        confirmationButton.pack( )
    elif previousRadioButtonOption != -1:
        for lbl in dictOflblParameters[ previousRadioButtonOption ]:
            lbl.pack_forget( )
        for lbl in dictOflblParameters[ radioButtonOption.get( ) ]:
            lbl.pack( )
    previousRadioButtonOption = radioButtonOption.get( )

        

def clickButton( ):
    if textBox.get( ) != "":
        lbl = tk.Label( text= textBox.get( ) )
        dictOflblParameters[ radioButtonOption.get( ) ].append( lbl )
        lbl.pack()
        textBox.delete(0, 'end')


def createLabel():
    lblOfRB.pack()

def main():
    
    root.title("Set-Up Actions")
    #root.geometry("300x200")
    
    createRadioButtons()
    createLabel()
    
    root.mainloop()
if __name__ == '__main__':
    main()
