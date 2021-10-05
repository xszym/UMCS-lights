import React, {useState, useEffect, useContext} from 'react'
import Segment from './Segment';
import {initValues} from "../helper";
import { w3cwebsocket as W3CWebSocket } from "websocket";
import codeContext from '../context/Code/CodeContext';
import {message} from "antd";

const {ipcRenderer} = window.require("electron");


const Emulator = () => {
  const [values, setValues] = useState();
  const CodeContext = useContext(codeContext);

  const ipcUpdate = (event, values) => {
    setValues(values);
  }

  useEffect(() => {
    setValues(initValues())
    ipcRenderer.on('update', ipcUpdate);
  }, [])

  useEffect(() => {
    if (CodeContext.liveMode) {
      // TODO - to env
      const client = new W3CWebSocket('ws://159.89.9.110:5678');

      client.onerror = () => {
        message.error('Error connecting to server');
      }

      client.onopen = () => {
        console.log('WebSocket Client Connected');
      };

      client.onmessage = (message) => {
        if (!CodeContext.liveMode) {
          return;
        }

        // TODO - to helper
        let values = initValues();
        let tmp = message.data.split(',')

        let i = 0;
        let j = 0;

        for (let k = 0; k < tmp.length; k += 3) {
          values[i][j][0] = tmp[k];
          values[i][j][1] = tmp[k + 1];
          values[i][j][2] = tmp[k + 2];

          j++;
          if (j === 28) {
            i++;
            j = 0;
          }
        }

        setValues(values);
      };

      return () => {
        console.log('closing')
        client.close()
      }
    }
  }, [CodeContext.liveMode])

  const generateSegments = () => {
    let segments = [];
    for (let i = 0; i < 5; i++) {
      let segmentsRow = [];

      for (let j = 0; j < 28; j++) {
        let color = [0, 0, 0];
        color = values[i][j];
        segmentsRow.push(<Segment id={i * 28 + j} key={i * 28 + j} color={color}/>);
      }

      if (i === 0) {
        segments.push(<div key={i} style={{display: "flex"}}>{segmentsRow}</div>);
      } else {
        segments.push(<div key={i} style={{display: "flex"}}>{segmentsRow}</div>);
      }

    }
    return <div style={{width: '90%', display: "block", alignItems: "center"}}>{segments}</div>
  }

  return (
    <>
      {
        values && generateSegments()
      }
    </>
  )
};

export default Emulator;
