// @flow
import ReactDOM from 'react-dom';
import React from 'react';
import LabelForm from './LabelForm';
import './fonts.css';

require('react-tap-event-plugin')();

setTimeout(() => {
  ReactDOM.render(<LabelForm/>, document.querySelector('#laibel'));
}, 500);
