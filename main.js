
const { response } = require('express')
const express = require('express')
const app = express()
// const chroma = require('chroma-js')
const { spawn } = require('child_process')
const { PythonShell } = require('python-shell')

const sqlite3 = require('sqlite3').verbose()
const db = new sqlite3.Database('./local_database/pydatabase.db', sqlite3.OPEN_READWRITE, (err) => {
    if (err) return console.error(err.message)

    console.log('connection sukses')

})
const testDb = new sqlite3.Database('./local_database/testdb.db', sqlite3.OPEN_READWRITE, (err) => {
    if (err) return console.error(err.message)

    console.log('connection sukses to test db')

})


app.listen(5000, () => console.log('listening at port 5000'))
app.use(express.static('interface'))
// app.use(express.static(__dirname + '/public'));
app.use(express.json())
app.post('/pyfile', (req, res) => {
    console.log(req.body.shouldRun)
    db.run('SELECT * FROM runningProgram WHERE id = 0')
    db.run(`UPDATE runningProgram SET shouldRun = "${req.body.shouldRun}"`)
    let options = {
        mode: 'text',
        scriptPath: 'C:/Users/noahm/Desktop/Projects/f1_telem/streaming',

    }
    PythonShell.run('frame_data.py', options, (err, res) => {
        if (err) console.log('error/stopped running')
        console.log('ran python script')
        console.log(err)
    })

    res.end()

})

app.get('/getDb', (req, res) => {
    // run testDB
})

