import {SET_CODE} from '../types';

export default (state, action) => {
  const {payload, type} = action

  switch (type) {
    case SET_CODE:
      return {
        ...state,
        code: payload
      };
    default:
      return state;
  }
};