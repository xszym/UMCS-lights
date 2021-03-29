import {SET_CODE, GET_CODES} from '../types'

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
    default:
      return state
  }
}