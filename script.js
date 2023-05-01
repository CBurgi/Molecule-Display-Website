/* javascript to accompany jquery.html */

$(document).ready(
    /* this defines a function that gets called after the document is in memory */
    function () {
        document.getElementById("open_page_button").click();
        
        // functionality for file submit
        let input = document.getElementById("sdf_file");
        let fileName = document.getElementById("file_name")
        input.addEventListener("change", ()=>{
            let inputFile = document.querySelector("input[type=file]").files[0];

            fileName.innerText = inputFile.name;
        })

        // functionality for adding element to database
        // checks to make sure element attributes are valid
        $("#add").click(
            function () {
                if (!$("#element_no").val() || $("#element_no").val() < 1 || $("#element_no").val() > 137) {
                    alert("Element number is empty or an incorrect value type.\n(Should be an integer between 1 and 137)");
                } else if (!$("#element_code").val()) {
                    alert("Element code is empty or an incorrect value type.\n(Should be 1 or 2 letters)");
                } else if (!$("#element_name").val()) {
                    alert("Element name is empty or an incorrect value type.\n(Should be max 31 letters)");
                } else if (!$("#radius").val() || $("#radius").val() < 1 || $("#radius").val() > 150) {
                    alert("Radius is empty or an incorrect value type.\n(Should be an integer between 1 and 150)");
                } else {
                    /* ajax post */
                    $.post("/element_add.html",
                        /* pass a JavaScript dictionary */
                        {
                            element_no: Math.round($("#element_no").val()),
                            element_code: $("#element_code").val(),
                            element_name: $("#element_name").val(),
                            colour1: $("#colour1").val(),
                            colour2: $("#colour2").val(),
                            colour3: $("#colour3").val(),
                            radius: Math.round($("#radius").val())
                        },
                        function (data, status) {
                            alert($("#element_name").val() + " " + data);
                        }
                    );
                }
            }
        );

        // functionality for deleting element from database
        // checks to make sure element attributes are valid
        $("#delete").click(
            function () {
                if (!$("#element_no").val() || $("#element_no").val() < 1 || $("#element_no").val() > 137) {
                    alert("Element number is empty or an incorrect value type.\n(Should be an integer between 1 and 137)");
                } else if (!$("#element_code").val()) {
                    alert("Element code is empty or an incorrect value type.\n(Should be 1 or 2 letters)");
                } else if (!$("#element_name").val()) {
                    alert("Element name is empty or an incorrect value type.\n(Should be max 31 letters)");
                } else if (!$("#radius").val() || $("#radius").val() < 1 || $("#radius").val() > 150) {
                    alert("Radius is empty or an incorrect value type.\n(Should be an integer between 1 and 150)");
                } else {
                    /* ajax post */
                    $.post("/element_delete.html",
                        /* pass a JavaScript dictionary */
                        {
                            element_no: Math.round($("#element_no").val()),
                            element_code: $("#element_code").val(),
                            element_name: $("#element_name").val(),
                            colour1: $("#colour1").val(),
                            colour2: $("#colour2").val(),
                            colour3: $("#colour3").val(),
                            radius: Math.round($("#radius").val())
                        },
                        function (data, status) {
                            alert($("#element_name").val() + " " + data);
                        }
                    );
                }
            }
        );

        // Failed ajax request attempt
        // $(".rotate").submit(function(event){
        //     event.preventDefault();
        //     $.ajax({
        //         url:"/rotate_mol.html",
        //         type: "POST",
        //         data: {axis: $("#axis").val(), degree: $("#degree").val(), name: $("#name").val()},
        //         success: function(data){
        //             $(".molecule").html(data);
        //         },
        //         error: function(){
        //             alert("Could not rotate molecule.");
        //         }
        //     });
        // });

    }
);

// functionality for main page
function openPage(evt, pageName) {
    // Declare all variables
    var i, tabcontent, tablinks;

    // Get all elements with class="tabcontent" and hide them
    tabcontent = document.getElementsByClassName("content");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }

    // Get all elements with class="tablinks" and remove the class "active"
    tablinks = document.getElementsByClassName("tab");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }

    // Show the current tab, and add an "active" class to the button that opened the tab
    document.getElementById(pageName).style.display = "block";
    evt.currentTarget.className += " active";
}

// alert for submiting .sdf file
function submitAlert(molName, exists){
    if(exists == "False"){
        alert(molName + " was added to Database.\nGo to the \"Display a molecule\" tab to check it out!")
    }else {
        report = "There was an error loading the .sdf file."
        if(exists == "True"){
            report = "A molecule with that name already exists."
        }
        alert(molName + " was not added to Database.\n" + report)
    }
}
