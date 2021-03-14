import React, {useContext} from 'react'
import codeContext from '../context/Code/CodeContext'
import {Button} from "antd";

const Code = () => {
  const CodeContext = useContext(codeContext);

  return (
    <>
      <h1>{CodeContext.code}</h1>
      <Button onClick={() => {CodeContext.setCode(CodeContext.code + '!')}}>Add</Button>
    </>
  )

};

export default Code;