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
        let r = runs[i];
        console.log(r);
        if ($("input[type='checkbox']", r).prop("checked")) {
            tb_runs.push($(r).data("run"));
        }
    }

    console.log(JSON.stringify({ desc: elem.data("desc"), expr: elem.data("expr"), runs: tb_runs }));

    $.get('tensorboard', { spec: JSON.stringify({ desc: elem.data("desc"), expr: elem.data("expr"), runs: tb_runs }) }, function(data) {
        var data = JSON.parse(data);
        window.open(data["url"], '_blank');
        loadHash();
    });
}

