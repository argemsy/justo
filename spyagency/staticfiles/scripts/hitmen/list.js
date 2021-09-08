let dt = $("#users_dt").DataTable({
    ajax: {
      url: "/users/api/v1/",
      headers: { Authorization: "jwt " + HDD.get(Django.name_jwt) },
      dataSrc: function (response) {
        return response.results;
      },
    },
    initComplete: function (settings, response) {
      console.log(response);
      html = `${response.title}<small class="subtitle"> ${response.subtitle}</small>`;
      $("#page-header").empty().html(html);
    },
    language: dtLanguage("Hitmen's"),
    columns: [
      { data: "id" },
      { data: "username" },
      { data: "email" },
      { data: "team" },
      { data: "rol" },
      { data: "status" },
      { data: "grupos" },
    ],
    responsive: true,
    destroy: true,
  });