import type { Config } from "tailwindcss";

const config: Config = {
    content: [
        "./app/**/*.{js,ts,jsx,tsx,mdx}",
    ],
    theme: {
        extend: {
            colors: {
                primary: "#0F172A",
                secondary: "#334155",
                accent: "#3B82F6",
            },
        },
    },
    plugins: [
        require('@tailwindcss/typography'),
    ],
};
export default config;
