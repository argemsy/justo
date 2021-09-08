html = `Hit<small class="subtitle"> Nuevo</small>`;
$("#page-header").empty().html(html);

$("#hitmen").select2({
  placeholder: "Asesino",
  allowClear: true,
  minimumResultsForSearch: 3,
  ajax: {
    url: "/hits/autocompletes/hitmens/",
    data: function (params) {
      var query = {
        q: params.term,
        page: params.page || 1,
      };

      // Query parameters will be ?search=[term]&page=[page]
      return query;
    },
  },
});
$("#level").select2({
  placeholder: "Nivel de peligrosidad",
  allowClear: true,
  minimumResultsForSearch: Infinity,
  data: [
    { id: 1, text: "Fácil" },
    { id: 2, text: "Intermedio" },
    { id: 3, text: "Difícil" },
  ],
});

function save_hit() {
  let $data = {
    hitmen: $("#hitmen").val(),
    first_name: $("#first_name").val(),
    last_name: $("#last_name").val(),
    level: $("#level").val(),
    hit_detail: $("#hit_detail").val(),
  };

  error = 0;
  for (data in $data) {
    if ($data[data] == "" || $data[data] == null) {
      error += 1;
    }
  }

  if (error > 0) {
    alert("error");
  } else {
    $.ajax({
      url: "/hits/api/v1/hits/",
      method: "POST",
      type: "json",
      data: $data,
      headers: { Authorization: "jwt " + HDD.get(Django.name_jwt) },
      success: function (response) {
        swal({
          title: "Excelente!",
          text: "Has creado a un nuevo Hit!",
          icon: "success",
          timer: 2000,
          showCancelButton: false,
          showConfirmButton: false,
        });

        setTimeout(function () {
          location.href = Django.next;
        }, 5000);
      },
      error: function (error) {
        console.log(error);
      },
    });
  }

  return false;
}
