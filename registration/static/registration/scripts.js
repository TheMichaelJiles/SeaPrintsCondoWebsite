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

Date.prototype.addDays = function(days) {
    var date = new Date(this.valueOf());
    date.setDate(date.getDate() + days);
    return date;
}

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
        showCalendar(currentMonth, currentYear);
    });
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

    tbl = document.getElementById("calendar-body");
    tbl.innerHTML = "";

    monthAndYear.innerHTML = months[month] + " " + year;
    selectYear.value = year;
    selectMonth.value = month;

    let date = 1;
    for (let i = 0; i < 6; i++) {
        let row = document.createElement("tr");

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

                if (dateIsAvailable(date, month, year)) {
                    cell.onclick = function() { onCellClick(this) };
                    cell.className = 'cell';
                } else {
                    cell.className = 'cell-disabled';
                }
                date++;
            }
        }
        tbl.appendChild(row);
    }

    if(checkinDate != null && checkoutDate != null) {
        highlightStaySpan();
    }
}

function dateIsAvailable(date, month, year) {
    return !dateIsTaken(date, month, year) && !dateIsInPast(date, month, year);
}

function dateIsTaken(date, month, year) {
    for (let taken of takenDates) {
        if (taken.getMonth() == month && taken.getUTCDate() == date && taken.getFullYear() == year) {
            return true;
        }
    }
    return false;
}

function dateIsInPast(date, month, year) {
    tempDate = new Date(year, month, date);
    return tempDate < today;
}

function daysInMonth(iMonth, iYear) {
    return 32 - new Date(iYear, iMonth, 32).getDate();
}

function onCellClick(cell) {
    if (checkinDate != null && checkoutDate != null) {
        checkinDate = null;
        checkoutDate = null;
        highlightStaySpan();
    }

    day = parseInt(cell.innerHTML);
    selectedDate = new Date(currentYear, currentMonth, day);
    if (selectedDate >= today) {
        if (checkinDate == null) {
            setCheckinDate(selectedDate);
            cell.className = 'cell-selected';
        } else if (checkinDate > selectedDate) {
            setCheckoutDate(checkinDate);
            setCheckinDate(selectedDate);
        } else {
            if (takenDatesBetween(checkinDate, selectedDate)) {
                checkinDate = null;
                checkoutDate = null;
                highlightStaySpan();
            } else {
                setCheckoutDate(selectedDate);
            }
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

function takenDatesBetween(checkinDate, checkoutDate) {
    dateSpan = getDateSpan(checkinDate, checkoutDate);
    for (date in dateSpan) {
        if (takenDates.includes(date)) {
            return true;
        }
    }
    return false;
}

function getDateSpan(startDate, stopDate) {
    var dateArray = new Array();
    var currentDate = startDate;
    while (currentDate <= stopDate) {
        dateArray.push(new Date (currentDate));
        currentDate = currentDate.addDays(1);
    }
    return dateArray;
}

function highlightStaySpan() {
    $("#calendar-body").each(function() {
        $('td', this).each(function() {
            styleCell(this)
        })
    })
}

function styleCell(cell) {
    cell.className = '';
    date = parseInt(cell.innerHTML);
    if (cellIsInStayRange(date)) {
        cell.className = 'cell-selected';
    } else if(dateIsAvailable(date, selectMonth.value, selectYear.value)) {
        cell.className = 'cell';
    } else {
        cell.className = 'cell-disabled';
    }
}

function cellIsInStayRange(date) {
    currentDate = new Date(currentYear, currentMonth, date);
    return checkinDate <= currentDate && currentDate <= checkoutDate;
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