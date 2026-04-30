# Medical Form Generator

Generate production-ready React/TypeScript components for a healthcare medication review UI — collapsible medication items, section cards with prescriber notes, 3-column dropdown rows, and Actionable/Not Actionable radio groups.

## Input JSON format

The user provides (or you infer from context) a JSON object like this:

```json
{
  "tabs": [
    { "label": "Actionable Medications", "count": 8, "active": true },
    { "label": "Medication Optimization History" }
  ],
  "actions": [
    { "label": "Add Drug", "icon": "plus" },
    { "label": "Active Drug List", "count": 13, "icon": "link" }
  ],
  "sections": [
    {
      "title": "Duration of Therapy"
    },
    {
      "title": "Efficacy",
      "prescriberNote": "Your patient reports suboptimal symptom improvement or is unsure if they are receiving benefit from taking this medication. Please evaluate your patient's response and consider discontinuing, adjusting or changing this medication.",
      "fields": [
        { "label": "How do you think you are responding to treatment?", "type": "select", "required": true },
        { "label": "Action For AP Review", "type": "select", "required": true },
        { "label": "Prescriber To Outreach", "type": "select", "required": true }
      ],
      "footerNote": "Note: The member could share comments around efficacy or lack of efficacy.",
      "hasActionable": true
    },
    {
      "title": "Treatment Goals & Plans",
      "prescriberNote": "Your patient would like to discuss treatment goals and plan for this medication. Please evaluate your patient's response and consider discontinuing, adjusting or changing this medication if warranted.",
      "fields": [
        { "label": "Did your doctor discuss a plan to discontinue, adjust or change this drug?", "type": "select", "required": true },
        { "label": "Action For AP Review", "type": "select", "required": true },
        { "label": "Prescriber To Outreach", "type": "select", "required": true }
      ],
      "hasActionable": true
    }
  ],
  "medications": [
    { "name": "Metropol Sub, Tab 50mg", "defaultExpanded": false },
    { "name": "Vyvanse Cap 60mg",       "defaultExpanded": true  }
  ]
}
```

## Files to generate

Generate all of these files. Write each one immediately — do not skip any.

| File | Purpose |
|---|---|
| `types.ts` | All TypeScript interfaces (Tab, Action, MedicationDef, Section, Field, FormState) — `MedicationDef` has `name` + `defaultExpanded`; sections live at the form level, not per-medication |
| `MedicalFormContainer.tsx` | Root component — tabs bar, action buttons, medication list |
| `MedicationItem.tsx` | Single collapsible medication row with its sections |
| `FormSection.tsx` | Collapsible section card — prescriber note, field grid, footer note, actionable radios |
| `FormRow.tsx` | 3-column grid row of dropdowns/inputs |
| `ActionableRadio.tsx` | "Actionable / Not Actionable" radio group |
| `index.ts` | Barrel export |

## Styling rules — LIGHT clinical theme

This is a clinical/healthcare UI. Use Tailwind CSS with a **white/light-gray** palette — NOT dark mode.

- **Page bg**: `bg-gray-50`
- **Cards/panels**: `bg-white border border-gray-200 rounded-lg`
- **Tab bar**: white bg, active tab has blue bottom border `border-b-2 border-blue-600 text-blue-600`, inactive `text-gray-500`
- **Collapsible headers**: `flex items-center gap-2 px-4 py-3 cursor-pointer hover:bg-gray-50 font-medium text-gray-800`
- **Chevron icon**: rotate 90° when expanded (use inline SVG or `›` character, transition with `transition-transform`)
- **Prescriber note**: `text-sm text-gray-600 italic px-4 pb-2`
- **Field label**: `text-sm font-medium text-gray-700 mb-1` with `*` in `text-red-500` for required
- **Select / dropdown**: `w-full border border-gray-300 rounded-md px-3 py-2 text-sm text-gray-500 bg-white focus:outline-none focus:ring-2 focus:ring-blue-500 appearance-none`
- **Footer note**: `text-xs text-gray-400 italic mt-1`
- **Actionable radio**: `flex items-center gap-4 mt-3` — radio + label pairs, `text-sm text-gray-700`
- **Add Drug button**: `flex items-center gap-1 text-sm font-medium text-blue-600 border border-blue-300 rounded px-3 py-1.5 hover:bg-blue-50`
- **Active Drug List link**: `text-sm text-blue-600 underline`
- **Section divider**: `border-t border-gray-100` between sections

## Component behaviour

- **Sections are shared** — every medication renders the same `sections` array defined at the top level. `MedicationItem` receives `sections` as a prop so all drugs show identical section structure.
- `defaultExpanded` on each medication controls whether the medication row starts open or collapsed. One medication can be open while others are collapsed simultaneously.
- All medications and sections are independently collapsible via `useState(defaultExpanded)` for `isOpen`
- `MedicationItem` renders a `>` chevron that rotates when expanded
- `FormSection` renders a `∨` chevron in the section header
- The `FormRow` renders exactly 3 columns using `grid grid-cols-3 gap-4`
- If a section has no `fields`, render just the collapsible header (e.g. "Duration of Therapy")
- `ActionableRadio` renders two radio inputs: value `"actionable"` and `"not_actionable"`
- `FormState` tracks all dropdown values and actionable selections keyed by `medicationName.sectionTitle.fieldLabel`
- All select options default to `""` (placeholder shown), pass `options: string[]` prop for real values (default to empty array — caller populates)

## Instructions

1. Read the JSON the user provides (or use the example above if none given).
2. Derive the component name prefix from `medications[0].name` or use `"Medical"` as fallback.
3. Generate all 7 files in one pass with correct TypeScript types throughout.
4. Do not use any external UI library — only React, TypeScript, and Tailwind CSS.
5. Do not use CSS modules or inline styles.
6. Every exported symbol gets a one-line JSDoc comment.
7. Write each file to the `generated_components/` directory (or the path the user specifies).

If the user has not provided a JSON, ask: "Please paste your medical form JSON, or reply 'example' to use the built-in medication review schema."
