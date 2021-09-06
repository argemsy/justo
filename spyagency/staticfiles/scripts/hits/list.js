let dt = $("#hits_dt").DataTable({
    ajax: {
        url: "/hits/api/v1/hits/",
        headers: { "Authorization": "jwt " + HDD.get(Django.name_jwt) },
        dataSrc: function (response) {
            return response.results;
        },
    },
    "initComplete": function (settings, response) {
        html = `${response.title}<small class="subtitle"> ${response.subtitle}</small>`
        $("#page-header").empty().html(html);

        create_url = response.create_url;
        if (create_url !== null) {
            $("#create_hits_button").removeClass("hide").attr("href", create_url)
        }

    },
    columns: [
        { "data": "id", "className": "text-center" },
        { "data": "code_hit" },
        { "data": "hitmen" },
        { "data": "target" },
        { "data": "status", "className": "text-center" },
        { "data": "level", "className": "text-center" },
        { "data": "assigned_by" },
        { "data": "buttons", "className": "text-center" },
    ],
    responsive: true,
    destroy: true,
})

// $(document).on('click', '[data-click="panel-lateral"]', function(e) {
// 	console.log(e)
// });