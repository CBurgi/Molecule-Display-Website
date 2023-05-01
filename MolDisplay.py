import molecule;

# radius = {
#     'H': 25,
#     'C': 40,
#     'O': 40,
#     'N': 40,
# }

# element_name = {
#     'H': 'grey',
#     'C': 'black',
#     'O': 'red',
#     'N': 'blue',
# }

header = """<svg version="1.1" width="1000" height="1000" xmlns="http://www.w3.org/2000/svg">"""
footer = """</svg>"""
offsetx = 500
offsety = 500

class Atom:
    def __init__(self, atom):
        self.atom = atom
        self.z = atom.z
    
    def __str__(self) -> str:
        return '''element [%s]: x=%f, y=%f, z=%f''' % (self.atom.element, self.atom.x, self.atom.y, self.z,)
    
    # returns svg code for creating the circle that will represent the atom
    def svg(self):
        for e_code, e_name  in element_name.items():
            if e_code == self.atom.element:
                return '  <circle cx="%.2f" cy="%.2f" r="%d" fill="url(#%s)"/>\n' % (offsetx + 100*self.atom.x, offsety + 100*self.atom.y, radius[self.atom.element], element_name[self.atom.element])
        return '  <circle cx="%.2f" cy="%.2f" r="%d" fill="url(#%s)"/>\n' % (offsetx + 100*self.atom.x, offsety + 100*self.atom.y, 32, "Default")
    
class Bond:
    def __init__(self, bond):
        self.bond = bond
        self.z = bond.z

    def __str__(self) -> str:
        return '''bond [%d - %d]: x1=%f, x2=%f, y1 = %f, y2 = %f, z=%f, epairs=%d''' % (self.bond.a1, self.bond.a2, self.bond.x1, self.bond.x2, self.bond.y1, self.bond.y2, self.z, self.bond.epairs)
    
    # returns the svg code for creating a rectangle that will represent the bond
    def svg(self):
        return '  <polygon points="%.2f,%.2f %.2f,%.2f %.2f,%.2f %.2f,%.2f" fill="green"/>\n' % (offsetx + 100*self.bond.x1 - self.bond.dy*10, offsety + 100*self.bond.y1 + self.bond.dx*10, offsetx + 100*self.bond.x1 + self.bond.dy*10, offsety + 100*self.bond.y1 - self.bond.dx*10, offsetx + 100*self.bond.x2 + self.bond.dy*10, offsety + 100*self.bond.y2 - self.bond.dx*10, offsetx + 100*self.bond.x2 - self.bond.dy*10, offsety + 100*self.bond.y2 + self.bond.dx*10, )
    
class Molecule (molecule.molecule):
    def __str__(self) -> str:
        ret = ""
        for a in range(self.atom_no):
            ret += str(Atom(self.get_atom(a))) +'\n'
        for b in range(self.bond_no):
            ret += str(Bond(self.get_bond(b))) + '\n'
        
        return ret
    
    # returns the svg code for creating all the atoms and bonds in the molecule
    # the code will be created using assending z-values
    def svg(self):
        ret = header
        a1 = Atom(self.get_atom(0))
        b1 = Bond(self.get_bond(0))
        a = 1
        b = 1
        while a <= self.atom_no or b <= self.bond_no:
            if a <= self.atom_no and b <= self.bond_no:
                if a1.z < b1.z:
                    ret += a1.svg()
                    if a < self.atom_no:
                        a1 = Atom(self.get_atom(a))
                    a += 1
                else:
                    ret += b1.svg()
                    if b < self.bond_no:
                        b1 = Bond(self.get_bond(b))
                    b += 1
            elif a <= self.atom_no:
                ret += a1.svg()
                if a < self.atom_no:
                    a1 = Atom(self.get_atom(a))
                a += 1
            else:
                ret += b1.svg()
                if b < self.bond_no:
                    b1 = Bond(self.get_bond(b))
                b += 1
        ret += footer

        return ret
    
    # creates all the atoms and bonds in the molecule based on a passed sdf file
    def parse(self, f):
        for i in range(3):
            next(f)
        l1 = next(f).split()
        a_max = int(l1[0])
        b_max = int(l1[1])
        for a in range(a_max):
            line = next(f).split()
            a_x, a_y, a_z = [float(line[x]) for x in range(3)]
            a_element = str(line[3])
            self.append_atom(a_element, a_x, a_y, a_z)
        for b in range(b_max):
            line = next(f).split()
            a1, a2, epairs = [int(line[x]) for x in range(3)]
            a1 = a1-1
            a2 = a2-1
            self.append_bond(a1, a2, epairs)
        
if __name__=="__main__":
    mol = Molecule()

    # mol.append_atom('H', 4, 5, 6)
    # mol.append_atom('O', 1, 2, 3)
    # mol.append_bond(1, 2, 2)
    # mol.sort()

    f = open("caffeine-3D-structure-CT1001987571.sdf", "r")
    mol.parse(f)    
    mol.sort()

    print(mol)
    print(mol.svg())