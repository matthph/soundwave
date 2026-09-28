const photoExts = ['jpg', 'jpeg', 'png', 'webp', 'gif'];

document.querySelectorAll('.gallery img[data-src]').forEach((img) => {
  const base = img.dataset.src;
  let index = 0;

  const tryNext = () => {
    if (index >= photoExts.length) {
      img.remove();
      return;
    }
    img.src = `${base}.${photoExts[index]}`;
    index += 1;
  };

  img.addEventListener('error', tryNext);
  tryNext();
});
