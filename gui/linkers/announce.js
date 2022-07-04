//  Announce  \\
function logAnnounce() {
    var fs = require("fs")
    var announcedFiles = fs.readdirSync("../announcedFiles/")

    var announcedUL = document.getElementById("announceConsole")

    announcedUL.innerHTML = ""

    announcedFiles.forEach(element => {
        var li = document.createElement("li")
        li.appendChild(document.createTextNode(element))
        announcedUL.appendChild(li)
    });
}

function announce(file = "5165") {
    let {PythonShell} = require("python-shell");
    let path = require("path")

    if (file == "5165") {
        var announcedFile = document.getElementById("toBeAnnounced").value
    }
    else {
        var announcedFile = file
    }

    var options = {
        scriptPath : path.join(__dirname, "/../engine/"),
        args : [announcedFile]
    }

    let pyshell = new PythonShell("Chunk_Announcer.py", options)

    pyshell.on('message', function(message) {
        console.log(message);
    })

    document.getElementById("toBeAnnounced").value = ""
    
}

//  Disover  \\
function logDiscover() {
    const fs = require('fs')

    fs.readFile("../engine/contentDictionary.txt", { encoding: "utf-8" }, function(err, data) {
        if (!err) {
            console.log(data);

            var discoverConsole = document.getElementById("discoverConsole")

            discoverConsole.innerHTML = ""

            var discoverObj = JSON.parse(data)

            for (var i in discoverObj) {
                const header = document.createElement("h5")
                const text = document.createTextNode(i + ": ")

                header.appendChild(text)
                discoverConsole.appendChild(header)

                const el = document.createElement("p")
                const textP = document.createTextNode("")
                el.appendChild(textP)
                discoverConsole.appendChild(el)

                discoverObj[i].forEach(element => {
                    el.innerHTML += element + "<br>"
                });
            }
        }
        else {
            console.log(err);
        }
    })
}


//  Download  \\
function download() {
    let {PythonShell} = require("python-shell");
    let path = require("path")

    var downloadFile = document.getElementById("toDownload").value

    console.log(downloadFile);

    var options = {
        args : [downloadFile]
    }

    PythonShell.run('../engine/Chunk_Downloader.py', options, function (err, results) {
        if (err) throw err;

        console.log(results);
    });

    document.getElementById("toDownload").value = ""
    announce(downloadFile)
}

//  Main
let {PythonShell} = require("python-shell");

let uploadShell = new PythonShell('../engine/Chunk_Uploader.py');
let discoverShell = new PythonShell('../engine/Chunk_Discovery.py')

logAnnounce()
logDiscover()

window.setInterval(function() {
    logAnnounce()
    logDiscover()
}, 3000)