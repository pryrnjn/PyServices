/**
 * Created by pryrnjn on 6/1/17.
 */
var FEED_URL = "/feed?q={searchTerm}";
var FEED_URL = "http://localhost:8080/feed?q={searchTerm}";

function fetchResults(key, cb) {
    if (typeof cb != "function") throw new Error("Invalid callback");
    $.get(FEED_URL.replace("{searchTerm}", key), cb);
}

function getSearchKey() {
    return $("#search_input").val();
}

function populateResultsTbl(data) {
    if ($.fn.dataTable.isDataTable('#dataTbl')) {
        var dataTbl = $('#dataTbl').dataTable();
        dataTbl.fnClearTable();
        dataTbl.fnAddData(data);
//            dataTbl.fnDraw();
    } else {
        $('#dataTbl').dataTable({
            retrieve: true,
            paging: false,
            search: true,
            order: false,
            data: data,
            columns: [
                {title: "Content"},
                {title: "Date", visible: false}
            ]
        });
    }
}
function search() {
    fetchResults(getSearchKey(), function (resp) {
        var data = [];
        for (var i in resp) {
            var record = resp[i];
            var html = "<div>"
                + "<div>" + getImgWidget(record.img) + "</div>"
                + "<div>" + record.text + "</div>"
                + "<div>" + getLinkWidget(record.link, record.source) + " - " + getLinkWidget(record.owner.link, record.owner.name) + " " + new Date(record.created_at * 1000).toLocaleString() + "</div>"
                + "</div>";
            data.push([html, record.created_at])
        }
        populateResultsTbl(data);
    })
}
function getImgWidget(src, width, height) {
    if (src)
        if (width && height)
            return "<img width='" + width + "' height='" + height + "' src='" + src + "'>";
        else
            return "<img src='" + src + "'>";
    return "";
}

function getLinkWidget(link, name) {
    if (link || name) {
        return "<a target='_blank' href='" + link + "'>" + name + "</a>";
    }
    return ""
}
function bindEvents() {
    $("#search_input").bind("enterKey", search)
    $("#search_btn").click(search)
}

