INSERT INTO users (id, username, email, password) 
VALUES 
(1, 'admin', 'admin@example.com', '$2b$10$92IXUNpkjO0rOQ5byY4oEeNp22c9Iu9FSCj3DdCBXDh2TbwIuZ06'),
(2, 'user1', 'user1@example.com', '$2b$10$92IXUNpkjO0rOQ5byY4oEeNp22c9Iu9FSCj3DdCBXDh2TbwIuZ06'),
(3, 'user2', 'user2@example.com', '$2b$10$92IXUNpkjO0rOQ5byY4oEeNp22c9Iu9FSCj3DdCBXDh2TbwIuZ06');

INSERT INTO tasks (id, title, description, status, assigned_to) 
VALUES 
(1, 'Task 1', 'This is task 1', 'pending', 1),
(2, 'Task 2', 'This is task 2', 'in_progress', 2),
(3, 'Task 3', 'This is task 3', 'done', 3),
(4, 'Task 4', 'This is task 4', 'pending', 1),
(5, 'Task 5', 'This is task 5', 'in_progress', 2);

INSERT INTO task_history (task_id, status, updated_at) 
VALUES 
(1, 'pending', '2022-01-01 12:00:00'),
(2, 'in_progress', '2022-01-02 13:00:00'),
(3, 'done', '2022-01-03 14:00:00'),
(4, 'pending', '2022-01-04 15:00:00'),
(5, 'in_progress', '2022-01-05 16:00:00');