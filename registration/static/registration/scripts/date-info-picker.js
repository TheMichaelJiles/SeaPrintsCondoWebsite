'use strict'

var cleaningFee;
var defaultPricePerNight;
var seasons;
var taxRate;
var minimumDaysOfStay;

function hideInformation() {
    $("#nights-text").html("Select Dates");
    $("#price-per-night").css('visibility', 'hidden');
    $("#middle").css("visibility", "hidden");
    $("#bottom").css("visibility", "hidden");
}

function showInformation(avgNightlyCost, numNights) {
    console.log(avgNightlyCost);
    avgNightlyCost = avgNightlyCost.toFixed(2);

    $("#price-per-night").css('visibility', 'visible');
    $("#middle").css("visibility", "visible");
    $("#bottom").css("visibility", "visible");

    $("#nights-text").html(numNights + " Nights");
    $("#price-per-night").html("$" + avgNightlyCost + "/night");

    $("#price-text").html(numNights + " x " + avgNightlyCost);
    $("#price-total-text").html("$" + (numNights * avgNightlyCost));

    $("#cleaning-total-fee").html("$" + cleaningFee.toFixed(2));

    let pretax = parseFloat(cleaningFee.toFixed(2)) + (numNights * parseFloat(avgNightlyCost));
    let taxAmount = pretax * taxRate;
    let total = pretax + taxAmount;

    $("#tax-total-fee").html("$" + taxAmount.toFixed(2));
    $("#total-fee").html("$" + total.toFixed(2));

}

$(document).ready(function() {
    hideInformation();
    $.getJSON("/registration/get_rates/", function(data) {
        cleaningFee = data.cleaning_fee;
        defaultPricePerNight = data.default.price;
        seasons = data.seasons;
        taxRate = data.tax_rate / 100;
        minimumDaysOfStay = data.minimum_days_of_stay;
    });
});