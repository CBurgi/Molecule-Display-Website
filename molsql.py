import os;
import sqlite3;
import MolDisplay;

tableNames = {
    'Elements'      :   'ELEMENT_NO, ELEMENT_CODE, ELEMENT_NAME, COLOUR1, COLOUR2, COLOUR3, RADIUS',
    'Atoms'         :   'ELEMENT_CODE, X, Y, Z',
    'Bonds'         :   'A1, A2, EPAIRS',
    'Molecules'     :   'NAME',
    'MoleculeAtom'  :   'MOLECULE_ID, ATOM_ID',
    'MoleculeBond'  :   'MOLECULE_ID, BOND_ID'
}

class Database:
    def __init__(self, reset = False):
        if os.path.exists( 'molecules.db' ) and reset == True:
            os.remove( 'molecules.db' )

        self.conn = sqlite3.connect( 'molecules.db' );
    
    # creates all the tables in our database
    def create_tables(self):

        self.conn.execute( """CREATE TABLE IF NOT EXISTS Elements 
                              ( ELEMENT_NO       INTEGER        NOT NULL,
                                ELEMENT_CODE     VARCHAR(3)     NOT NULL,
                                ELEMENT_NAME     VARCHAR(32)    NOT NULL,
                                COLOUR1          CHAR(6)        NOT NULL,
                                COLOUR2          CHAR(6)        NOT NULL,
                                COLOUR3          CHAR(6)        NOT NULL,
                                RADIUS           DECIMAL(3)     NOT NULL,
                                PRIMARY KEY (ELEMENT_CODE) );""" )

        self.conn.execute( """CREATE TABLE IF NOT EXISTS Atoms
                              ( ATOM_ID         INTEGER         NOT NULL    PRIMARY KEY,
                                ELEMENT_CODE    VARCHAR(3)      NOT NULL,
                                X               DECIMAL(7, 4)   NOT NULL,
                                Y               DECIMAL(7, 4)   NOT NULL,
                                Z               DECIMAL(7, 4)   NOT NULL,
                                FOREIGN KEY (ELEMENT_CODE) REFERENCES Elements);""" )

        self.conn.execute( """CREATE TABLE IF NOT EXISTS Bonds
                              ( BOND_ID  INTEGER       NOT NULL    PRIMARY KEY,
                                A1       INTEGER       NOT NULL,
                                A2       INTEGER       NOT NULL,
                                EPAIRS   INTEGER       NOT NULL );""" )

        self.conn.execute( """CREATE TABLE  IF NOT EXISTS Molecules
                              ( MOLECULE_ID     INTEGER     NOT NULL    PRIMARY KEY,
                                NAME            TEXT        NOT NULL    UNIQUE);""" )

        self.conn.execute( """CREATE TABLE IF NOT EXISTS MoleculeAtom
                              ( MOLECULE_ID     INTEGER     NOT NULL,
                                ATOM_ID         INTEGER     NOT NULL,
                                PRIMARY KEY (MOLECULE_ID, ATOM_ID),
                                FOREIGN KEY (MOLECULE_ID) REFERENCES Molecules,
                                FOREIGN KEY (ATOM_ID) REFERENCES Atoms );""" )
        
        self.conn.execute( """CREATE TABLE IF NOT EXISTS MoleculeBond
                              ( MOLECULE_ID     INTEGER     NOT NULL,
                                BOND_ID         INTEGER     NOT NULL,
                                PRIMARY KEY (MOLECULE_ID, BOND_ID),
                                FOREIGN KEY (MOLECULE_ID) REFERENCES Molecules,
                                FOREIGN KEY (BOND_ID) REFERENCES Bonds );""" )
        self.conn.commit()
    
    # inserts the passed values into the passed table
    def __setitem__(self, table, values):
        if (table == 'Molecules'):
            valString = "(?)"
            query = f"INSERT INTO {table}({tableNames[table]}) VALUES {valString}"
            self.conn.execute(query, (values,))
        else:
            valString = "(" + ",".join("?" for i in range(len(values))) + ")"
            query = f"INSERT INTO {table}({tableNames[table]}) VALUES {valString}"
            self.conn.execute(query, values)
        self.conn.commit()

    def delete_element(self, eleno, elecode, elename, col1, col2, col3, rad):
        deleted = False

        values = (eleno, elecode, elename, col1, col2, col3, rad)
        test = self.conn.execute("""SELECT ELEMENT_CODE
                            FROM    Elements
                            WHERE   ELEMENT_NO    =   ?
                            AND     ELEMENT_CODE    =   ?
                            AND     ELEMENT_NAME    =   ?
                            AND     COLOUR1    =   ?
                            AND     COLOUR2    =   ?
                            AND     COLOUR3    =   ?
                            AND     RADIUS    =   ?""", values).fetchone()
        
        if test:
            self.conn.execute("""DELETE FROM Elements
                                WHERE   ELEMENT_NO    =   ?
                                AND     ELEMENT_CODE    =   ?
                                AND     ELEMENT_NAME    =   ?
                                AND     COLOUR1    =   ?
                                AND     COLOUR2    =   ?
                                AND     COLOUR3    =   ?
                                AND     RADIUS    =   ?""", values)
            deleted = True
        
        self.conn.commit()
        return deleted

    
    # add an atom to our database
    # adds passed atom's (MolDisplay.Atom) attrebutes to the Atoms table
    # adds entry to MoleculeAtom table that links passed molecule to atom
    def add_atom(self, molname, atom):
        values = (atom.atom.element, atom.atom.x, atom.atom.y, atom.atom.z)
        self.__setitem__('Atoms', values)
        atom_id = self.conn.execute("""SELECT    ATOM_ID
                                    FROM        Atoms   
                                    WHERE       ELEMENT_CODE    = ?
                                    AND         X               = ?
                                    AND         Y               = ?
                                    AND         Z               = ?""", values).fetchone()[0]
        
        
        mol_id = self.conn.execute("""SELECT     MOLECULE_ID
                                    FROM        Molecules
                                    WHERE       NAME       = ?""", (molname,)).fetchone()[0]

        IDs = (mol_id, atom_id)

        self.conn.execute("""INSERT  INTO    MoleculeAtom(MOLECULE_ID, ATOM_ID)
                                    VALUES  (?,?)""", IDs)
        
        self.conn.commit()


    # add a bond to our database
    # adds passed bond's (MolDisplay.Bond) attrebutes to the Bonds table
    # adds entry to MoleculeBond table that links passed molecule to bond
    def add_bond(self, molname, bond):
        values = (bond.bond.a1, bond.bond.a2, bond.bond.epairs)
        self.__setitem__('Bonds', values)
        bond_id = self.conn.execute("""SELECT    BOND_ID
                                    FROM        Bonds
                                    WHERE       A1      = ?
                                    AND         A2      = ?
                                    AND         EPAIRS  = ?""", values).fetchone()[0]
        
        mol_id = self.conn.execute("""SELECT     MOLECULE_ID
                                    FROM        Molecules
                                    WHERE       NAME       = ?""", (molname,)).fetchone()[0]

        IDs = (mol_id, bond_id)
        
        self.conn.execute("""INSERT  INTO    MoleculeBond(MOLECULE_ID, BOND_ID)
                                    VALUES  (?,?)""", IDs)
        
        self.conn.commit()
    
    # creates a molecule based on the passed stf file and gives it the passed name
    # adds created molecule to our database including all atoms and bonds
    def add_molecule(self, name, fp):
        mol = MolDisplay.Molecule()
        mol.parse(fp)

        self.conn.execute("""INSERT  INTO    Molecules(NAME)
                                    VALUES  (?)""", (name,))
    
        for a in range(mol.atom_no):
            tempAtom = MolDisplay.Atom(mol.get_atom(a))
            self.add_atom(name, tempAtom)
        
        for b in range(mol.bond_no):
            tempBond = MolDisplay.Bond(mol.get_bond(b))
            self.add_bond(name, tempBond)

        self.conn.commit()
    
    # returns a molecule (MolDisplay.Molecule) that has all the values of the molecule
    # in our database that has the passed name
    # atoms and bonds in the molecule are ordered by their id's in our database
    def load_mol(self, name):
        mol = MolDisplay.Molecule()

        atoms = self.conn.execute("""SELECT     ELEMENT_CODE, X, Y, Z
                                    FROM        Atoms, MoleculeAtom, Molecules
                                    WHERE       (Atoms.ATOM_ID = MoleculeAtom.ATOM_ID
                                    AND         MoleculeAtom.MOLECULE_ID = Molecules.MOLECULE_ID
                                    AND         Molecules.NAME = ?)
                                    ORDER BY    Atoms.ATOM_ID ASC""", (name,)).fetchall()
        for a in atoms:
            mol.append_atom(a[0], a[1], a[2], a[3])
        
        bonds = self.conn.execute("""SELECT     A1, A2, EPAIRS
                                    FROM        Bonds, MoleculeBond, Molecules
                                    WHERE       (Bonds.BOND_ID = MoleculeBond.BOND_ID
                                    AND         MoleculeBond.MOLECULE_ID = Molecules.MOLECULE_ID
                                    AND         Molecules.NAME = ?)
                                    ORDER BY    Bonds.BOND_ID ASC""", (name,)).fetchall()
        for b in bonds:
            mol.append_bond(b[0], b[1], b[2])
        
        return mol
    
    # returns a list of molecule names based on our database
    def getMolNames(self):
        names = self.conn.execute("""SELECT     NAME
                            FROM        MOLECULES""").fetchall()
        return names

    # returns a dictionary of element codes and their radii based on our database
    def radius(self):
        eleRads = self.conn.execute("""SELECT   ELEMENT_CODE, RADIUS
                                        FROM    Elements""").fetchall()
        return dict(eleRads)
        
    
    # returns a dictionary of element codes and their names based on our database
    def element_name(self):
        eleNames = self.conn.execute("""SELECT   ELEMENT_CODE, ELEMENT_NAME
                                        FROM    Elements""").fetchall()
        return dict(eleNames)

    # returns svg code that dictated the gradients of the circles of all the atoms in our database
    def radial_gradients(self):
        string = """"""

        eleGrades = self.conn.execute("""SELECT   ELEMENT_NAME, COLOUR1, COLOUR2, COLOUR3
                                        FROM    Elements""").fetchall()
        
        for e in eleGrades:
            string += """<radialGradient id="%s" cx="-50%%" cy="-50%%" r="220%%" fx="20%%" fy="20%%">
    <stop offset="0%%" stop-color="#%s"/>
    <stop offset="50%%" stop-color="#%s"/>
    <stop offset="100%%" stop-color="#%s"/>
</radialGradient>\n""" % (e[0], e[1], e[2], e[3])
        
        # for default element
        string += """<radialGradient id="Default" cx="-50%" cy="-50%" r="220%" fx="20%" fy="20%">
    <stop offset="0%" stop-color="#808080"/>
    <stop offset="50%" stop-color="#0f0f0f"/>
    <stop offset="100%" stop-color="#020202"/>
</radialGradient>\n"""
        return string


if __name__ == "__main__":
    db = Database();
    # db = Database(reset=True);
    # db.create_tables();
    # db['Elements'] = ( 1, 'H', 'Hydrogen', 'FFFFFF', '050505', '020202', 25 );
    # db['Elements'] = ( 6, 'C', 'Carbon', '808080', '010101', '000000', 40 );
    # db['Elements'] = ( 7, 'N', 'Nitrogen', '0000FF', '000005', '000002', 40 );
    # db['Elements'] = ( 8, 'O', 'Oxygen', 'FF0000', '050000', '020000', 40 );
    # fp = open( 'water-3D-structure-CT1000292221.sdf' );
    # db.add_molecule( 'Water', fp );
    # fp = open( 'caffeine-3D-structure-CT1001987571.sdf' );
    # db.add_molecule( 'Caffeine', fp );
    # fp = open( 'CID_31260.sdf' );
    # db.add_molecule( 'Isopentanol', fp );
    MolDisplay.radius = db.radius();
    MolDisplay.element_name = db.element_name();
    MolDisplay.header += db.radial_gradients();
    for molecule in [ 'Water', 'Caffeine', 'Isopentanol' ]:
        print("Printing " + molecule)
        mol = db.load_mol( molecule );
        mol.sort();
        fp = open( molecule + ".svg", "w" );
        fp.write( mol.svg() );
        fp.close();