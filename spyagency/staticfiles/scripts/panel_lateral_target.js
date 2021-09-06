template_target = (id) => {
    $.ajax({
        url: `/hits/api/v1/targets/${id}/`,
        method: "GET",
        headers: { "Authorization": "jwt " + HDD.get(Django.name_jwt) },
        success: function (response) {
            let html = `<h5>Objetivo</h5>
                            <div class="row m-t-10">
                                <table class="table table-striped table-bordered table-td-valign-middle">
                                    <tr>
                                        <th>Identificador</th><td>${response.id}</td>
                                    </tr>
                                    <tr>
                                        <th>Nombre</th><td>${response.first_name}</td>
                                    </tr>
                                    <tr>
                                        <th>Apellido</th><td>${response.last_name}</td>
                                    </tr>
                                </table>
                            </div>
                            <div class="divider"></div>
                            `;
            $('[data-click="theme-panel-expand"]').trigger("click")
            $("#panel_right_content").empty().append(html)
        },
        error: function (error) {
            console.log(error)
        }
    })

}