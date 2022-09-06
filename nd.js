
const { response } = require('express')
const express = require('express')
const app = express()
// const chroma = require('chroma-js')
const { spawn } = require('child_process')
// const child = spawn('python3', ['streaming/frame_data.py'])



const shellOptions = {
    mode: 'text',
    scriptPath: 'C:/Users/noahm/Desktop/Projects/f1_telem/streaming',
}
const { PythonShell } = require('python-shell')
const pyshell = new PythonShell('frame_data.py', shellOptions)




const sqlite3 = require('sqlite3').verbose()
const db = new sqlite3.Database('./flask_db.db', sqlite3.OPEN_READWRITE, (err) => {
    if (err) return console.error(err.message)})

//     console.log('connection sukses')

// })
// const testDb = new sqlite3.Database('./local_database/testdb.db', sqlite3.OPEN_READWRITE, (err) => {
//     if (err) return console.error(err.message)

//     console.log('connection sukses to test db')

// })


app.listen(5000, () => console.log('listening at port 5000'))
app.use(express.static('interface'))
// app.use(express.static(__dirname + '/public'));
app.use(express.json())
app.post('/pyfile', (req, res) => {
    
    // db.run('SELECT * FROM runningProgram WHERE id = 0')
    // db.run(`UPDATE runningProgram SET shouldRun = "${req.body.shouldRun}"`)
    console.log('fetched pyfile')
    pyshell.run((err, res) => {
        if (err) console.log('error/stopped running')
        console.log('ran python script')
        console.log(err)
    })


    pyshell.end(function (err) {
        if (err) {
            console.log(err);
        }
    });
    // python_process = pyshell.childProcess;


    res.end()

})

// app.get('/stop_python', function (req, res) {
    
//     pyshell.childProcess.kill('SIGINT');
//     res.send('Stopped');
// });

app.get('/getDb', (req, res) => {
    // run testDB
})

