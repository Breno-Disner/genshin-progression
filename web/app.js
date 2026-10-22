const views = [...document.querySelectorAll('.view')];
const nav = [...document.querySelectorAll('nav a')];
function route() {
  const id = location.hash.slice(1) || 'overview';
  const view = document.getElementById(id);
  const target = view?.classList.contains('view') ? view : document.getElementById('overview');
  views.forEach(section => { section.hidden = section !== target; });
  nav.forEach(link => {
    if (link.hash === `#${target.id}`) link.setAttribute('aria-current', 'page');
    else link.removeAttribute('aria-current');
  });
  document.getElementById('location').textContent = nav.find(link => link.hash === `#${target.id}`).textContent.trim().slice(1).trim();
  window.scrollTo(0, 0);
}
const normalize = value => value.normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase();
function filter(id) {
  const section = document.getElementById(id);
  const query = normalize(section.querySelector('[data-search]').value.trim());
  const date = section.querySelector('[data-date-filter]')?.value || '';
  let visible = 0;
  const cards = [...section.querySelectorAll('.searchable')];
  cards.forEach(card => {
    card.hidden = !normalize(card.textContent).includes(query) || (!!date && card.dataset.date !== date);
    if (!card.hidden) visible++;
  });
  section.querySelector('.result-count').textContent = `${visible} de ${cards.length} registros`;
  section.querySelector('.empty').hidden = visible !== 0;
}
document.querySelectorAll('[data-search], [data-date-filter]').forEach(input => {
  input.addEventListener('input', () => filter(input.dataset.search || input.dataset.dateFilter));
});
document.querySelectorAll('[data-clear]').forEach(button => button.addEventListener('click', () => {
  const section = document.getElementById(button.dataset.clear);
  section.querySelectorAll('input').forEach(input => { input.value = ''; });
  filter(section.id);
}));
['diary', 'snapshots', 'benchmarks'].forEach(filter);
window.addEventListener('hashchange', route);
route();

document.querySelectorAll('[data-chart-tab]').forEach(button => {
  button.addEventListener('click', () => {
    document.querySelectorAll('[data-chart-tab]').forEach(tab => {
      tab.setAttribute('aria-pressed', String(tab === button));
    });
    document.querySelectorAll('[data-chart-panel]').forEach(panel => {
      panel.hidden = panel.dataset.chartPanel !== button.dataset.chartTab;
    });
  });
});
