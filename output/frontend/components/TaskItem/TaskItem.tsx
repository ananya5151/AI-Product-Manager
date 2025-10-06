import React, { useState } from 'react';
import styles from './TaskItem.module.css';

interface Props {
  id: string;
  title: string;
  isCompleted: boolean;
  /**
   * An async function to call the update API.
   * It should throw an error on failure to allow the component to handle it.
   */
  onUpdateStatus: (id: string, newCompletedState: boolean) => Promise<void>;
}

export const TaskItem: React.FC<Props> = ({ id, title, isCompleted, onUpdateStatus }) => {
  const [isUpdating, setIsUpdating] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const handleCheckboxChange = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const newCompletedState = event.target.checked;
    
    setIsUpdating(true);
    setError(null);

    try {
      await onUpdateStatus(id, newCompletedState);
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'An unknown error occurred.';
      setError(`Failed to update: ${errorMessage}`);
      // Note: The parent component is the source of truth for `isCompleted`.
      // If the API call fails, the parent's state won't be updated, and on the next render,
      // this component will revert to the original `isCompleted` prop value.
    } finally {
      setIsUpdating(false);
    }
  };

  const titleClassName = `${styles.title} ${isCompleted ? styles.completed : ''}`;

  return (
    <li className={styles.container}>
      <div className={styles.taskContent}>
        <input
          type="checkbox"
          id={`task-${id}`}
          checked={isCompleted}
          onChange={handleCheckboxChange}
          disabled={isUpdating}
          aria-label={`Mark task '${title}' as ${isCompleted ? 'incomplete' : 'complete'}`}
        />
        <label htmlFor={`task-${id}`} className={titleClassName}>
          {title}
        </label>
      </div>
      {isUpdating && <div className={styles.status}>Updating...</div>}
      {error && <div className={styles.error}>{error}</div>}
    </li>
  );
};
