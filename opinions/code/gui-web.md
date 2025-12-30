# Opinion: Web GUI Application

> Extends [gui.md](gui.md) with web-specific patterns

## Base Opinion

See [gui.md](gui.md) for general GUI ideals. This file adds web-specific constraints.

## Architecture

- Component-based UI structure
- Clear separation of state management from presentation
- API-first backend integration
- Progressive enhancement where feasible

## Performance

- Optimize initial load time (code splitting, lazy loading)
- Minimize layout shifts (CLS)
- Responsive images and assets
- Cache strategies for static and dynamic content

## Browser Considerations

- Cross-browser compatibility
- Mobile-first responsive design
- Touch and mouse input support
- Handle offline/poor connectivity gracefully

## Security

- Sanitize all user input
- HTTPS only
- CSP headers where possible
- No sensitive data in client-side storage

## Accessibility

- Semantic HTML
- ARIA labels where needed
- Keyboard navigation
- Color contrast compliance (WCAG)
- Focus management for dynamic content

## Anti-Patterns

- Inline styles for theming
- Direct DOM manipulation in component frameworks
- Blocking scripts in document head
- Client-side secrets or API keys
- Infinite scroll without pagination fallback

## Summary

Web GUIs prioritizing performance, cross-browser compatibility, security, and accessibility.
