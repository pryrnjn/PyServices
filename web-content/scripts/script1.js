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

    var list = ['https://www.instagram.com/p/BU1B4URF8Xf5bn5lX6NrzBJN1AV46JFa67ALFo0/', 'https://www.instagram.com/p/BVpnnDplCW7vnBaA9v2Kuq6irKiLt_7_kEKLas0/', 'https://www.instagram.com/p/BXmbAT3lm4AuvSCHvIae9qPZS2fiGBt9n5Sl8I0/', 'https://www.instagram.com/p/BVP7ZYKFmhk31uoSmVKjorT_nlJqIK3SYX_d4E0/', 'https://www.instagram.com/p/BVp55mPlPoCAN0MiIrjXyggQaqD8HC946wkXnQ0/', 'https://www.instagram.com/p/BULw6H5lPkDEi_jG5XxpwHf5musk21P0rIYyIc0/', 'https://www.instagram.com/p/BWFWkImFaWUHRIEAs1pOsgQv6npih_dTJ7nuKI0/', 'https://www.instagram.com/p/BVJb80nFE9RP1ToJwMt3ojpYdd1cZ8H1dDvjYQ0/', 'https://www.instagram.com/p/Ba9UNHzlU6w4PqUItYJV7_u_KV2IUKVQ0RbIAs0/', 'https://www.instagram.com/p/BX0r22uFZzHYoyqyID3bL1KmZHOO908s7teZJI0/', 'https://www.instagram.com/p/BSoljzwAwShSg2_B18wmBgTXUtuaVhVzSv4oJU0/', 'https://www.instagram.com/p/BWZbkUwldvNTOWgzvfvLPe5QHXpPhJtiwyRaRc0/', 'https://www.instagram.com/p/BWHXdGKFEeagcFs2qs4blmYqR9XR0YwDReKhQw0/', 'https://www.instagram.com/p/BatL2ShFagSeFDCu7ZYfBPc0kIAF6Wnk62nXpc0/', 'https://www.instagram.com/p/BdegbKqBObr/', 'https://www.instagram.com/p/BdounAmh2oj/', 'https://www.instagram.com/p/BeI6HYTB4s7/', 'https://www.instagram.com/p/BeJ481_BV2W/', 'https://www.instagram.com/p/BeA1N0ZBHqL/', 'https://www.instagram.com/p/BdiZWu8BQxr/', 'https://www.instagram.com/p/BdcAjl8hVEk/', 'https://www.instagram.com/p/BdmZ2IzB1t6/', 'https://www.instagram.com/p/Bdt3jUUBxAc/', 'https://www.instagram.com/p/BeCzCy9B0Cz/', 'https://www.instagram.com/p/Bd4h9FfBCy2/', 'https://www.instagram.com/p/BdrQgN_hvV1/', 'https://www.instagram.com/p/BeFe2NtBtx9/', 'https://www.instagram.com/p/Bdfo6RzhJUx/', 'https://www.instagram.com/p/BeAAbMAB63f/', 'https://www.instagram.com/p/BeISe34B4jr/', 'https://www.instagram.com/p/Bdp_dxWh8kN/', 'https://www.instagram.com/p/BdhH3kOBsov/', 'https://www.instagram.com/p/Bde8Ztdh5px/', 'https://www.instagram.com/p/BdZvBOHBc5G/', 'https://www.instagram.com/p/BeGDsKhhuEv/', 'https://www.instagram.com/p/Bd9NS53Bzk9/', 'https://www.instagram.com/p/BdStRkZhioy/', 'https://www.instagram.com/p/BdR8LgxBCC3/', 'https://www.instagram.com/p/BdZWTUHhzgF/', 'https://www.instagram.com/p/BdW20pQBFpp/', 'https://www.instagram.com/p/BdUHqqRhjXs/', 'https://www.instagram.com/p/BdNNkWehIRb/', 'https://www.instagram.com/p/BdQHSBVBa4l/', 'https://www.instagram.com/p/BdKGIjSBokO/', 'https://www.instagram.com/p/BdMcs2Wh3ys/', 'https://www.instagram.com/p/BdPJWaABKc6/', 'https://www.instagram.com/p/BdO0sbhBNir/', 'https://www.instagram.com/p/Bc_f9yWBwye/', 'https://www.instagram.com/p/BdHJaxQBxZv/', 'https://www.instagram.com/p/BdCR45wBnNl/', 'https://www.instagram.com/p/BdHKOnZhj8k/', 'https://www.instagram.com/p/Bc9gaN3FqQB/', 'https://www.instagram.com/p/BdJuVKSBkPp/', 'https://www.instagram.com/p/BdHjN4ghXD0/', 'https://www.instagram.com/p/BdDQ6l9BWCc/', 'https://www.instagram.com/p/BdDNwCqBicb/', 'https://www.instagram.com/p/BdAGwVpB7I9/', 'https://www.instagram.com/p/BdE6qNjBWDl/', 'https://www.instagram.com/p/Bc9MIwgBKXj/', 'https://www.instagram.com/p/BcxP6DxBYPH/', 'https://www.instagram.com/p/Bc2VlqDhZot/', 'https://www.instagram.com/p/Bc3tWh0B5Ce/', 'https://www.instagram.com/p/Bc7PfOiBGYv/', 'https://www.instagram.com/p/BcygW_DBdRO/', 'https://www.instagram.com/p/Bczlej6h1ZZ/', 'https://www.instagram.com/p/Bcw_DH_BbEm/', 'https://www.instagram.com/p/Bc6nH4oh9t3/', 'https://www.instagram.com/p/Bc7JJHmBWB7/', 'https://www.instagram.com/p/Bc6kGwXBzG7/', 'https://www.instagram.com/p/Bc4Sf52BmlE/', 'https://www.instagram.com/p/Bcrc_8aBCrS/', 'https://www.instagram.com/p/Bcm5dabhJ8d/', 'https://www.instagram.com/p/BcudT9chnEr/', 'https://www.instagram.com/p/BclteQeBoS2/', 'https://www.instagram.com/p/BcocyMWBaXx/', 'https://www.instagram.com/p/Bcj9om9hdlq/', 'https://www.instagram.com/p/BcteWDdBKl2/', 'https://www.instagram.com/p/BcmXS9mhei0/', 'https://www.instagram.com/p/BcoRgFwh1ER/', 'https://www.instagram.com/p/BcvTgMMhuB2/', 'https://www.instagram.com/p/BcrqlSCh9ys/', 'https://www.instagram.com/p/BceRmj5hDBX/', 'https://www.instagram.com/p/Bcjuq5Ih3Lb/', 'https://www.instagram.com/p/Bcd_XBSBISV/', 'https://www.instagram.com/p/Bcgms8uh3QX/', 'https://www.instagram.com/p/BchkS2CB1Un/', 'https://www.instagram.com/p/BciJ_vZhXr5/', 'https://www.instagram.com/p/BcjMcMchbTo/', 'https://www.instagram.com/p/Bcg1ac2hj9z/', 'https://www.instagram.com/p/Bce2St_h1CG/', 'https://www.instagram.com/p/BchrwywBF8Q/', 'https://www.instagram.com/p/BceOcR4h3l0/', 'https://www.instagram.com/p/BchJNa3B7eW/', 'https://www.instagram.com/p/BccCdVmh9t4/', 'https://www.instagram.com/p/BcZHj5xBRNA/', 'https://www.instagram.com/p/BcZR3DUhDog/', 'https://www.instagram.com/p/BcXG2EShAgc/', 'https://www.instagram.com/p/BccRo0Dh8CG/', 'https://www.instagram.com/p/BcY51fMhiJM/', 'https://www.instagram.com/p/Bcb6pQ_B97V/', 'https://www.instagram.com/p/BcZw7ishKi4/', 'https://www.instagram.com/p/BcbdyI7BKvY/', 'https://www.instagram.com/p/BcZLLvEB2jX/', 'https://www.instagram.com/p/BcRIx0cB5Ym/', 'https://www.instagram.com/p/BcTwy9LhNe6/', 'https://www.instagram.com/p/BcWhH39B0Bm/', 'https://www.instagram.com/p/BcR2FSBBT1_/', 'https://www.instagram.com/p/BcRMzY1hS7e/', 'https://www.instagram.com/p/BcPZPPhhBxh/', 'https://www.instagram.com/p/BcXB84eh2YO/', 'https://www.instagram.com/p/BcOkMvxh_fV/', 'https://www.instagram.com/p/BcUkRFCB1J0/', 'https://www.instagram.com/p/BcOujgpBkty/', 'https://www.instagram.com/p/BcMw1FdhZ6b/', 'https://www.instagram.com/p/BcKIHNehiDm/', 'https://www.instagram.com/p/BcHrMYyhN9S/', 'https://www.instagram.com/p/BcJUgKeBV12/', 'https://www.instagram.com/p/BcJfcmPh1TF/', 'https://www.instagram.com/p/BcHOIz5hzV6/', 'https://www.instagram.com/p/BcKgqjKB4lb/', 'https://www.instagram.com/p/BcMCN5WBFSP/', 'https://www.instagram.com/p/BcM6Y_rh_jj/', 'https://www.instagram.com/p/BcLyOFJBDu5/', 'https://www.instagram.com/p/BcGt5k5BHbA/', 'https://www.instagram.com/p/BcJ00GXBQnD/'];

    for (var i in list){
        var url = list[i];
        $.get("https://api.instagram.com/oembed/?url=" + url, cb)
        .fail(function (err) {
            alert(err.responseText);
//                throw new Error(err.responseText);
        });
    };
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
    fetchResults('', function (resp) {
        populateResultsTbl(parseData(resp));
    })
}

function parseData(inputData) {
    return [[JSON.parse(inputData).html, '']]

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
