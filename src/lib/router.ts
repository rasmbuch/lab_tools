export type Route = 'dashboard' | 'energy' | 'intensity' | 'eta' | 'omega' | 'about' | 'impressum' | 'aboutme';

const HASH_TO_ROUTE: Record<string, Route> = {
  '':          'dashboard',
  'energy':    'energy',
  'intensity': 'intensity',
  'eta':       'eta',
  'omega':     'omega',
  'about':     'about',
  'impressum': 'impressum',
  'aboutme':   'aboutme',
};

export function parseHash(): Route {
  const hash = window.location.hash.replace(/^#\/?/, '');
  return HASH_TO_ROUTE[hash] ?? 'dashboard';
}

export function navigate(route: Route): void {
  window.location.hash = route === 'dashboard' ? '/' : `/${route}`;
}
