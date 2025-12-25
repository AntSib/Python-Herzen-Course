const socket = io();
const table = document.getElementById("rates-table");
const form = document.getElementById("codes-form");
const input = document.getElementById("codes-input");

const subscribedCodes = new Set();

/* === CONNECT === */

socket.on("client_id", data => {
    document.getElementById("client-id").textContent = data.client_id;
});

/* === UPDATES FROM SERVER === */

socket.on("rates_update", rates => {
    rates.forEach(rate => {
        if (subscribedCodes.has(rate.char_code)) {
            updateRow(rate);
        }
    });
});

/* === FORM SUBMIT === */

form.addEventListener("submit", e => {
    e.preventDefault();

    const codes = input.value
        .replace(/,/g, '')
        .toUpperCase()
        .split(/\s+/)
        .filter(Boolean);

    if (!codes.length) return;

    codes.forEach(c => subscribedCodes.add(c));
    socket.emit("subscribe", { codes });

    fetch("/fetch", {
        method: "POST",
        body: new URLSearchParams({ codes: codes.join(" ") })
    })
    .then(r => r.json())
    .then(data => {
        data.rates.forEach(updateRow);
    });
    input.value = "";
});

/* === TABLE BUILDERS === */

function updateRow(rate) {
    let row = document.getElementById(rate.char_code);

    if (!row) {
        row = document.createElement("tr");
        row.id = rate.char_code;
        row.innerHTML = `
            <td>${rate.char_code}</td>
            <td class="rate"></td>
            <td class="date"></td>
            <td>
              <button data-code="${rate.char_code}">Удалить</button>
            </td>
        `;
        row.querySelector("button").onclick = removeRow;
        table.appendChild(row);
    }

    row.querySelector(".rate").textContent = rate.rate;
    row.querySelector(".date").textContent = rate.datetime;
}

function removeRow(e) {
    const code = e.target.dataset.code;
    subscribedCodes.delete(code);
    document.getElementById(code)?.remove();
    socket.emit("unsubscribe", { code });
}
