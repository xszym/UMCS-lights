import React, {useReducer} from 'react'

import CodeContext from './CodeContext'
import CodeReducer from './CodeReducer'

import {SET_CODE} from "../types";

const CodeState = (props) => {
  let initialState = {
    code: ''
  };

  const [state, dispatch] = useReducer(CodeReducer, initialState);

  const setCode = (code) => {
    console.log(code)
    dispatch({ type: SET_CODE, payload: code});
  };

  return (
    <CodeContext.Provider
      displayName='CodeContext'
      value={{
        code: state.code,
        setCode,
      }}
    >
      {props.children}
    </CodeContext.Provider>
  )
};

export default CodeState;