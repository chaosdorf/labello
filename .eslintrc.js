module.exports = {
  extends: 'marudor',
  env: {
    browser: true,
    node: true,
  },
  globals: {
    IS_PRODUCTION: false,
    sizesBitmap: false,
    sizesOutline: false,
    fontsOutline: false,
    fontsBitMap: false,
    aligns: false,
    charStyles: false,
    cuts: false,
  },
  rules: {
    'no-mixed-operators': 0,
  },
};
