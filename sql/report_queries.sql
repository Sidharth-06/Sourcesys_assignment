-- SourceSys assignment query practice
-- This file demonstrates DDL, DML, DQL, GROUP BY, ORDER BY, HAVING, and TCL.

-- 1. Sample data insertion
insert into sourcesys.departments (department_name, description)
values
    ('Human Resources', 'Handles recruitment and employee records'),
    ('Finance', 'Manages budgets and payments'),
    ('Technology', 'Maintains systems and software')
on conflict (department_name) do nothing;

insert into sourcesys.projects (project_name, start_date, status)
values
    ('Inventory System', '2026-01-15', 'active'),
    ('Payroll Dashboard', '2026-02-10', 'completed'),
    ('HR Portal', '2026-03-05', 'on_hold'),
    ('Support Tracker', '2026-03-12', 'active'),
    ('Budget Analyzer', '2026-03-20', 'completed')
on conflict do nothing;

insert into sourcesys.people (first_name, last_name, email, birth_date)
values
    ('Aarav', 'Sharma', 'aarav.sharma@example.com', '2002-05-14'),
    ('Diya', 'Patel', 'diya.patel@example.com', '2001-09-09'),
    ('Rohan', 'Iyer', 'rohan.iyer@example.com', '2003-01-22')
on conflict (email) do nothing;

-- 2. DQL: retrieve all projects
select id, project_name, start_date, status
from sourcesys.projects;

-- 3. ORDER BY: newest projects first
select project_name, start_date, status
from sourcesys.projects
order by start_date desc, project_name asc;

-- 4. WHERE + ORDER BY: only active projects
select project_name, start_date
from sourcesys.projects
where status = 'active'
order by start_date asc;

-- 5. GROUP BY + COUNT
select status, count(*) as total_projects
from sourcesys.projects
group by status
order by total_projects desc, status asc;

-- 6. GROUP BY + HAVING
select status, count(*) as total_projects
from sourcesys.projects
group by status
having count(*) >= 2
order by status asc;

-- 7. DDL: alter table example
alter table sourcesys.departments
add column if not exists location varchar(120);

-- 8. DML: update example
update sourcesys.projects
set status = 'completed'
where project_name = 'Inventory System';

-- 9. DML: delete example
delete from sourcesys.projects
where status = 'archived';

-- 10. TCL: rollback example
begin;

update sourcesys.projects
set status = 'on_hold'
where project_name = 'HR Portal';

rollback;

-- 11. TCL: commit example
begin;

update sourcesys.projects
set status = 'completed'
where project_name = 'Payroll Dashboard';

commit;
