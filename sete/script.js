document.getElementById("output").textContent = "Loading Pyodide...";
let pyodideReady = loadPyodide();

async function init() {
    const pyodide = await pyodideReady;


    document.getElementById("output").textContent = "Loading Python...";
    const scriptResponse = await fetch("../assets/LPS_web.py");
    if (!scriptResponse.ok) document.getElementById("output").textContent = "Loading failed.";
    if (!scriptResponse.ok) alert("Python load failed: " + scriptResponse.status);
    const scriptCode = await scriptResponse.text();
    await pyodide.runPythonAsync(scriptCode);


    document.getElementById("output").textContent = "Loading CSV...";
    const csvResponse = await fetch("data.csv");
    if (!csvResponse.ok) document.getElementById("output").textContent = "Loading failed.";
    if (!csvResponse.ok) alert("CSV load failed: " + csvResponse.status);
    const csvText = await csvResponse.text();
    pyodide.globals.set("csv_text", csvText);

    
    let titles = await pyodide.runPythonAsync(`
matrix = Matrix(csv_text)
matrix.get_titles()
`);

    let startMenu = document.getElementById("start");
    let endMenu = document.getElementById("end");
    document.getElementById("output").textContent = "Loaded.";

    titles.forEach(t => {
        startMenu.add(new Option(t, t));
        endMenu.add(new Option(t, t));
    });
}

async function runLPS() {
    const pyodide = await pyodideReady;

    let start = document.getElementById("start").value;
    let end = document.getElementById("end").value;

    pyodide.globals.set("start_name", start);
    pyodide.globals.set("end_name", end);

    let result = await pyodide.runPythonAsync(`
matrix = Matrix(csv_text)
lps = Dijkstra(matrix.get(), matrix.get_titles())
lps.get(matrix.title_position(start_name), matrix.title_position(end_name))
`);

    document.getElementById("output").textContent = result;
}

init();
