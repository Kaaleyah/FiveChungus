function upload() {
    let {PythonShell} = require("python-shell");
    let path = require("path")

    var options = {
        scripthPath : path.join(__dirname, "/../engine"),
        args : []
    }

    let pyshell = new PythonShell("Chunk_Uploader.py", options)

    pyshell.on("message", function(message) {
        document.getElementById("uploadConsole").innerHTML +=  message + "<br>"
    })
}
