const redis = require("redis");
const redisClient = redis.createClient("redis://redis:6379");
const { NodeVM } = require("vm2");

// https://www.npmjs.com/package/vm2

redisClient.on("error", function (error) {
  console.error(error);
});

/// Handles switching DMX values for the next frame
function _NextFrame(dmxValuesIn) {
  // TODO - Check if dmxValuesIn is correct
  redisClient.set("DMXvalues", dmxValuesIn.toString());
  redisClient.set("DMXvalues_update_timestamp", Date.now().toString());
}

/// Handles initializing the array with DMX values
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

/// Handles errors from inside code emulation
function _GetError(message) {
  console.error(message);
}

/// Enables us to stop code emulation from the outside
let working = true;
function _IsWorking() {
  return working;
}

let vm = new NodeVM({
  timeout: 5,
  sandbox: {
    _IsWorking,
    _NextFrame,
    _InitValues,
    _GetError,
  },
  console: "redirect",
});

vm.on("console.log", (data) => {
  console.log(data);
});

// TODO - User code should be fetched from queue instead
const UserCode = `
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
    await sleep(10000)
}
`;

code = `
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
` + UserCode + `
_loop()
  .catch(err => {
    if(err !== 'Stop') _GetError(err.message);
  });
`;

try {
  vm.run(code, "_vm.js");
} catch (error) {
  console.error(error.message);
}
