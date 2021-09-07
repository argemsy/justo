login =()=>{
    let $data = {
        "username": $("#username").val(),
        "password": $("#password").val(),
    }

    let error = 0
    for(data in $data){
        if($data[data] == null || $data[data] == ""){
            error += 1;
        }
    }
    if($("#password").val().length < 8){
        swal({
            title:"Importante",
            text: "La contraseña debe tener una longitud de mínimo 8 caracteres",// debe contener una letra minúscula, una mayúscula, un número y un caracter especial como mínimo.",
            icon: "warning",
            timer: 5000,
            buttons: false,
        });
        return false;
    }
    var testEmail = /^[A-Z0-9._%+-]+@([A-Z0-9-]+\.)+[A-Z]{2,4}$/i;
    if(!testEmail.test($("#username").val())){
        swal({
            title:"Importante",
            text: "Por favor ingrese un email válido para poder procesar su registro.",// debe contener una letra minúscula, una mayúscula, un número y un caracter especial como mínimo.",
            icon: "warning",
            timer: 5000,
            buttons: false,
        });
        return false;
    }

    if(error > 0){
        swal({
            title:"Importante",
            text: "Debe suministrar los datos email y password, ambos son necesario para poder ingresar",
            icon: "warning",
            timer: 5000,
            buttons: false,
        });
        return false;
    }else{

        $.ajax({
            url:"/auth/obtain-token/",
            method: "POST",
            data: $data,
            success:function(response){
                HDD.set(Django.name_jwt, response.token);
                HDD.set('username', $("#username").val());
                Cookies.set(Django.name_jwt, response.token);
                
                if(response.token){
                    setTimeout(function(){
                        location.href = location.origin + Django.next
                    }, 50)
                }else{

                    setTimeout(function(){
                        location.href = '/';
                    }, 50)
                }
            },
            error:function(error){
                swal({
                    title:"Upss",
                    text: error.responseJSON.non_field_errors[0],
                    icon: "error",
                    timer: 5000,
                    buttons: false,
                });
            }
        });

        return false;
    }

}

$("#password").keypress(function(e) {
    //mayor compatibilidad entre navegadores.   
    var code = (e.keyCode ? e.keyCode : e.which);
    if(code==13){
        login();
        return false;         
    }
});