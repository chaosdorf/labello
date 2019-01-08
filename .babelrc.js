module.exports = {
  presets: [
    [
      '@babel/preset-env',
      {
        loose: false,
        useBuiltIns: 'entry',
        modules: false,
      },
    ],
    '@babel/preset-react',
    '@babel/preset-flow',
    'babel-preset-joblift',
  ],
  env: {
    production: {
      compact: true,
      plugins: ['@babel/plugin-transform-react-constant-elements'],
    },
  },
};
