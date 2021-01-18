const colors = require('tailwindcss/colors')

module.exports = {
  purge: {},
  theme: {
    extends: {
      colors: {
        blue: colors.cyan
      }
    }
  },
  variants: {
    extend: {
      backgroundColor: ['disabled'],
      cursor: ['disabled']
    }
  }
};
