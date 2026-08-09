import React, { useState } from 'react';
import { useForm } from 'react-hook-form';
import { taskService } from '../services/taskService';
import { useHistory } from 'react-router-dom';
import { toast } from 'react-toastify';

const TaskForm = ({ task, onSubmit }) => {
  const { register, handleSubmit, errors } = useForm({
    defaultValues: task || {
      title: '',
      description: '',
      dueDate: '',
      assignedTo: '',
    },
  });
  const [loading, setLoading] = useState(false);
  const history = useHistory();

  const handleFormSubmit = async (data) => {
    try {
      setLoading(true);
      if (task) {
        await taskService.updateTask(task.id, data);
        toast.success('Task updated successfully');
      } else {
        const newTask = await taskService.createTask(data);
        toast.success('Task created successfully');
        history.push(`/tasks/${newTask.id}`);
      }
    } catch (error) {
      toast.error('Error creating or updating task');
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit(handleFormSubmit)}>
      <div className="form-group">
        <label>Title:</label>
        <input
          type="text"
          {...register('title', { required: true })}
          className={`form-control ${errors.title ? 'is-invalid' : ''}`}
        />
        {errors.title && <div className="invalid-feedback">Title is required</div>}
      </div>
      <div className="form-group">
        <label>Description:</label>
        <textarea
          {...register('description', { required: true })}
          className={`form-control ${errors.description ? 'is-invalid' : ''}`}
        />
        {errors.description && (
          <div className="invalid-feedback">Description is required</div>
        )}
      </div>
      <div className="form-group">
        <label>Due Date:</label>
        <input
          type="date"
          {...register('dueDate', { required: true })}
          className={`form-control ${errors.dueDate ? 'is-invalid' : ''}`}
        />
        {errors.dueDate && <div className="invalid-feedback">Due date is required</div>}
      </div>
      <div className="form-group">
        <label>Assigned To:</label>
        <input
          type="text"
          {...register('assignedTo', { required: true })}
          className={`form-control ${errors.assignedTo ? 'is-invalid' : ''}`}
        />
        {errors.assignedTo && (
          <div className="invalid-feedback">Assigned to is required</div>
        )}
      </div>
      <button type="submit" disabled={loading} className="btn btn-primary">
        {loading ? 'Submitting...' : task ? 'Update Task' : 'Create Task'}
      </button>
    </form>
  );
};

export default TaskForm;