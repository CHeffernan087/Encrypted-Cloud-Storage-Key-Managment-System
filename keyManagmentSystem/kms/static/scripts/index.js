/**
 * 
 * encryption and decryption stuff
 */


function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


function toHex(str) {
    var result = '';
    for (var i=0; i<str.length; i++) {
      result += str.charCodeAt(i).toString(16);
    }
    return result;
  }
    

var keyGen = KEYUTIL
var key = keyGen.generateKeypair("RSA", 1024)
var privateKey = key.prvKeyObj;
var publicKey = key.pubKeyObj;
console.log("Obj : ",privateKey)


var testText = "Vivvvaaa las Vegas"	
var pemPriv = keyGen.getPEM(privateKey, "PKCS8PRV")
console.log("privateKey: \n"+pemPriv)

var publicPem = keyGen.getPEM(publicKey, "PKCS8PUB")
console.log("privateKey: \n"+publicPem)

privateKey = keyGen.getKeyFromPlainPrivatePKCS8PEM(pemPriv)
publicKey = keyGen.getKey(publicPem)





 //returns a hexadecimal encrypted string
 var encrypted = KJUR.crypto.Cipher.encrypt(testText, publicKey, "RSAOAEP384")
 console.log(encrypted)
 //can decrypt a hexadecimal string using the private key
 var decrypt = KJUR.crypto.Cipher.decrypt(encrypted, privateKey, "RSAOAEP384")
 console.log(decrypt)



console.log("hasnt broken baby")

$("document").ready(function(){
$("#clickme").click(function(){
   
    const selectedFile = document.getElementById('input').files[0];
    console.log(selectedFile)
   
    var reader = new FileReader();
    //var bin = reader.readAsArrayBuffer ( selectedFile )


    
    


    // Read the file
    //reads the file and outputs a base 64 string
      reader.readAsDataURL(selectedFile);
    // Specify the handler for the `load` event
      reader.onload = function (e) {
       
        //the results of reading in the file
        var bytes = e.target.result;
        //returns a hexadecimal encrypted string
        var encrypted = KJUR.crypto.Cipher.encrypt(bytes, publicKey, "RSAOAEP384")
        console.log(encrypted)

        //can decrypt a hexadecimal string using the private key
        var decrypt = KJUR.crypto.Cipher.decrypt(encrypted, privateKey, "RSAOAEP384")
        console.log(decrypt)
      }
      
})

$("#submitKey").click(function(){
    var keyFile = document.getElementById('pemInput').files[0];
    console.log(keyFile)

    var privKey = document.getElementById('privKey').files[0];
    var privReader = new FileReader();
    privReader.readAsText(privKey);
    privReader.onload = function(e) {
                // browser completed reading file - display it
               console.log(e.target.result)
                privateKey = keyGen.getKeyFromPlainPrivatePKCS8PEM(e.target.result)
                console.log(privateKey)

                


                var blob = new Blob([e.target.result], {
                    type: 'application/x-pem-file'
                });
            }


    if(keyFile){
        var reader = new FileReader();
            reader.readAsText(keyFile);
            reader.onload = function(e) {
                // browser completed reading file - display it
               console.log(e.target.result)
                var publicKey = keyGen.getKey(e.target.result)
                console.log(publicKey)

                


                var blob = new Blob([e.target.result], {
                    type: 'application/x-pem-file'
                });




                filename = "key.pem"
                var form = new FormData();
                const file = new File([blob],filename, {type: "application/x-pem-file"})
                console.log(file)
                form.append("key", file);
               
    
                let csrftoken = getCookie('csrftoken');      
                console.log(csrftoken)
                $.ajaxSetup({
                    beforeSend: function(xhr, settings) {
                        
                            xhr.setRequestHeader("X-CSRFToken", csrftoken);
                        
                    }
                });
    
                $.ajax(
    
                    options = {
                        contentType : false,
                        processData:false,
                        url : "pubkey/", // the endpoint
                        type : "POST", // http method
                        data:form,
                        dataType: 'text',
                        
                        // handle a successful response
                        success : function(data,status,xhr) {
                         
                            console.log(data)
                            console.log(privateKey)
                            console.log(keyGen.getPEM(privateKey, "PKCS8PRV"))
                            var sessionID = KJUR.crypto.Cipher.decrypt(data, privateKey,"RSAOAEP")
                         
                            console.log(jesus)
                      
                            Swal.fire({
                                type: 'success',
                                title: 'Submission Recieved.',
                                text: 'Marks were uploaded to the database',
                               
                              })

                           
                        },
                
                        // handle a non-successful response
                        error : function(xhr,errmsg,err) {
                            Swal.fire({
                                type: 'error',
                                title: 'Oops...',
                                text: 'An error was returned. Data not written to database!',
                               
                              })
                              console.log(errmsg)
                              console.log(err)
    
                            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
                        }
                    }
                );






            };
    }
    else{
        Swal.fire("You Haven't selected a file!")
    }
})




/**
 * 
 * key input stuff
 * 
 */

// Swal.fire({
//     title: 'Select image',
//     input: 'file',
//     inputAttributes: {
//       'accept': 'image/*',
//       'aria-label': 'Upload your profile picture'
//     }
//   })
  
//   if (file) {
//     const reader = new FileReader
//     reader.onload = (e) => {
//       Swal.fire({
//         title: 'Your uploaded picture',
//         imageUrl: e.target.result,
//         imageAlt: 'The uploaded picture'
//       })
//     }
//     reader.readAsDataURL(file)
//   }

/**
 * 
 * 
 * 
 */

/**
 * Drag and drop file upload.
 */





var isAdvancedUpload = function() {
    var div = document.createElement('div');
    return (('draggable' in div) || ('ondragstart' in div && 'ondrop' in div)) && 'FormData' in window && 'FileReader' in window;
  }();



  if (isAdvancedUpload) {
    // ...
  }

var $form = $('.box');

if (isAdvancedUpload) {
  $form.addClass('has-advanced-upload');
}


/** Adding A new User to the System*/




$("#genKey").click(function(){
    var keyFile = document.getElementById('pemInput').files[0];

    if(keyFile){
        var reader = new FileReader();
            reader.readAsText(keyFile);
            reader.onload = function(e) {
                // browser completed reading file - display it
               console.log(e.target.result)
                var publicKey = keyGen.getKey(e.target.result)
                console.log(publicKey)

                //make blob of the pem structure
                var blob = new Blob([e.target.result], {
                    type: 'application/x-pem-file'
                });
                
                //attach blob file to form structure to send to the backend
                filename = "key.pem"
                var form = new FormData();
                const file = new File([blob],filename, {type: "application/x-pem-file"})
                form.append("key", file);
               
    
                let csrftoken = getCookie('csrftoken');      
                console.log(csrftoken)
                $.ajaxSetup({
                    beforeSend: function(xhr, settings) {
                        
                            xhr.setRequestHeader("X-CSRFToken", csrftoken);
                        
                    }
                });
    
                $.ajax(
    
                    options = {
                        contentType : false,
                        processData:false,
                        url : "addUser/", // the endpoint
                        type : "POST", // http method
                        data:form,
                        dataType: 'text',
                        
                        // handle a successful response
                        success : function(data,status,xhr) {
                         
                            console.log(data)
                           

                            Swal.fire({
                                title: 'You have been added to the list of Users!',
                                type: 'success',
                                confirmButtonColor: '#3085d6',
                                confirmButtonText: 'Ok'
                              }).then((result) => {
                                if (result.value) {
                                    var newUrl = "groups/"+ data
                                    // $.get( newUrl,function(){});
                                    //go to dashboard view
                                    window.location.replace(newUrl);
                                }
                              })

                             

                            //Add the link somewhere, an appendChild statement will do.
                            //Then run this
                            document.getElementById('someLink').click();
                           
                        },
                
                        // handle a non-successful response
                        error : function(xhr,errmsg,err) {
                            Swal.fire({
                                type: 'error',
                                title: 'Oops...',
                                text: 'An error was returned. Data not written to database!',
                               
                              })
                              console.log(errmsg)
                              console.log(err)
    
                            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
                        }
                    }
                );






            };
    }
    else{
        Swal.fire("You Haven't selected a file!")
    }
})

})