var starColor = "#5ECBD8";
var defaultColor = "#ffffff";

function colorStar(number, hexColor) {
    let starId = "#star-" + number;
    $(starId + "> g > path").each(function(index) {
        $(this).attr("fill", hexColor);
    });
}

function colorStarRange(number, hexColor) {
    for (let i = 1; i <= number; i++) {
        colorStar(i, hexColor);
    }
    for (let i = number + 1; i <= 5; i++) {
        colorStar(i, defaultColor);
    }
}

function setStarClickListeners() {
    for (let i = 1; i <= 5; i++) {
        let starId = "#star-" + i;
        $(starId).click(function() {
            colorStarRange(i, starColor);
            $("#id_rating").val(i.toString());
        });
    }
}

$(document).ready(function() {
    let initialRating = 5;
    colorStarRange(initialRating, starColor);
    $("#id_rating").val(initialRating.toString());
    setStarClickListeners();
});