modal_body_template = (obj) => {
  return `<div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h4 class="modal-title">Edición del Hit #${obj.title}</h4>
          <button type="button" class="close" data-dismiss="modal" aria-hidden="true">×</button>
        </div>
        <div class="modal-body">
          ${obj.content}
        </div>
        <div class="modal-footer">
          <a href="javascript:;" class="btn btn-white" data-dismiss="modal">Close</a>
          <a href="javascript:;" onclick="return editHit(${obj.id}, '${obj.rol}');" class="btn btn-primary">Editar</a>
        </div>
      </div>
    </div>`;
};

table_info_template = (key, value) => {
  return `<tr>
					<th>${key}</th><td>${value}</td>
				</tr>`;
};

let id = getUrlLastParameter();
url = `/hits/api/v1/hits/${id}/`;

$.ajax({
  url: url,
  method: "GET",
  type: "json",
  headers: { Authorization: "jwt " + HDD.get(Django.name_jwt) },
  success: function (response) {
    html = `${response.title}<small class="subtitle"> ${response.subtitle}</small>`;
    $("#page-header").empty().html(html);
    html = `<tr>
						<th>Asignación</th><td>${response.code_hit}</td>
					</tr>
					<tr>
						<th>Asesino - Team</th><td>${response.hitmen}</td>
					</tr>
					<tr>
						<th>Descripción</th><td>${response.hit_detail}</td>
					</tr>
					<tr>
						<th>Objetivo</th><td>${response.target}</td>
					</tr>
					<tr>
						<th>Status del hit</th><td>${response.status}</td>
					</tr>
          <tr>
						<th>Hit asigando desde</th><td>${response.assigned_at}</td>
					</tr>
					<tr>
						<th>Asignado por</th><td>${response.assigned_by}</td>
					</tr>`;
    $("#hit_dt").empty().append(html);

    // definimos la funcion que levanta al modal
    loadModal = () => {
      if (response.status == "Finalizado" || response.status == "Fallido") {
        swal({
          icon: "info",
          title: "Información",
          text:
            "Este hit se encuentra con status " +
            response.status +
            " y no puede ser editado.",
          timer: 5000,
          buttons: false,
        });
      } else {
        let obj = {
          id: id,
          title: id,
          content: response.modal,
          rol: response.rol,
        };

        $("#modalGeneral")
          .empty()
          .append(modal_body_template(obj))
          .modal({ show: true });

        $(".select2").select2({
          dropdownParent: $("#modalGeneral"),
        });
      }
    };
  },
  error: function (error) {
    console.log(error);
  },
});

function editHit(pk, rol) {
  url = `/hits/api/v1/hits/${pk}/`;

  $.ajax({
    url: url,
    method: "put",
    type: "json",
    data: {
      hitmen: $("#hitmen").val(),
      status: $("input[name='customRadio']:checked").val(),
    },
    headers: { Authorization: "jwt " + HDD.get(Django.name_jwt) },
    success: function (response) {
      $.when(
        $("#modalGeneral").modal("toggle"),
        swal({
          icon: "success",
          title: "Éxito",
          text: "Ha editado satisfactoriamente el Hit.",
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
}
