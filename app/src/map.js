import React, { Component } from 'react'
import { Map, TileLayer, Marker, Popup } from 'react-leaflet'
import { TwitterTweetEmbed } from 'react-twitter-embed';

export default class SimpleExample extends Component {
  constructor(props){
    super(props)
    this.state = {
      lat: 39.8283,
      lng: -98.5795,
      zoom: 5,
    }
  }

  shouldComponentUpdate(nextProps) {
    return nextProps.tweets !== this.props.tweets;
  }

  render() {
    const position = [this.state.lat, this.state.lng]
    return (
      <div>
        <Map center={position} zoom={this.state.zoom}>
          <TileLayer
            attribution='&amp;copy <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          />
          { this.props.tweets?
            this.props.tweets.map((tweet) =>
            <Marker key={tweet.id} position={[tweet.latitude, tweet.longitude]}>
              <Popup>
                <TwitterTweetEmbed tweetId={tweet.id} />
              </Popup>
            </Marker>
          ): null}
        </Map>
      </div>
    )
  }
}
