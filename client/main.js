const electron = require('electron');
const app = electron.app;
const BrowserWindow = electron.BrowserWindow;
const isDev = require('electron-is-dev');
const electronLocalshortcut = require('electron-localshortcut');

const emulator = require('../emulate/emulate');

const path = require('path');
const {ipcMain} = require('electron');


let mainWindow = null;

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1300,
    height: 800,
    webPreferences: {nodeIntegration: true, webSecurity: false, contextIsolation: false},
    minWidth: 600,
    title: 'UMCS Led Emulator'
  });
  mainWindow.loadURL(isDev ? 'http://localhost:3000' : `file://${path.join(__dirname, './build/index.html')}`);
  if (isDev) {
    // Open the DevTools.
    //BrowserWindow.addDevToolsExtension('<location to your react chrome extension>');
    mainWindow.webContents.openDevTools();
  }
  mainWindow.on('closed', () => mainWindow = null);

  electronLocalshortcut.register(mainWindow, ['Ctrl+R', 'F4'], () => {
    // working = false;
    mainWindow.webContents.send('stop');
  });

  electronLocalshortcut.register(mainWindow, ['Ctrl+S'], () => {
    mainWindow.webContents.send('save');
  });
}

app.on('ready', createWindow);

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

app.on('activate', () => {
  if (mainWindow === null) {
    createWindow();
  }
});

ipcMain.on('code', (event, arg) => {
  working = true;
  runCodeVM(arg);
});

let working = false;

ipcMain.on('stop', (event, arg) => {
  working = false;
  mainWindow.webContents.send('stop');
});

function nextFrame(values) {
  mainWindow.webContents.send('update', values);
}

function getError(err) {
  mainWindow.webContents.send('error', err);
  console.log(err);
}

function getLog(data) {
  mainWindow.webContents.send('log', data);
  console.log(data)
}

function getWorking() {
  return working;
}

function runCodeVM(userCode) {
  const vm = emulator.initVm(nextFrame, getError, getLog, getWorking);
  const code = emulator.generateEmulatorCode(userCode);
  try {
    vm.run(code, '_vm.js')
  } catch (error) {
    console.log(error.message)
    mainWindow.webContents.send('error', error.message);
  }
}
