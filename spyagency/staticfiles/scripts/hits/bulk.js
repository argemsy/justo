let dt = $("#hits_dt").DataTable({
  ajax: {
    url: "/hits/api/vi/hits/bulk/",
    headers: { Authorization: "jwt " + HDD.get(Django.name_jwt) },
    dataSrc: function (response) {
      return response.results;
    },
  },
  initComplete: function (settings, response) {
    html = `${response.title}<small class="subtitle"> ${response.subtitle}</small>`;
    $("#page-header").empty().html(html);

    create_url = response.create_url;
    if (create_url !== null) {
      $("#create_hits_button").removeClass("hide").attr("href", create_url);
    }
  },
  language: dtLanguage("Re-asignaciones"),
  columns: [
    { data: "id" },
    { data: "code_hit" },
    { data: "hitmen" },
    { data: "target" },
    { data: "status", className: "text-center" },
    { data: "level", className: "text-center" },
    { data: "assigned_by" },
    { data: "buttons_bulk", className: "text-center" },
  ],
  responsive: true,
  destroy: true,
});

// $(document).on('click', '[data-click="panel-lateral"]', function(e) {
// 	console.log(e)
// });

modal_body_template = (obj) => {
  return `<div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h4 class="modal-title">Edición del Hit #${obj.pk}</h4>
          <button type="button" class="close" data-dismiss="modal" aria-hidden="true">×</button>
        </div>
        <div class="modal-body">
          <select name="hitmen" id="hitmen" class="select2" style="width: 100%;">
          </select>
        </div>
        <div class="modal-footer">
          <a href="javascript:;" class="btn btn-white" data-dismiss="modal">Cerrar</a>
          <a href="javascript:;" onclick="return editHit(${obj.pk});" class="btn btn-primary">Editar</a>
        </div>
      </div>
    </div>`;
};

loadModal = (obj) => {
  if (obj.status == 2 || obj.status == 3) {
    estado = {
      2: "Finalizado",
      3: "Fallido",
    };
    swal({
      title: "Información",
      text: `Este hit se encuentra ${
        estado[obj.status]
      } y no puede ser editado`,
      icon: "info",
      buttons: false,
      timer: 5000,
    });
  } else {
    $("#modalGeneral")
      .empty()
      .append(modal_body_template(obj))
      .modal({ show: true });
    $("#hitmen").select2({
      placeholder: "Asesino",
      allowClear: true,
      dropdownParent: $("#modalGeneral"),
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
  }
};

editHit = (pk) => {
  url = `/hits/api/v1/hits/${pk}/`;

  $.ajax({
    url: url,
    method: "put",
    type: "json",
    data: {
      hitmen: $("#hitmen").val(),
    },
    headers: { Authorization: "jwt " + HDD.get(Django.name_jwt) },
    success: function (response) {
      $.when(
        $("#modalGeneral").modal("toggle"),
        swal({
          icon: "success",
          title: "Éxito",
          text: "Has reasignado al asesino de este Hit satisfactoriamente.",
          timer: 5000,
          buttons: false,
        })
      ).then(() => {
        setTimeout(function () {
          location.reload();
        }, 50);
      });
    },
    error: function (error) {
      console.log(error);
    },
  });
};
