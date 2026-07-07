/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./shortener/templates/**/*.html",
  ],
  theme: {
    extend: {
      colors: {
        "surface-dim": "#131313",
        "surface-bright": "#3a3939",
        "surface-container-lowest": "#0e0e0e",
        "surface-container-low": "#1c1b1b",
        "surface-container": "#201f1f",
        "surface-container-high": "#2a2a2a",
        "surface-container-highest": "#353534",
        "on-surface": "#e5e2e1",
        "on-surface-variant": "#c4c9ac",
        "inverse-surface": "#e5e2e1",
        "inverse-on-surface": "#313030",
        outline: "#8e9379",
        "outline-variant": "#444933",
        "surface-tint": "#abd600",
        "primary-container": "#c3f400",
        "on-primary-container": "#556d00",
        "inverse-primary": "#506600",
        "secondary-container": "#474746",
        "on-secondary-container": "#b7b5b4",
        "surface": "#131313",
        background: "#131313",
        "on-background": "#e5e2e1",
        "surface-variant": "#353534",
      },
      fontFamily: {
        sans: ["Geist", "sans-serif"],
        mono: ["Geist Mono", "monospace"],
      },
      borderRadius: {
        DEFAULT: "0.125rem",
        lg: "0.25rem",
        xl: "0.5rem",
        "2xl": "0.75rem",
      },
      spacing: {
        "stack-sm": "8px",
        "stack-md": "16px",
        "stack-lg": "32px",
        gutter: "24px",
        "margin-mobile": "16px",
        "margin-desktop": "40px",
        "container-max": "1200px",
      },
      fontSize: {
        "headline-lg": [
          "48px",
          { lineHeight: "1.1", letterSpacing: "-0.02em", fontWeight: "700" },
        ],
        "headline-lg-mobile": [
          "32px",
          { lineHeight: "1.2", letterSpacing: "-0.02em", fontWeight: "700" },
        ],
        "headline-md": [
          "24px",
          { lineHeight: "1.3", letterSpacing: "-0.01em", fontWeight: "600" },
        ],
        "body-lg": [
          "18px",
          { lineHeight: "1.6", letterSpacing: "0", fontWeight: "400" },
        ],
        "body-md": [
          "16px",
          { lineHeight: "1.6", letterSpacing: "0", fontWeight: "400" },
        ],
        "label-md": [
          "14px",
          { lineHeight: "1", letterSpacing: "0.02em", fontWeight: "500" },
        ],
        "label-sm": [
          "12px",
          { lineHeight: "1", letterSpacing: "0.05em", fontWeight: "600" },
        ],
        "mono-label": [
          "14px",
          { lineHeight: "1", letterSpacing: "0", fontWeight: "400" },
        ],
      },
    },
  },
  plugins: [],
};
