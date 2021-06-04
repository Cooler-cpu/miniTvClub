import { combineReducers } from "redux";


import auth from "./auth"; // auth reducer
import message from "./message"; //message reducer



export default combineReducers({
  auth,
  message,
});