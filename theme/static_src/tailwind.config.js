/**
 * This is a minimal config.
 *
 * If you need the full config, get it from here:
 * https://unpkg.com/browse/tailwindcss@latest/stubs/defaultConfig.stub.js
 */
const defaultTheme = require('tailwindcss/defaultTheme')

module.exports = {
  mode : 'jit',
  darkMode: 'media',
  content: [
    /**
     * HTML. Paths to Django template files that will contain Tailwind CSS classes.
     */

    /*  Templates within theme app (<tailwind_app_name>/templates), e.g. base.html. */
    '../templates/**/*.html',

    /*
     * Main templates directory of the project (BASE_DIR/templates).
     * Adjust the following line to match your project structure.
     */
    '../../radio_funk/templates/**/*.html',

    /*
     * Templates in other django apps (BASE_DIR/<any_app_name>/templates).
     * Adjust the following line to match your project structure.
     */
    '../../**/templates/**/*.html'

    /**
     * JS: If you use Tailwind CSS in JavaScript, uncomment the following lines and make sure
     * patterns match your project structure.
     */
    /* JS 1: Ignore any JavaScript in node_modules folder. */
    // '!../../**/node_modules',
    /* JS 2: Process all JavaScript files in the project. */
    // '../../**/*.js',

    /**
     * Python: If you use Tailwind CSS classes in Python, uncomment the following line
     * and make sure the pattern below matches your project structure.
     */
    // '../../**/*.py'
  ],
  theme: {
    extend: {
      screens: {
        xs: '475px',
        ...defaultTheme.screens
      },
      fontFamily: {
        body: ["'Dongle'", "sans-serif"],
        sans: ["'Source Serif 4'", "system-ui"],
      },
      color: {
        grey : {
          900: "#1F1D2B",
          800: "#252836",
          700: "#393C49",
          500: "#ABBBC2",
          400: "#B7B9D2",
          100: "#EBE6E9"
        },
        yellow: {
          400: "#FFCE45",
          700: "#D4AC2B",
          900: "#9D5C0D"
        },
        primary: "#D4AC2B"
      },
      boxShadow : {
        primary : "6px 6px 10px rgba(255,224,51, 0.32)",
        'inverse-top' : "4px 4px #252B36",
        'inverse-bottom' : "4px -4px #252B36",
      }
    },
  },
  variants: {
    extend: {},
    scrollBar: ["rounded"],
  },
  plugins: [
    /**
     * '@tailwindcss/forms' is the forms plugin that provides a minimal styling
     * for forms. If you don't like it or have own styling for forms,
     * comment the line below to disable '@tailwindcss/forms'.
     */
    require('@tailwindcss/forms'),
    require('@tailwindcss/typography'),
    require('@tailwindcss/line-clamp'),
    require('@tailwindcss/aspect-ratio'),
    require('tailwind-scrollbar-hide'),
    require('tailwind-scrollbar')
  ]
}
