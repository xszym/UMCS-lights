const {NodeVM} = require("vm2");
// https://www.npmjs.com/package/vm2


function generateEmulatorCode(userCode) {
  return `
let values = _InitValues();
function NextFrame() {
  if(_IsWorking() === false)
    throw 'Stop';
  _NextFrame(values);
}

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

async function _loop() {
  while (true) {
    await loop();
    if(_IsWorking() === false) break;
  }
}
` + userCode + `
_loop()
  .catch(err => {
    if(err !== 'Stop') _GetError(err.message);
  });
`;
}


function initVm(_NextFrame, _GetError, _Log, _IsWorking) {
  function _InitValues() {
    let values = [];
    for (let i = 0; i < 5; i++) {
      let row = [];
      for (let j = 0; j < 28; j++) {
        row.push([0, 0, 0]);
      }
      values.push(row);
    }
    return values;
  }

  let vm = new NodeVM({
    timeout: 1000,
    sandbox: {
      _IsWorking,
      _NextFrame,
      _InitValues,
      _GetError,
    },
    console: "redirect",
    require: {
      external: ['request'],
    }
  });

  vm.on("console.log", (data) => {
    _Log(data);
  });

  return vm;
}

module.exports = {
  initVm: initVm,
  generateEmulatorCode: generateEmulatorCode
}
