'use strict'

var isRulesChecked = false;
var isContractChecked = false;

function setContractDisplay(shown) {
    if (shown) {
        $("#contract-section").css("display", "block");
    } else {
        $("#contract-section").css("display", "none");
    }
}

function setFormDisplay(shown) {
    if (shown) {
        $("#form-section").css("display", "block");
    } else {
        $("#form-section").css("display", "none");
    }
}

$(document).ready(function() {
    setContractDisplay(false);
    setFormDisplay(false);

    $("#rules-checkbox").prop("checked", false);
    $("#rules-checkbox").change(function() {
        isRulesChecked = $(this).prop("checked");
        setFormDisplay(isRulesChecked && isContractChecked);
    });

    $("#contract-checkbox").prop("checked", false);
    $("#contract-checkbox").change(function() {
        isContractChecked = $(this).prop("checked");
        setFormDisplay(isRulesChecked && isContractChecked);
    });
});