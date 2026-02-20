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
    const scriptResponse = await fetch("../assets/LPS_web.py");
    if (!scriptResponse.ok) document.getElementById("output").textContent = "Loading failed.";
    if (!scriptResponse.ok) alert("Python load failed: " + scriptResponse.status);
    const scriptCode = await scriptResponse.text();
    await pyodide.runPythonAsync(scriptCode);


    print("Loading CSV...", "add");
    const csvResponse = await fetch("https://end0832.github.io/LPS/" + subdomain + "/data.csv");
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
    print("Loaded.", "replace");

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
