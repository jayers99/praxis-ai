---
domain: code
version: "1.0"
status: active
subtype: mobile
author: human
last_reviewed: "2026-01-04"
---

# Mobile Development Principles

This opinion file provides guidance for mobile application development across iOS, Android, and cross-platform frameworks.

## Platform-Specific Considerations

### iOS Development
- Follow Apple Human Interface Guidelines
- Use SwiftUI for modern UI development
- Implement proper App Store submission workflows
- Handle App Transport Security requirements

### Android Development
- Follow Material Design guidelines
- Use Jetpack Compose for modern UI
- Handle Play Store submission requirements
- Implement proper ProGuard/R8 configuration

### Cross-Platform
- Evaluate framework trade-offs (React Native, Flutter, etc.)
- Plan for platform-specific code when necessary
- Test on both platforms throughout development

## Mobile-Specific Architecture

### State Management
- Choose appropriate state management for your framework
- Plan for offline-first architecture when needed
- Handle background state transitions properly

### Performance
- Optimize for battery life and data usage
- Implement proper image caching and lazy loading
- Profile and measure performance regularly
- Test on low-end devices

### Security
- Implement certificate pinning for sensitive apps
- Use secure storage for tokens and credentials
- Handle biometric authentication properly
- Plan for jailbreak/root detection if needed

### Testing
- Implement unit tests for business logic
- Add UI tests for critical user flows
- Test on multiple device sizes and OS versions
- Use platform-specific testing tools (XCTest, Espresso)

## Release Management

### App Store Submission
- Automate build and submission processes
- Implement phased rollouts
- Monitor crash reports and analytics
- Plan for app review guidelines compliance

### Over-the-Air Updates
- Consider CodePush or similar for rapid updates
- Balance update frequency with user experience
- Maintain proper versioning strategy

## Quality Gates for Mobile Projects

### Formalize Stage
- [ ] Platform(s) selected and justified
- [ ] Architecture pattern chosen (MVVM, MVI, etc.)
- [ ] State management approach defined
- [ ] Offline/online requirements documented
- [ ] Performance requirements specified
- [ ] Security requirements documented

### Execute Stage
- [ ] UI tests cover critical user paths
- [ ] Tested on minimum supported OS versions
- [ ] Performance profiling completed
- [ ] Accessibility testing performed
- [ ] App Store/Play Store listings prepared

### Sustain Stage
- [ ] Crash reporting integrated and monitored
- [ ] Analytics tracking user behavior
- [ ] Regular security updates planned
- [ ] OS version adoption tracked
- [ ] Update rollout process documented
