const api_addr = "http://127.0.0.1"
const api_exp = api_addr + "/matrix/power"

async function apiFetchJSON(data, path, method) {
    let req = {
        method: method,
        headers: {
            'Content-Type': 'application/json',
        },
    }
    if (data != null) req.body = JSON.stringify(data);

    const response = await fetch(path, req);
    return await response.json();
}

function operationSelect() {
    let selected = document.getElementById('operationSelect').value
    console.log(selected)
}

function generateMatrix() {
    const size = Number(document.getElementById('sizeInput').value);
    if (size < 2 || size > 10) {
        document.getElementById('sizeInput').value = 2
        alert("Size must be between 2 and 10.");
        return;
    }
    
    const matrixContainer = document.getElementById('matrixContainer');
    matrixContainer.innerHTML = ''; // Clear previous matrix
    
    for (let i = 0; i < size; i++) {
        const row = document.createElement('div');
        for (let j = 0; j < size; j++) {
            const input = document.createElement('input');
            input.type = 'number';
            input.name = `cell-${i}-${j}`;
            input.required = true;
            row.appendChild(input);
        }
        matrixContainer.appendChild(row);
    }
}

function matrixToTable(matrix) {
    const matrixContainer = document.getElementById('matrixResultContainer');
    matrixContainer.innerHTML = ''
    const table = document.createElement('table');
    const tbody = document.createElement('tbody');

    for (row of matrix) {
        const tr = document.createElement('tr');
        for (elem of row) {
            const td = document.createElement('td');
            td.textContent = elem.toString()
            tr.appendChild(td);
        }
        tbody.appendChild(tr);
    }

    const h = document.createElement("H3");
    const t = document.createTextNode("Result Matrix:");
    h.appendChild(t);
    matrixContainer.appendChild(h)

    table.appendChild(tbody);
    matrixContainer.appendChild(table);
}

function submitMatrix(event) {
    event.preventDefault();

    const exponent = Number(document.getElementById('exponentInput').value);
    if (!Number.isInteger(exponent)) {
        alert("Exponent must be an integer.")
        return
    }
    if (exponent < 2) {
        alert("Exponent value must be >= 2.")
        return
    }
    
    const inputs = document.querySelectorAll('#matrixContainer input');
    const matrix = [];
    inputs.forEach(input => {
        const [_, i, j] = input.name.split('-');
        if (!matrix[i]) matrix[i] = [];
        matrix[i][j] = Number(input.value);
    });
    
    window.console.log(matrix);

    apiFetchJSON(
        {  
            "matrix": matrix,
            "exponent": exponent
        },
        api_exp,
        'POST'
    )
    .then(data => {
        apiFetchJSON(null, api_exp+"?id="+data.id, 'GET')
            .then(data => matrixToTable(data.result.matrix))
    })
    .catch(error => console.error('Error:', error));
}

window.onload = generateMatrix