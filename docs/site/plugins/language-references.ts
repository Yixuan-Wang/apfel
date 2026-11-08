import { defineMdastPlugin } from "satteri";

const languages = new Set([
  "cpp",
  "go",
  "golang",
  "haskell",
  "hs",
  "julia",
  "jl",
  "kotlin",
  "kt",
  "py",
  "python",
  "rl",
  "rlang",
  "rs",
  "rust",
]);

function isLanguage(value: string): boolean {
  return languages.has(value);
}

function languageReferenceData(
  name: string,
  attributes: Record<string, string | null | undefined> | null | undefined,
) {
  const href = attributes?.href;
  const title = attributes?.title;
  const hProperties: Record<string, string | string[]> = {
    className: ["ref", name],
  };

  if (typeof href === "string" && href !== "") hProperties.href = href;
  if (typeof title === "string" && title !== "") hProperties.title = title;

  return {
    hName: typeof href === "string" && href !== "" ? "a" : "span",
    hProperties,
  };
}

/**
 * Renders `:python[content]{href="..."}`-style inline directives as language
 * references. The language name selects its visual treatment; it is not visible
 * document text.
 */
export const languageReferenceDirectives = defineMdastPlugin({
  name: "language-reference-directives",
  textDirective(node, context) {
    if (!isLanguage(node.name)) return;
    context.setProperty(node, "data", languageReferenceData(node.name, node.attributes));
  },
  link(node) {
    const [marker, ...children] = node.children;
    const name =
      marker?.type === "textDirective" && isLanguage(marker.name)
        ? marker.name
        : marker?.type === "text"
          ? marker.value.match(/^:([a-z]+)\s+/)?.[1]
          : undefined;

    if (!name || !isLanguage(name)) return;

    if (marker?.type === "text") {
      const text = marker.value.replace(/^:[a-z]+\s+/, "");
      if (text) children.unshift({ type: "text", value: text });
    }

    return {
      ...node,
      children,
      data: languageReferenceData(name, { href: node.url, title: node.title }),
    };
  },
});
