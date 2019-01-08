// @flow
import './fonts.css';
import LabelForm from './LabelForm';
import React from 'react';
import ReactDOM from 'react-dom';

setTimeout(() => {
  ReactDOM.render(<LabelForm />, document.querySelector('#laibel'));
}, 500);
