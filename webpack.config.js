/* eslint camelcase: 0 header/header: 0 */
const path = require('path');
const process = require('process');
const webpack = require('webpack');

const node_env = process.env.NODE_ENV || 'development';
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
  plugins.push(new webpack.optimize.UglifyJsPlugin());
}

module.exports = {
  context: __dirname,
  resolve: {
    extensions: ['.js', '.jsx'],
    modules: [path.resolve('src'), 'node_modules'],
  },
  entry: ['entry.js'],
  output: {
    path: path.resolve('www'),
    filename: 'app.js',
    publicPath: '',
  },
  module: {
    rules: [
      { test: /\.less$/, loader: 'style-loader!css-loader!less-loader' },
      { test: /\.css$/, loader: 'style-loader!css-loader' },
      {
        test: /\.jsx?$/,
        exclude: /(node_modules|primusClient)/,
        loader: 'babel-loader',
        include: [path.resolve(__dirname, 'src')],
        query: { cacheDirectory: true },
      },
      { test: /\.(jpg|png|gif)$/, loader: 'file-loader!image-loader' },
      { test: /\.woff2?(\?v=.*)?$/, loader: 'file-loader' },
      { test: /\.(eot|ttf|svg|otf)(\?v=.*)?$/, loader: 'file-loader' },
    ],
  },
  plugins,
};

if (process.env.NODE_ENV !== 'production') {
  //Art der Sourcemap
  module.exports.devtool = 'source-map';
  module.exports.module.rules.push({
    enforce: 'pre',
    test: /.jsx?$/,
    loader: 'eslint-loader',
    include: [path.resolve(__dirname, 'src')],
    exclude: /(.*\.config.*|.*node_modules.*|.*inferno.*)/,
  });
}
