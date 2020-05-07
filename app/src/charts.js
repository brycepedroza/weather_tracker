import React from 'react';
import {
  XYPlot,
  XAxis,
  YAxis,
  VerticalGridLines,
  HorizontalGridLines,
  VerticalBarSeries,
} from 'react-vis';
import { List, Card } from 'antd';

function generate_graphs(tweets){
  let graphs = []
  // Temperature Init
  let temp_interval = 5;
  let temp_max = 120;
  let temperature = [];
  for (let i = 0; i <= temp_max/temp_interval; i ++){
    temperature.push({
      x: i * temp_interval,
      y: 0,
      data: []
    })
  }

  // Humidity Init
  let humidity_interval = .1;
  let humidity_max = 1;
  let humidity = [];
  for (let i = 0; i <= humidity_max/humidity_interval; i ++){
    humidity.push({
      x: i * humidity_interval,
      y: 0,
      data: []
    })
  }

  // UV Init
  let uv_interval = 1;
  let uv_max = 12;
  let uv = [];
  for (let i = 0; i <= uv_max/uv_interval; i ++){
    uv.push({
      x: i * uv_interval,
      y: 0,
      data: []
    })
  }

  // General Condition Summary Init
  let summary = [];

  // Binning
  for (let index in tweets) {
    let tweet = tweets[index];

    // Temperature
    let temp_bin = Math.floor(tweet.temperature/temp_interval)
    if (temp_bin >= 0 && temp_bin !== undefined && temp_bin <= temp_max/temp_interval) {
      temperature[temp_bin].data.push(tweet.sentiment)
    }

    // Humidity
    let humidity_bin = Math.floor(tweet.humidity/humidity_interval)
    if (humidity_bin >= 0 && humidity_bin !== undefined && humidity_bin <= humidity_max/humidity_interval) {
      humidity[humidity_bin].data.push(tweet.sentiment)
    }

    // Humidity
    let uv_bin = Math.floor(tweet.uv_index/uv_interval)
    if (uv_bin >= 0 && uv_bin !== undefined && uv_bin <= uv_max/uv_interval) {
      uv[uv_bin].data.push(tweet.sentiment)
    }

    // Summary
    let description = tweet.summary;
    let found = false;
    // Go through list and see if we have seen this summary;
    for (let index in summary) {
      if (summary[index].x === description){
        summary[index].data.push(tweet.sentiment)
        found = true;
        break;
      }
    }
    if (!found) {
      summary.push({
        x: description,
        y: 0,
        data: [tweet.sentiment]
      })
    }

  }

  // Temp Calculations
  for (let index in temperature) {
    let total = 0;
    for (let y in temperature[index].data) {
      total = total + temperature[index].data[y]
    }
    const average = total/temperature[index].data.length
    if (!isNaN(average)){
      temperature[index].y = average
    }
    delete temperature[index].data
  }
  graphs.push ({
    data: temperature,
    name: "Temperature Sentiment",
    xType: "linear",
    width: 300
  })

  // Humidity Calculations
  for (let index in humidity) {
    let total = 0;
    for (let y in humidity[index].data) {
      total = total + humidity[index].data[y]
    }
    const average = total/humidity[index].data.length
    if (!isNaN(average)){
      humidity[index].y = average
    }
    delete humidity[index].data
  }
  graphs.push ({
    data: humidity,
    name: "Humdity Sentiment",
    xType: "linear",
    width: 300
  })

  // UV Index Calculations
  for (let index in uv) {
    let total = 0;
    for (let y in uv[index].data) {
      total = total + uv[index].data[y]
    }
    const average = total/uv[index].data.length
    if (!isNaN(average)){
      uv[index].y = average
    }
    delete uv[index].data
  }
  graphs.push ({
    data: uv,
    name: "UV Index Sentiment",
    xType: "linear",
    width: 300
  })

  // General Condition Summary
  for (let index in summary) {
    let total = 0;
    for (let y in summary[index].data) {
      total = total + summary[index].data[y]
    }
    const average = total/summary[index].data.length
    if (!isNaN(average)){
      summary[index].y = average
    }
    delete summary[index].data
  }
  graphs.push ({
    data: summary,
    name: "General Conditions Sentiment",
    xType: "ordinal",
    width: 600
  })
  console.log(summary)
  return graphs
}

export default class Example extends React.Component {
  constructor(props){
    super(props)
    this.state = {
      useCanvas: false,
      graphs: generate_graphs(this.props.tweets)
    }
  }

  componentDidUpdate(prevProps) {
    if(this.props.tweets !== prevProps.tweets) // Check if it's a new user, you can also use some unique property, like the ID  (this.props.user.id !== prevProps.user.id)
    {
      this.update_graphs(this.props.tweets);
    }
  }

  update_graphs(tweets){
    this.setState({
      graphs: generate_graphs(this.props.tweets)
    })
  }

  render() {
    return (
      <div style={{padding: 25}}>
            <List
              grid={{
                gutter: 16,
                xs: 1,
                sm: 2,
              }}
              dataSource={this.state.graphs}
              renderItem={item => (
                <List.Item >
                  <div>
                    <p> {item.name} </p>
                    <XYPlot width={item.width} height={300} xType={item.xType} >
                      <VerticalGridLines />
                      <HorizontalGridLines />
                      <XAxis />
                      <YAxis />
                      <VerticalBarSeries data={item.data} />
                    </XYPlot>
                  </div>

                </List.Item>
              )}
            />
      </div>
    );
  }
}
