const TARGET_ROUTE = 'targetRoute';

export function setRouteToSessionStorage(route) {
  sessionStorage.setItem(TARGET_ROUTE, route);
}

export function getRouteFromSessionStorage() {
  return sessionStorage.getItem(TARGET_ROUTE) || '/catalog';
}

export function removeRouteFromSessionStorage() {
  sessionStorage.removeItem(TARGET_ROUTE);
}
