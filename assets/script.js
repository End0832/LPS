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

function error(err, pmsg, amsg) {
    print(pmsg, "replace");
    alert(`${amsg}:\n${err.message}`);
    throw err;
}

print("Loading Pyodide...", "replace");
let pyodideReady = loadPyodide();

async function init() {
    const pyodide = await pyodideReady;


    print("Loading Python...", "add");
    try {
        const scriptResponse = await fetch("https://end0832.github.io/LPS/assets/LPS.py");
        await pyodide.runPythonAsync(`local = False`);
        const scriptCode = await scriptResponse.text();
        await pyodide.runPythonAsync(scriptCode);
    } catch(err) {
        error(err, "Loading failed.", "Python load failed");
    }


    print("Loading CSV...", "add");
    try {
        const csvResponse = await fetch("https://end0832.github.io/LPS/" + subdomain + "/data.csv");
        const csvText = await csvResponse.text();
        pyodide.globals.set("csv_text", csvText);
    
        let titles = await pyodide.runPythonAsync(`matrix = Matrix(csv_text)\nmatrix.get_titles()`);
    
        let fromBox = document.getElementById("from_box");
        let toBox = document.getElementById("to_box");
    
        titles.forEach(t => {
            fromBox.add(new Option(t, t));
            toBox.add(new Option(t, t));
        });
    } catch(err) {
        error(err, "Loading failed.", "CSV load failed");
    }


    print("Trying...", "replace");
    try {
        await runLPS();
        print("Loaded.", "replace");
    } catch(err) {
        error(err, "Error.", "Test failed");
    }
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
lps.get(matrix.get_title_pos(from_box_val), matrix.get_title_pos(to_box_val))
`);
    print(result, "replace");
}

init();
