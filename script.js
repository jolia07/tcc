const daysContainer = document.getElementById("days");
const monthYear = document.getElementById("month-year");
const prevBtn = document.getElementById("prev");
const nextBtn = document.getElementById("next");

const months = [
    "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
    "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"
];

let currentDate = new Date();

function renderCalendar() {
    daysContainer.innerHTML = "";
    let firstDay = new Date(currentDate.getFullYear(), currentDate.getMonth(), 1).getDay();
    let lastDate = new Date(currentDate.getFullYear(), currentDate.getMonth() + 1, 0).getDate();

    monthYear.innerText = `${months[currentDate.getMonth()]} ${currentDate.getFullYear()}`;

    for (let i = 0; i < firstDay; i++) {
        let emptyDiv = document.createElement("div");
        daysContainer.appendChild(emptyDiv);
    }

    for (let day = 1; day <= lastDate; day++) {
        let dayDiv = document.createElement("div");
        dayDiv.innerText = day;
        daysContainer.appendChild(dayDiv);
    }
}

prevBtn.addEventListener("click", () => {
    currentDate.setMonth(currentDate.getMonth() - 1);
    renderCalendar();
});

nextBtn.addEventListener("click", () => {
    currentDate.setMonth(currentDate.getMonth() + 1);
    renderCalendar();
});

renderCalendar();
