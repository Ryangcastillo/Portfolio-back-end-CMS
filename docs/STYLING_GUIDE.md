# Styling Guide & Design System

> Frontend component conventions, design system usage, and UI consistency guidelines for Stitch CMS

**Reference**: CONST-P11 (UI Consistency), ADR-0002 (Frontend Technology Decisions)

## 🎨 Overview

This guide establishes styling conventions, component patterns, and design system usage for Stitch CMS frontend development. It ensures consistent user experience and maintainable UI code across the application.

## Tailwind CSS Setup & Best Practices

1. **Version & Installation** – Use the latest stable version of Tailwind CSS. Install locally via npm/yarn, avoid global installs.
2. **Configuration** – Customize `tailwind.config.js` to define your color palette, spacing scale, font families, and breakpoints. Example:

```js
// tailwind.config.js
module.exports = {
  content: ['./src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#f0f9ff',
          500: '#3b82f6',
          900: '#1e3a8a',
        },
      },
    },
  },
  plugins: [],
};
```

3. **Utility‑first philosophy** – Use Tailwind's utility classes for most layouts, spacing, typography, and colors. Avoid custom CSS unless necessary.
4. **JIT mode & Purge** – Enable just‑in‑time (JIT) mode and configure purge to remove unused styles for lean CSS bundles.
5. **Class ordering** – Use recommended class ordering (via ESLint plugin) for readability and maintainability.

---

## 🏗️ Design System Foundation

### Technology Stack (per ADR-0002)
- **Framework**: Next.js 14+ with App Router
- **Styling**: Tailwind CSS v4.1.9 with custom configuration
- **Components**: Shadcn/ui component library
- **Theming**: CSS variables with dark/light mode support
- **Animations**: Tailwind Animate CSS + custom animations
- **Icons**: Lucide React icon library

### Design Principles
1. **Consistency**: Uniform spacing, typography, and color usage
2. **Accessibility**: WCAG 2.1 AA compliance minimum
3. **Responsive**: Mobile-first, progressive enhancement
4. **Performance**: Optimized CSS delivery and minimal runtime
5. **Maintainability**: Systematic approach to styling

## 🎨 Color System

### Color Palette
Our color system uses CSS variables for consistency and theme switching:

#### **Primary Colors**
```css
:root {
  --background: #ffffff;        /* Main background */
  --foreground: #000000;        /* Primary text */
  --primary: #000000;           /* Primary actions */
  --primary-foreground: #ffffff; /* Text on primary */
}

.dark {
  --background: #0a0a0a;        /* Dark background */
  --foreground: #ffffff;        /* Dark text */
  --primary: #ffffff;           /* Dark primary */
  --primary-foreground: #000000; /* Dark primary text */
}
```

#### **Semantic Colors**
```css
:root {
  /* UI Elements */
  --card: #ffffff;
  --card-foreground: #000000;
  --popover: #ffffff;
  --popover-foreground: #000000;
  
  /* Interactive */
  --secondary: #f3f4f6;
  --secondary-foreground: #000000;
  --accent: #f3f4f6;
  --accent-foreground: #000000;
  
  /* Feedback */
  --destructive: #ef4444;
  --destructive-foreground: #ffffff;
  --success: #10b981;
  --warning: #f59e0b;
  
  /* Borders & Backgrounds */
  --border: #e5e7eb;
  --input: #ffffff;
  --ring: #3b82f6;
  --muted: #f9fafb;
  --muted-foreground: #6b7280;
}
```

### Usage Guidelines
✅ **Do**:
- Use CSS variables for all colors
- Follow semantic naming (destructive for errors, etc.)
- Support both light and dark themes
- Test color contrast ratios

❌ **Don't**:
- Use hardcoded hex values in components
- Create custom colors without system integration
- Ignore dark mode variations
- Use colors that fail accessibility standards

## 📝 Typography System

### Font Stack
```css
/* Primary font - Geist Sans */
font-family: var(--font-geist-sans), ui-sans-serif, system-ui;

/* Monospace font - Geist Mono */  
font-family: var(--font-geist-mono), ui-monospace, 'Cascadia Code';
```

### Typography Scale
```css
/* Headings */
.text-4xl { font-size: 2.25rem; line-height: 2.5rem; }    /* h1 */
.text-3xl { font-size: 1.875rem; line-height: 2.25rem; }  /* h2 */
.text-2xl { font-size: 1.5rem; line-height: 2rem; }       /* h3 */
.text-xl  { font-size: 1.25rem; line-height: 1.75rem; }   /* h4 */
.text-lg  { font-size: 1.125rem; line-height: 1.75rem; }  /* h5 */

/* Body text */
.text-base { font-size: 1rem; line-height: 1.5rem; }      /* Default */
.text-sm   { font-size: 0.875rem; line-height: 1.25rem; } /* Small */
.text-xs   { font-size: 0.75rem; line-height: 1rem; }     /* Extra small */

/* Weight variations */
.font-light    { font-weight: 300; }
.font-normal   { font-weight: 400; }
.font-medium   { font-weight: 500; }
.font-semibold { font-weight: 600; }
.font-bold     { font-weight: 700; }
```

### Typography Components
```tsx
// Heading component with consistent styling
const Heading = ({ level, children, className = "" }: {
  level: 1 | 2 | 3 | 4 | 5;
  children: React.ReactNode;
  className?: string;
}) => {
  const baseClasses = "font-semibold tracking-tight";
  const levelClasses = {
    1: "text-4xl",
    2: "text-3xl", 
    3: "text-2xl",
    4: "text-xl",
    5: "text-lg"
  };
  
  const Tag = `h${level}` as keyof JSX.IntrinsicElements;
  
  return (
    <Tag className={cn(baseClasses, levelClasses[level], className)}>
      {children}
    </Tag>
  );
};
```

## 🏗️ Layout System

### Spacing Scale
```css
/* Tailwind spacing system */
.p-1  { padding: 0.25rem; }   /* 4px */
.p-2  { padding: 0.5rem; }    /* 8px */
.p-3  { padding: 0.75rem; }   /* 12px */
.p-4  { padding: 1rem; }      /* 16px */
.p-5  { padding: 1.25rem; }   /* 20px */
.p-6  { padding: 1.5rem; }    /* 24px */
.p-8  { padding: 2rem; }      /* 32px */
.p-10 { padding: 2.5rem; }    /* 40px */
.p-12 { padding: 3rem; }      /* 48px */
```

### Grid System
```tsx
// Responsive grid layout
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
  {/* Grid items */}
</div>

// Container widths
<div className="container mx-auto px-4">          {/* Default container */}
<div className="max-w-4xl mx-auto px-6">         {/* Content container */}
<div className="max-w-2xl mx-auto px-4">         {/* Narrow container */}
```

### Layout Components
```tsx
// Page layout wrapper
const PageLayout = ({ children, title }: {
  children: React.ReactNode;
  title?: string;
}) => (
  <div className="min-h-screen bg-background">
    <div className="container mx-auto px-4 py-8">
      {title && <Heading level={1} className="mb-8">{title}</Heading>}
      {children}
    </div>
  </div>
);

// Card layout
const Card = ({ children, className = "" }: {
  children: React.ReactNode;
  className?: string;
}) => (
  <div className={cn(
    "bg-card text-card-foreground rounded-lg border shadow-sm p-6",
    className
  )}>
    {children}
  </div>
);
```

## 🧩 Component Conventions

### Shadcn/ui Components
We use Shadcn/ui as our base component library with customizations:

#### **Component Import Structure**
```tsx
// UI components (from Shadcn/ui)
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

// Custom components (organized by domain)
import { LoginForm } from "@/components/auth/login-form";
import { ContentEditor } from "@/components/content/content-editor";
import { DashboardLayout } from "@/components/dashboard/dashboard-layout";
```

#### **Component Customization**
```tsx
// Extend Shadcn components with custom variants
const buttonVariants = cva(
  "inline-flex items-center justify-center rounded-md text-sm font-medium transition-colors",
  {
    variants: {
      variant: {
        default: "bg-primary text-primary-foreground hover:bg-primary/90",
        destructive: "bg-destructive text-destructive-foreground hover:bg-destructive/90",
        outline: "border border-input hover:bg-accent hover:text-accent-foreground",
        secondary: "bg-secondary text-secondary-foreground hover:bg-secondary/80",
        ghost: "hover:bg-accent hover:text-accent-foreground",
        link: "underline-offset-4 hover:underline text-primary",
        // Custom variants for Stitch CMS
        cms: "bg-gradient-to-r from-primary to-secondary hover:opacity-90",
      },
      size: {
        default: "h-10 py-2 px-4",
        sm: "h-9 px-3 rounded-md",
        lg: "h-11 px-8 rounded-md",
        icon: "h-10 w-10",
      },
    },
    defaultVariants: {
      variant: "default",
      size: "default",
    },
  }
);
```

### Custom Component Patterns

#### **Form Components**
```tsx
// Consistent form styling
const FormField = ({ 
  label, 
  error, 
  children, 
  required = false 
}: FormFieldProps) => (
  <div className="space-y-2">
    <Label className={cn(
      "text-sm font-medium",
      error && "text-destructive"
    )}>
      {label}
      {required && <span className="text-destructive ml-1">*</span>}
    </Label>
    {children}
    {error && (
      <p className="text-sm text-destructive">{error}</p>
    )}
  </div>
);

// Usage example
<FormField label="Email" error={errors.email} required>
  <Input 
    type="email" 
    {...register('email')}
    className={cn(error && "border-destructive")}
  />
</FormField>
```

#### **Loading States**
```tsx
// Consistent loading patterns
const LoadingSpinner = ({ size = "default" }: { size?: "sm" | "default" | "lg" }) => {
  const sizeClasses = {
    sm: "w-4 h-4",
    default: "w-6 h-6", 
    lg: "w-8 h-8"
  };
  
  return (
    <div className={cn("animate-spin rounded-full border-2 border-muted border-t-primary", sizeClasses[size])} />
  );
};

const LoadingButton = ({ loading, children, ...props }: ButtonProps & { loading?: boolean }) => (
  <Button disabled={loading} {...props}>
    {loading && <LoadingSpinner size="sm" className="mr-2" />}
    {children}
  </Button>
);
```

## 📱 Responsive Design

### Breakpoints
```css
/* Tailwind breakpoints */
sm: 640px   /* Small devices */
md: 768px   /* Medium devices */  
lg: 1024px  /* Large devices */
xl: 1280px  /* Extra large devices */
2xl: 1536px /* 2X large devices */
```

### Responsive Patterns
```tsx
// Mobile-first responsive design
<div className="
  grid 
  grid-cols-1           /* Mobile: 1 column */
  md:grid-cols-2        /* Tablet: 2 columns */  
  lg:grid-cols-3        /* Desktop: 3 columns */
  gap-4 
  md:gap-6              /* Larger gaps on bigger screens */
">

// Responsive text sizes
<h1 className="
  text-2xl              /* Mobile: 24px */
  md:text-3xl           /* Tablet: 30px */
  lg:text-4xl           /* Desktop: 36px */
">

// Responsive padding/margins  
<div className="
  p-4                   /* Mobile: 16px padding */
  md:p-6                /* Tablet: 24px padding */
  lg:p-8                /* Desktop: 32px padding */
">
```

### Navigation Patterns
```tsx
// Responsive navigation
const Navigation = () => (
  <nav className="border-b">
    <div className="container mx-auto px-4">
      <div className="flex items-center justify-between h-16">
        <Logo />
        
        {/* Desktop navigation */}
        <div className="hidden md:flex items-center space-x-8">
          <NavLinks />
        </div>
        
        {/* Mobile navigation toggle */}
        <div className="md:hidden">
          <MobileMenuButton />
        </div>
      </div>
    </div>
    
    {/* Mobile menu */}
    <MobileMenu className="md:hidden" />
  </nav>
);
```

## ♿ Accessibility Guidelines

### WCAG 2.1 AA Compliance
✅ **Requirements**:
- Color contrast ratio ≥ 4.5:1 for normal text
- Color contrast ratio ≥ 3:1 for large text
- All interactive elements keyboard accessible
- Proper heading hierarchy (h1 → h2 → h3)
- Alt text for all meaningful images
- Form labels properly associated

### Accessibility Patterns
```tsx
// Proper form labeling
<div className="space-y-2">
  <Label htmlFor="email">Email Address</Label>
  <Input 
    id="email"
    type="email" 
    aria-describedby="email-error"
    aria-invalid={!!errors.email}
  />
  {errors.email && (
    <p id="email-error" className="text-sm text-destructive" role="alert">
      {errors.email.message}
    </p>
  )}
</div>

// Keyboard navigation
const DropdownMenu = () => (
  <div 
    role="menu" 
    onKeyDown={handleKeyDown}
    aria-labelledby="menu-button"
  >
    <button 
      role="menuitem" 
      tabIndex={0}
      className="focus:outline-none focus:ring-2 focus:ring-primary"
    >
      Menu Item
    </button>
  </div>
);

// Screen reader support
<button aria-label="Close dialog" className="sr-only">
  <X className="w-4 h-4" />
</button>
```

### Focus Management
```css
/* Focus styles */
.focus\:ring-2:focus {
  --tw-ring-offset-shadow: var(--tw-ring-inset) 0 0 0 var(--tw-ring-offset-width) var(--tw-ring-offset-color);
  --tw-ring-shadow: var(--tw-ring-inset) 0 0 0 calc(2px + var(--tw-ring-offset-width)) var(--tw-ring-color);
  box-shadow: var(--tw-ring-offset-shadow), var(--tw-ring-shadow), var(--tw-shadow, 0 0 #0000);
}

.focus\:ring-primary:focus {
  --tw-ring-color: hsl(var(--primary));
}
```

## 🎭 Animation Guidelines

### Animation Principles
1. **Purposeful**: Animations should enhance UX, not distract
2. **Fast**: Keep animations under 300ms for micro-interactions
3. **Easing**: Use natural easing curves (ease-out, ease-in-out)
4. **Reduced Motion**: Respect prefers-reduced-motion settings

### Animation Patterns
```css
/* Tailwind animate classes */
.animate-fade-in {
  animation: fadeIn 200ms ease-out;
}

.animate-slide-in {
  animation: slideIn 300ms ease-out;
}

.animate-pulse {
  animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}

/* Custom animations */
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

@keyframes slideIn {
  from { transform: translateX(-100%); }
  to { transform: translateX(0); }
}
```

### React Animation Patterns
```tsx
// Conditional animations with framer-motion
const AnimatedCard = ({ isVisible }: { isVisible: boolean }) => (
  <motion.div
    initial={{ opacity: 0, y: 20 }}
    animate={{ opacity: isVisible ? 1 : 0, y: isVisible ? 0 : 20 }}
    transition={{ duration: 0.2, ease: "easeOut" }}
    className="bg-card rounded-lg p-6"
  >
    Content
  </motion.div>
);

// Loading state animations
const SkeletonLoader = () => (
  <div className="animate-pulse">
    <div className="h-4 bg-muted rounded w-3/4 mb-2"></div>
    <div className="h-4 bg-muted rounded w-1/2"></div>
  </div>
);
```

## 📁 File Organization

### Component Structure
```
components/
├── ui/                     # Shadcn/ui base components
│   ├── button.tsx
│   ├── input.tsx
│   ├── card.tsx
│   └── ...
├── auth/                   # Authentication components
│   ├── login-form.tsx
│   ├── signup-form.tsx
│   └── auth-layout.tsx
├── content/                # Content management components  
│   ├── content-editor.tsx
│   ├── content-list.tsx
│   └── ai-assistant.tsx
└── shared/                 # Shared utility components
    ├── loading-spinner.tsx
    ├── error-boundary.tsx
    └── page-layout.tsx
```

### Styling File Organization
```
app/
├── globals.css             # Global styles and Tailwind imports
├── layout.tsx              # Root layout with theme provider
└── (routes)/
    ├── page.tsx            # Route-specific components
    └── components/         # Route-specific styling

styles/                     # (removed - using app/globals.css)
```

## 🔧 Development Tools

### Required VS Code Extensions
- **Tailwind CSS IntelliSense**: Auto-completion for Tailwind classes
- **TypeScript**: Type checking and IntelliSense
- **ES7+ React/Redux/React-Native snippets**: React snippets
- **Auto Rename Tag**: Synchronized tag renaming
- **Prettier**: Code formatting

### Configuration Files
```json
// .vscode/settings.json
{
  "tailwindCSS.experimental.classRegex": [
    ["cva\\(([^)]*)\\)", "[\"'`]([^\"'`]*).*?[\"'`]"],
    ["cx\\(([^)]*)\\)", "(?:'|\"|`)([^']*)(?:'|\"|`)"]
  ],
  "css.validate": false,
  "scss.validate": false
}
```

## 📊 Performance Considerations

### CSS Optimization
- Use Tailwind's purge functionality to remove unused styles
- Prefer utility classes over custom CSS
- Use CSS variables for theme switching
- Optimize critical rendering path

### Component Performance
```tsx
// Lazy loading for non-critical components
const HeavyComponent = lazy(() => import('./heavy-component'));

// Memoization for expensive renders
const OptimizedComponent = memo(({ data }: { data: ComplexData }) => {
  const processedData = useMemo(() => processData(data), [data]);
  
  return <div>{/* Render with processedData */}</div>;
});

// Image optimization
<Image
  src="/placeholder.jpg"
  alt="Placeholder"
  width={400}
  height={300}
  loading="lazy"
  className="rounded-lg"
/>
```

---

## Design System Tokens

- **Colors** – Use semantic names (primary, secondary, success, error) and reference design system values in `tailwind.config.js`.
- **Typography** – Define font families and sizes. Use Tailwind's text- utilities. Headings: bold, consistent sizing; body: regular weight.
- **Spacing & Layout** – Create a spacing scale (multiples of 4px). Use Tailwind's p-, m-, gap-, and grid classes for consistency.

---

## Responsive & Accessibility

- **Mobile‑first** – Start with mobile styles, use responsive prefixes (sm:, md:, lg:, xl:).
- **Custom breakpoints** – Define custom screens in `tailwind.config.js` if needed.
- **Accessibility** – Ensure color contrast, keyboard navigation, and focus styles. Use `focus-visible` for cues.

---

## Component‑level Styling

1. **Tailwind for most components** – Use utility classes in JSX/HTML. Group classes logically (layout, typography, colors).
2. **CSS Modules** – For complex/unique styles, use `Component.module.css` scoped to the component.
3. **CSS‑in‑JS** – Use for dynamic styles based on props or theme context.
4. **Avoid global styles** – Limit to resets and root variables. Scope all component styles.

---

## Error Prevention & Linting

- **Tailwind CSS linter** – Use ESLint with `eslint-plugin-tailwindcss` for class ordering and conflict detection. Fail CI on linter errors.
- **Purge unused styles** – Configure purge paths to remove unused classes in production.
- **Consistent naming** – Avoid mixing color shades on the same element. Use variants (hover:, focus:) instead of overrides.
- **Prettier** – Format markup and class names consistently.

---

## Documentation & Examples

Document components with description, props, and styling notes. Provide usage examples in Storybook or MDX.

Example structure:
```
src/
  features/
    button/
      Button.tsx
      Button.module.css
      index.ts
```

Example button component:
```js
// Button.tsx
export function Button({ children }: { children: React.ReactNode }) {
  return (
    <button
      className="px-4 py-2 rounded-md bg-primary-500 text-white hover:bg-primary-600 focus:outline-none focus:ring-2 focus:ring-primary-400"
    >
      {children}
    </button>
  );
}
```

Utility classes handle spacing (`px-4`, `py-2`), border radius (`rounded-md`), colors (`bg-primary-500`, `hover:bg-primary-600`, `text-white`), and accessibility (`focus:outline-none`, `focus:ring-2`, `focus:ring-primary-400`).

By following these guidelines, your application remains visually consistent, responsive, and maintainable.

---