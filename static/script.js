// // timer which will display when we make fetch request or automation request
// const timerElement = document.createElement('div');
// timerElement.id = 'timer';
// timerElement.style.display = 'block';
// // message for client for not close the window, becuase automation takes time according to provided record size, internet connectivity, loading etc. sometimes it can take more than 30 mins for 150 websites.
// const timerTag = document.createElement('p');
// timerTag.id = 'automationInfo';
// timerTag.textContent = "Please wait! Automation takes some time according to your data and website complexity.";

// // top header of automation report
// const reportsMainHeader = document.createElement('h2');
// reportsMainHeader.id = "reportsMainHeader";
// reportsMainHeader.textContent = "Automation Report";

// // we will display the report in two sub reports for better understanding
// const reportSubHeader1 = document.createElement('h3');
// reportSubHeader1.id = "reportSubHeader1";
// reportSubHeader1.textContent = "Report";
// const reportSubHeader2 = document.createElement('h3');
// reportSubHeader2.id = "reportSubHeader2";
// reportSubHeader2.textContent = "Detailed Failed Automation Report";

// // tables for entring the report data
// const table1 = document.createElement('table');
// const table2 = document.createElement('table');

// const errorMessage = document.createElement('div')
// errorMessage.id = 'error-message'

// apply event listener, so that we will notified when user uploads and submit the form.


document.getElementById("inputForm").addEventListener("submit", function (e) {
    // e.preventDefault();

    // // now inject the required, updared HTML one by one 
    // document.getElementById("fetchBanner").appendChild(timerElement);
    // document.getElementById("fetchBanner").appendChild(timerTag);

    // // Clear out previous content
    // const report1 = document.getElementById('report1');
    // const report2 = document.getElementById('report2');
    // const reportsHeader = document.getElementById("reportsHeader");

    // // clear previous headers and tables
    // report1.innerHTML = "";  // clear previous content in report1
    // report2.innerHTML = "";  // clear previous content in report2
    // reportsHeader.innerHTML = "";  // clear previous report headers
    // errorMessage.innerHTML = ""
    // document.getElementById("horizonLine").style.display = "none"; // Hide the horizon line

    // console.log(report1.innerHTML)
    // console.log(report2.innerHTML)

    // const table1Header = document.createElement('tr');
    // const table2Header = document.createElement('tr');
    // const headers1 = ['Description', 'Total Number'];
    // const headers2 = ['Errors', 'In Total Websites'];

    // headers1.forEach(headerText => {
    //     const th = document.createElement('th');
    //     th.textContent = headerText;
    //     table1Header.appendChild(th);
    // });

    // headers2.forEach(headerText => {
    //     const th = document.createElement('th');
    //     th.textContent = headerText;
    //     table2Header.appendChild(th);
    // });

    const form = document.getElementById("inputForm");
    const formData = new FormData(form);

    // startTimer(10);  // Start the timer

    // Fetch data from the automation API
    fetch('/automate/contact_us', {
        method: 'POST',
        body: formData
    }).then(response => {
        if (response.status !== 200) {
            return response.json().then(data => {
                throw new Error(data.message);
            });
        }
        // If status is OK, return the response as JSON
        return response.json();
    }).then(data => {
        data = data['report'];

        // // Stop the timer and remove timer-related elements
        // stopTimer();
        // timerElement.remove();
        // timerTag.remove();

        // // Display the horizon line and set up the report headers
        // document.getElementById("horizonLine").style.display = "block";

        // // Append the main header and setup the first report
        // reportsHeader.appendChild(reportsMainHeader);

        // report1.appendChild(reportSubHeader1)
        // table1.appendChild(table1Header);  // Append table header to table1
        // report1.appendChild(table1);  // Append table1 to report1

        // // Populate table1 with data
        // Object.entries(data).forEach(([key, val]) => {
        //     if (key === 'Total Faild Automation by Reason') {
        //         return;  // Skip the loop for this key
        //     }
        //     const row = document.createElement('tr');
        //     const cell1 = document.createElement('td');
        //     const cell2 = document.createElement('td');

        //     cell1.textContent = key;
        //     cell2.textContent = val;
        //     row.appendChild(cell1);
        //     row.appendChild(cell2);

        //     table1.appendChild(row);
        // });

        // // Setup the second report (table2 for detailed failure reasons)
        // report2.appendChild(reportSubHeader2);
        // table2.appendChild(table2Header);  // Append table2Header to table2
        // report2.appendChild(table2);  // Append table2 to report2

        // // Populate table2 with detailed failure reasons
        // Object.entries(data).forEach(([key, val]) => {
        //     if (key === 'Total Faild Automation by Reason') {
        //         Object.entries(val).forEach(([reason, count]) => {
        //             const row = document.createElement('tr');
        //             const cell1 = document.createElement('td');
        //             const cell2 = document.createElement('td');

        //             cell1.textContent = reason;
        //             cell2.textContent = count;
        //             row.appendChild(cell1);
        //             row.appendChild(cell2);

        //             table2.appendChild(row);
        //         });
        //     }
        // });

    }).catch(error => {
        console.log(error)
        // stopTimer();  // Stop the timer on error
        // timerElement.remove();
        // timerTag.remove();  // Remove the informational message
        // errorMessage.innerHTML = `<pre>${error.message}</pre>`
        // document.body.appendChild(errorMessage)
    });
});

// // Timer functionality
// let countdownInterval;  // Global variable to store the timer interval

// // Function to start a countdown timer in minutes
// function startTimer(minutes) {
//     let time = minutes * 60; // Convert minutes to seconds

//     function updateTimer() {
//         const minutesLeft = Math.floor(time / 60);
//         const secondsLeft = time % 60;

//         // Update the timer display
//         timerElement.innerHTML = `Time left: ${minutesLeft}:${secondsLeft < 10 ? '0' : ''}${secondsLeft}`;

//         // Decrease time by 1 second
//         time--;

//         // Reset the timer when time runs out
//         if (time < 0) {
//             time = minutes * 60;  // Reset to initial time
//         }
//     }

//     // Update the timer every second
//     countdownInterval = setInterval(updateTimer, 1000);
//     updateTimer();  // Run the first instance immediately
// }

// // Function to stop the timer
// function stopTimer() {
//     clearInterval(countdownInterval);  // Clear the interval to stop the countdown
// }
