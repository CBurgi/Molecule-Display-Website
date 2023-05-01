# Molecule-Display-Website

Welcome to Cole's Molecule Database!

This full-stack program uses C, Python, SQLite, JavaScript, HTML, CSS, and an Ajax webserver to create, store, and render atoms, bonds, and molecules. All funtionality of the program can be accessed from a front-end web page that was designed using web development methodologies to be easy to navigate and scalable for many different screen types. From the 3 main tabs on the web page users can:
1. Add or remove elements from the database. The user can define the radius and colour of these elements, which are called based on their element number when rendering a molecule's atoms.
2. Upload a .sdf molecule file. These files are then parsed and stored in the database. The user also defines the molecule's name when uploading.
3. Display a molecule. Here the user chooses a molecule to render from the ones currently stored in the database. When viewing the molecule the user can rotate it on all 3 axes.

This program was developed using Agile development's scrum methodology and was split into 4 sprints:
1. Core Library (C). Includes base functionality for atoms, bonds, and molecules, and how they interact with eachother.
2. Base Webserver (Python). Includes ability to convert .sdf file into .svg file rendering the molecule and basic webeserver to upload these .sdf files and display these renderings.
3. Database (Python, SQL). Includes database inplementation to store atoms, bonds, and molecules along with all their associated elements and interactions.
4. Final Webpage (Python, JavaScript, HTML, CSS). Final webpage that allows end user to access all the program's features in a simple and intuitive way.
Full testing was done on each of these stages and user error resolusion techniques were implementes to ensure a smooth experience.
