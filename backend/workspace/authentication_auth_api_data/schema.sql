CREATE TABLE Users (
  id INT AUTO_INCREMENT,
  username VARCHAR(255) NOT NULL,
  email VARCHAR(255) NOT NULL,
  password VARCHAR(255) NOT NULL,
  role ENUM('admin', 'user') NOT NULL DEFAULT 'user',
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY (username),
  UNIQUE KEY (email)
);

CREATE TABLE Tasks (
  id INT AUTO_INCREMENT,
  title VARCHAR(255) NOT NULL,
  description TEXT,
  status ENUM('pending', 'in_progress', 'completed') NOT NULL DEFAULT 'pending',
  assigned_to INT,
  created_by INT NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  FOREIGN KEY (assigned_to) REFERENCES Users(id),
  FOREIGN KEY (created_by) REFERENCES Users(id)
);

CREATE TABLE Task_History (
  id INT AUTO_INCREMENT,
  task_id INT NOT NULL,
  status ENUM('pending', 'in_progress', 'completed') NOT NULL,
  updated_by INT NOT NULL,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  FOREIGN KEY (task_id) REFERENCES Tasks(id),
  FOREIGN KEY (updated_by) REFERENCES Users(id)
);

CREATE TABLE Comments (
  id INT AUTO_INCREMENT,
  task_id INT NOT NULL,
  comment TEXT NOT NULL,
  created_by INT NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  FOREIGN KEY (task_id) REFERENCES Tasks(id),
  FOREIGN KEY (created_by) REFERENCES Users(id)
);

CREATE INDEX idx_tasks_assigned_to ON Tasks (assigned_to);
CREATE INDEX idx_tasks_created_by ON Tasks (created_by);
CREATE INDEX idx_task_history_task_id ON Task_History (task_id);
CREATE INDEX idx_task_history_updated_by ON Task_History (updated_by);
CREATE INDEX idx_comments_task_id ON Comments (task_id);
CREATE INDEX idx_comments_created_by ON Comments (created_by);