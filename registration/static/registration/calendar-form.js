$("#calendarSubmit").attr('disabled', true);

function isValidEmail(email) {
    return /^\w+([.-]?\w+)@\w+([.-]?\w+)(.\w{2,3})+$/.test(email);
}

function isValidPhonenumber(number) {
    return /^\d{10}$/.test(number);
}

function isValidNumberOfGuests(numberGuests) {
    return numberGuests > 0;
    //Enforce max number guests
}

function isValidName(name) {
    return $.trim(name) != "";
}

function checkFields() {
    let canSubmit = isValidEmail($("#id_email_contact").val());
    canSubmit = canSubmit && isValidPhonenumber($("#id_phone_contact").val());
    canSubmit = canSubmit && isValidNumberOfGuests($("#id_number_of_guests").val());
    canSubmit = canSubmit && isValidName($("#id_name"));
    canSubmit = canSubmit && checkinDate != null && checkoutDate != null;
    if (canSubmit) {
        $("#calendarSubmit").removeAttr("disabled");
    } else {
        $("#calendarSubmit").attr('disabled', true);
    }
}

$( document ).ready(function() {
    $("#id_email_contact").change(checkFields);
    $("#id_phone_contact").change(checkFields);
    $("#id_number_of_guests").change(checkFields);
    $("#id_name").change(checkFields);
    $("#id_total_price").change(checkFields);


    $('#calendar-form').submit(function(event) {

        var checkinInput = $("<input>")
            .attr("type", "hidden")
            .attr("name", "checkinDate").val(checkinDate.toISOString(true));

        var checkoutInput = $("<input>")
            .attr("type", "hidden")
            .attr("name", "checkoutDate").val(checkoutDate.toISOString(true));    
        $('#calendar-form').append(checkinInput);
        $('#calendar-form').append(checkoutInput);
    })
});