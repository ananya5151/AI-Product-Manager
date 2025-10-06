import React, { useState, FormEvent } from 'react';
import styles from './AddTaskForm.module.css';

// A generic Task type that might be shared across the application
interface Task {
  id: string | number;
  title: string;
  description?: string;
  completed: boolean;
}

// Define the component's props
interface Props {
  onTaskAdded: (newTask: Task) => void;
}

const AddTaskForm: React.FC<Props> = ({ onTaskAdded }) => {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    if (!title.trim()) {
      setError('Task title is required.');
      return;
    }

    setIsLoading(true);
    setError(null);

    try {
      // Replace with your actual API endpoint
      const response = await fetch('/api/tasks', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ title, description }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.message || 'Failed to add task.');
      }

      const newTask: Task = await response.json();

      // Notify parent component about the new task
      onTaskAdded(newTask);

      // Reset form fields upon successful submission
      setTitle('');
      setDescription('');

    } catch (err) {
      if (err instanceof Error) {
        setError(err.message);
      } else {
        setError('An unexpected error occurred. Please try again.');
      }
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <form className={styles.form} onSubmit={handleSubmit} aria-labelledby="form-title">
      <h2 id="form-title" className={styles.title}>Add New Task</h2>
      {error && <div className={styles.error} role="alert">{error}</div>}
      <div className={styles.formGroup}>
        <label htmlFor="task-title" className={styles.label}>
          Title
        </label>
        <input
          id="task-title"
          type="text"
          className={styles.input}
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          disabled={isLoading}
          required
          aria-required="true"
        />
      </div>
      <div className={styles.formGroup}>
        <label htmlFor="task-description" className={styles.label}>
          Description (Optional)
        </label>
        <textarea
          id="task-description"
          className={styles.textarea}
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          disabled={isLoading}
        />
      </div>
      <button type="submit" className={styles.submitButton} disabled={isLoading}>
        {isLoading ? 'Adding...' : 'Add Task'}
      </button>
    </form>
  );
};

export default AddTaskForm;
