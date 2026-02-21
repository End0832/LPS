let subdomain = window.location.pathname.split("/").filter(s => s.length > 0)
subdomain = subdomain[subdomain.length - 1]

function print(text, arg) {
    if (arg === "add") {
        document.getElementById("output").textContent = document.getElementById("output").textContent + "\n" + text;
    }
    if (arg === "replace") {
        document.getElementById("output").textContent = text;
    }
}

print("Loading Pyodide...", "replace");
let pyodideReady = loadPyodide();

async function init() {
    const pyodide = await pyodideReady;


    print("Loading Python...", "add");
    const scriptResponse = await fetch("https://end0832.github.io/LPS/assets/LPS.py");
    if (!scriptResponse.ok) {
        print("Loading failed.", "replace");
        alert("Python load failed: " + scriptResponse.status);
    }
    pyodide.globals.set("local", False)
    const scriptCode = await scriptResponse.text();
    await pyodide.runPythonAsync(scriptCode);


    print("Loading CSV...", "add");
    const csvResponse = await fetch("https://end0832.github.io/LPS/" + subdomain + "/data.csv");
    if (!csvResponse.ok) {
        print("Loading failed.", "replace");
        alert("CSV load failed: " + csvResponse.status);
    }
    const csvText = await csvResponse.text();
    pyodide.globals.set("csv_text", csvText);

    
    let titles = await pyodide.runPythonAsync(`
matrix = Matrix(csv_text)
matrix.get_titles()
`);

    let fromBox = document.getElementById("from_box");
    let toBox = document.getElementById("to_box");
    print("Loaded.", "replace");

    titles.forEach(t => {
        fromBox.add(new Option(t, t));
        toBox.add(new Option(t, t));
    });
}

async function runLPS() {
    const pyodide = await pyodideReady;

    let fromBoxVal = document.getElementById("from_box").value;
    let toBoxVal = document.getElementById("to_box").value;

    pyodide.globals.set("from_box_val", fromBoxVal);
    pyodide.globals.set("to_box_val", toBoxVal);

    let result = await pyodide.runPythonAsync(`
matrix = Matrix(csv_text)
lps = Dijkstra(matrix.get(), matrix.get_titles())
lps.get(matrix.title_position(from_box_val), matrix.title_position(to_box_val))
`);

    print(result, "replace");
}

init();
