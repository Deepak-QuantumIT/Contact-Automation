const timerElement = document.createElement('div');
timerElement.id = 'timer';
timerElement.style.display = 'block';
const timerTag = document.createElement('p');
timerTag.id = 'automationInfo';
timerTag.textContent = "Automation Under Process! We will notify you by email with Automation Report when process completed.";

const errorMessage = document.createElement('div')
errorMessage.id = 'error-message'

document.getElementById("inputForm").addEventListener("submit", function (e) {
    e.preventDefault();

    document.getElementById("fetchBanner").appendChild(timerElement);
    document.getElementById("fetchBanner").appendChild(timerTag);

    errorMessage.remove()

    const form = document.getElementById("inputForm");
    const formData = new FormData(form);

    fetch('/automate/contact_us', {
        method: 'POST',
        body: formData
    }).then(response => {
        if (response.status !== 200) {
            return response.json().then(data => {
                throw new Error(data.message);
            });
        }
        return response.json();
    }).then(data => {
        data = data['report'];
        timerElement.remove();
        timerTag.remove();

    }).catch(error => {
        console.log(error)
        timerElement.remove();
        timerTag.remove();
        errorMessage.innerHTML = `<pre>${error.message}</pre>`
        document.body.appendChild(errorMessage)
    });
})