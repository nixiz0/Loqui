// Sélectionner tous les éléments avec la classe "command"
const commandElements = document.querySelectorAll('.command');

// Pour chaque élément, ajouter un bouton de copie
commandElements.forEach(element => {
  const copyButton = document.createElement('button');
  copyButton.innerHTML = '+';
  copyButton.classList.add('copy-button');
  
  // Créer un gestionnaire d'événements pour le clic sur le bouton de copie
  copyButton.addEventListener('click', (event) => {
    const textToCopy = element.textContent.trim();

    // Créer un texte temporaire pour copier le texte sans inclure le bouton
    const tempElem = document.createElement('textarea');
    tempElem.value = textToCopy;
    document.body.appendChild(tempElem);
    tempElem.select();
    document.execCommand('copy');
    document.body.removeChild(tempElem);
  });
  
  // Ajouter le bouton de copie à côté de l'élément
  element.parentNode.insertBefore(copyButton, element.nextSibling);
});
