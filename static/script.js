const matrixSizeContainer = document.getElementById('matrixSizeContainer')
const matrixContainer = document.getElementById('matrixContainer')
const operandContainer = document.getElementById('operandContainer')

const operationMap = new Map([
    [
        "power", 
        {
            apiPath: "/matrix/power",
            operandName: "exponent",
            getBody: function () {
                const exponent = Number(document.getElementById('exponentInput').value);
                if (!Number.isInteger(exponent)) {
                    alert("Exponent must be an integer.")
                    return null
                }
                if (exponent < 2) {
                    alert("Exponent value must be >= 2.")
                    return null
                }
                return {
                    "matrix": inputsToMatrix(),
                    "exponent": exponent
                }
            },
            setLayout: function() {
                setSquareMatrixLayout()
                setSquareMatrix()
                operandContainer.innerHTML = '' +
                '<label for="Exponent">Exponent:</label>' +
                '<input id="exponentInput" name="Exponent" type="number" min="2" value="2">'
            }
        }
    ],
    [
        "multiplication_scalar", 
        {
            apiPath: "/matrix/multiplication/scalar",
            operandName: "scalar",
            getBody: function () {
                const val = Number(document.getElementById('scalarInput').value);
                return {
                    "matrix": inputsToMatrix(),
                    "scalar": val
                }
            },
            setLayout: function() {
                setMatrixLayout()
                setMatrix()
                operandContainer.innerHTML = '' +
                '<label for="Scalar">Scalar:</label>' +
                '<input id="scalarInput" name="Scalar" type="number" value="2">'
            }
        }
    ],
])

var currentOperation = document.getElementById('operationSelect').value

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
    currentOperation = operationMap.get(document.getElementById('operationSelect').value)
    console.log(currentOperation)
    currentOperation.setLayout()
}

function setMatrixLayout() {
    matrixSizeContainer.innerHTML = '' +
        '<label for="MatrixRows">Matrix size:</label>' +
        '<input name="MatrixRows" onchange="setMatrix()" id="rowInput" type="number" min="2" max="10" value="2"></input>' +
        '<label for="MatrixColumns">X</label>' +
        '<input name="MatrixColumns" onchange="setMatrix()" id="columnInput" type="number" min="2" max="10" value="2"></input>'

}

function setSquareMatrixLayout() {
    matrixSizeContainer.innerHTML = '' +
    '<label for="MatrixSize">Matrix size:</label>' +
    '<input name="MatrixSize" onchange="setSquareMatrix()" id="sizeInput" type="number" min="2" max="10" value="2"></input>'
}

function setMatrix() {
    const rows = inputClamp('rowInput', 2, 10)
    const columns = inputClamp('columnInput', 2, 10)
    if ( rows && columns) generateMatrix(rows, columns)
    else {
        document.getElementById('rowInput').value = 2
        document.getElementById('columnInput').value = 2
        generateMatrix(2, 2)
    }
}

function setSquareMatrix() {
    const size = inputClamp('sizeInput', 2, 10)
    if (size) generateMatrix(size, size)
    else generateMatrix(2, 2)
}

function inputClamp(elementId, min, max) {
    const val = Number(document.getElementById(elementId).value);
    if (val < min || val > max) {
        document.getElementById(elementId).value = min
        alert("Size must be between 2 and 10.");
        return null;
    }
    return val
}

function generateMatrix(rows, columns) {
    matrixContainer.innerHTML = ''; // Clear previous matrix
    
    for (let i = 0; i < rows; i++) {
        const row = document.createElement('div');
        for (let j = 0; j < columns; j++) {
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

function inputsToMatrix() {
    const inputs = document.querySelectorAll('#matrixContainer input');
    const matrix = [];
    inputs.forEach(input => {
        const [_, i, j] = input.name.split('-');
        if (!matrix[i]) matrix[i] = [];
        matrix[i][j] = Number(input.value);
    });
    return matrix
}

function submitMatrix(event) {
    event.preventDefault();
    
    const body = currentOperation.getBody()
    if (body == null) return

    apiFetchJSON(
        body,
        currentOperation.apiPath,
        'POST'
    )
    .then(data => {
        apiFetchJSON(null, currentOperation.apiPath+"?id="+data.id, 'GET')
            .then(data => matrixToTable(data.result.matrix))
    })
    .catch(error => console.error('Error:', error));
}

window.onload = operationSelect
