/* eslint camelcase: 0 */
const path = require('path');
const process = require('process');
const webpack = require('webpack');
const fs = require('fs');

let node_env = process.env.NODE_ENV || 'development';
if (!fs.existsSync(`./src/config.${node_env}.js`)) {
  node_env = 'development';
}
const plugins = [
  new webpack.NoErrorsPlugin(),
  new webpack.DefinePlugin({
    'process.env': {
      NODE_ENV: JSON.stringify(node_env),
    },
    IS_PRODUCTION: JSON.stringify(node_env === 'production'),
  }),
];

if (node_env === 'production') {
  plugins.push(
    new webpack.optimize.UglifyJsPlugin()
  );
}

module.exports = {
  devtool: node_env === 'production' ? undefined : 'inline-cheap-module-source-map',
  eslint: {
    configFile: './.eslintrc.js',
    failOnWarning: false,
    failOnError: true,
  },
  context: __dirname,
  resolve: {
    extensions: ['', '.js', '.jsx', '.json'],
    root: path.resolve('src'),
  },
  entry: [
    './src/entry.js',
  ],
  output: {
    path: path.resolve('www'),
    filename: 'app.js',
    publicPath: '',
  },
  module: {
    loaders: [
      { test: /\.less$/, loader: 'style!css!less' },
      { test: /\.css$/, loader: 'style!css' },
      { test: /\.CSS.js$/, exclude: /(node_modules|dependency)/, loader: 'inline-css!babel!eslint' },
      { test: /^((?!CSS\.js$).)*(\.jsx?)$/,
        exclude: /(node_modules|external)/,
        loader: 'babel!eslint',
      },
      { test: /\.(jpg|png|gif)$/, loader: 'file!image' },
      { test: /\.woff2?(\?v=.*)?$/, loader: 'file' },
      { test: /\.(eot|ttf|svg|otf)(\?v=.*)?$/, loader: 'file' },
    ],
  },
  plugins,
};
