<?php
require_once '../include/common.php';

$accountType = "patient";
require_once '../include/protect.php';
?>
<html>
<head>
    <!--Install jquery -->
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js"></script>
    <style>
        /*.table-bordered th, .table-bordered td { border: 2px solid #ddd!important }*/
    </style>
</head>
<header>
    <?php include '../include/codeLinks.php';?>
    <link rel = "stylesheet" type = "text/css" href = "../include/stylesheet.css" />
</header>


<body>
<!-- Import navigation bar -->
<?php include '../include/patientNavbar.php';?>
</br></br>

<br/>
<div id="main-container" class="container">
    <div class = "whitetextbig" style="color: white; font-weight: bold; font-size: 200%;">        
            Book an appointment
    </div> 
    <br> 
    <div class ="index-errormsg"></div>
    <br>  
    <table class="table table-striped table-light table-hover text-center" id="doctorsTable">
    <thead>
        <tr >
        <th scope="col">#</th>
        <th scope="col">Name</th>
        <th scope="col">Gender</th>
        <th scope="col">Age</th>
        <th scope="col">Experience</th>
        <th scope="col">Specialisation</th>
        <th scope="col">View profile</th>
        </tr>
    </thead>
    <tbody>
    </tbody>
    </table>   
</div>
<script>    
    // Helper function to display error message
    function showError(message) {
        console.log('Error logged')
        // Display an error on top of the table
        $('.index-errormsg').html(message)
    }
    //This is the form id, not the submit button id!
    $(async() => { 
        //This is the url found above the get_all function in doctor.py. Basically you are trying to send data(username and password) to that url using post and receive its response
        //The response you get is found is sent by the json function of the doctor class in doctor.py
        var serviceURL = "http://127.0.0.1:5002/view-all-doctors";
        try {
                //console.log(JSON.stringify({ username: username, password: password,}))
                const response =
                 await fetch(
                   serviceURL, { method: 'GET' }
                );
                const data = await response.json();
                console.log(data)
                //The error message is stored in the data array sent by patient.py! If there is a message variable, it means there is an error
                if (data['message']) {
                    showError(data['message'])
                } else {
                    // for loop to setup all table rows with obtained doctors data
                    //data = data["doctors"];
                    $('#doctorsTable').append("<tbody>");
                    //get current year
                    var currentyear = new Date().getFullYear();
                    //Js month is off by 1
                    var currentmonth = new Date().getMonth() + 1;
                    var currentday = new Date().getDate();
                    for (i = 0; i < data.length; i++) {
                        //Calculate age using date of birth, dob needs to be str not date in mysql or its format will be very weird
                        //Split the dob, first element is year, 2nd is month, 3rd is day
                        dobarr = data[i].dob.split("-") ;
                        age =  currentyear - dobarr[0];
                        console.log(age,currentmonth, currentday, dobarr[1], dobarr[2]);
                        //If havent past birthday yet, deduct age by one
                        if ( (currentmonth < dobarr[1]) || (currentmonth == dobarr[1] && currentday < dobarr[2]) ) {
                            age = age - 1;
                        }            
                        Row =
                            "<tr><th scope='row'>" + data[i].doctor_id + "</th>" +
                            "<td>" + data[i].name + "</td>" +
                            "<td>" + data[i].gender + "</td>" +
                            "<td>" + age + "</td>" +
                            "<td>" + data[i].experience + "</td>" +
                            "<td>" + data[i].specialisation + "</td>" +
                            "<td> <a href='viewDoctor.php?username=" + data[i].username + "'>View profile</a> </td></tr>";
                        $('#doctorsTable').append(Row);
                    }
                    //Add the t body
                    $('#doctorsTable').append("</tbody>");              
                }
            } catch (error) {
                // Errors when calling the service; such as network error, service offline, etc
                showError
              ('There is a problem retrieving doctors data, please try again later. Tip: Did you forget to run doctor.py? :)<br />'+error);
               
            } 
    });
</script>
</body>

</html>