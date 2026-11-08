import path from "node:path";
import { languageReferenceDirectives } from "./plugins/language-references";

// The Python source is the third volume. The engine sets DOCS_SOURCE_ROOT to the
// source mount path inside the container; locally it defaults to a sibling checkout.
const sourceRoot = process.env.DOCS_SOURCE_ROOT ?? ".";

/**
 * Per-package site configuration. The engine (`astro.config.mjs`) reads this
 * fragment and wires it into Starlight. Paths are resolved relative to the
 * project root.
 */
const site = {
  url: "https://apfel.yixuan-wang.site",
  title: "Apfel",
  description: "A Python functional extras library.",
  favicon: "/favicon.svg",
  logo: {
    src: "./docs/site/assets/apple.png",
    alt: "Apfel",
    replacesTitle: false,
  },
  social: [
    { icon: "github", label: "GitHub", href: "https://github.com/Yixuan-Wang/apfel" },
  ],
  // Markdown (mdast) plugins contributed by this package.
  mdastPlugins: [languageReferenceDirectives],
  // Package stylesheets, applied after the engine defaults so they can override.
  styles: ["./docs/site/styles/style.css", "./docs/site/styles/this.css"],
  // starlight-pydocs configuration. Omit to disable API reference generation.
  pydocs: {
    packages: [
      {
        name: "apfel",
        base: "api/apfel",
        docstringStyle: "google",
        search: [path.join(sourceRoot, "src")],
        members: {
          // include: [
          //   "apfel.core.**",
          //   "apfel.container.**",
          //   "apfel.expr.**",
          //   "apfel.impt.**",
          // ],
          exclude: ["apfel", "apfel.experimental.**"],
        },
        filters: {
          private: false,
          special: true,
          imported: false,
          inherited: false,
          duplicateAliases: false,
          reexports: "link",
        },
        sourceLink: {
          host: "github",
          repo: "Yixuan-Wang/apfel",
          root: sourceRoot,
        },
        sidebar: { label: "Reference", collapsed: true },
      },
    ],
    inventories: ["python"],
  },
  // Guide sidebar. The pydocs group is appended by the engine when pydocs is set.
  sidebar: [
    {
      label: "Guide",
      items: [
        { label: "Introduction", slug: "introduction" },
        { label: "Installation", slug: "installation" },
        { label: "Prelude", slug: "prelude" },
      ],
    },
  ],
};

export default site;
