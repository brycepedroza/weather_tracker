let axios = require("axios");


let baseURL;
if (process.env.REACT_APP_ENV === "dev"){
  baseURL = ""
}
else if (process.env.REACT_APP_ENV === "local"){
  baseURL="http://localhost:1337/api"
}
else if (process.env.REACT_APP_ENV === "prod"){
  baseURL="https://weathertracker.azurewebsites.net/api"
}

const client = axios.create({
  baseURL: baseURL,
  json: true,
})

export function get_recent_tweets(cb) {
  // US bounding box
  let params = {
    lat1:  24.686952,
    lat2:  50.457504,
    long1: -126.210938,
    long2: -66.708984
  }
  return client({
    method: "get",
    params: params,
    url: "/region"}).then(checkStatus).then(cb).catch(error => {
      if (error.response){
        cb({data: error.response.data, response: error.response.status});
      }
    })
}

export function get_all_tweets(cb) {
  return client({
    method: "get",
    url: "/all"}).then(checkStatus).then(cb).catch(error => {
      if (error.response){
        cb({data: error.response.data, response: error.response.status});
      }
    })
}

function checkStatus(response){
  if (response.status >= 200 && response.status < 300 ) {
    return {data: response.data, status: response.status}
  }
  const error = new Error(`HTTP Error ${response.statusText}`);
  error.status = response.statusText;
  error.response = response;
  throw error;
}
