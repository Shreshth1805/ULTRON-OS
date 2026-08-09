INSERT INTO users (id, username, email, password, role) 
VALUES 
(1, 'admin', 'admin@example.com', '$2b$10$92IXUNpkjO0rOQ5byY4oEeNp22c5nr0kHUyc4skj3iMyEgyXOj9m', 'admin'),
(2, 'user', 'user@example.com', '$2b$10$92IXUNpkjO0rOQ5byY4oEeNp22c5nr0kHUyc4skj3iMyEgyXOj9m', 'user');

INSERT INTO tasks (id, title, description, status, assigned_to) 
VALUES 
(1, 'Task 1', 'This is task 1', 'pending', 1),
(2, 'Task 2', 'This is task 2', 'in_progress', 2),
(3, 'Task 3', 'This is task 3', 'done', 1);

INSERT INTO task_comments (id, task_id, comment, created_by) 
VALUES 
(1, 1, 'This is a comment on task 1', 1),
(2, 2, 'This is a comment on task 2', 2),
(3, 3, 'This is a comment on task 3', 1);

INSERT INTO task_attachments (id, task_id, file_name, file_type) 
VALUES 
(1, 1, 'attachment1.txt', 'text/plain'),
(2, 2, 'attachment2.pdf', 'application/pdf'),
(3, 3, 'attachment3.jpg', 'image/jpeg');