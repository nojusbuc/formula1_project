try {
    const startBtn = document.querySelector('.live-telemetry-button')
    startBtn.addEventListener('click', startReceivingData)
}
catch(err) {
    console.log(err)
}

try {
    const stopBtn = document.querySelector('.back-to-homepage')
    stopBtn.addEventListener('click', stopReceivingData)
}
catch (err) {
    console.log(err)
}


// const stopBtn = document.querySelector('.stop')

console.log("oy")

function startReceivingData() {

    // location.href = '/telemetry'
    fetch('/pyfile', {})

}

function stopReceivingData() {
    location.href = '/'
    console.log('hihi')
    // fetch('/stop_python', {})

    // //call the end function in python
    // fetch('/pyfile', {
    //     headers: {
    //         'Content-type': 'application/json'
    //     },
    //     method: 'POST',
    //     body: JSON.stringify({ 'shouldRun': 'False' })

    // db.run('SELECT * FROM runningProgram WHERE id = 0')
    // db.run('UPDATE runningProgram SET shouldRun = "False"')

    // db.close(err => {
    //     if (err) return console.error(err.message)
    // })

}

// startBtn.addEventListener('click', startReceivingData)
// stopBtn.addEventListener('click', stopReceivingData)

