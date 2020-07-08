$(function() {
    $("#pdf-viewer").on('load', function () {
        var iframe = document.getElementById("pdf-viewer").contentWindow;
        $(iframe).on('scroll', function () { 
            alert("scrolling");
            if ($(iframe).scrollTop() + $(iframe).height() == $(iframe.document).innerHeight()) {
                alert("Reached bottom!");
                $("#contract-checkbox").removeAttr("disabled");
                $("#rules-checkbox").removeAttr("disabled");
            }
        });


    });

})