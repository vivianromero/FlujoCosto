var notify_badge_class;
var notify_menu_class;
var notify_api_url;
var notify_fetch_count;
var notify_unread_url;
var notify_mark_all_unread_url;
var notify_refresh_period = 15000;
// Set notify_mark_as_read to true to mark notifications as read when fetched
var notify_mark_as_read = false;
var consecutive_misfires = 0;
var registered_functions = [];

function fill_notification_badge(data) {
    var badges = document.getElementsByClassName(notify_badge_class);
    if (badges) {
        for (var i = 0; i < badges.length; i++) {
            // if (data.unread_count > 0) {
                badges[i].innerHTML = data.unread_count;
                console.log(badges[i])
            // }
        }
    }
}

function fill_notification_list(data) {
    var menus = document.getElementsByClassName(notify_menu_class);
    if (menus) {
        var messages = data.unread_list.map(function (item) {
            var message = "";

            if (typeof item.actor !== 'undefined') {
                message = item.actor;
            }
            if (typeof item.verb !== 'undefined') {
                message = message + " " + item.verb;
            }
            if (typeof item.target !== 'undefined') {
                message = message + " " + item.target;
            }
            if (typeof item.timestamp !== 'undefined') {
                message = message + " " + item.timestamp;
            }
            return '<li>' + message + '</li>';
        }).join('')

        for (var i = 0; i < menus.length; i++) {
            menus[i].innerHTML = messages;
        }
    }
}

function fill_notification_dropdown_list(data) {
    var menus = document.getElementsByClassName(notify_menu_class);
    let selected_language = document.getElementById('select_language').value
    if (menus) {
        var messages = data.unread_list.map(function (item) {
            var message = "";
            var timestamp = "";
            let href = "";

            if (typeof item.verb !== 'undefined') {
                message = message + item.verb;
            }
            if (typeof item.description !== 'undefined') {
                href = href + item.description;
            } else {
                href = "#"
            }
            if (typeof item.timestamp !== 'undefined') {
                let p_timestamp = Date.parse(item.timestamp)
                let d_timestamp = new Date(p_timestamp)
                moment.locale(selected_language)
                let m_timestamp = moment(d_timestamp).fromNow()

                timestamp = timestamp + m_timestamp;

            }
            let line1 = '<a href="' + href + '" class="dropdown-item"><i class="fas fa-envelope mr-2"></i> '
            let line2 = '<span class="float-right text-muted text-sm">'
            let line3 = '</span></a> <div class="dropdown-divider"></div>'

            return line1 + message + line2 + timestamp + line3;
        }).join('')
        let line41 = '<a id="a_notifications_dropdown_footer"\n' +
            '           hx-post="{% url \'notifications:mark_all_as_read\' %}"\n' +
            '           hx-trigger="click"\n' +
            '           hx-target="#notifications_dropdown_menu"\n' +
            '           hx-swap="none" href="#" class="dropdown-footer">'
        let line42 = '<i class="fas fa-envelope-open mr-2"></i>'
        let line43 = '</a><div class="dropdown-divider"></div>'
        let text = ""
        if (selected_language === 'es') {
            text = text + 'Marcar todas las notificaciones como leídas'
        } else {
            text = text + 'Mark all notifications as read'
        }

        for (var i = 0; i < menus.length; i++) {
            menus[i].innerHTML = messages;
            // menus[i].innerHTML = messages + line41 + line42 + text + line43;
        }
    }
}

function register_notifier(func) {
    registered_functions.push(func);
}

function fetch_api_data() {
    // only fetch data if a function is setup
    if (registered_functions.length > 0) {
        var r = new XMLHttpRequest();
        var params = '?max=' + notify_fetch_count;

        if (notify_mark_as_read) {
            params += '&mark_as_read=true';
        }

        r.addEventListener('readystatechange', function(event) {
            if (this.readyState === 4) {
                if (this.status === 200) {
                    consecutive_misfires = 0;
                    var data = JSON.parse(r.responseText);
                    for (var i = 0; i < registered_functions.length; i++) {
                       registered_functions[i](data);
                    }
                } else {
                    consecutive_misfires++;
                }
            }
        });
        r.open("GET", notify_api_url + params, true);
        r.send();
    }
    if (consecutive_misfires < 10) {
        setTimeout(fetch_api_data, notify_refresh_period);
    } else {
        var badges = document.getElementsByClassName(notify_badge_class);
        if (badges) {
            for (var i = 0; i < badges.length; i++) {
                badges[i].innerHTML = "!";
                badges[i].title = "Connection lost!"
            }
        }
    }
}

setTimeout(fetch_api_data, 1000);
