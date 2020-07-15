var starColor = "#F5AB43";
var defaultColor = "#D4D4D4";

var currentRating = 5;

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
            currentRating = i;
        });
    }
}

function setStarHoverListeners() {
    for (let i = 1; i <= 5; i++) {
        let starId = "#star-" + i;
        $(starId).hover(function() {
            colorStarRange(i, starColor);
        }, function() {
            colorStarRange(currentRating, starColor);
        });
    }
}

$(document).ready(function() {
    colorStarRange(currentRating, starColor);
    $("#id_rating").val(currentRating.toString());
    setStarClickListeners();
    setStarHoverListeners();
});