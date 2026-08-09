Array.from(document.getElementsByTagName("a")).forEach((link) => {
  link.target = "_blank";
  link.rel = "noopener noreferrer";

  if (link.innerText.startsWith(":")) {
    const directive = link.childNodes[0].textContent.match(/^:(\w+)/)[1];
    link.classList.add("ref", directive);

    link.childNodes[0].textContent = link.childNodes[0].textContent.replace(/^:\w+\s*/, "");
  }
});