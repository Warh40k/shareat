export default async function loadLayoutMiddleware(to) {
  const layout = to.meta.layout || 'DefaultLayout';
  const component = await import(`@/core/ui/layouts/${layout}.vue`);
  to.meta.layoutComponent = component.default;
}
