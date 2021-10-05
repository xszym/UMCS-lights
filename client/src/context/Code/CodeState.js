import React, {useReducer} from 'react'
import axios from 'axios'

import CodeContext from './CodeContext'
import CodeReducer from './CodeReducer'

import {GET_CODES, SET_CODE, SET_LIVE_MODE} from "../types"

const CodeState = (props) => {
  let initialState = {
    code: '' +
      'async function loop() {\n' +
      '\t// Your code goes here\n' +
      '\tawait sleep(46);\n' +
      '\tNextFrame();\n' +
      '}',
    codes: [],
    liveMode: false,
  }

  const [state, dispatch] = useReducer(CodeReducer, initialState)

  const setCode = (code) => {
    dispatch({type: SET_CODE, payload: code})
  }

  const getCodes = async (filter) => {
    try {
      let queryParams = ''
      if (filter === 'approved') {
        queryParams = '?approved=True'
      } else if (filter === 'examples') {
        queryParams = '?example=True'
      }

      const response = await axios.get(`/api/codes/${queryParams}`)
      console.log(response.data)
      dispatch({type: GET_CODES, payload: response.data})
    } catch (err) {
      console.log(err)
    }
  }

  const submitCode = async (formData) => {
    try {
      console.log(formData)
      const data = {...formData, 'code': state.code}
      const response = await axios.post('/api/codes/', data)
    } catch (err) {
      console.log(err)
      throw err
    }
  }

  const setLiveMode = (data) => {
    dispatch({type: SET_LIVE_MODE, payload: data})
  }

  return (
    <CodeContext.Provider
      displayName='CodeContext'
      value={{
        code: state.code,
        codes: state.codes,
        liveMode: state.liveMode,
        setCode,
        getCodes,
        submitCode,
        setLiveMode,
      }}
    >
      {props.children}
    </CodeContext.Provider>
  )
};

export default CodeState
