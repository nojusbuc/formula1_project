const numb = document.querySelector('.number');
let counter = 0;
const cnt = document.querySelector('.speed')
let oldSpeed = 0
const throttleElement = document.querySelector('.throttle')
const brakeElement = document.querySelector('.brake')
const gearElement = document.querySelector('.gear-count')
const frontLeftTireWearElement = document.querySelector('.frontleft-tire-wear-count')
const frontRightTireWearElement = document.querySelector('.front-right-tire-wear-count')
const rearLeftTireWearElement = document.querySelector('.rear-left-tire-wear-count')
const rearRightTireWearElement = document.querySelector('.rear-right-tire-wear-count')
const positionElement = document.querySelector('.position-count')
const engineRPMElement = document.querySelector('.engine-rpm-count')
const bestLapElement = document.querySelector('.best-lap-count')
const lastLapElement = document.querySelector('.last-lap-count')
const sectorOneElement = document.querySelector('.sector1-time-num')
const sectorTwoElement = document.querySelector('.sector2-time-num')






setInterval(async () => {

    const response = await fetch('telem-data.json')
    const data = await response.json()
    updateSpeed(JSON.parse(data)['speed'])
    updateThrottle(JSON.parse(data)['throttle'])
    updateBrake(JSON.parse(data)['brake'])
    updateGear(JSON.parse(data)['gear'])





    // fetch('telem-data.json')
    //     .then(response => response.json())
    //     .then(data =>
    //         updateSpeed(JSON.parse(data)['speed']))



}, 100)

// function updateSpeed(speed) {
//     const maxSpeed = 350
//     // let deg = Math.round(speed / maxSpeed * 360)
//     let deg = speed / maxSpeed * 360

//     // let oldDeg = Math.round(oldSpeed / maxSpeed * 360)
//     let oldDeg = oldSpeed / maxSpeed * 360

//     const increment = ((deg - oldDeg) / 10)
//     // console.log(oldDeg, increment, deg)


//     setInterval(function () {
//         if (Math.round(deg) != Math.round(oldDeg)) {
//             if (oldDeg > 180 && oldDeg <= 360 && deg >= 0 && deg <= 360) {

//                 document.documentElement.style.setProperty('--left-rotation', '180deg')
//                 document.documentElement.style.setProperty('--right-rotation', `${oldDeg - 180}deg`)
//                 oldDeg += increment

//             }
//             if (oldDeg <= 180 && oldDeg >= 0 && deg >= 0 && deg <= 360) {

//                 document.documentElement.style.setProperty('--left-rotation', `${oldDeg}deg`)
//                 document.documentElement.style.setProperty('--right-rotation', `0deg`)
//                 oldDeg += increment
//             }
//             // if (parseInt(numb.innerText) != Math.round(oldDeg / 360 * 350)) {
//             //     numb.innerText = Math.round(oldDeg / 360 * 350)

//             // }
//             numb.innerText = Math.round(oldDeg / 360 * 350)



//         }

//         // console.log('degrees equal')



//     }, 10)
//     oldSpeed = numb.innerText
//     // console.log(oldSpeed)
// }

function updateSpeed(speed) {


    const numb = document.querySelector('.number')
    const speedometer = document.querySelector('.red')
    const maxDistance = speedometer.getTotalLength()
    const maxSpeed = 350
    const ratio = maxDistance / maxSpeed

    const newOffset = maxDistance - speed * ratio

    // const prevSpeed = numb.innerText
    const speedIncrement = (speed - prevSpeed) / 10
    console.log(speedIncrement)

    speedometer.style.strokeDashoffset = newOffset

    setInterval(function () {
        // let currentSpeed = Math.round(parseInt(numb.innerText) + speedIncrement)

        // numb.innerText = parseInt(numb.innerText) + speedIncrement
        // console.log(parseInt(speedIncrement))
        // speedometer.style.strokeDashoffset += offsetIncrement
        // speedometer.style.strokeDashoffset = parseInt(window.getComputedStyle(speedometer).strokeDashoffset.replace(/\D/g, "")) + offsetIncrement

    }, 10)

    prevSpeed = numb.innerText

}








function updateThrottle(throttle) {

    let currentThrottle = throttleElement.offsetHeight / 120 * 100
    // console.log(currentThrottle)
    let increment = (throttle - currentThrottle) / 10

    setInterval(function () {

        // if (Math.round(currentThrottle) != Math.round(throttle) &&
        //     currentThrottle + increment <= 100 && currentThrottle + increment >= 0) {
        //     currentThrottle += increment
        //     // console.log(increment)
        //     console.log('print true')

        // }
        // throttleElement.style.height = `${currentThrottle}%`
        // console.log(currentThrottle)
        throttleElement.style.height = `${throttle}%`

    }, 10)

    // throttleElement.style.height = `${throttle}%`
    // console.log(throttleElement.style.height)
}

function updateBrake(brake) {
    let currentBrake = brakeElement.offsetHeight / 120 * 100
    brakeElement.style.height = brake;
    setInterval(function () {
        // console.log(currentBrake)
        if (Math.round(parseInt(brakeElement.style.height.replace(/\D/g, ''))) != brake) {
            // console.log(brake)
            currentBrake += (brake - currentBrake) / 10
            brakeElement.style.height = `${currentBrake
                }%`

        }

    }, 10)

}

function updateGear(gear) {
    gearElement.textContent = gear
}