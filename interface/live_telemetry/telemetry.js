// variables for speed
const numb = document.querySelector('.number')
const speedometer = document.querySelector('.red')
const maxDistance = speedometer.getTotalLength()
const maxSpeed = 350
const ratio = maxDistance / maxSpeed

//variables for throttle
const throttleRect = document.querySelector('.throttle-rect')
const brakeRect = document.querySelector('.brake-rect')



let counter = 0;
const cnt = document.querySelector('.speed')
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