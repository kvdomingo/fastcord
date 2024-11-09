import * as sortImports from "@trivago/prettier-plugin-sort-imports";
import * as sveltePlugin from "prettier-plugin-svelte";
import * as tailwindPlugin from "prettier-plugin-tailwindcss";

/** @typedef {import("prettier").Options} PrettierOptions */
/** @typedef {import("@trivago/prettier-plugin-sort-imports").PluginConfig} SortImportsOptions */
/** @typedef {PrettierOptions | SortImportsOptions} Options */

/** @type {Options} */
const options = {
  arrowParens: "avoid",
  bracketSpacing: true,
  endOfLine: "lf",
  importOrder: ["^@?svelte", "<THIRD_PARTY_MODULES>", "^[./]"],
  importOrderSeparation: true,
  importOrderSortSpecifiers: true,
  jsxSingleQuote: false,
  quoteProps: "consistent",
  semi: true,
  singleQuote: false,
  printWidth: 88,
  tabWidth: 2,
  trailingComma: "all",
  plugins: [sortImports, sveltePlugin, tailwindPlugin],
  overrides: [
    {
      files: "*.svelte",
      options: {
        parser: "svelte",
      },
    },
  ],
};

export default options;
