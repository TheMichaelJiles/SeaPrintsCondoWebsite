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

/**
 * Function executed when the webpage is loaded. JSON request must happen BEFORE showCalendar
 */
function init() {
    $.getJSON("/registration/get_taken_dates/", function(dateData) {
        for (let date of dateData) {
            let currentDate = new Date(date);
            takenDates.push(currentDate);
        }
        showCalendar(currentMonth, currentYear);
    });
}

/**
 * Transitions calendar to the next month, incrementing the year if necessary
 */
function next() {
    currentYear = (currentMonth === 11) ? currentYear + 1 : currentYear;
    currentMonth = (currentMonth + 1) % 12;
    showCalendar(currentMonth, currentYear);
}

/**
 * Transitions calendar to the previous month, devrementing the year if necessary
 */
function previous() {
    currentYear = (currentMonth === 0) ? currentYear - 1 : currentYear;
    currentMonth = (currentMonth === 0) ? 11 : currentMonth - 1;
    showCalendar(currentMonth, currentYear);
}

/**
 * Transitions calendar to the month and year selected
 */
function jump() {
    currentYear = parseInt(selectYear.value);
    currentMonth = parseInt(selectMonth.value);
    showCalendar(currentMonth, currentYear);
}

/**
 * Builds a calendar for the passed in month and year
 * @param month the month for the calendar
 * @param year the year for the calendar
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

    if (checkinDate != null && checkoutDate != null) {
        highlightStaySpan();
    }
}

/**
 * Checks if a given date is not taken and is not in the past
 * @param date the day of the month of the date
 * @param month the month of the date
 * @param year the year of the date
 */

function dateIsAvailable(date, month, year) {
    return !dateIsTaken(date, month, year) && !dateIsInPast(date, month, year);
}

/**
 * Checks if a date is present in the takenDates list
 * @param date the day of the month of the date
 * @param month the month of the date
 * @param year the year of the date
 */
function dateIsTaken(date, month, year) {
    for (let taken of takenDates) {
        if (taken.getMonth() == month && taken.getUTCDate() == date && taken.getFullYear() == year) {
            return true;
        }
    }
    return false;
}

/**
 * Checks if a date is in the past
 * @param date the day of the month of the date
 * @param month the month of the date
 * @param year the year of the date
 */
function dateIsInPast(date, month, year) {
    tempDate = new Date(year, month, date);
    return tempDate < today;
}

/**
 * Returns the number of days in the month of the passed in year
 * @param iMonth the month to be checked 
 * @param iYear the year the month is in
 */
function daysInMonth(iMonth, iYear) {
    return 32 - new Date(iYear, iMonth, 32).getDate();
}

/**
 * Event to fire when a cell is clicked. This method will evaluate the input,
 * assign the checkin and checkout dates, and format the cells if necessary
 * @param cell the cell that was clicked
 */
function onCellClick(cell) {
    if (checkinDate != null && checkoutDate != null) {
        resetCalendar();
    }

    day = parseInt(cell.innerHTML);
    selectedDate = new Date(currentYear, currentMonth, day);
    if (selectedDate >= today) {
        assignCheckinAndCheckoutDates(selectedDate, cell);
    }

    displayTestLabel();
}

/**
 * Handles the assignmend of checkin and checkout dates and formats cells
 * if necessary
 * @param {*} selectedDate The date selected by the user
 * @param {*} cell the cell that was clicked 
 */
function assignCheckinAndCheckoutDates(selectedDate, cell) {
    if (checkinDate == null) {
        setCheckinDate(selectedDate);
        cell.className = 'cell-selected';
    } else if (checkinDate > selectedDate) {
        if (takenDatesBetween(selectedDate, checkinDate)) {
            resetCalendar();
            alert('Dates conflict with another stay, please select a new range.');
        } else {
            setCheckoutDate(checkinDate);
            setCheckinDate(selectedDate);
        }
        highlightStaySpan();
    } else {
        if (takenDatesBetween(checkinDate, selectedDate)) {
            resetCalendar();
            alert('Dates conflict with another stay, please select a new range.');
        } else {
            setCheckoutDate(selectedDate);
        }
        highlightStaySpan();
    }
}

/**
 * Function to reset the calendar. Checkin and checkout dates are
 * set to null, and all days are cleared using the highlightStaySpan function
 */
function resetCalendar() {
    checkinDate = null;
    checkoutDate = null;
    highlightStaySpan();
}

/**
 * Returns whether or not there is a taken date between dateOne and dateTwo
 * @param startDate  the startDate 
 * @param endDate  the endDate 
 */
function takenDatesBetween(startDate, endDate) {
    for (let taken of takenDates) {
        console.log(taken);
        if (startDate <= taken && taken <= endDate) {
            console.log(taken + " was in range");
            return true;
        }
    }
    return false;
}

/**
 * Iterates over all cells in the calendar, highlighting the cell if
 * it falls between the checkin and checkout dates, and removing the
 * highlight if the date is not in that range or the checkin or checkout
 * date is null
 */
function highlightStaySpan() {
    $("#calendar-body").each(function() {
        $('td', this).each(function() {
            styleCell(this)
        });
    });
}

/**
 * Styles the cell according to if the date is available, unavailable, or in stay range
 * @param cell the cell to be styled
 */
function styleCell(cell) {
    date = parseInt(cell.innerHTML);
    if (cellIsInStayRange(date)) {
        cell.className = 'cell-selected';
    } else if (dateIsAvailable(date, selectMonth.value, selectYear.value)) {
        cell.className = 'cell';
    } else {
        cell.className = 'cell-disabled';
    }
}

/**
 * Returns whether or not the cell is in the stay range
 * @param date the innerHTML of the current cell
 */
function cellIsInStayRange(date) {
    currentDate = new Date(currentYear, currentMonth, date);
    return checkinDate <= currentDate && currentDate <= checkoutDate;
}

/**
 * Checks if the checkin and checkout dates are null, and alerts the user if they are
 */
function datesAreNull() {
    if (checkinDate == null || checkoutDate == null) {
        alert("Invalid Dates");
        return true;
    }
    return false;
}

/**
 * Sets the checkinDate
 * @param date the new checkinDate 
 */
function setCheckinDate(date) {
    checkinDate = date;
    $("#id_in_date").val(date.toUTCString());
}

/**
 * Sets the checkoutDate
 * @param date the new checkoutDate 
 */
function setCheckoutDate(date) {
    checkoutDate = date;
    $("#id_out_date").val(date.toUTCString());
}

/**
 * Handles submission and validation of the form
 */
$(document).ready(function() {
    $('#calendar-form').submit(function(event) {
        if (datesAreNull()) {
            event.preventDefault();
        }
    });
    init();
});

/**
 * Displays a test label, this is for simple debugging
 */
function displayTestLabel() {
    if (checkinDate != null && checkoutDate != null) {
        label = document.getElementById('testLabel');
        label.innerHTML = "Checkin Date: " + checkinDate.toUTCString() + "\n" + "Checkout Date: " + checkoutDate.toUTCString();
    }
}