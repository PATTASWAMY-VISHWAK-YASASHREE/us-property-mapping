# Frontend Component Structure

This directory contains the Vue components for the Wealth Map application, organized by functionality.

## Authentication Components

Located in `/components/auth/`:

- **LoginForm.vue**: User login form with email and password fields
- **RegisterForm.vue**: User registration form with validation
- **InviteUsers.vue**: Interface for inviting new users to the platform
- **MfaSetup.vue**: Multi-factor authentication setup wizard
- **PasswordReset.vue**: Password reset request and confirmation forms

## Layout Components

Located in `/components/layout/`:

- **MainLayout.vue**: Main application layout wrapper
- **Sidebar.vue**: Application sidebar with navigation
- **Header.vue**: Application header with search and user menu
- **NotificationCenter.vue**: Notification dropdown and management
- **UserMenu.vue**: User profile dropdown menu
- **AppHeader.vue**: Legacy header component
- **AppFooter.vue**: Footer component

## Map Components

Located in `/components/map/`:

- **PropertyMap.vue**: Main map component for displaying properties
- **MapControls.vue**: Zoom, pan, and other map control buttons
- **PropertyCluster.vue**: Clustering component for property markers
- **PropertyMarker.vue**: Individual property marker on the map
- **MapLayerSelector.vue**: Layer toggle controls for the map

## Search Components

Located in `/components/search/`:

- **SearchBar.vue**: Global search input component

## Testing

Component tests are located in `__tests__` directories within each component category. Tests are written using Vitest and Vue Test Utils.

## Component Relationships

- `MainLayout.vue` uses `Sidebar.vue` and `Header.vue`
- `Header.vue` uses `NotificationCenter.vue` and `UserMenu.vue`
- `PropertyMap.vue` uses `MapControls.vue`, `MapLayerSelector.vue`, `PropertyMarker.vue`, and `PropertyCluster.vue`

## Styling

Components use scoped CSS to prevent style leakage. The application uses a combination of custom CSS and utility classes.