import React from 'react';
import styles from './Task.module.css';

// Define the component's props interface
interface Props {
  /** A unique identifier for the task. */
  id: string | number;
  /** The title or description of the task. */
  title: string;
  /** The completion status of the task. */
  completed: boolean;
  /** Callback function to be invoked when the checkbox is toggled. */
  onToggle: (id: string | number) => void;
}

/**
 * Task component displays a single task item with a title and a checkbox.
 */
const Task: React.FC<Props> = ({ id, title, completed, onToggle }) => {

  // Handler to call the onToggle prop with the task's id
  const handleToggle = () => {
    onToggle(id);
  };

  // Combine class names conditionally for styling
  const titleClasses = `${styles.title} ${completed ? styles.completed : ''}`;

  return (
    <div className={styles.container}>
      <input
        type="checkbox"
        id={`task-${id}`}
        checked={completed}
        onChange={handleToggle}
        className={styles.checkbox}
        aria-label={`Mark task '${title}' as ${completed ? 'incomplete' : 'complete'}`}
      />
      <label htmlFor={`task-${id}`} className={titleClasses}>
        {title}
      </label>
    </div>
  );
};

export default Task;
