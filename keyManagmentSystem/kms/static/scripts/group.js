
$(document).ready(function(){
$("#genKey").click(function(){
    
    var privKeyFile = document.getElementById('privateKey').files[0];
    var fileUpload = document.getElementById('fileUpload').files[0];

//     if(keyFile){
//         var reader = new FileReader();
//             reader.readAsText(keyFile);
//             reader.onload = function(e) {
//                 // browser completed reading file - display it
//                console.log(e.target.result)
//                 var publicKey = keyGen.getKey(e.target.result)
//                 console.log(publicKey)

//                 //make blob of the pem structure
//                 var blob = new Blob([e.target.result], {
//                     type: 'application/x-pem-file'
//                 });
                
//                 //attach blob file to form structure to send to the backend
//                 filename = "key.pem"
//                 var form = new FormData();
//                 const file = new File([blob],filename, {type: "application/x-pem-file"})
//                 form.append("key", file);
               
    
//                 let csrftoken = getCookie('csrftoken');      
//                 console.log(csrftoken)
//                 $.ajaxSetup({
//                     beforeSend: function(xhr, settings) {
                        
//                             xhr.setRequestHeader("X-CSRFToken", csrftoken);
                        
//                     }
//                 });
    
//                 $.ajax(
    
//                     options = {
//                         contentType : false,
//                         processData:false,
//                         url : "addUser/", // the endpoint
//                         type : "POST", // http method
//                         data:form,
//                         dataType: 'text',
                        
//                         // handle a successful response
//                         success : function(data,status,xhr) {
                         
//                             console.log(data)
                           

//                             Swal.fire({
//                                 title: 'You have been added to the list of Users!',
//                                 type: 'success',
//                                 confirmButtonColor: '#3085d6',
//                                 confirmButtonText: 'Ok'
//                               }).then((result) => {
//                                 if (result.value) {
//                                     var newUrl = "groups/"+ data
//                                     // $.get( newUrl,function(){});
//                                     //go to dashboard view
//                                     window.location.replace(newUrl);
//                                 }
//                               })

                             

//                             //Add the link somewhere, an appendChild statement will do.
//                             //Then run this
//                             document.getElementById('someLink').click();
                           
//                         },
                
//                         // handle a non-successful response
//                         error : function(xhr,errmsg,err) {
//                             Swal.fire({
//                                 type: 'error',
//                                 title: 'Oops...',
//                                 text: 'An error was returned. Data not written to database!',
                               
//                               })
//                               console.log(errmsg)
//                               console.log(err)
    
//                             console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
//                         }
//                     }
//                 );






//             };
//     }
//     else{
//         Swal.fire("You Haven't selected a file!")
//     }
 })

})