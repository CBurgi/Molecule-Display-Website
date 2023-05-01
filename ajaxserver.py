from http.server import HTTPServer, BaseHTTPRequestHandler;

import sys;     # to get command line argument for port
import urllib;  # code to parse for data
import io;

import molsql;
import MolDisplay

# list of files that we allow the web-server to serve to clients
# (we don't want to serve any file that the client requests)
public_files = [ '/', '/main.html', '/sdf_upload.html', '/style.css', '/script.js' ];

db = molsql.Database(reset = False)
# db = molsql.Database(reset = True)
# db.create_tables();
# db['Elements'] = ( 1, 'H', 'Hydrogen', 'FFFFFF', '050505', '020202', 25 );
# db['Elements'] = ( 6, 'C', 'Carbon', '808080', '010101', '000000', 40 );
# db['Elements'] = ( 7, 'N', 'Nitrogen', '0000FF', '000005', '000002', 40 );
# db['Elements'] = ( 8, 'O', 'Oxygen', 'FF0000', '050000', '020000', 40 );
MolDisplay.radius = db.radius()
MolDisplay.element_name = db.element_name()
MolDisplay.header += db.radial_gradients()

class MyHandler( BaseHTTPRequestHandler ):
    def do_GET(self):
        # used to GET a file from the list ov public_files, above
        if self.path in public_files:   # make sure it's a valid file
            self.send_response( 200 );  # OK
            self.send_header( "Content-type", "text/html" );

            if self.path == '/':
                fp = open('main.html')
            else: fp = open( self.path[1:] ); 
            # [1:] to remove leading / so that file is found in current dir

            # load the specified file
            page = fp.read();
            fp.close();

            # adding all molecules in database to "Display Molecule" select
            temp = 'a'
            if self.path == '/script.js':
                page += addMolecules
                molNames = db.getMolNames()
                for s in molNames:
                    page += moleculeA % (temp, temp, s[0], temp)
                    temp += 'a'
                page += '}'

            # create and send headers
            self.send_header( "Content-length", len(page) );
            self.end_headers();

            # send the contents
            self.wfile.write( bytes( page, "utf-8" ) );

        else:
            # if the requested URL is not one of the public_files
            self.send_response( 404 );
            self.end_headers();
            self.wfile.write( bytes( "404: not found", "utf-8" ) );

    def do_POST(self):
        # For when the main page is reloaded (see display.html)
        if self.path =="/main.html":
            self.send_response( 200 );  # OK
            self.send_header( "Content-type", "text/html" );
            fp = open('main.html')
            page = fp.read();
            fp.close();
            temp = 'a'
            if self.path == '/script.js':
                page += addMolecules
                molNames = db.getMolNames()
                for s in molNames:
                    page += moleculeA % (temp, temp, s[0], temp)
                    temp += 'a'
                page += '}'

            # create and send headers
            self.send_header( "Content-length", len(page) );
            self.end_headers();

            # send the contents
            self.wfile.write( bytes( page, "utf-8" ) );

        # For adding elements
        elif self.path == "/element_add.html":
            message = "was added to database."

            content_length = int(self.headers['Content-Length']);
            body = self.rfile.read(content_length);
            postvars = urllib.parse.parse_qs( body.decode( 'utf-8' ) );
            values = (postvars['element_no'][0], postvars['element_code'][0], postvars['element_name'][0], 
                      str(postvars['colour1'])[3:-2], str(postvars['colour2'])[3:-2], str(postvars['colour3'])[3:-2], 
                      postvars['radius'][0])
            
            exising_elements = db.element_name()

            exists = False
            for e_code, e_name  in exising_elements.items():
                if e_code == values[1]:
                    message = "was not added to database.\nAn element with that code already exists."
                    exists = True
                    break

            if not exists:
                db['Elements'] = values

            self.send_response( 200 ); # OK
            self.send_header( "Content-type", "text/plain" );
            self.send_header( "Content-length", len(message) );
            self.end_headers();

            self.wfile.write( bytes( message, "utf-8" ) );
        
        # For deleting elements
        elif self.path == "/element_delete.html":

            content_length = int(self.headers['Content-Length']);
            body = self.rfile.read(content_length);
            postvars = urllib.parse.parse_qs( body.decode( 'utf-8' ) );
            message = "was deleted from database."
            if not db.delete_element(postvars['element_no'][0], postvars['element_code'][0], postvars['element_name'][0], 
                      str(postvars['colour1'])[3:-2], str(postvars['colour2'])[3:-2], str(postvars['colour3'])[3:-2], 
                      postvars['radius'][0]):
                message = "was not deleted from database.\nValues did not match a database element."
                

            self.send_response( 200 ); # OK
            self.send_header( "Content-type", "text/plain" );
            self.send_header( "Content-length", len(message) );
            self.end_headers();

            self.wfile.write( bytes( message, "utf-8" ) );

        # For uploading a .sdf file
        elif self.path == "/sdf_upload.html":
            content_length = int(self.headers['Content-Length']);
            data = self.rfile.read(content_length);
            # code to handle sdf_upload

            # created file from the uploaded file
            f = io.TextIOWrapper(io.BytesIO(data))
            # created name from the uploaded text
            # I know this seems like a weird way to get it but it works okay
            molName = str(data).split("\\r\\n")[3]

            # fails if there is any error reading the file
            try:
                for i in range(4):    # skip 4 lines for the text
                    next(f)
                for i in range(4):    # skip 4 lines for the file
                    next(f)
                
                exists = "False"
                for s in db.getMolNames():
                    if s[0] == molName:
                        exists = "True"
                        break
                
                if exists == "False":
                    db.add_molecule( molName, f );
            except:
                exists = "Error"
            finally:
                # Text needs to be inserted when display is used to show molecule
                page = open("display.html").read() % ("")
                page += sdf_upload_return % (molName, exists)
                page += displayEnd

                self.send_response( 200 ); # OK
                self.send_header( "Content-type", "text/html" );
                self.send_header( "Content-length", len(page) );
                self.end_headers();

                self.wfile.write( bytes( page, "utf-8" ) );

        # For displaying molecule (and rotating molecule)
        elif self.path == "/display_mol.html":

            length = int(self.headers.get('content-length'))
            data = self.rfile.read(length)
            f = io.TextIOWrapper(io.BytesIO(data))
            # f = postvars['name']
            next(f)
            rotate = False
            if(str(next(f).strip()).endswith('"deg"')):
                rotate = True
                next(f)
                deg = int(str(next(f)).strip())
                for i in range(3):
                    next(f)
                axis = str(next(f)).strip()
                for i in range(3):
                    next(f)
                name = str(next(f)).strip()
            else: 
                next(f)
                name = str(next(f)).strip()

            self.send_response(200)
            mol = db.load_mol(name)

            page = open("display.html").read() % (name)

            if rotate:
                if axis == "X":
                    mx = MolDisplay.molecule.mx_wrapper(deg,0,0)
                if axis == "Y":
                    mx = MolDisplay.molecule.mx_wrapper(0,deg,0)
                if axis == "Z":
                    mx = MolDisplay.molecule.mx_wrapper(0,0,deg)
                mol.xform( mx.xform_matrix )

            mol.sort()
            page += mol.svg()
            page += open("rotate.html").read() % (name, name)
            page += displayEnd
            
            self.send_header( "Content-length", len(page) );
            self.end_headers();
            self.wfile.write(bytes(page, "utf-8"))
        
        # for rotating file without reloading page (does not work)
        # elif self.path == "/rotate_mol.html":
        #     content_length = int(self.headers['Content-Length']);
        #     data = self.rfile.read(content_length);

        #     postvars = urllib.parse.parse_qs( body.decode( 'utf-8' ) );

        #     axis = postvars["axis"][0]
        #     deg = postvars["degree"][0]
        #     name = postvars["name"][0]

        #     mol = db.load_mol(name)

        #     if axis == "X":
        #         mx = MolDisplay.molecule.mx_wrapper(deg,0,0)
        #     elif axis == "Y":
        #         mx = MolDisplay.molecule.mx_wrapper(0,deg,0)
        #     else:
        #         mx = MolDisplay.molecule.mx_wrapper(0,0,deg)
        #     mol.xform( mx.xform_matrix )

        #     mol.sort()
        #     svg = mol.svg()
        
        #     self.send_response( 200 ); # OK
        #     self.send_header( "Content-type", "text/html" );
        #     self.send_header( "Content-length", len(svg) );
        #     self.end_headers();

        #     self.wfile.write( bytes( svg, "utf-8" ) );

        else:
            self.send_response( 404 );
            self.end_headers();
            self.wfile.write( bytes( "404: not found", "utf-8" ) );

# see DO_GET: adding all molecules in database to "Display Molecule" select
addMolecules = """
function dropAddMolecules() {
var x = document.getElementById("molSelect");
x.innerHTML = '';"""
moleculeA = """
var option%s = document.createElement("option");
option%s.text = "%s";
x.add(option%s, x[0]);
"""
sdf_upload_return = """
    <form action="main.html" enctype="multipart/form-data" method="post">
        <button id="open_page_button" type="submit" onclick="submitAlert('%s', '%s')"</button>
    </form>"""


displayEnd = """
</section>
</body>
</html>"""

httpd = HTTPServer( ( 'localhost', int(sys.argv[1]) ), MyHandler );
httpd.serve_forever();
