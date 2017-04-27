// @flow
import LabelForm from './LabelForm';
import React from 'react';
import ReactDOM from 'react-dom';
import './fonts.css';

require('react-tap-event-plugin')();

setTimeout(() => {
  ReactDOM.render(<LabelForm />, document.querySelector('#laibel'));
}, 500);
