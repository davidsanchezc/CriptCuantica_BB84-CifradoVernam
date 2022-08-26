import tkinter as tk
from PIL import Image, ImageTk 
from channel import *

class System:
    def __init__(self):
        #channel handles Alice, Bob, and Eve
        self.channel = None
        #information about the current state of the simulation
        self.currentStep = 0
        self.number_of_error_steps = 0
        self.phase = 0
        #storage of label objects
        self.phase1Objects = []
        self.phase2Objects = []
        self.phase3Objects = []
        self.phase4Objects = []
        #helper variable for plotting
        self.two_values = []
        #set up tkinter window
        self.initializeTkinter()


    def go_to_next_phase(self):
        """prepares variables and menu for the upcoming phase"""
        #transmission and measurement of qubits
        if self.phase ==0:
            number = self.getNumber("probability")
            while number==None:
                number = self.getNumber("probability")
            self.channel = Channel(number)
            self.go_to_phase1(number)
        #key sifting
        elif self.phase ==1:
            self.go_to_phase2()  
        #calculation of error rate
        elif self.phase ==2:
            self.go_to_phase3()
        #error correction
        elif self.phase ==3:
            self.go_to_phase4()
        elif self.phase==4:
            self.go_to_phase5()
        self.phase += 1


    def simulate_one_cycle(self):
        """Alice generates one qubit, Bob (and possibly Eve) measures it,
        result is displayed in window"""
        plottingList = self.channel.simulate_one_cycle(self.currentStep)
        self.displaying(self.currentStep, plottingList)
        self.currentStep += 1

    def simulate_multiple_cycle(self):
        """Alice generates a by the user defined number of qubits, Bob (and 
        possibly Eve) measures it, results are displayed in window"""
        number = int(self.getNumber("int"))
        while number==None:
            number = self.getNumber("int")
        for i in range(number):
            self.simulate_one_cycle()
        

    def initializeTkinter(self):
        """Tkinter setup and preparation of the start-menu"""
        self.window = tk.Tk()
        self.window.title("Matemática Discreta: Protocolo BB84")
        self.window.geometry("1000x800+100+10")
        self.window.iconbitmap("Uni.ico")

        self.menu_frame = tk.Frame(master=self.window)
        self.menu_frame.grid(row=0, column =0)
        self.process_frame1 = tk.Frame(master=self.window)
        self.process_frame1.grid(row=0, column=1)
        self.process_frame = tk.Frame(master=self.process_frame1)
        self.process_frame.grid(row=1, column =1)
        self.phase_label = tk.Text(master = self.menu_frame, width=25, height=10)
        self.phase_label.grid(row=0, column = 0)
        self.phase_label.insert(tk.END, 'Bienvenido :D\nPor favor selecciona\nla tasa de espionaje\n - 0: sin espía\n - ]0,1]: con espía')
        self.entry_frame = tk.Frame(master=self.menu_frame, width=25, height=3)
        self.entry_frame.grid(row=3, column=0)
        self.main_label = tk.Label(master= self.entry_frame, text="Ingresar tasa de espionaje")
        self.main_label.grid(row=0,column=0)
        self.entry = tk.Entry(master=self.entry_frame)
        self.entry.grid(row=1,column=0)
        self.entrymsg = tk.Entry(self.entry_frame)
        self.empty_space = tk.Label(master = self.menu_frame, width=25, height=5)
        self.empty_space.grid(row=1, column=0)
        self.empty_space2 = tk.Label(master = self.menu_frame, width=25, height=5)
        self.empty_space2.grid(row=2, column=0)

        self.btnmsg = tk.Button(master=self.menu_frame,
                                text="Ingresar mensaje",
                                width=25,
                                height=5,
                                command=self.enter_msg)

        self.btn_3 = tk.Button(master=self.menu_frame,
                                   text="Comenzar",
                                   width=25,
                                   height=5,
                                   command = self.go_to_next_phase)
        self.btn_3.grid(row=4, column=0)

        self.btn_4 = tk.Button(master=self.menu_frame,
                               text="Salir",
                               width=25,
                               height=5,
                               command = self.window.destroy)
        self.btn_4.grid(row=5,column=0)

        self.window.mainloop()


    def getNumber(self, typeArgument):
        """returns number entered by the user, raises exceptions in invalid cases"""
        try:
            #get number
            number = float(self.entry.get())
            self.entry.delete(0,tk.END)
            try:
                #check if value ranges are respected
                if typeArgument=="probability" and (number<0 or number>1):
                    raise ValueError("Debe ingresar una probabilidad entre 0 y 1")
                elif typeArgument=="int" and number<=0:
                    raise ValueError("El número debe ser positivo")
                return number
            except ValueError:
                #tell user to reenter a valid number
                self.errorwindow = tk.Tk()
                label = tk.Label(master=self.errorwindow, text='Preste atención a los rangos de valores permitidos')
                label.grid(row=0, column=0)
                button = tk.Button(master=self.errorwindow, text="OK", width=15, 
                                   height=5, command = self.errorwindow.destroy)
                button.grid(row=1, column=0)
                return None
        except:
            #tell user to enter number
            self.errorwindow = tk.Tk()
            label = tk.Label(master=self.errorwindow, text='Debe ingresar un número')
            label.grid(row=0, column=0)
            button = tk.Button(master=self.errorwindow, text="OK", width=15, 
                               height=5, command = self.errorwindow.destroy )
            button.grid(row=1, column=0)
        

    def go_to_phase1(self, number):
        """displays menu and table layout for phase "transmission and measurement of qubits"""
        #prepare setup for efficient displaying of qubits
        if number >0:
            self.eavesdropper = True
            self.indexList = [0,1,4,5]
            self.eList = [2,3]
        else:
            self.indexList = [0,1,2,3]
            self.eList = []
            self.eavesdropper = False
            
        #setup table for dispaying of qubits
        self.bb84_label = tk.Label(master=self.process_frame1, text="PROTOCOLO BB84", height=3)
        self.bb84_label.grid(row=0, column=1)
        self.phase1_frame =tk.Frame(master=self.process_frame)
        self.phase1_frame.grid(row=0, column=0)

        label = tk.Label(self.phase1_frame, text='Alice', width = 10, height = 1)
        label.grid(row=0,column=0)
        label_b = tk.Label(self.phase1_frame, text='Bob', width = 10, height = 1)
        text = ["Bit", "Base", "Qubit"]
        if self.eavesdropper:
            label = tk.Label(self.phase1_frame, text='Eva', width = 10, height = 1)
            label.grid(row=3,column=0)
            label_b.grid(row=6,column=0)
            labels = text * 2
        else:
            label_b.grid(row=3,column =0)
            labels = text
        labels = labels + text
        for i in range(len(labels)):
            if i%3==2:
                h = 2
            else:
                h=1
            label = tk.Label(master=self.phase1_frame, text=labels[i], width = 10, height = h)
            label.grid(row = i, column = 1)
        #setup menu
        self.phase_label.delete(1.0, tk.END)
        self.phase_label.insert(tk.END,"Fase 1:\nTransmisión de qubits")
        self.empty_space.grid_forget()
        self.btn_1 = tk.Button(master=self.menu_frame,
                               text="Simular un qubit",
                               width=25,
                               height=5,
                               bg="grey",
                               fg="black",
                               command = self.simulate_one_cycle
                               )
        self.btn_1.grid(row=1,column=0)
        self.empty_space2.grid_forget()
        self.btn_2 = tk.Button(master=self.menu_frame,
                               text="Simular qubits",
                               width=25,
                               height=5,
                               command = self.simulate_multiple_cycle
                               )
        self.btn_2.grid(row=2,column=0)
        self.main_label['text']="Número de qubits"
        
        self.empty_space3 = tk.Label(master = self.entry_frame, width=25,
                                     height=3)
        self.btn_3['text']="Siguiente fase"
        self.btn_3.grid_forget()
        self.empty_space.grid(row=4,column=0)
            
    def go_to_phase2(self):
        """display menu for phase "key sifting" """
        self.phase_label.delete(1.0, tk.END)
        self.phase_label.insert(tk.END,'Fase 2:\nSeleccionar clave')
        self.btn_1['text'] = 'Comparar bases'
        self.btn_2.grid_remove()
        self.btn_3.grid_forget()
        self.empty_space2.grid(row=2, column=0)
        self.empty_space.grid(row=4, column =0)
        self.btn_1['command'] = self.compare_bases
        self.main_label.grid_forget()
        self.entry.grid_forget()
        self.empty_space3.grid(row=0, column=0)
        
    def go_to_phase3(self):
        """display menu for phase "calculation of error rate" """
        self.empty_space3.grid_forget()
        self.phase_label.delete(1.0, tk.END)
        self.phase_label.insert(tk.END,'Fase 3:\nTasa de error')
        self.btn_1['text'] = 'Calcular tasa de error'
        self.main_label['text'] = 'Elegir número de ejemplos'
        self.btn_1['command'] = self.error_rate
        self.entry.grid(row=1,column=0)
        self.main_label.grid(row=0, column=0)
        self.btn_3.grid_forget()
        self.empty_space.grid(row=4, column=0)


    def go_to_phase4(self):
        """display menu for phase "calculation of error rate" """
        self.phase_label.delete(1.0, tk.END)
        self.phase_label.insert(tk.END, 'Fase 4:\nObtención de la clave')
        self.main_label.grid_forget()
        self.entry.grid_forget()
        self.empty_space3.grid(row=0, column=0)
        self.empty_space2.grid_remove()
        self.btn_3.grid_forget()
        self.finish_routine()


    def go_to_phase5(self):
        self.empty_space3.grid_forget()
        self.phase_label.delete(1.0, tk.END)
        self.phase_label.insert(tk.END,'Fase 5:\nCifrado de Vernam\n(ingresar mensaje)')
        self.main_label['text'] = 'Escribir mensaje'
        self.btnmsg.grid(row=2, column=0)
        self.entrymsg.grid(row=1,column=0)
        self.main_label.grid(row=0, column=0)
        self.btn_3.grid_forget()
        self.empty_space.grid(row=4, column=0)


    def displaying(self, number, plottingList):
        """display the transmission and measurement of one qubit in the tkinter window"""
        objects = []
        rn=0
        images = 0
        for i in plottingList:
            if i[0]!=-1:
                label = tk.Label(master=self.phase1_frame, text=str(i[0]), width=2, height=1)
                label.grid(row=rn, column=2+number)
                objects.append(label)
                rn+=1
                if i[1]==0:
                    basis = '+'
                else:
                    basis = 'x'
                label2 = tk.Label(master=self.phase1_frame, text=basis, width=2, height=1)
                label2.grid(row=rn, column=2+number)
                objects.append(label2)
                rn+=1

                #if images!=len(plottingList)-1:
                name = str(i[0])+str(i[1])+'.png'
                load = Image.open(name)
                render = ImageTk.PhotoImage(load)
                img = tk.Label(master=self.phase1_frame, image=render)
                img.image = render
                img.grid(row=rn, column=2+number)
                rn+=1
                images+=1
            else:
                objects.append(None)
                objects.append(None)
                rn+=3
                images+=1
        self.phase1Objects.append(objects)

        if self.currentStep == 0:
            self.empty_space.grid_forget()
            self.btn_3.grid(row=4, column=0)


    def compare_bases(self):
        """perform the step key sifting and display the result"""
        for i in range(self.currentStep):
            #determine of bases are the same
            value = self.channel.compareBasis(i)
            #highlight in green if so
            if value:
                for n in self.indexList:
                    self.phase1Objects[i][n]['background']='green2'
                if self.eavesdropper:
                    if self.channel.compareBasisE(i):
                        for n in self.eList:
                            self.phase1Objects[i][n]['background']='pale green'
        #replace the bit arrays by the new ones
        self.channel.replaceKey()
        #display the new bit arrays
        self.phase2_frame = tk.Frame(master=self.process_frame)
        self.phase2_frame.grid(row=1,column=0)
        row_b = self.setUpNames(self.phase2_frame)
        offset =2
        tmp = []
        bitArray = self.channel.getBits()
        for n in range(len(bitArray[0])):
            for i in range(len(bitArray)):
                if bitArray[i][n] !=-1:
                    label = tk.Label(master=self.phase2_frame, text=str(bitArray[i][n]), width=2, height=1)
                    label.grid(row=1+i, column=offset+n)
                if len(bitArray)==2 or i!=1:
                    tmp.append(label)
            self.phase2Objects.append(tmp)
            tmp = []
        #display go-to-next-phase button
        self.empty_space.grid_forget()
        self.btn_3.grid(row=4, column=0)


    def setUpNames(self, frame):
        """displays the table header in a given frame"""
        label = tk.Label(master=frame, text="Clave Compartida",width = 15, height = 2)
        label.grid(row=0,column=1)
        label_a = tk.Label(master=frame, text='Alice',width = 10, height =1)
        label_a.grid(row=1,column=1)
        if self.eavesdropper:
            label_e = tk.Label(master=frame, text='Eva',width = 10, height =1)
            label_e.grid(row=2, column=1)
            row_b=3
        else:
            row_b=2
        label_b = tk.Label(master=frame, text='Bob',width = 10, height =1)
        label_b.grid(row=row_b, column=1)
        return row_b


    def error_rate(self):
        """calculates the error rate on a random subsample of the size that
        the user specified"""
        number = int(self.getNumber("int"))
        while number==None:
            number = self.getNumber("int")
        if number > self.channel.a.getArrayLength():
            number == self.channel.a.getArrayLength()-1
        #get subset for error calculation
        subset = self.channel.getSubset(number)

        counter = 0
        for i in subset:
            #display subset for calculation
            for label in self.phase2Objects[i]:
                label['background'] = 'orange'
            #count errors
            if self.channel.compareBit(i)==False:
                counter+=1
        #calculate error
        error=float(counter)/float(len(subset))

        #display results
        self.phase3_frame = tk.Frame(master=self.process_frame)
        self.phase3_frame.grid(row=2, column=0)
        error_label = tk.Label(master=self.phase3_frame, text = 'La tasa de error es ' + str(error) + '. Quieres abortar o continuar con el proceso?' )
        error_label.grid(row=0, column=0)
        self.button_frame = tk.Frame(master=self.phase3_frame)
        self.button_frame.grid(row=1, column=0)
        #give the user the choice to abort or to continue
        button_abort = tk.Button(master=self.button_frame, text = 'Abortar', command = self.abort)
        button_abort.grid(row=0, column=0)
        button_continue = tk.Button(master=self.button_frame, text = 'Continuar con el proceso', command = self.continue_postprocessing)
        button_continue.grid(row=0,column=1)


    def continue_postprocessing(self):
        """displays table after the error rate calculation"""
        self.channel.forgetIndices()
        self.button_frame.grid_forget()
        self.button_frame.destroy()
        frame = tk.Frame(master=self.process_frame)
        frame.grid(row=3,column=0)
        row_b = self.setUpNames(frame)
        offset = 2
        tmp = []
        self.key_alice = ''
        self.key_bob = ''
        bitArray = self.channel.getBits()
        for n in range(len(bitArray[0])):
            for i in range(len(bitArray)):
                if bitArray[i][n] !=-1:
                    if i == 0:
                        self.key_alice += str(bitArray[i][n])
                    if i == len(bitArray)-1:
                        self.key_bob += str(bitArray[i][n])
                    label = tk.Label(master=frame, text=str(bitArray[i][n]), width=2, height=1)
                    label.grid(row=1+i, column=offset+n)
                    # key = bitArray[i][n]
                    if len(bitArray)==2 or i!=1:
                        tmp.append(label)
            self.phase3Objects.append(tmp)
            tmp = []
        self.go_to_next_phase()


    def finish_routine(self):
        """prepares menu for restart and displays message about result"""
        self.empty_space.grid_forget()
        self.btn_1.grid_forget()
        self.btn_2.grid_forget()
        self.empty_space.grid(row=1, column=0)
        self.empty_space2.grid(row=2, column=0)
        self.btn_3.grid(row=4, column=0)
        frame = tk.Frame(master = self.process_frame)
        frame.grid(row=6, column=0)
        self.channel.replaceKey()


    def enter_msg(self):
        self.empty_space.grid(row=1, column=0)
        self.empty_space2.grid(row=2, column=0)
        self.btnmsg.grid_forget()
        self.entrymsg.grid_forget()
        self.main_label.grid_forget()

        self.phase_label.delete(1.0, tk.END)
        self.phase_label.insert(tk.END, 'Fase 6: Cifrado de Vernam (encriptación)')
        self.btn_2['text'] = 'Encriptar'
        self.btn_2['command'] = self.encrypted
        self.btn_2.grid(row=3, column=0)
        self.empty_space.grid(row=4, column=0)

        self.frame1 = tk.Frame(master=self.process_frame)
        self.frame1.grid(row=7, column=0)

        self.frame = tk.Frame(master=self.frame1)
        self.frame.grid(row=1, column=0)

        label = tk.Label(self.frame1, text="CIFRADO DE VERNAM", height=3)
        label.grid(row=0)

        label = tk.Label(self.frame, text="Mensaje enviado por Alice:\t\t")
        label.grid(row=1, column=0)
        #mensaje ingresado
        msg = self.entrymsg.get()
        label = tk.Label(self.frame, text=msg)
        label.grid(row=1, column=1)

        label = tk.Label(self.frame, text="Mensaje de Alice en binario:\t", height=2)
        label.grid(row=2, column=0)
        binstr =''
        #se convierte el mensaje a binario
        for i in range(len(msg)):
            binstr += format(ord(msg[i]), 'b')
            while len(binstr) % 8 != 0:
                binstr = binstr[:i*8] + '0' + binstr[i*8:i*8+8]
        self.msg = binstr
        label = tk.Label(self.frame, text=self.msg)
        label.grid(row=2, column=1)


    def encrypted(self):
        self.empty_space3.grid(row=0, column=0)
        self.empty_space3.grid(row=0, column=0)
        self.empty_space.grid(row=1, column=0)
        self.empty_space2.grid(row=2, column=0)
        self.btn_2.grid_forget()
        self.main_label.grid_forget()
        self.phase_label.delete(1.0, tk.END)
        self.phase_label.insert(tk.END, 'Fase 6: Cifrado de Vernam (desencriptación)')
        self.btn_2['text'] = 'Desencriptar'
        self.btn_2['command'] = self.decrypted
        self.btn_2.grid(row=4, column=0)

        label = tk.Label(self.frame, text="Clave de Alice redimensionada:\t")
        label.grid(row=3, column=0)
        #clave de Alice redimensionada al tamaño del mensaje
        self.key_alice = self.resizekey(self.msg, self.key_alice)
        label = tk.Label(self.frame, text=self.key_alice)
        label.grid(row=3, column=1)

        label = tk.Label(self.frame, text="Mensaje encriptado en binario:\t", height=2)
        label.grid(row=4, column=0)
        #mensaje encriptado en binario con la operación XOR
        self.encryp_msg = self.XOR(self.msg,self.key_alice)
        label = tk.Label(self.frame, text=self.encryp_msg)
        label.grid(row=4, column=1)

        label = tk.Label(self.frame, text="Mensaje encriptado:\t\t")
        label.grid(row=5, column=0)
        # mensaje final, si no hubo complicaciones debería ser igual al enviado
        self.encryp = ''.join(chr(int(self.encryp_msg[i * 8:i * 8 + 8], 2)) for i in range(len(self.encryp_msg) // 8))
        label = tk.Label(self.frame, text=self.encryp)
        label.grid(row=5, column=1)

    def decrypted(self):
        self.empty_space3.grid(row=0, column=0)
        self.empty_space3.grid(row=0, column=0)
        self.empty_space.grid(row=1, column=0)
        self.empty_space2.grid(row=2, column=0)
        self.btn_2.grid_forget()
        self.phase_label.delete(1.0, tk.END)
        self.main_label.grid_forget()
        self.btn_3['text'] = 'Reiniciar'
        self.btn_3['command'] = self.restart
        self.btn_3.grid(row=4, column=0)

        label = tk.Label(self.frame, text="Clave de Bob redimensionada:\t")
        label.grid(row=6, column=0)
        #clave de Bob redimensionada al tamaño del mensaje
        self.key_bob = self.resizekey(self.msg,self.key_bob)
        label = tk.Label(self.frame, text=self.key_bob)
        label.grid(row=6, column=1)

        label = tk.Label(self.frame, text="Mensaje en binario desencriptado:\t", height=2)
        label.grid(row=7, column=0)
        #mensaje desencriptado en binario con la operación XOR
        self.decryp_msg = self.XOR(self.encryp_msg, self.key_bob)
        label = tk.Label(self.frame, text=self.decryp_msg)
        label.grid(row=7, column=1)

        label = tk.Label(self.frame, text="Mensaje recibido por Bob:\t\t")
        label.grid(row=8, column=0)
        #mensaje final, si no hubo complicaciones debería ser igual al enviado
        self.msg = ''.join(chr(int(self.decryp_msg[i*8:i*8+8],2)) for i in range(len(self.decryp_msg)//8))
        label = tk.Label(self.frame, text=self.msg)
        label.grid(row=8, column=1)


    def resizekey(self, msg, key):
        n = len(msg)
        # si la clave y el mensaje son de diferente tamaño
        while len(key) != n:
            # si clave < mensaje, se repite la clave hasta que tengan el mismo tamaño
            if len(key) < n:
                key += key
            # si clave > mensaje, se acorta la clave hasta que tengan el mismo tamaño
            elif len(key) > n:
                key = key[:n]
        return key


    def XOR(self, msg, key):
        cryp = ''
        for i in range(len(msg)):
            if msg[i] == key[i]:
                cryp += '0'
            else:
                cryp += '1'
        return cryp


    def restart(self):
        """resets all necessary values and restarts tkinter"""
        self.window.destroy()
        self.channel = None
        self.currentStep = 0
        self.number_of_error_steps = 0
        self.phase = 0
        self.phase1Objects = []
        self.phase2Objects = []
        self.phase3Objects = []
        self.phase4Objects = []
        self.two_values = []
        self.initializeTkinter()


    def abort(self):
        """restarts program"""
        self.restart()