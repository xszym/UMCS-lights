const emulator = require('./emulate');

const redis = require("redis");
const redisClient = redis.createClient("redis://redis:6379");

redisClient.on("error", function (error) {
  console.error(error);
});

function myNextFrame(dmxValuesIn) {
  // TODO - Check if dmxValuesIn is correct
  redisClient.set("DMXvalues", dmxValuesIn.toString());
  redisClient.set("DMXvalues_update_timestamp", Date.now().toString());
}

function getError(message) {
  console.error(message);
}

// TODO - User code should be taken from stdin
const USER_CODE = `
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
`;

let working = true;

function getWorking() {
  return working;
}

const code = emulator.generateEmulatorCode(USER_CODE)

let vm = emulator.initVm(myNextFrame, getError, getWorking);

try {
  vm.run(code, "_vm.js");
} catch (error) {
  console.error(error.message);
}
