
//* localStorage *//
var HDD = {
    get: function (key) {
        return localStorage.getItem(key);
    },
    get_default: function (key, value_default) {
        try {
            return localStorage.getItem(key);
        }
        catch (err) {
            return value_default;
        }
    },
    set: function (key, val) {
        return localStorage.setItem(key, val);
    },
    unset: function (key) {
        return localStorage.removeItem(key);
    },
    setJ: function (key, val) {
        return localStorage.setItem(key, JSON.stringify(val));
    },
    getJ: function (key) {
        return JSON.parse(localStorage.getItem(key));
    }
};

//* session *//
function sessionExit(redirect = true) {

    HDD.unset('username');
    HDD.unset(Django.name_jwt);

    Cookies.remove(Django.name_jwt)

    if (redirect) {
        setTimeout(function () { location.href = '/'; }, 40);
    }
};


function refreshJwtToken() {

    $.ajax({
        url: "/auth/refresh-token/",
        method: "POST",
        data: { token: HDD.get(Django.name_jwt) },
        headers: { Authorization: 'jwt ' + HDD.get(Django.name_jwt) },
        success: function (response) {
            HDD.set(Django.name_jwt, response.token);
            Cookies.set(Django.name_jwt, response.token);
        },
        error: function (error) {
            console.log(error)
        }
    })

}

function userInSession(redirect = true) {

    if (HDD.get(Django.name_jwt) == null) {
        sessionExit(redirect);
        return;
    }
    if (HDD.get('username') == null) {

        $.ajax({
            url: Django.api_user,
            method: "GET",
            headers: { Authorization: 'jwt ' + HDD.get(Django.name_jwt) },
            success: function (response) {
                HDD.set('username', response.data.username);
                $(".text_username").text(HDD.get('username'));
            },
            error: function (error) {
                console.log(error)
            }
        })

    }
    else {
        $(".text_username").text(HDD.get('username'));
    }
    refreshJwtToken();
}


function openPanel(id, panel_type) {
    var targetContainer = '.theme-panel';
    var targetClass = 'active';
    // if ($(targetContainer).hasClass(targetClass)) {

    //     if (HDD.get("panel_open") == null)
    //     {
    //         HDD.set("panel_open", id);
    //     }

    //     if(HDD.get("panel_open") == id)
    //     {
    //         $(document).trigger('closed_panel');
    //         HDD.set('panel_page','0');
    //         $(targetContainer).removeClass(targetClass);
    //     }
    // }
    // else
    // {
    //     $(document).trigger('open_panel');
    //     HDD.set('panel_page','1');
    //     $(targetContainer).addClass(targetClass);
    //     if (panel_type == 'onu') {
    //       panel_onu_content('#panel_right_content',HDD.get("panel_open"));
    //     }
    //     if (panel_type == 'fsp'){
    //       panel_fsp_content('#panel_right_content',HDD.get("panel_open"));
    //     }
    //     if (panel_type == 'cpeutp'){
    //       panel_utpcpe_content('#panel_right_content',HDD.get("panel_open"));        
    //     }

    //     if (panel_type == 'setupbox'){
    //       panel_tv_content('#panel_right_content',HDD.get("panel_open"));
    //     }

    // }

    // HDD.set("panel_open", id);

}


function updateDatatable(selector = null) {
    var target = selector ? selector : '.table';
    if ($.fn.dataTable.isDataTable(target)) {
        var table = $(target).DataTable();
        table.ajax.reload();
        //temp_table.ajax.url( temp_table.ajax.url() ).load();
    }
}

function getUrlLastParameter(excludeParams = true) {
    var parts = location.href.split('/');
    var lastSegment = parts.pop() || parts.pop();

    if (excludeParams) {
        if (lastSegment.startsWith('?')) {
            return parts.pop();
        }
        else {
            return lastSegment;
        }

    }
    else {
        return lastSegment;
    }
}

function appendScript(url) {
    let script = document.createElement("script");
    script.src = url;
    script.async = false; //IMPORTANT
    document.getElementById("insert_script_here").appendChild(script);
}


$(document).on('click', '[data-click="panel-lateral"]', function (e) {

    let id = e.target.dataset.id;
    let panel = e.target.dataset.panel;
    if (panel == "panel_target") {
        template_target(id)
    }

});