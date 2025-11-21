# Facility App

The `facility` app models the physical locations inside an organization—training centers,
departments, quarters/cabins, and onsite faculty profiles.

## Responsibilities

- `Facility`, `Department`, `QuartersType`, and `Quarters` models with address + hierarchy mixins.
- `FacultyProfile` plus associated forms/tables/serializers for portal management.
- Views that allow admins and faculty leaders to manage facilities, schedule sessions, and assign
  quarters to staff.
- Integration points with `enrollment` for facility enrollments, class offerings, and faculty
  assignments.

## Highlights

- Quarters support capacity tracking and feed the availability service whenever factions,
  leaders, or faculty reserve cabins.
- Facility manage views (`facility/views/facility.py`) expose dashboards for sessions, faculty,
  and weeks using the shared `BaseManageView`.
- Departments inherit shared mixins so they gain slug uniqueness, auditing, and settings management
  out of the box.

## Tests

```bash
python manage.py test facility
```

Use these tests to validate new quarters, facility, or faculty profile functionality.
