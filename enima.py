# Comment fonctionne Enigma? On choisit parmis les rotors prédéfinis 3 rotors, il seront juxtaposés.
 # chaque rotor a l'alphabet placé random, et le rotor à droite tourne d'un cran à chaque lettre tapée.
 #le rotor à sa gauche tourne si le rotor à sa droite a effectué une rotation complète, et ainsi de suite pour le 3ème.
#On a aussi un plug board comme dans les enigmas de la marine, donc quand on a obtenu une lettre en output chiffrée, elle est recodée car elle est connectée à une autre (10 paires possibles)


alph = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ_.'

class Rotor:        
    def __init__(self,turnover,ordering):
        self.to = turnover
        self.order = ordering
        self.position = 'A'
        
    def setup(self,position):
        self.position = position
        for i in range(alph.index(self.position)):
            new_order = '{0}{1}'.format(self.order.split(self.order[0])[1],self.order[0])
            self.order = new_order
            new_new_order =''
            for element in self.order:
                new_new_order = '{0}{1}'.format(new_new_order,alph[alph.find(element)-1])
            self.order = new_new_order
        
    def step(self):
        new_order = '{0}{1}'.format(self.order.split(self.order[0])[1],self.order[0])
        self.order = new_order
        if alph.index(self.position)+1 < len(alph):
            self.position = alph[alph.index(self.position)+1]
        else:
            self.position = alph[0]
        new_new_order =''
        for element in self.order:
            new_new_order = '{0}{1}'.format(new_new_order,alph[alph.find(element)-1])
        self.order = new_new_order
        
    def fo_action(self,letter):
        pos = alph.find(letter)
        if pos == -1:
            print(letter,'Une lettre capitale on a dit!')
            return()
        else:
            return(self.order[pos])
        
    def re_action(self,letter):
        pos = self.order.find(letter)
        if pos == -1:
            print(letter,'Une lettre capitale on a dit!')
            return()
        else:
            return(alph[pos])

class Reflector:
    def __init__(self,ordering):
        self.order = ordering
    def action(self,letter):
        pos = alph.find(letter)
        if pos == -1:
            print(letter,'Une lettre capitale on a dit!')
            return()
        else:
            return(self.order[pos])

def make_rotors(rotors,start_pos):
    I =        Rotor(['R'],'EKMFLGDQV.ZNTOWYHXUSPA_IBRCJ')
    II =       Rotor(['F'],'AJDK_SIRUXBLHWTMCQGZ.NPYFVOE')
    III =      Rotor(['W'],'BDFHJLCPRTXV.ZNYEIWGAKMUSQO_')
    IV =       Rotor(['K'],'ESOVPZJ.AYQUIRHXLNFTGK_DCMWB')
    V =        Rotor(['A'],'VZBRGIT_YUPSDNHLX.AWMJQOFECK')
    VI =   Rotor(['A','N'],'.JPGVOUM_FYQBENHZRDKASXLICTW')
    VII =  Rotor(['A','N'],'NZJHGRC_XMYSWBOUFAIV.LPEKQDT')
    VIII = Rotor(['A','N'],'FK_Q.HTLXOCBJSPDZRAMEWNIUYGV')
    reflector =  Reflector('EJMZALYXVBWFCRQUONTSPIKHGD._')
    left = locals()[rotors[0]]
    mid = locals()[rotors[1]]
    right = locals()[rotors[2]]
    left.setup(start_pos[0])
    mid.setup(start_pos[1])
    right.setup(start_pos[2])
    #print(len(left.order),len(mid.order),len(right.order),len(reflector.order))
    return(reflector,left,mid,right)

def get_setup():
    r = input("Donner 3 rotors qui seront disposés de gauche à droite parmis les choix: I II III IV V VI VII VIII.(par exemple, II I IV fait que II est le rotor de gauche): ")
    rotors = r.split()
    while len(rotors) != 3 or len(set(rotors)) != len(rotors) :
        r = input("Raté! Choisis bien 3 rotors et METS DES ESPACES ENTRE: ")
        rotors = r.split()
        
    s = input("Maintenant, ça serait cool si tu donnais la position des rotors(leur lettre de commencement).Par exemple, tu peux mettre D K Y: ")
    start_pos = s.split()
    while len(start_pos) != 3:
        s = input("Raté! Choisis bien les positions et METS DES ESPACES ENTRE: ")
        start_pos = s.split()
    p = input("Bienvenue sur le plug board! Choisis 10 lettres à connecter: par exemple A-D B-H K-Z créera ces 3 combinaisons: ")
    pairs = p.split()
    letters = []
    for element in pairs:
        letters.extend(element.split('-'))
    while len(pairs) > 10 or len(letters) != len(set(letters)):
        letters = []
        p = input("Raté! Choisis bien les 10 combos et METS DES ESPACES ENTRE: ")
        pairs = p.split()
        for element in pairs:
            letters.extend(element.split('-')) 
    pairs = []
    return(rotors,start_pos,pairs)


def main(): #quand on appuie sur une touche ça fait tourner le(s) rotor(s) et ça envoie un signal au plugboard de faire passer la lettre dans les rotors. Puis on envoie ça au réflector pour retourner dans les rotors. Finalement, il y a le terme chiffré.
    rotors,start_pos,pairs = get_setup()
    message = ''
    while message != 'OVER':
        reflector,left,mid,right =  make_rotors(rotors,start_pos)
        message = input('Entre ton message ENTIEREMENT AVEC DES LETTRES CAPITALES. Pour faire des espaces, utilise _ (et afin de stopper le programme écrit juste OVER): ') 
        output = ''
        for letter in message:
            if mid.position in mid.to:
                left.step()
                mid.step()
            if right.position in right.to:
                mid.step()
            right.step()
            letter = plugboard(letter,pairs)
            letter = (right.fo_action(letter))
            letter = (mid.fo_action(letter))
            letter = (left.fo_action(letter))
            letter = (reflector.action(letter))
            letter = (left.re_action(letter))
            letter = (mid.re_action(letter))
            letter = (right.re_action(letter))
            letter = plugboard(letter,pairs)
            output = '{0}{1}'.format(output,letter)
        print(output)
    return()

def plugboard(letter,pairs):
    for pair in pairs:
        if letter == pair.split('-')[0]:
            letter = pair.split('-')[1]
        elif letter == pair.split('-')[1]:
            letter = pair.split('-')[0]
    return(letter)

main()

#E-R T-Y U-I O-P Q-S D-F G-H J-K L-M W-X