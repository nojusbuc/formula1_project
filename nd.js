const { response } = require('express')
const express = require('express')
const app = express()
// const chroma = require('chroma-js')
const { spawn } = require('child_process')
// const child = spawn('python3', ['streaming/frame_data.py'])

const sqlite3 = require('sqlite3').verbose()
const db = new sqlite3.Database('./flask_db.db', sqlite3.OPEN_READWRITE, (err) => {
    if (err) return console.error(err.message)
})
db.run('UPDATE streaming SET should_run = 0 WHERE str_id = 1')

const shellOptions = {
    mode: 'text',
    scriptPath: 'C:/Users/noahm/Desktop/Projects/f1_telem/streaming',
}
let { PythonShell } = require('python-shell')
// const pyshell = new PythonShell('frame_data.py', shellOptions)

// console.log(pyshell)





//     console.log('connection sukses')

// })
// const testDb = new sqlite3.Database('./local_database/testdb.db', sqlite3.OPEN_READWRITE, (err) => {
//     if (err) return console.error(err.message)

//     console.log('connection sukses to test db')

// })

PythonShell.run('frame_data.py', shellOptions, (err, res) => {
    if (err) console.log('error/stopped running')
    console.log('ran python script')
    console.log(err)
})


app.listen(8080, () => console.log('listening at port 5000'))
app.use(express.static('interface'))
// app.use(express.static(__dirname + '/public'));
app.use(express.json())
app.get('/pyfile', (req, res) => {
    db.run('UPDATE streaming SET should_run = 1 WHERE str_id = 1')

    // db.run('SELECT * FROM runningProgram WHERE id = 0')
    // db.run(`UPDATE runningProgram SET shouldRun = "${req.body.shouldRun}"`)
    console.log('fetched pyfile')
    


    // pyshell.end(function (err) {
    //     if (err) {
    //         console.log(err);
    //     }
    // });
    // python_process = pyshell.childProcess;


    res.end()

})

app.get('/stop_python', function (req, res) {
    db.run('UPDATE streaming SET should_run = 0 WHERE str_id = 1')
});

app.get('/getDb', (req, res) => {
    // run testDB
})