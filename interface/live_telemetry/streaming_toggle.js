
// const startBtn = document.querySelector('.live-telemetry-button')
// const stopBtn = document.querySelector('.back-to-homepage')
// const stopBtn = document.querySelector('.stop')



function startReceivingData() {

    location.href = '/live_telemetry/telem.html'

    fetch('/pyfile', {
        headers: {
            'Content-type': 'application/json'
        },
        method: 'POST',
        body: JSON.stringify({ 'shouldRun': 'True' })
    })


}

function stopReceivingData() {
    location.href = '/'

    //call the end function in python
    fetch('/pyfile', {
        headers: {
            'Content-type': 'application/json'
        },
        method: 'POST',
        body: JSON.stringify({ 'shouldRun': 'False' })
    })
    // db.run('SELECT * FROM runningProgram WHERE id = 0')
    // db.run('UPDATE runningProgram SET shouldRun = "False"')

    // db.close(err => {
    //     if (err) return console.error(err.message)
    // })

}

// startBtn.addEventListener('click', startReceivingData)
// stopBtn.addEventListener('click', stopReceivingData)

