Array.from(document.getElementsByTagName("a")).forEach((link) => {
  if (link.innerText.startsWith(":")) {
    const directive = link.childNodes[0].textContent.match(/^:(\w+)/)[1];
    link.classList.add("ref", directive);

    link.childNodes[0].textContent = link.childNodes[0].textContent.replace(/^:\w+\s*/, "");
  }
});