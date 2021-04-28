import React, {useState, useEffect} from 'react'
import Segment from './Segment';

const { ipcRenderer } = window.require("electron");


const Emulator = () => {
    const [values, setValues] = useState();

    const ipcUpdate = (event, values) => {
        setValues(values);
    }

    useEffect(() => {
        setValues(initValues())
        ipcRenderer.on('update', ipcUpdate);
    }, [])

    const initValues = () => {
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
