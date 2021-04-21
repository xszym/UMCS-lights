const {NodeVM} = require('vm2');

// https://www.npmjs.com/package/vm2

function test() {
    console.log('123')
}

function _NextFrame(dmxValuesIn) {
    // Check if 'dmxValuesIn' are correct size
    
    console.log(dmxValuesIn)
    // publish DMX values to world and lights

    // Wrzucamy do redisa wartości
}

function _initValues() {
    let values = [];
    for (let i = 0; i < 5; i++) {
        let tmp = []
        for (let j = 0; j < 28; j++) {
            tmp.push([0, 0, 0]);
        }
        values.push(tmp);
    }
    return values;
}

function _getError() {

}

let working = true;

function _ifWorking() {
    return working;
}

let kinectValues = {x: 0, y: 0};

function GetKinect() {
    // let mousePos = electron.screen.getCursorScreenPoint();
    // return mousePos;
    // return {x: 800, y: 100};
    return kinectValues;
}

let vm = new NodeVM({
    timeout: 5,
    sandbox: {
        _ifWorking,
        test,
        _NextFrame,
        _initValues,
        _getError,
        GetKinect,
    },
    console: 'redirect'
})

vm.on('console.log', (data) => {
    console.log(data)
})

code = `
let values = _initValues(); 
function NextFrame() { 
    if(_ifWorking() === false) 
        throw 'Stop'; 
    _NextFrame(values);
} 

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
} 

async function _loop() {
    while(true){
      await loop()
      if(_ifWorking() === false) break; 
    }
  } 
`

code += `
let v = 0;

async function loop() {
    for (let i = 0; i < 5; i++) {
        for (let j = 0; j < 28; j++) {
            values[i][j] = [v, v, v]
        }
    }
    v += 1;
    if (v > 255) v = 0;
    NextFrame(values)
    await sleep(1000)
}
` + ' ' +
` 
_loop()
.catch(err => {
    if(err !== 'Stop') _getError(err.message);
})
`
// PISZE USER

try {
    vm.run(code, '_vm.js')
}
catch(error) {
    console.log(error.message)
}
