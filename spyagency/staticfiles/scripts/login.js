login =()=>{
    $.ajax({
        url:"/auth/obtain-token/",
        method: "POST",
        data: {
            "username": $("#username").val(),
            "password": $("#password").val(),
        },
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
            console.log(error)
        }
    });

    return false;
}

$("#password").keypress(function(e) {
    //mayor compatibilidad entre navegadores.   
    var code = (e.keyCode ? e.keyCode : e.which);
    if(code==13){
        login();
        return false;         
    }
});