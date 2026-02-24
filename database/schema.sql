CREATE TABLE Departments (
    dept_id INT PRIMARY KEY AUTO_INCREMENT,
    dept_name VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE Users (
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    dept_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (dept_id) REFERENCES Departments(dept_id)
);

CREATE TABLE Roles (
    role_id INT PRIMARY KEY AUTO_INCREMENT,
    role_name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT
);

CREATE TABLE Data_Resources (
    resource_id INT PRIMARY KEY AUTO_INCREMENT,
    resource_name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT,
    sensitivity_level ENUM('Low','Medium','High') NOT NULL,
    data_owner_id INT NOT NULL,
    FOREIGN KEY (data_owner_id) REFERENCES Users(user_id) ON DELETE CASCADE
);

CREATE TABLE Permissions (
    permission_id INT PRIMARY KEY AUTO_INCREMENT,
    action VARCHAR(50) NOT NULL,
    resource_id INT NOT NULL,
    FOREIGN KEY (resource_id) REFERENCES Data_Resources(resource_id) ON DELETE CASCADE
);

CREATE TABLE User_Roles (
    user_id INT,
    role_id INT,
    assigned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, role_id),
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    FOREIGN KEY (role_id) REFERENCES Roles(role_id)
);

CREATE TABLE Role_Permissions (
    role_id INT,
    permission_id INT,
    PRIMARY KEY (role_id, permission_id),
    FOREIGN KEY (role_id) REFERENCES Roles(role_id) ON DELETE CASCADE,
    FOREIGN KEY (permission_id) REFERENCES Permissions(permission_id) ON DELETE CASCADE
);
