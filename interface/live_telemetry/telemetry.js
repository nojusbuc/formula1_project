// variables for speed
const numb = document.querySelector('.number')
const speedometer = document.querySelector('.red')
const maxDistance = speedometer.getTotalLength()
const maxSpeed = 350
const ratio = maxDistance / maxSpeed

//variables for throttle
const throttleRect = document.querySelector('.throttle-rect')
const brakeRect = document.querySelector('.brake-rect')


// variable for color calculator
// const f = chroma.scale(['green', 'yellow', 'red']);

// tyres variables
const tyreBoxes = document.querySelectorAll('.tyre-box')
const tyreWearCounts = document.querySelectorAll('.tyre-wear-count')
const tyreSurfaceTemps = document.querySelectorAll('.tyre-surface-temp')

// variables for drs

const drsBox = document.querySelector('.drs-box')

//variables for ers
const ersBox = document.querySelector('.ers-box')


let counter = 0;
const cnt = document.querySelector('.speed')
const throttleElement = document.querySelector('.throttle')
const brakeElement = document.querySelector('.brake')
const gearElement = document.querySelector('.gear-count')
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
    updateDRS(JSON.parse(data)['drs'])
    updateERS(JSON.parse(data)['ersActivated'])
    updateTyreWear(JSON.parse(data)['tyreWear'])
    updateTyreTemps(JSON.parse(data)['tyreSurfaceTemps'])

}, 100)

function updateSpeed(speed) {

    const newOffset = maxDistance - speed * ratio
    speedometer.style.strokeDashoffset = newOffset

    setInterval(function () {

        speedValue = speedometer.style.strokeDashoffset
        numb.innerText = Math.round(maxSpeed - speedValue / ratio) + ' kph'

    }, 20)


}

function updateThrottle(throttle) {

    throttleRect.style.transform = `scaleY(${throttle * 100}%)`

}

function updateBrake(brake) {
    brakeRect.style.transform = `scaleY(${brake * 100}%)`

}

function updateGear(gear) {
    gearElement.textContent = 'GEAR ' + gear
}

const tyreColorCalculator = (percentage, tyreElement) => {

}

const updateDRS = (drs) => {
    if (drs == 1) {
        drsBox.style.backgroundColor = '#349905'
    } else {
        drsBox.style.backgroundColor = ""
    }
}

const updateERS = (ers) => {
    if (ers == true) {
        ersBox.style.backgroundColor = '#349905'
    } else {
        ersBox.style.backgroundColor = ""
    }
}

const updateTyreWear = (tyreWear) => {


    for (let i = 0; i < 4; i++) {
        tyreWearCounts[i].textContent = `Wear: ${tyreWear[i]}`
    }


}

const updateTyreTemps = (tyreTemps) => {
    for (let i = 0; i < 4; i++) {
        tyreSurfaceTemps[i].textContent = `Temp: ${tyreTemps[i]}`
    }
}