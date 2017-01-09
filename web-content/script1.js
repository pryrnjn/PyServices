/**
 * Created by pryrnjn on 6/1/17.
 */
var FEED_URL = "/feed?q={searchTerm}";
var FEED_URL = "http://localhost:8080/feed?q={searchTerm}";

// Enable pusher logging - don't include this in production
Pusher.logToConsole = true;

var pusher = new Pusher('772c22382c098e14619e', {
    encrypted: true
});
Pusher.logToConsole = true;

var CHANNEL_NAME = "";
var EVENT_NAME = "feed";

function subscribeChannel(channel, event) {
    var channel = pusher.subscribe(channel);
    channel.bind(event, function (data) {
        populateResultsTbl(parseData(data), true);

    });
}
function unSubscribeChannel(channel) {
    pusher.unsubscribe(channel);
}

function getChannelName(key){
    return key.split(" ").join(".");
}

function fetchResults(key, cb) {
    if (typeof cb != "function") throw new Error("Invalid callback");
    $.get(FEED_URL.replace("{searchTerm}", key), cb)
        .fail(function (err) {
            alert(err.responseText);
//                throw new Error(err.responseText);
        }).done(function () {
        if (getChannelName(key) != CHANNEL_NAME) {
            unSubscribeChannel(CHANNEL_NAME);
            CHANNEL_NAME = getChannelName(key);
            subscribeChannel(CHANNEL_NAME, EVENT_NAME);
        }
    });
}

function getSearchKey() {
    return $.trim($("#search_input").val());
}

function populateResultsTbl(data, isAppend) {
    if (!$.fn.dataTable.isDataTable('#dataTbl')) {
        $('#dataTbl').dataTable({
            retrieve: true,
            paging: true,
            search: true,
            order: false,
            data: [],
            columns: [
                {title: "Content"},
                {title: "Date", visible: false}
            ],
            "aaSortingFixed": [[1, 'desc']]
        });
    }
    var dataTbl = $('#dataTbl').dataTable();
    if (!isAppend) {
        dataTbl.fnClearTable();
    }
    if (data instanceof Array && data.length > 0) {
        dataTbl.fnAddData(data);
    }
}

function search() {
    fetchResults(getSearchKey(), function (resp) {
        populateResultsTbl(parseData(resp));
    })
}

function parseData(inputData) {
    var data = [];
    for (var i in inputData) {
        var record = inputData[i];
        var html = "<div>"
            + "<div>" + getImgWidget(record.img) + "</div>"
            + "<div>" + record.text + "</div>"
            + "<div>" + getLinkWidget(record.link, record.source) + " - " + getLinkWidget(record.owner.link, record.owner.name) + " " + new Date(record.created_at * 1000).toLocaleString() + "</div>"
            + "</div>";
        data.push([html, record.created_at])
    }
    return data;
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
    $("#search_input").bind("enterKey", search);
    $("#search_btn").click(search);
}

