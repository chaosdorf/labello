// @flow
import React from 'react';
import { autobind } from 'core-decorators';
import 'elemental/less/elemental.less';
import { FormInput, FormSelect, Checkbox, Button, Form } from 'elemental';

type State = {
  selectedSize: string,
  selectedFont: string,
  selectedAlign?: string,
  outline: bool,
  bold: bool,
}

const style = {
  label: {
    padding: 10,
    width: 450,
    wordBreak: 'break-all',
  },
};


export default class LabelForm extends React.Component {
  state: State = {
    outline: true,
    bold: false,
    selectedFont: 'lettergothic',
    selectedSize: '33',
  };
  handleChange(type: string, value: string) {
    this.setState({
      [type]: value,
    });
  }
  handleBoolChange(type: string, e: Event) {
    this.setState({
      // $FlowFixMe
      [type]: e.target.checked,
    });
  }
  render() {
    const { selectedSize, selectedFont, selectedAlign, outline, bold } = this.state;
    const size = Number.parseInt(selectedSize, 10);
    const labelStyle = Object.assign({}, style.label, {
      fontFamily: selectedFont,
      fontSize: size / 2 - (size > 50 ? 1 : 0),
      fontWeight: bold ? 'bold' : 'normal',
    });
    return (
      <Form method="POST" action="/">
        <FormInput name="text" style={labelStyle} multiline placeholder="Label Text"/>
        <br/>
        <div>
          <Checkbox label="Outline Font" checked={outline} onChange={this.handleBoolChange.bind(this, 'outline')}/>
          <Checkbox name="bold" label="bold" checked={bold} onChange={this.handleBoolChange.bind(this, 'bold')}/>
        </div>
        {outline ? (
          <FormSelect name="fontSize" label="Size" value={selectedSize}
            onChange={this.handleChange.bind(this, 'selectedSize')}
            options={sizesOutline}/>
        ) : (
          <FormSelect name="fontSize" label="Size" value={selectedSize}
            onChange={this.handleChange.bind(this, 'selectedSize')}
            options={sizesBitmap}/>
        )}

        {outline ? (
          <FormSelect name="font" label="Font" value={selectedFont}
            onChange={this.handleChange.bind(this, 'selectedFont')}
            options={fontsOutline}/>
        ) : (
          <FormSelect name="font" label="Font" value={selectedFont}
            onChange={this.handleChange.bind(this, 'selectedFont')}
            options={fontsBitMap}/>
        )}

        <FormSelect name="align" label="Align" value={selectedAlign}
          onChange={this.handleChange.bind(this, 'selectedAlign')}
          options={aligns}/>

        <Button submit>Print</Button>
      </Form>
    );
  }
}
