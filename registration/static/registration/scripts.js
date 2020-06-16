today = new Date();
currentMonth = today.getMonth();
currentYear = today.getFullYear();
selectYear = document.getElementById("year");
selectMonth = document.getElementById("month");
checkinDate = null;
checkoutDate = null;

months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];

monthAndYear = document.getElementById("monthAndYear");
showCalendar(currentMonth, currentYear);

function next() {
    currentYear = (currentMonth === 11) ? currentYear + 1 : currentYear;
    currentMonth = (currentMonth + 1) % 12;
    showCalendar(currentMonth, currentYear);
}

function previous() {
    currentYear = (currentMonth === 0) ? currentYear - 1 : currentYear;
    currentMonth = (currentMonth === 0) ? 11 : currentMonth - 1;
    showCalendar(currentMonth, currentYear);
}

function jump() {
    currentYear = parseInt(selectYear.value);
    currentMonth = parseInt(selectMonth.value);
    showCalendar(currentMonth, currentYear);
}

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
                if (date === today.getDate() && year === today.getFullYear() && month === today.getMonth()) {
                    cell.classList.add("bg-info");
                } // color today's date
                cell.appendChild(cellText);
                row.appendChild(cell);
                date++;
            }
            cell.onclick = function() {onCellClick(this)};
        }

        tbl.appendChild(row); // appending each row into calendar body.
    }
}

function daysInMonth(iMonth, iYear) {
    return 32 - new Date(iYear, iMonth, 32).getDate();
}

function onCellClick(cell) {
    day = parseInt(cell.innerHTML);
    selectedDate = new Date(currentYear, currentMonth, day);
    if(selectedDate >= today) {
        if(checkinDate == null) {
            setCheckinDate(selectedDate);
        } else if(checkinDate > selectedDate) {
            setCheckoutDate(checkinDate);
            setCheckinDate(selectedDate);
        } else {
            setCheckoutDate(selectedDate);
        }

        if(checkinDate != null && checkoutDate != null) {
            highlightStaySpan();
        }
    }

    label = document.getElementById('testLabel');
    label.innerHTML = "Checkin Date: " + checkinDate.toString() + "\n" +  "Checkout Date: " + checkoutDate.toString();
}

function setCheckinDate(date) {
    checkinDate = date;
    $("#id_in_date").val(date);
}

function setCheckoutDate(date) {
    checkoutDate = date;
    $("#id_out_date").val(date);
}

function highlightStaySpan() {
    days = document.getElementById('calendar-body');
    passedCheckinDate = false;
    for (let row of days.rows) {
        for(let cell of row.cells) {
            cell.style.backgroundColor="transparent";
            passedCheckinDate = checkinDate.getDate() <= parseInt(cell.innerHTML) && parseInt(cell.innerHTML) <= checkoutDate.getDate();
            if(passedCheckinDate) {
                cell.style.backgroundColor = "lightseagreen";
            }
        }
    }
}

/*

*/

function checkDates() {
    if(checkinDate == null || checkoutDate == null) {
        alert("Invalid Dates");
        return false;
    }
    return true;
}

$( document ).ready(function() {
    
    $('#calendar-form').submit(function(event) {
        if(!checkDates()) {
            event.preventDefault();
        }
    })
});