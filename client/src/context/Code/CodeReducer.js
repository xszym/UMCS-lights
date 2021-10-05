import {SET_CODE, GET_CODES, SET_LIVE_MODE} from '../types'

export default (state, action) => {
  const {payload, type} = action

  switch (type) {
    case SET_CODE:
      return {
        ...state,
        code: payload,
      }
    case GET_CODES:
      return {
        ...state,
        codes: payload,
      }
    case SET_LIVE_MODE:
      return {
        ...state,
        liveMode: payload,
      }
    default:
      return state
  }
}
