import plugin from 'tailwindcss/plugin'
import defaultTheme from 'tailwindcss/defaultTheme'

export default {
  content: [
    './pages/**/*.vue',
    './components/**/*.vue',
    './layouts/**/*.vue',
    './app.vue'
  ],
  theme: {
    screens: {
      sm: '480px',
      md: '768px',
      lg: '976px',
      xl: '1440px',
    },
    extend: {
      fontFamily: {
        sans: [
          'Montserrat',
          ...defaultTheme.fontFamily.sans,
        ]
      },
      spacing: {
        32: '8rem',
        '-32': '-8rem',
      },
      colors: {
        bluepastel: '#C4E6FA',
        pricefree: '#E6F4FE',
        pricebasic: '#FEF6E9',
        pricepremium: '#EBF4F3',

        /**
         * palette generated with https://uicolors.app/create
         */
        cerulean: {
          '50': '#eff9ff',
          '100': '#def2ff',
          '200': '#b6e8ff',
          '300': '#75d8ff',
          '400': '#2cc4ff',
          '500': '#009fe3', // default value
          '600': '#008ad4',
          '700': '#006eab',
          '800': '#005d8d',
          '900': '#064d74',
          '950': '#04314d',
          DEFAULT: '#009fe3',
        },
        purple: {
          '50': '#eef1ff',
          '100': '#e1e6fe',
          '200': '#c8d1fd',
          '300': '#a7b1fa',
          '400': '#8489f5',
          '500': '#6966ee',
          '600': '#584ae1',
          '700': '#4c3bc7',
          '800': '#3e33a0',
          '900': '#36307f',
          '950': '#29235c', // default value
          DEFAULT: '#29235c',
        },
      },
    }
  },
  plugins: [
    plugin(function({ addBase, theme }) {
      addBase({
        'h1': {
          fontSize: theme('fontSize.3xl'),
          fontWeight: theme('fontWeight.semibold'),
        },
        'h2': {
          fontSize: theme('fontSize.xl'),
          fontWeight: theme('fontWeight.semibold'),
        },
        'h3': {
          fontSize: theme('fontSize.lg')
        },
      })
    })
  ]

}
