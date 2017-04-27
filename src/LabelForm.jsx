// @flow
import React from 'react';
import 'elemental/less/elemental.less';
import { Button, Checkbox, Form, FormInput, FormSelect } from 'elemental';

type State = {
  selectedSize: string,
  selectedFont: string,
  selectedAlign?: string,
  outline: boolean,
  bold: boolean
};

const style = {
  label: {
    padding: 10,
    width: 450,
    maxWidth: '100%',
    wordBreak: 'break-all',
  },
};

export default class LabelForm extends React.Component {
  state: State = {
    outline: true,
    bold: false,
    selectedFont: 'lettergothic',
    selectedSize: '42',
  };
  handleChange(type: string) {
    return (value: string) => {
      this.setState({
        [type]: value,
      });
    };
  }
  handleBoolChange(type: string) {
    return (e: Event) => {
      this.setState({
        // $FlowFixMe
        [type]: e.target.checked,
      });
    };
  }
  render() {
    const {
      selectedSize,
      selectedFont,
      selectedAlign,
      outline,
      bold,
    } = this.state;
    const size = Number.parseInt(selectedSize, 10);
    const labelStyle = Object.assign({}, style.label, {
      fontFamily: selectedFont,
      fontSize: size / 2 - (size > 50 ? 1 : 0),
      fontWeight: bold ? 'bold' : 'normal',
    });
    return (
      <Form method="POST" target="_blank" action="/">
        <FormInput
          name="text"
          style={labelStyle}
          multiline
          placeholder="Label Text"/>
        <br />
        <div>
          <Checkbox
            label="Outline Font"
            checked={outline}
            onChange={this.handleBoolChange('outline')}/>
          <Checkbox
            name="bold"
            label="bold"
            checked={bold}
            onChange={this.handleBoolChange('bold')}/>
        </div>
        {outline
          ? <FormSelect
              name="fontSize"
              label="Size"
              value={selectedSize}
              onChange={this.handleChange('selectedSize')}
              options={sizesOutline}/>
          : <FormSelect
              name="fontSize"
              label="Size"
              value={selectedSize}
              onChange={this.handleChange('selectedSize')}
              options={sizesBitmap}/>}

        {outline
          ? <FormSelect
              name="font"
              label="Font"
              value={selectedFont}
              onChange={this.handleChange('selectedFont')}
              options={fontsOutline}/>
          : <FormSelect
              name="font"
              label="Font"
              value={selectedFont}
              onChange={this.handleChange('selectedFont')}
              options={fontsBitMap}/>}

        <FormSelect
          name="align"
          label="Align"
          value={selectedAlign}
          onChange={this.handleChange('selectedAlign')}
          options={aligns}/>

        <Button submit>{'Print'}</Button>
      </Form>
    );
  }
}
