//Variables
var today = new Date();
var currentMonth = today.getMonth();
var currentYear = today.getFullYear();
var selectYear = document.getElementById("year");
var selectMonth = document.getElementById("month");
var checkinDate = null;
var checkoutDate = null;

var months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
var takenDates = [];
var monthAndYear = document.getElementById("monthAndYear");

//Execution:
init();
//End Execution

/*
Function executed when the webpage is loaded. JSON request must happen BEFORE showCalendar
*/
function init() {
    $.getJSON("registration/get_taken_dates", function(dateData) {
        for (let date of dateData) {
            let currentDate = new Date(date);
            takenDates.push(currentDate);
        }
    });

    showCalendar(currentMonth, currentYear);
}

/*
Transitions calendar to the next month, incrementing the year if necessary
*/
function next() {
    currentYear = (currentMonth === 11) ? currentYear + 1 : currentYear;
    currentMonth = (currentMonth + 1) % 12;
    showCalendar(currentMonth, currentYear);
}

/*
Transitions calendar to the previous month, devrementing the year if necessary
*/
function previous() {
    currentYear = (currentMonth === 0) ? currentYear - 1 : currentYear;
    currentMonth = (currentMonth === 0) ? 11 : currentMonth - 1;
    showCalendar(currentMonth, currentYear);
}

/*
Transitions calendar to the month and year selected
*/
function jump() {
    currentYear = parseInt(selectYear.value);
    currentMonth = parseInt(selectMonth.value);
    showCalendar(currentMonth, currentYear);
}

/*
Builds a calendar for the passed in month and year
*/
function showCalendar(month, year) {
    let firstDay = (new Date(year, month)).getDay();

    tbl = document.getElementById("calendar-body"); // body of the calendar

    // clearing all previous cells
    tbl.innerHTML = "";

    // filing data about month and in the page via DOM.
    monthAndYear.innerHTML = months[month] + " " + year;
    selectYear.value = year;
    selectMonth.value = month;

    // creating all cells
    let date = 1;
    for (let i = 0; i < 6; i++) {

        // creates a table row
        let row = document.createElement("tr");

        //creating individual cells, filing them up with data.
        for (let j = 0; j < 7; j++) {
            if (i === 0 && j < firstDay) {
                cell = document.createElement("td");
                cellText = document.createTextNode("");
                cell.appendChild(cellText);
                row.appendChild(cell);
            } else if (date > daysInMonth(month, year)) {
                break;
            } else {
                cell = document.createElement("td");
                cellText = document.createTextNode(date);
                cell.appendChild(cellText);
                row.appendChild(cell);
                let isTaken = false;
                for (let taken of takenDates) {
                    if (taken.getMonth() == month && taken.getUTCDate() == date && taken.getFullYear() == year) {
                        isTaken = true;
                    }
                }
                if (isTaken || dateIsInPast(date, month, year)) {
                    cell.classList.add('disabled-date');
                } else {
                    cell.onclick = function() { onCellClick(this) };
                    cell.classList.add('cell');
                }
                date++;
            }
        }
        tbl.appendChild(row); // appending each row into calendar body.
    }
}

function dateIsInPast(date, month, year) {
    if (year < today.getFullYear()) {
        return true;
    }
    if (month < today.getMonth()) {
        return true;
    }
    if (date <= today.getUTCDate()) {
        return true;
    }
    return false;
}

function daysInMonth(iMonth, iYear) {
    return 32 - new Date(iYear, iMonth, 32).getDate();
}

function onCellClick(cell) {
    day = parseInt(cell.innerHTML);
    selectedDate = new Date(currentYear, currentMonth, day);
    if (selectedDate >= today) {
        if (checkinDate == null) {
            setCheckinDate(selectedDate);
        } else if (checkinDate > selectedDate) {
            setCheckoutDate(checkinDate);
            setCheckinDate(selectedDate);
        } else {
            setCheckoutDate(selectedDate);
        }

        if (checkinDate != null && checkoutDate != null) {
            highlightStaySpan();
        }
    }

    label = document.getElementById('testLabel');
    if (checkinDate != null && checkoutDate != null) {
        label.innerHTML = "Checkin Date: " + checkinDate.toUTCString() + "\n" + "Checkout Date: " + checkoutDate.toUTCString();
    }
}

function highlightStaySpan() {
    $("#calendar-body").each(function() {
        $('td', this).each(function() {
            highlightCell(this)
            this.classList.remove('cell');
            this.classList.add('cell-selected');
        })
    })
}

function highlightCell(cell) {
    cell.classList.add('cell');
    cellIsInStayRange = checkinDate.getDate() <= parseInt(cell.innerHTML) && parseInt(cell.innerHTML) <= checkoutDate.getDate();
    if (cellIsInStayRange) {
        cell.classList.add('cell-selected');
    }
}

function datesAreNull() {
    if (checkinDate == null || checkoutDate == null) {
        alert("Invalid Dates");
        return true;
    }
    return false;
}

function setCheckinDate(date) {
    checkinDate = date;
    $("#id_in_date").val(date.toUTCString());
}

function setCheckoutDate(date) {
    checkoutDate = date;
    $("#id_out_date").val(date.toUTCString());
}

$(document).ready(function() {
    $('#calendar-form').submit(function(event) {
        if (datesAreNull()) {
            event.preventDefault();
        }
    });

});