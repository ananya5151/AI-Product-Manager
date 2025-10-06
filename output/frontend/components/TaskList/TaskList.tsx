import React, { useState, useEffect } from 'react';
import styles from './TaskList.module.css';

// Define the shape of a single task object
interface Task {
  id: number;
  title: string;
  completed: boolean;
}

// Props for the individual Task component
interface TaskComponentProps {
  task: Task;
}

// Props for the main TaskList component
interface Props {}

// A simple mock API function to simulate fetching data
const mockFetchTasks = (): Promise<Task[]> => {
  return new Promise(resolve => {
    setTimeout(() => {
      resolve([
        { id: 1, title: 'Learn React Hooks', completed: true },
        { id: 2, title: 'Create TaskList component', completed: true },
        { id: 3, title: 'Use TypeScript', completed: false },
        { id: 4, title: 'Implement CSS Modules', completed: false },
        { id: 5, title: 'Drink coffee', completed: true },
      ]);
    }, 1500); // Simulate network delay
  });
};

/**
 * A single Task component to display task details.
 * It's defined within the TaskList file for self-containment.
 */
const TaskComponent: React.FC<TaskComponentProps> = ({ task }) => {
  const itemClasses = `${styles.taskItem} ${task.completed ? styles.completed : ''}`;

  return (
    <li className={itemClasses}>
      <span className={styles.taskTitle}>{task.title}</span>
      <span className={styles.taskStatus}>{task.completed ? 'Done' : 'Pending'}</span>
    </li>
  );
};

/**
 * TaskList component fetches and displays a list of tasks.
 * It handles loading and error states.
 */
const TaskList: React.FC<Props> = () => {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const getTasks = async () => {
      try {
        setLoading(true);
        setError(null);
        const fetchedTasks = await mockFetchTasks();
        setTasks(fetchedTasks);
      } catch (err) {
        setError('Failed to fetch tasks. Please try again later.');
      } finally {
        setLoading(false);
      }
    };

    getTasks();
  }, []); // Empty dependency array ensures this runs only once on mount

  if (loading) {
    return <div className={styles.stateMessage}>Loading tasks...</div>;
  }

  if (error) {
    return <div className={`${styles.stateMessage} ${styles.error}`}>{error}</div>;
  }

  return (
    <div className={styles.container}>
      <h1 className={styles.header}>My Tasks</h1>
      {tasks.length > 0 ? (
        <ul className={styles.list}>
          {tasks.map(task => (
            <TaskComponent key={task.id} task={task} />
          ))}
        </ul>
      ) : (
        <p className={styles.stateMessage}>No tasks to display.</p>
      )}
    </div>
  );
};

export default TaskList;
