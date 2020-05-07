import clsx from 'clsx';
import * as React from 'react';
import styles from './example.css';
import {List, AutoSizer} from 'react-virtualized';
import { TwitterTweetEmbed } from 'react-twitter-embed';

export default class ListExample extends React.PureComponent {

  constructor(props, context) {
    super(props);
    // console.log(props, props.tweets.length)
    this.state = {
      listHeight: 500,
      listRowHeight: 500,
      overscanRowCount: 10,
      scrollToIndex: undefined,
      useDynamicRowHeight: false,
    };

    this._getRowHeight = this._getRowHeight.bind(this);
    this._noRowsRenderer = this._noRowsRenderer.bind(this);
    this._onRowCountChange = this._onRowCountChange.bind(this);
    this._onScrollToRowChange = this._onScrollToRowChange.bind(this);
    this._rowRenderer = this._rowRenderer.bind(this);
  }

  shouldComponentUpdate(newProps){
    return newProps.tweets !== this.props.tweets
  }

  render() {
    const {
      listHeight,
      listRowHeight,
      overscanRowCount,
      scrollToIndex,
      useDynamicRowHeight,
    } = this.state;

    console.log(this.props.tweets, this.props.tweets.length)
    return (
        <div>
          <AutoSizer disableHeight>
            {({width}) => (
              <List
                ref="List"
                className={styles.List}
                height={listHeight}
                overscanRowCount={overscanRowCount}
                noRowsRenderer={this._noRowsRenderer}
                rowCount={this.props.tweets.length}
                rowHeight={
                  useDynamicRowHeight ? this._getRowHeight : listRowHeight
                }
                rowRenderer={this._rowRenderer}
                scrollToIndex={scrollToIndex}
                width={width}
              />
            )}
          </AutoSizer>
        </div>
    );
  }

  _getDatum(index) {
    const {tweets} = this.props;

    return tweets[index];
  }

  _getRowHeight({index}) {
    // return this._getDatum(index).size;
    return 100
  }

  _noRowsRenderer() {
    return <div className={styles.noRows}>No rows</div>;
  }

  _onRowCountChange(event) {
    const rowCount = parseInt(event.target.value, 10) || 0;

    this.setState({rowCount});
  }

  _onScrollToRowChange(event) {
    const {rowCount} = this.state;
    let scrollToIndex = Math.min(
      rowCount - 1,
      parseInt(event.target.value, 10),
    );

    if (isNaN(scrollToIndex)) {
      scrollToIndex = undefined;
    }

    this.setState({scrollToIndex});
  }

  _rowRenderer({index, isScrolling, key, style}) {
    const {showScrollingPlaceholder, useDynamicRowHeight} = this.state;

    if (showScrollingPlaceholder && isScrolling) {
      return (
        <div
          className={clsx(styles.row, styles.isScrollingPlaceholder)}
          key={key}
          style={style}>
          Scrolling...
        </div>
      );
    }

    const datum = this._getDatum(index);

    let additionalContent;

    if (useDynamicRowHeight) {
      additionalContent = (
        <div>
          It is large-sized.
          <br />
          It has a 3rd row.
        </div>)
    }

    return (
      <div className={styles.row} key={key} style={style}>
        <div style={{margin: 'auto'}}>
        <TwitterTweetEmbed className="SUPERAWESOME" style={{maxWidth: "100% !important"}} tweetId={datum.id} />
        </div>
      </div>
    );
  }
}
