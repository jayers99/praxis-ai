# Opinion: GUI Application

> Desktop and web graphical user interfaces

## Design Constraints

- Responsive to user input (no blocking operations on UI thread)
- Consistent visual hierarchy and spacing
- Accessible (keyboard navigation, screen reader support)
- Graceful error handling with user-friendly messages
- State changes are predictable and reversible where possible

## Requirements

- Clear visual feedback for all user actions
- Loading states for async operations
- Undo/redo for destructive actions where feasible
- Consistent component patterns throughout application

## Anti-Patterns

- Modal dialogs for non-critical information
- Hidden or buried settings
- Ambiguous icons without labels
- Inconsistent navigation patterns
- Silent failures

## Assumed Context

- Used by non-technical users
- Variable screen sizes and input methods
- Accessibility requirements

## Summary

Prioritize responsiveness, clarity, accessibility, and forgiving interactions.
