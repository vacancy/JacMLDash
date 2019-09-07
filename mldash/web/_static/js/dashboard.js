/*
 * dashboard.js
 * Copyright (C) 2019 Jiayuan Mao <maojiayuan@gmail.com>
 *
 * Distributed under terms of the MIT license.
 */

function loadPageWithURI(anchor) {
    var run = null;
    var expr = null;
    var desc = null;
    if (anchor.indexOf('/run/') != -1) {
        index = anchor.indexOf('/run/');
        run = anchor.substr(index + 5);
        anchor = anchor.substr(0, index);
    }
    if (anchor.indexOf('/expr/') != -1) {
        index = anchor.indexOf('/expr/');
        expr = anchor.substr(index + 6);
        anchor = anchor.substr(0, index);
    }
    if (anchor.indexOf('#desc/') != -1) {
        index = anchor.indexOf('#desc/');
        desc = anchor.substr(index + 6);
        anchor = anchor.substr(0, index);
    }

    if (run != null) {
        $.get('run', { desc: desc, expr: expr, run: run }, function(data, status) {
            $("#main").html(data);
        });
    } else if (expr != null) {
        $.get('expr', { desc: desc, expr: expr }, function(data, status) {
            $("#main").html(data);
        });
    } else if (desc != null) {
        $.get('desc', { desc: desc }, function(data, status) {
            $("#main").html(data);
        });
    }
}

function loadPage(elem) {
    loadPageWithURI($(elem).attr("href"));
    return true;
}

function loadHash() {
    hash = $(location).attr("hash");
    if (hash != "") {
        loadPageWithURI(hash);
    }
}

function runTensorboard(elem) {
    var elem = $(elem);
    var runs = $(".run-row");
    var tb_runs = [];
    for (var i = 0; i < runs.length; i++) {
        let r = $(runs[i]);
        if ($("input[type='checkbox']", r).prop("checked")) {
            tb_runs.push({
                desc: $(r).data("desc"),
                expr: $(r).data("expr"),
                run: $(r).data("run"),
                highlight: $(r).data("highlight")
            });
        }
    }

    $.get('tensorboard/start', { spec: JSON.stringify(tb_runs) }, function(data) {
        var data = JSON.parse(data);
        window.open(data["url"], '_blank');
        loadHash();
    });
}

function termTensorboard(elem) {
    var elem = $(elem);
    $.get('tensorboard/terminate', { index: elem.data("index") }, function(data) {
        loadHash();
    });
}

function updateText(elem) {
    var elem = $(elem);
    var pre = $("#" + elem.data("preid"));
    var cont = $("#" + elem.data("preid")).parent();
    $(elem).hide(function() {
        cont.html($('<div class="py-1"><textarea class="form-control" id="' + elem.data("preid") + '-editor">' + pre.html() + '</textarea>' +
            '<a href="javascript:;" onClick="finUpdateText(this)" data-preid="' + elem.data("preid") + '">Save</a></div>'));
        var text = $("#" + elem.data("preid") + "-editor");
        text.focus();
    });
}

function finUpdateText(elem) {
    var elem = $(elem);
    var text = $("#" + elem.data("preid") + "-editor");
    var link = $("#" + elem.data("preid") + "-link");
    var cont = elem.parent().parent();

    desc = link.data("desc");
    expr = link.data("expr");
    run = link.data("run");
    if (run && expr && desc) {
        $.get("run/update/text", {key: link.data("key"), value: text.val(), desc: desc, expr: expr, run: run});
    } else if (expr && desc) {
        $.get("expr/update/text", {key: link.data("key"), value: text.val(), desc: desc, expr: expr});
    } else if (desc) {
        $.get("desc/update/text", {key: link.data("key"), value: text.val(), desc: desc});
    }

    cont.html('<pre id="' + elem.data("preid") + '">' + text.val() + '</pre>');
    link.show();
}

