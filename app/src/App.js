import React, { useState, useEffect } from 'react';
import logo from './logo.svg';
import './App.css';
import Map from './map.js'
import Charts from "./charts.js"

require('dotenv').config()

let api = require("./api.js");

console.log(process.env)

function App() {
  const [recent_tweets, setRecentTweets] = useState([])
  useEffect(() => {
    api.get_recent_tweets().then(results => {
      console.log(results.data.tweets)
      setRecentTweets(results.data.tweets)
    })
  }, [])

  const [all_tweets, setAllTweets] = useState([])
  useEffect(() => {
    api.get_all_tweets().then(results => {
      console.log(results.data.tweets)
      setAllTweets(results.data.tweets)
    })
  }, [])

  return (
    <div className="App">
      <Map tweets={recent_tweets}/>
      <Charts tweets={all_tweets}/>
    </div>
  );
}

export default App;
