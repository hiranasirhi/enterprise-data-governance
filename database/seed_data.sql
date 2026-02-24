-- -------------------------------
-- Departments
-- -------------------------------
INSERT IGNORE INTO Departments (dept_name)
VALUES 
('HR'), 
('Finance'), 
('IT'), 
('Operations');

-- -------------------------------
-- Roles
-- -------------------------------
INSERT IGNORE INTO Roles (role_name, description)
VALUES 
('Employee','Basic access'),
('HR_Manager','Manages HR'),
('Finance_Manager','Manages Finance'),
('IT_Admin','System Admin');

-- -------------------------------
-- Users
-- -------------------------------
INSERT IGNORE INTO Users (full_name,email,password_hash,dept_id)
VALUES
('Ali Khan','ali@company.com','hashed_pw1',1),
('Sara Ahmed','sara@company.com','hashed_pw2',2),
('Usman Raza','usman@company.com','hashed_pw3',3),
('Hira Nasir', 'hiranasir@company.com', 'hashed_pw4', 1);

-- -------------------------------
-- User Roles
-- -------------------------------
-- Ali = Employee
INSERT IGNORE INTO User_Roles (user_id, role_id)
VALUES 
((SELECT user_id FROM Users WHERE full_name='Ali Khan'), 
 (SELECT role_id FROM Roles WHERE role_name='Employee'));

-- Hira = HR_Manager
INSERT IGNORE INTO User_Roles (user_id, role_id)
VALUES 
((SELECT user_id FROM Users WHERE full_name='Hira Nasir'), 
 (SELECT role_id FROM Roles WHERE role_name='HR_Manager'));

-- Sara = Finance_Manager
INSERT IGNORE INTO User_Roles (user_id, role_id)
VALUES
((SELECT user_id FROM Users WHERE full_name='Sara Ahmed'),
 (SELECT role_id FROM Roles WHERE role_name='Finance_Manager'));

-- Usman = IT_Admin
INSERT IGNORE INTO User_Roles (user_id, role_id)
VALUES
((SELECT user_id FROM Users WHERE full_name='Usman Raza'),
 (SELECT role_id FROM Roles WHERE role_name='IT_Admin'));

-- -------------------------------
-- Data Resources
-- -------------------------------
INSERT IGNORE INTO Data_Resources (resource_name, description, sensitivity_level, data_owner_id)
VALUES
('Payroll Database', 'Employee salary records', 'High', (SELECT user_id FROM Users WHERE full_name='Hira Nasir')),
('Customer Records', 'Client personal data', 'Medium', (SELECT user_id FROM Users WHERE full_name='Sara Ahmed')),
('Internal Policy Docs', 'Company internal policies', 'Low', (SELECT user_id FROM Users WHERE full_name='Hira Nasir'));

-- -------------------------------
-- Permissions
-- -------------------------------
INSERT IGNORE INTO Permissions (action, resource_id)
VALUES
('READ', (SELECT resource_id FROM Data_Resources WHERE resource_name='Payroll Database')),
('WRITE', (SELECT resource_id FROM Data_Resources WHERE resource_name='Payroll Database')),
('READ', (SELECT resource_id FROM Data_Resources WHERE resource_name='Customer Records')),
('UPDATE', (SELECT resource_id FROM Data_Resources WHERE resource_name='Customer Records')),
('READ', (SELECT resource_id FROM Data_Resources WHERE resource_name='Internal Policy Docs'));

-- -------------------------------
-- Role → Permission Mapping
-- -------------------------------
-- HR_Manager → Payroll Database READ + WRITE
INSERT IGNORE INTO Role_Permissions (role_id, permission_id)
VALUES
((SELECT role_id FROM Roles WHERE role_name='HR_Manager'),
 (SELECT permission_id FROM Permissions WHERE action='READ' AND resource_id=(SELECT resource_id FROM Data_Resources WHERE resource_name='Payroll Database'))),
((SELECT role_id FROM Roles WHERE role_name='HR_Manager'),
 (SELECT permission_id FROM Permissions WHERE action='WRITE' AND resource_id=(SELECT resource_id FROM Data_Resources WHERE resource_name='Payroll Database')));

-- Finance_Manager → Customer Records READ + UPDATE
INSERT IGNORE INTO Role_Permissions (role_id, permission_id)
VALUES
((SELECT role_id FROM Roles WHERE role_name='Finance_Manager'),
 (SELECT permission_id FROM Permissions WHERE action='READ' AND resource_id=(SELECT resource_id FROM Data_Resources WHERE resource_name='Customer Records'))),
((SELECT role_id FROM Roles WHERE role_name='Finance_Manager'),
 (SELECT permission_id FROM Permissions WHERE action='UPDATE' AND resource_id=(SELECT resource_id FROM Data_Resources WHERE resource_name='Customer Records')));

-- Employee → Internal Policy Docs READ
INSERT IGNORE INTO Role_Permissions (role_id, permission_id)
VALUES
((SELECT role_id FROM Roles WHERE role_name='Employee'),
 (SELECT permission_id FROM Permissions WHERE action='READ' AND resource_id=(SELECT resource_id FROM Data_Resources WHERE resource_name='Internal Policy Docs')));

-- IT_Admin → All resources READ + WRITE + UPDATE
INSERT IGNORE INTO Role_Permissions (role_id, permission_id)
VALUES
((SELECT role_id FROM Roles WHERE role_name='IT_Admin'),
 (SELECT permission_id FROM Permissions WHERE action='READ' AND resource_id=(SELECT resource_id FROM Data_Resources WHERE resource_name='Payroll Database'))),
((SELECT role_id FROM Roles WHERE role_name='IT_Admin'),
 (SELECT permission_id FROM Permissions WHERE action='WRITE' AND resource_id=(SELECT resource_id FROM Data_Resources WHERE resource_name='Payroll Database'))),
((SELECT role_id FROM Roles WHERE role_name='IT_Admin'),
 (SELECT permission_id FROM Permissions WHERE action='READ' AND resource_id=(SELECT resource_id FROM Data_Resources WHERE resource_name='Customer Records'))),
((SELECT role_id FROM Roles WHERE role_name='IT_Admin'),
 (SELECT permission_id FROM Permissions WHERE action='UPDATE' AND resource_id=(SELECT resource_id FROM Data_Resources WHERE resource_name='Customer Records'))),
((SELECT role_id FROM Roles WHERE role_name='IT_Admin'),
 (SELECT permission_id FROM Permissions WHERE action='READ' AND resource_id=(SELECT resource_id FROM Data_Resources WHERE resource_name='Internal Policy Docs')));
