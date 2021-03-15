import React, {useContext} from 'react'
import codeContext from '../context/Code/CodeContext'
import {Button} from "antd";

import Emulator from "./Emulator";
import Editor from "./Editor";

const Code = () => {
  const CodeContext = useContext(codeContext);

  return (
    <>
      <Button onClick={() => {
        CodeContext.setCode(CodeContext.code + '!')
      }}>Add</Button>
      <Emulator/>
      <Editor/>
    </>
  )

};

export default Code;