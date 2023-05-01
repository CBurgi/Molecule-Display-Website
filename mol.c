#include "mol.h"
//make 17231 if stopping negative numbers
#define SHORT_MAX 65535


void nullMallocTest(const void *test){
    if(test == NULL){
        fprintf(stderr, " [Memory allocation failed.] \n");
        exit(-1);
    }
}

//Sets the atom's variables to the variables that element, x, y, and z point to.
void atomset( atom *atom, char element[3], double *x, double *y, double *z ){
    if(atom == NULL){
        puts(" [Cannot set variables of a NULL atom pointer.] ");
        return;
    }
    if(element == NULL){
        puts(" [Trying to assign NULL element to atom. Set to \"\"] ");
        strcpy(atom->element, "");
    }else strcpy(atom->element, element);
    if(x == NULL){
        puts(" [Trying to assign NULL x-position to atom. Set to 0] ");
        atom->x = 0;
    }else atom->x = *x;
    if(y == NULL){
        puts(" [Trying to assign NULL y-position to atom. Set to 0] ");
        atom->y = 0;
    }else atom->y = *y;
    if(z == NULL){
        puts(" [Trying to assign NULL z-position to atom. Set to 0] ");
        atom->z = 0;
    }else atom->z = *z;
}
//Sets the variables that element, x, y, and z point to to the atom's variables.
void atomget( atom *atom, char element[3], double *x, double *y, double *z ){
    char tempE[3] = "";
    double tempX = 0, tempY = 0, tempZ = 0;
    if(atom != NULL){
        strcpy(tempE, atom->element);
        tempX = atom->x;
        tempY = atom->y;
        tempZ = atom->z;
    }else puts(" [Trying to get variables of a NULL atom pointer. Element set to \"\", positions set to 0] ");
    if(element == NULL){
        puts(" [Cannot assign element name to NULL pointer.] ");
    }else strcpy(element, tempE);
    if(x == NULL){
        puts(" [Cannot assign x-position to NULL pointer.] ");
    }else *x = tempX;
    if(y == NULL){
        puts(" [Cannot assign y-position to NULL pointer.] ");
    }else *y = tempY;
    if(z == NULL){
        puts(" [Cannot assign z-position to NULL pointer.] ");
    }else *z = tempZ;
}

//Sets the bond's variables to the variables that a1, a2, and epairs point to.
void bondset( bond *bond, unsigned short *a1, unsigned short *a2, atom **atoms, unsigned char *epairs ){
    if(bond == NULL){
        puts(" [Cannot set variables of a NULL bond pointer.] ");
        return;
    }
    printf("test");
    bond->a1 = *a1;
    bond->a2 = *a2;
    bond->atoms = *atoms;
    bond->epairs = *epairs;

    compute_coords(bond);
}

//Sets the variables that a1, a2, and epairs point to to the bond's variables.
void bondget( bond *bond, unsigned short *a1, unsigned short *a2, atom **atoms, unsigned char *epairs ){
    if(bond == NULL){
        puts(" [Cannot get variables of a NULL bond pointer.] ");
        return;
    }
    *a1 = bond->a1;
    *a2 = bond->a2;
    *atoms = bond->atoms;
    *epairs = bond->epairs;
}

//computes the coords of the passed bond based on the atoms to which it is attached
void compute_coords(bond *bond){
    atom a1 = bond->atoms[bond->a1];
    atom a2 = bond->atoms[bond->a2];

    bond->x1 = a1.x;
    bond->x2 = a2.x;
    bond->y1 = a1.y;
    bond->y2 = a2.y;
    bond->z = (a1.z + a2.z)/2;
    bond->len = sqrt( (a2.x-a1.x)*(a2.x-a1.x) + (a2.y-a1.y)*(a2.y-a1.y));
    bond->dx = (a2.x - a1.x)/bond->len;
    bond->dy = (a2.y - a1.y)/bond->len;
}

//Allocates all the memory needed for a molecule with the passed number
//of max atoms and bonds.
molecule *molmalloc( unsigned short atom_max, unsigned short bond_max ){
    unsigned short tempAtomMax = 0, tempBondMax = 0;
    //make 34463 to stop negative numbers
    if(atom_max > SHORT_MAX){
        puts(" [Trying to set atom_max higher than variable type allows, set to 0.] ");
    }else tempAtomMax = atom_max;
    if(bond_max > SHORT_MAX){
        puts(" [Trying to set bond_max higher than variable type allows, set to 0.] ");
    }else tempBondMax = bond_max;

    molecule *temp = (molecule*)malloc(sizeof(molecule));
    nullMallocTest(temp);

    temp->atom_max = tempAtomMax;
    temp->atom_no = 0;
    temp->atoms = (atom*)malloc(sizeof(atom) * tempAtomMax);
    if(temp->atoms == NULL)return NULL;
    temp->atom_ptrs = (atom**)malloc(sizeof(atom*) * tempAtomMax);
    if(temp->atom_ptrs == NULL)return NULL;
    temp->bond_max = tempBondMax;
    temp->bond_no = 0;
    temp->bonds = (bond*)malloc(sizeof(bond) * tempBondMax);
    if(temp->bonds == NULL)return NULL;
    temp->bond_ptrs = (bond**)malloc(sizeof(bond*) * tempBondMax);
    if(temp->bond_ptrs == NULL)return NULL;

    return temp;
}

//Returns a molecule that is a copy of the passed molecule
molecule *molcopy( molecule *src ){
    //unsigned short tempAtomMax = 0, tempBondMax = 0;

    if(src == NULL){
        puts(" [Trying to copy a NULL molecule pointer, all values set to 0.] ");
        molecule *err = molmalloc(0, 0);
        if(err == NULL)return NULL;
        return err;
    }
    molecule *dest = molmalloc(src->atom_max, src->bond_max);
    if(dest == NULL)return NULL;

    for(int i=0; i<src->atom_no; i++){
        molappend_atom(dest, &src->atoms[i]);
    }
    for(int i=0; i<src->bond_no; i++){
        molappend_bond(dest, &src->bonds[i]);
    }

    return dest;
}

//Frees the memory of a molecule
//WARNING: Unlike real life, matter can be destroyed here
void molfree( molecule *ptr ){
    if(ptr == NULL){
        puts(" [Molecule is already empty.] ");
        return;
    }
    free(ptr->atoms);
    free(ptr->atom_ptrs);
    free(ptr->bonds);
    free(ptr->bond_ptrs);
    free(ptr);
}

//Appends the passed atom to the passed molecule.
//Allocates new memory to the molecule's list of atoms if necessary
void molappend_atom( molecule *mol, atom *new ){
    if(mol == NULL){
        puts(" [Cannot append atom to a NULL molecule pointer.] ");
        return;
    }
    if(new == NULL){
        puts(" [Cannot append a NULL atom pointer to molecule.] ");
        return;
    }
    for(int i = 0; i<mol->atom_no; i++){
        if(mol->atom_ptrs[i] == new){
            puts(" [This atom is already part of this molecule.] ");
            return;
        }
    }
    int atom_no = mol->atom_no;
    int atom_max = mol->atom_max;

    //reallocating memory if at max atoms for the molecule
    if(atom_no == atom_max){
        if(atom_max == SHORT_MAX){
            puts(" [This molecule has the max number of adams already.] ");
            return;
        }
        if(atom_max == 0){
            mol->atoms = (atom*)realloc(mol->atoms, sizeof(atom));
            nullMallocTest(mol->atoms);
            mol->atom_ptrs = (atom**)realloc(mol->atom_ptrs, sizeof(atom*));
            nullMallocTest(mol->atom_ptrs);
            mol->atom_max++;
        }else{
            if(mol->atom_max >= SHORT_MAX / 2){
                mol->atom_max = SHORT_MAX;
                mol->atoms = (atom*)realloc(mol->atoms, sizeof(atom) * SHORT_MAX);
                nullMallocTest(mol->atoms);
                mol->atom_ptrs = (atom**)realloc(mol->atom_ptrs, sizeof(atom*) * SHORT_MAX);
                nullMallocTest(mol->atom_ptrs);
            }else {
                mol->atom_max *= 2;
                mol->atoms = (atom*)realloc(mol->atoms, sizeof(atom) * atom_max *2);
                nullMallocTest(mol->atoms);
                mol->atom_ptrs = (atom**)realloc(mol->atom_ptrs, sizeof(atom*) * atom_max *2);
                nullMallocTest(mol->atom_ptrs);
            }
        }
        for(int i=0;i<atom_max;i++){
            mol->atom_ptrs[i] = &mol->atoms[i];
        }
    }

    mol->atoms[atom_no] = *new;
    mol->atom_ptrs[atom_no] = &mol->atoms[atom_no];
    //printf("%p, %i, %f\n",(void *)mol->atom_ptrs[atom_no], mol->atom_max, mol->atom_ptrs[atom_no]->z);
    mol->atom_no++;
}

//Appends the passed bond to the passed molecule.
//Allocates new memory to the molecule's list of bonds if necessary
void molappend_bond( molecule *mol, bond *new ){
    if(mol == NULL){
        puts(" [Cannot append bond to a NULL molecule pointer.] ");
        return;
    }
    if(new == NULL){
        puts(" [Cannot append a NULL bond pointer to molecule.] ");
        return;
    }
    // for(int i = 0; i<mol->bond_no; i++){
    //     if((mol->bond_ptrs[i]->a1 == new->a1 && mol->bond_ptrs[i]->a2 == new->a2)
    //         || (mol->bond_ptrs[i]->a1 == new->a2 && mol->bond_ptrs[i]->a2 == new->a1)){
    //             puts(" [There is already a bond connecting these 2 atoms.] ");
    //             return;
    //         }
    // }
    for(int i = 0; i<mol->bond_no; i++){
        if(mol->bond_ptrs[i] == new){
            puts(" [This bond is already part of this molecule.] ");
            return;
        }
    }
    int bond_no = mol->bond_no;
    int bond_max = mol->bond_max;

    //reallocating memory if at max bonds for the molecule
    if(bond_no == bond_max){
        if(bond_max == SHORT_MAX){
            puts(" [This molecule has the max number of bonds already.] ");
            return;
        }
        if(bond_max == 0){
            mol->bonds = (bond*)realloc(mol->bonds, sizeof(bond));
            nullMallocTest(mol->bonds);
            mol->bond_ptrs = (bond**)realloc(mol->bond_ptrs, sizeof(bond*));
            nullMallocTest(mol->bond_ptrs);
            mol->bond_max++;
        }else{
            if(mol->bond_max >= SHORT_MAX / 2){
                mol->bond_max = SHORT_MAX;
                mol->bonds = (bond*)realloc(mol->bonds, sizeof(bond) * SHORT_MAX);
                nullMallocTest(mol->bonds);
                mol->bond_ptrs = (bond**)realloc(mol->bond_ptrs, sizeof(bond*) * SHORT_MAX);
                nullMallocTest(mol->bond_ptrs);
            }else {
                mol->bond_max *= 2;
                mol->bonds = (bond*)realloc(mol->bonds, sizeof(bond) * bond_max *2);
                nullMallocTest(mol->bonds);
                mol->bond_ptrs = (bond**)realloc(mol->bond_ptrs, sizeof(bond*) * bond_max *2);
                nullMallocTest(mol->bond_ptrs);
            }
        }
        for(int i=0;i<bond_max;i++){
            mol->bond_ptrs[i] = &mol->bonds[i];
        }
    }

    mol->bonds[mol->bond_no] = *new;
    mol->bond_ptrs[mol->bond_no] = &mol->bonds[mol->bond_no];
    mol->bond_no++;
}

//Sorts the atoms and bonds in the passed molecule by
//z-value (lowest to highest)
void molsort( molecule *mol ){
    if(mol == NULL){
        puts(" [Cannot sort a NULL molecule pointer.] ");
        return;
    }
    if(mol->atom_no == 0){
        puts(" [No atoms in molecule to sort.] ");
        return;
    }
    qsort(mol->atom_ptrs, mol->atom_no, sizeof(atom*), atom_comp);
    qsort(mol->bond_ptrs, mol->bond_no, sizeof(bond*), bond_comp);
}
int atom_comp( const void *a1, const  void *a2){
    atom *a1_ptr, *a2_ptr;

    a1_ptr = *(atom **)a1;
    a2_ptr = *(atom **)a2;

    return (a1_ptr->z > a2_ptr->z) - (a1_ptr->z < a2_ptr->z);
}
int bond_comp( const void *b1, const void *b2){
    bond *b1_ptr, *b2_ptr;

    b1_ptr = *(bond **)b1;
    b2_ptr = *(bond **)b2;

    return (b1_ptr->z > b2_ptr->z) - (b1_ptr->z < b2_ptr->z);
}

//Makes matrices for rotation transformations about all 3 axes
void xrotation( xform_matrix x_matrix, unsigned short deg ){
    if(x_matrix == NULL){
        puts(" [Cannot set rotation of a NULL xform_matrix pointer.] ");
        return;
    }
    double rad = deg * (M_PI / 180.0);
    x_matrix[0][0] = 1;
    x_matrix[0][1] = 0;
    x_matrix[0][2] = 0;
    x_matrix[1][0] = 0;
    x_matrix[1][1] = cos(rad);
    x_matrix[1][2] = 0-sin(rad);
    x_matrix[2][0] = 0;
    x_matrix[2][1] = sin(rad);
    x_matrix[2][2] = cos(rad);
}
void yrotation( xform_matrix y_matrix, unsigned short deg ){
    if(y_matrix == NULL){
        puts(" [Cannot set rotation of a NULL xform_matrix pointer.] ");
        return;
    }
    double rad = deg * (M_PI / 180.0);
    y_matrix[0][0] = cos(rad);
    y_matrix[0][1] = 0;
    y_matrix[0][2] = sin(rad);
    y_matrix[1][0] = 0;
    y_matrix[1][1] = 1;
    y_matrix[1][2] = 0;
    y_matrix[2][0] = 0-sin(rad);
    y_matrix[2][1] = 0;
    y_matrix[2][2] = cos(rad);
}
void zrotation( xform_matrix z_matrix, unsigned short deg ){
    if(z_matrix == NULL){
        puts(" [Cannot set rotation of a NULL xform_matrix pointer.] ");
        return;
    }
    double rad = deg * (M_PI / 180.0);
    z_matrix[0][0] = cos(rad);
    z_matrix[0][1] = 0-sin(rad);
    z_matrix[0][2] = 0;
    z_matrix[1][0] = sin(rad);
    z_matrix[1][1] = cos(rad);
    z_matrix[1][2] = 0;
    z_matrix[2][0] = 0;
    z_matrix[2][1] = 0;
    z_matrix[2][2] = 1;
}

//Transforms a molecule using the passed matrix
void mol_xform( molecule *mol, xform_matrix matrix ){
    if(mol == NULL){
        puts(" [Cannot rotate a NULL molecule pointer.] ");
        return;
    }
    if(matrix == NULL){
        puts(" [Cannot rotate molecule using a NULL xform_matrix pointer.] ");
        return;
    }
    atom *a_ptr = mol->atoms;
    double newX, newY, newZ;
    for(int i=0; i<mol->atom_no; i++){
        newX = (a_ptr+i)->x * matrix[0][0] + (a_ptr+i)->y * matrix[0][1] + (a_ptr+i)->z * matrix[0][2];
        newY = (a_ptr+i)->x * matrix[1][0] + (a_ptr+i)->y * matrix[1][1] + (a_ptr+i)->z * matrix[1][2];
        newZ = (a_ptr+i)->x * matrix[2][0] + (a_ptr+i)->y * matrix[2][1] + (a_ptr+i)->z * matrix[2][2];
        (a_ptr+i)->x = newX;
        (a_ptr+i)->y = newY;
        (a_ptr+i)->z = newZ;
    }
    
    bond *b_ptr = mol->bonds;
    for (int i=0; i<mol->bond_no; i++){
        compute_coords(b_ptr+i);
    }
}
