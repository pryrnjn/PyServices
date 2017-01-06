/**
 * Created by pryrnjn on 6/1/17.
 */
var FEED_URL = "http://54.152.65.154:8080/feed?q={searchTerm}";
var FEED_URL = "http://localhost:8080/feed?q={searchTerm}";

function getIcon(source) {
    switch (source) {
        case "twitter":
            return "https://pbs.twimg.com/profile_images/767879603977191425/29zfZY6I.jpg";
        case "instagram":
            return "https://5a5a57ff32a328601212-ee0df397c56b146e91fe14be42fa361d.ssl.cf1.rackcdn.com/icon/instagram_logos_app_icon/YyepHGHDvkl1wFkUHw8Y/Instagram-v051916_200.png";
        default:
            return "Unknown"
    }
}
function fetchResults(key, cb) {
    if (typeof cb != "function") throw new Error("Invalid callback");
    $.get(FEED_URL.replace("{searchTerm}", key), cb);
}

function getSearchKey() {
    return $("#search_input").val();
}

function populateResultsTbl(data) {
    for (var i in data) {
        var row = data[i];
        row[0] = "<img width='40' height='40' src='" + getIcon(row[0]) + "'>"
    }

    var dataTbl = $('#dataTbl');
    if (dataTbl != null) {
        dataTbl.empty();
    }
    $('#dataTbl').DataTable({
        data: data,
        columns: [
            {title: "Source"},
            {title: "Content"},
            {title: "Date"}
        ]
    });
}
function search() {
    fetchResults(getSearchKey(), function (resp) {
        var data = [];
        for (var i in resp) {
            var record = resp[i];
            data.push([record.source, record.text, new Date(record.created_at * 1000)])
        }
        populateResultsTbl(data);
    })
}
function bindEvents() {
    $("#search_input").bind("enterKey", search)
    $("#search_btn").click(search)
}

