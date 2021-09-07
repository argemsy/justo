create_account = () => {
  let $data = {
    email: $("#email").val(),
    password: $("#password").val(),
  };
  let errors = 0;
  for (data in $data) {
    if ($data[data] == null || $data[data] == "") {
      errors += 1;
    }
  }

  if ($("#password").val().length < 8) {
    swal({
      title: "Importante",
      text: "La contraseña debe tener una longitud de mínimo 8 caracteres debe contener una letra minúscula, una mayúscula, un número y un caracter especial como mínimo.",
      icon: "warning",
      timer: 5000,
      buttons: false,
    });
    return false;
  }

  if (errors > 0) {
    swal({
      title: "Importante",
      text: "Debe suministrar los datos email y password, ambos son necesario para poder registrarse.",
      icon: "warning",
      timer: 5000,
      buttons: false,
    });
    return false;
  } else {
    $.ajax({
      url: "/users/api/v1/",
      method: "POST",
      type: "json",
      data: $data,
      success: function (response) {
          $.when(
            swal({
                title: "Éxito",
                text: "Acaba de registrarse en nuestra plataforma",
                icon: "success",
                timer: 5000,
                buttons: false,
              })
          ).then(()=>{
            setTimeout(function () {
                location.href = "/";
              }, 50);
          });

      },
      error: function (error) {
        email = error.responseJSON["email"];
        password = error.responseJSON["password"];
        if (email) {
          swal({
            title: "Upss",
            text: email[0],
            icon: "error",
            timer: 5000,
            buttons: false,
          });
        }
        if (password) {
          swal({
            title: "Upss",
            text: password[0],
            icon: "error",
            timer: 5000,
            buttons: false,
          });
        }
      },
    });
  }
  return false;
};
