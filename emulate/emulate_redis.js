const fs = require("fs");

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
  process.exit(1);
}

let working = true;

function getWorking() {
  return working;
}

function getLog(data) {
  console.log(data);
}

fs.readFile('tmp', 'utf8', function(err, data) {
    if (err) throw err;
    run(data)
});

function run(userCode) {
  const code = emulator.generateEmulatorCode(userCode);

  let vm = emulator.initVm(myNextFrame, getError, getLog, getWorking);

  try {
    vm.run(code, "_vm.js");
  } catch (error) {
    console.error(error.message);
    process.exit(1);
  }
}

